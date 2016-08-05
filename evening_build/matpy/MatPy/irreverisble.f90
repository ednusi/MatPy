!!!!--2014-12-02--!!!!!!!!!
!
! If there is any error or you have any problem using this code, please contact:
! Shengyen Li, Shenyen.li@gmail.com
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!

subroutine mechanics(p_stress,ss_stress,Tsam,M_para,samples,stress_strain,WTN)

  implicit none

  integer, parameter:: no_phase=1, no_phase_calc=1
  integer, parameter:: maxiterstep=20000
  integer:: no_iter

  real*8, parameter:: pi=acos(-1.0d0)

  real*8:: mu_shmodulus(no_phase), burgers
  real*8:: density0(no_phase)
  real*8:: tot_shear_strain
  real*8:: totstress, totstrain, totstress_p, totstrain_p
  real*8:: dstrain(no_phase), dstrain_pre(no_phase), delta_strain
  real*8:: stress(no_phase)
  real*8:: stress_b, stress_in, stress_p(no_phase), necking_strength, necking_strain
  real*8:: stress_material(no_phase)
  real*8:: Tfactor,alpha
  real*8:: gsize(no_phase)
  real*8:: C(no_phase), nmax(no_phase), n(no_phase), lumda(no_phase), Gact(no_phase)
  real*8:: k1, k2, const1, delta_density(no_phase)
  real*8:: vibfreq, strain_rate, KB
  real*8:: dsds,nkdiff
  real*8:: nusrdG(no_phase)

!=== phase ===
  real*8:: dsdsphase(no_phase), pphasestrain(no_phase), pphasestress(no_phase)
  integer:: neckingphase(no_phase)
  integer:: foritergor

  integer, parameter:: isowork=0   ! =1, the calculation is under "isowork" approx.
                                   ! =0, the calculation is under "isostrain" approx.
                                   ! for superalloys: 
                                   ! (1) gamma-gamma_prime is assumed
                                   ! (2) gamma_prime is the precipitate phase
                                   ! isostrain (isowork=0) is the only approach 

  real*8:: densityin(no_phase)
  integer:: i, sam
  integer:: necking
  real*8:: Vf(no_phase)

! /*/*/*/ inputs /*/*/*/
  real*8, dimension(samples), intent(in):: p_stress,ss_stress
  real*8, dimension(samples), intent(in):: Tsam

  integer, intent(in):: samples

  real*8, dimension(2), intent(in):: M_para
! /-/-/-/ outputs /-/-/-/
  real*8, dimension(2*maxiterstep), intent(out):: stress_strain
  real*8, intent(out):: WTN
  integer:: ind_SS

  real*8:: SR(samples)

!  M_para(1)=-180
!  M_para(2)=3.08

  nkdiff=1000.0d0
  KB=1.3806488d-23

  alpha=0.25d0
  Tfactor=3.06d0       ! Taylor Factor
  burgers=2.5d-10      ! magnitude of burgers vector
  vibfreq=1.0d+13

!--- conditions for tensile test ---
  SR=1d-3
  ind_SS=1


  do sam=1,samples

      mu_shmodulus(1)=(298.*3./8.)*(1.-0.5*(Tsam(sam)-300.)/1673.)*1000d0  ! input GPa

!      stress_strain(1)=0d0
!      stress_strain(2)=0d0

      strain_rate=SR(sam)*2.5d0/0.83d0 ! shear strain rate

!+++ Ni-gamma +++
      density0(1)=1.0d+12
      gsize(1)=20.0d-6
      lumda(1)=1.5D-7
      nmax(1)=4.0d0

      C(1)=M_para(1)
      Gact(1)=M_para(2)*1.602176565d-19
      nusrdG(1)=vibfreq*exp(-Gact(1)/(KB*Tsam(sam)))/strain_rate
!print*, nusrdG(1),exp(-Gact(1)/(KB*Tsam(sam))),Gact(1),KB*Tsam(sam)

      Vf(1)=1d0
!print*, vf(1)
!      if(vf(1)>0.5d0) Vf(1)=1d0-vf(1)

      stress_p(1)=p_stress(sam)/Tfactor
      stress_material(1)=ss_stress(sam)/Tfactor  ! Peierl's + solid solution strengthening

!print*, p_stress(sam),ss_stress(sam)

      necking=0

!=== SS curve ===
      stress=0.0d0
      delta_strain=1d-4
      dstrain=0.0d0
      dstrain_pre=0.0d0

      densityin=density0
      n=0.0d0

      dsdsphase=0d0
      pphasestrain=0d0
      pphasestress=0d0
      neckingphase=0

      totstress_p=0.0d0
      totstrain_p=0d0
      totstress=0.0d0
      totstrain=0.0d0
      WTN=0d0
      no_iter=0

      do foritergor=1,maxiterstep,1
!print*, foritergor,maxiterstep

        tot_shear_strain=foritergor*delta_strain
        no_iter=foritergor+1

        if(isowork==1) then  ! iso-work
          print*, "NOT CORRECT MODEL SELECTION FOR SUPERALLOY"
        else if(isowork==0) then  ! iso-strain
          do i=1,no_phase_calc
            if(neckingphase(i)==0) dstrain(i)=delta_strain
          end do
        end if

        do i=1,no_phase_calc
          if(neckingphase(i)==0) then
            dstrain(i)=dstrain(i)+dstrain_pre(i)
            dstrain_pre(i)=dstrain(i)
          end if
        end do

        do i=1,no_phase_calc,1

          if(Vf(i)>0.0d0) then

            stress_b=0.0d0
            stress_b=mu_shmodulus(i)*burgers*nmax(i)*(1.0d0-exp(-lumda(i)*dstrain(i)/(burgers*nmax(i))))/gsize(i)

            stress_in=0.0d0
            stress_in=alpha*mu_shmodulus(i)*burgers*sqrt(densityin(i))

            stress(i)=0.0d0
            stress(i)=stress_material(i) + stress_b + sqrt(stress_in**2.0d0 + stress_p(i)**2.0d0)

            const1=mu_shmodulus(i)*(burgers**2.0d0)+stress(i)*burgers/sqrt(densityin(i))

            k1=const1*nusrdG(i)*densityin(i)
            k2=0.5d0*C(i)*alpha*mu_shmodulus(i)*(burgers**2.0d0)-const1

            delta_density(i)=delta_strain*( k1 - sqrt(stress_in**2.0d0 + stress_p(i)**2.0d0)) / k2
            densityin(i)=densityin(i)+delta_density(i)

          end if

        end do

        totstress=0.0d0
        totstrain=0.0d0

        if(isowork==1) then
          do i=1,no_phase_calc,1
            if(Vf(i) > 0.0d0 .and. neckingphase(i)==0) then
              totstress=totstress+stress(i)*Vf(i)
              totstrain=totstrain+dstrain(i)*Vf(i)
            end if
          end do
        else if(isowork==0) then
          do i=1,no_phase_calc,1
            if(Vf(i)>0.0d0 .and. neckingphase(i)==0) then
              totstress=totstress+stress(i)*Vf(i)
            end if
          end do
          totstrain=tot_shear_strain

!          totstrain=0d0
!          do i=1,no_phase_calc,1
!            totstrain=totstrain+dstrain(i)
!          end do
        end if

        totstress=totstress*Tfactor
        totstrain=totstrain/Tfactor


        WTN=WTN+totstress*(totstrain-totstrain_p)
        stress_strain(2*foritergor-1)=totstrain*100d0
        stress_strain(2*foritergor)=totstress
!print*, foritergor,2*foritergor,stress_strain(2*foritergor-1),stress_strain(2*foritergor)

        if(isnan(totstrain) .or. isnan(totstress)) goto 1979

        do i=1,no_phase_calc
          dsdsphase(i)=(stress(i)*Tfactor-pphasestress(i)) &
                      /(dstrain(i)/Tfactor-pphasestrain(i))

          pphasestress(i)=stress(i)*Tfactor
          pphasestrain(i)=dstrain(i)/Tfactor
        end do

        dsds=(totstress-totstress_p)/(totstrain-totstrain_p)

!        if(dsds <= totstress .and. necking==0) then
!        if(dsds <= 0 .and. necking==0) then
!          necking=1
!          goto 1979
!        end if

        if(abs(dsds-totstress) < nkdiff) then
          necking_strength=dsds
          necking_strain=totstrain
          nkdiff=abs(dsds-totstress)
        end if

        totstress_p=totstress
        totstrain_p=totstrain

      end do

1979 continue
  end do


  return

end subroutine


