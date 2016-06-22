"""This will contain the mcfunc for the Irreversible stress-strain model"""

import numpy as np
import math
import matplotlib.pyplot as plot
from matplotlib import ticker

import matplotlib
from mpl_toolkits.mplot3d import Axes3D

import scipy.optimize as sciop
from scipy.optimize import basinhopping
import subprocess

bashCommand = "make fortran"
import subprocess
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)

import irreverisble #importing the fortran mechanics routine

class StressStrain:
	
	def __init__(self,data_file):
		global exp						   # experimental dataset to minimize parameters
		exp = []                           # ***** target 
		exp = np.loadtxt(data_file)		   # ***** file which contains data	

	
	def _error_evaluation_rms(self, errors):
		
		sum_of_squares = 0
		
		for error in errors:
			sum_of_squares = sum_of_squares + error**2
			
		return ((sum_of_squares/len(errors))**(1./2.)) #incorporated division by n, which is the proper rms 

	def mcfunc(self, model_parameters):
		
		no_samples = 1
		
		#experimental parameters
		T_service = 22. + 273.
		prec_stress = 0
		SS_stress = 750

		strain_stress, WTN = irreverisble.mechanics(prec_stress,SS_stress,T_service,model_parameters,no_samples)
		strain_stress = np.array(np.trim_zeros(strain_stress)).reshape(-1,2)
		#print strain_stress

		#----------------------------
		cal_val = []
		errors = []

		#traverses experimental data points
		for iexp, data in enumerate(exp[:,0]):
			
			#finding nearest neighbors that surround the data points, and using them to determine the error
			for ical, data in enumerate(strain_stress[:,0]):
				
				ical = ical-1 # May or may not be advantageous to keep this instead of the range attribute for mem save
				
				left_strainpoint = strain_stress[ical,0]
				right_strainpoint = strain_stress[ical+1,0]
				
				exp_datapoint = exp[iexp,0]
				
				if(exp_datapoint>left_strainpoint and exp_datapoint<right_strainpoint):
									
					# stores the differences between the successive approximations so we interpolate
					left_difference = exp_datapoint-left_strainpoint
					right_difference = right_strainpoint-exp_datapoint
					
					total_difference = left_difference+right_difference
					
					left_weight = left_difference/total_difference
					right_weight = right_difference/total_difference
					  
					# interpolate stress based on strain?
					interpolated_strain = left_weight*left_strainpoint + right_weight*right_strainpoint
					interpolated_stress = left_weight*strain_stress[ical,1] + right_weight*strain_stress[ical+1,1]
						
					stress_error = interpolated_stress - exp[iexp,1]    
					#print stress_error
					
					#adds value, we want to find difference between these approximated data points and the real results
					cal_val.append([interpolated_strain,interpolated_stress])                 
					errors.append(stress_error)
					
					break

		#print errors
		error_rms = _error_evaluation_rms(errors)    
		cal_val = np.asarray(cal_val)

		#print cal_val
		#----------------------------

		# return error as well as the results of stress-strain curve?
		#return strain_stress, error_rms
		return error_rms

