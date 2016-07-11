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

""" Compiles the Fortran code """
bashCommand = "make fortran"
import subprocess
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
from DataModelDict import DataModelDict as dmd

import irreverisble #importing the fortran mechanics routine

class StressStrain:
	
	# can take different file types
	def __init__(self,data_file,type='txt'):
				
		if type is 'txt':
			self.exp = np.loadtxt(data_file)		   # ***** file which contains data	
			
		elif type is 'xml':

			table = dmd(open(data_file, "r")).find('stressStrain')
			distable = []

			for row in table['rows'].iteraslist('row'):
				disrow = []
					
				for column in row.iteraslist('column'):
					disrow.append(column['#text'])
				
				distable.append(disrow)

			del distable[0] # gets rid of header
			self.exp = np.array(distable)

	# returns experimental data gathered from initialization
	def get_experimental_data(self):
		return self.exp
	
	# root means squared used to evaluate magnitude of error
	def error_evaluation_rms(self, errors):
		
		sum_of_squares = 0
		
		for error in errors:
			sum_of_squares = sum_of_squares + error**2
			
		return ((sum_of_squares/len(errors))**(1./2.)) #incorporated division by n, which is the proper rms 

	# looks at mechanical properties of material based on the physical model and experimental parameters
	# minimizes difference between experimental data and physical model
	def mcfunc(self, model_parameters):
		
		no_samples = 1
		
		#experimental parameters
		T_service = 22. + 273.
		prec_stress = 0
		SS_stress = 750

		strain_stress, WTN = irreverisble.mechanics(prec_stress,SS_stress,T_service,model_parameters,no_samples)
		strain_stress = np.array(np.trim_zeros(strain_stress)).reshape(-1,2)
		
		cal_val = []
		errors = []

		#traverses experimental data points
		for iexp, data in enumerate(self.exp[:,0]):
			
			#finding nearest neighbors that surround the data points, and using them to determine the error
			for ical, data in enumerate(strain_stress[:,0]):
				
				ical = ical-1 # May or may not be advantageous to keep this instead of the range attribute for mem save
				
				left_stresspoint = strain_stress[ical,0]
				right_stresspoint = strain_stress[ical+1,0]
				
				exp_datapoint = self.exp[iexp,0]
				
				# finding the two nearest stress points and interpolating stress and strain
				if(exp_datapoint>left_stresspoint and exp_datapoint<right_stresspoint):
									
					# stores the differences between the successive approximations so we interpolate
					left_difference = exp_datapoint-left_stresspoint
					right_difference = right_stresspoint-exp_datapoint
					
					total_difference = left_difference+right_difference
					
					left_weight = left_difference/total_difference
					right_weight = right_difference/total_difference
					  
					# interpolate strain based on stress
					interpolated_stress = left_weight*left_stresspoint + right_weight*right_stresspoint
					interpolated_strain = left_weight*strain_stress[ical,1] + right_weight*strain_stress[ical+1,1]
						
					strain_error = interpolated_strain - self.exp[iexp,1]    
					
					#adds value, we want to find difference between these approximated data points and the real results
					cal_val.append([interpolated_stress,interpolated_strain])                 
					errors.append(strain_error)
					
					break

		error_rms = self.error_evaluation_rms(errors)    
		cal_val = np.asarray(cal_val)

		return error_rms

