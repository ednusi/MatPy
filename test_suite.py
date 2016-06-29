"""
test_suite.py

Contains all functionality needed to optimize functions, test their
performance, and format them for ML.
06-27-16

-Edward Nusinovich
"""

import numpy as np
import scipy as sp
import math

from scipy.optimize import minimize
from sklearn.linear_model import LinearRegression
from sklearn.cluster import MiniBatchKMeans as mbkmeans
from sklearn.cluster import KMeans

import timeit
from memory_profiler import memory_usage
from pybrain.optimization import GA

# fits a linear regression to the data and returns it
def linfit(data, start=None):

	return LinearRegression().fit(*format_data(data,start))
	
# clusters the data using mini batch kmeans
def kminicluster(data, numclusters, start=None,init='kmeans++'):
	
	return mbkmeans(n_clusters=numclusters,init=init).fit(*format_data(data,start))
	
# same as above but without mini batch (runs slower, should be more accurate)
def kcluster(data,numclusters,start=None,init='kmeans++'):
	
	return KMeans(n_clusters=numclusters,init=init).fit(*format_data(data,start))
	
# this method will put data in the appropriate format for regression (Scikit-Learn)
def format_data(data, start=None):
	
	return (expToTrain(data, start),data[start:,1])
	
# given two arrays, returns a combined list where each element is x_i,y_i
def combine_data(data1,data2):
	
	return np.array([list(a) for a in zip(data1,data2)])

# converts every non-numerical list value to zero
def regularize(data):
	
	for index, val in enumerate(data):
		if math.isinf(val) or math.isnan(val):
			data[index]=0
        
	return data

# takes predictions from kmeans clustering and split the table into two groups
def splitdata(data, predictions):
	
	initgroup = predictions[0]
	splitgroup = 0

	for index, val in enumerate(predictions):
		
		# as soon as we reach the new group, we have found our dividing point
		if val != initgroup:
			splitgroup = index
			break
        
	"""Instead of creating tuples, we create lists"""
	elastic = combine_data(data[:splitgroup,0],data[:splitgroup,1]) 
	plastic = combine_data(data[splitgroup:,0],data[splitgroup:,1])
	
	return elastic, plastic
	
def get_slopes(model):
    
    strain = model[:,0]
    stress = model[:,1]

    slopes = []

    """Approximating the partial derivatives of stress/strain"""
    for index in xrange(len(stress)-1):

        rise = (stress[index+1]-stress[index])
        run = (strain[index+1]-strain[index])

        if run==0:
            slopes.append(0)

        else:
            slopes.append(rise/run)

    return np.array(slopes)

# converts a bunch of domain values to lists, because each domain value must be iterable for training data
def expToTrain(exp,start=None):
	
	x_train = []
	
	for data in exp[start:,0]:
		x_train.append([data, ])
	
	return x_train
      
# takes specific methods provided by scipy.optimize
def minimize_suite(function, methods, guess):

	start = np.zeros(0)
	stop = np.zeros(0)
	num_iters = np.zeros(0)
	most_mem = np.zeros(0)
	result = []

	# testing every minimization method
	for method in methods:
        
		def iter_minimize(method, num_iters, start, stop, guess):

			start = np.append(start,timeit.default_timer())

			# Possibly was finding the iterations in the wrong order
			cur_result = minimize(function, x0 = guess, method = method, tol=1e-6) 
			result.append(cur_result)

			keys = cur_result.keys() # contains all traits of result
			iterations = -1

			if 'nit' in keys:    
				iterations = cur_result.get('nit')

			num_iters = np.append(num_iters,iterations)
			stop = np.append(stop,timeit.default_timer())

			return num_iters, start, stop

		# tracks amount of memory used  by current process (-1) every interval (.2 seconds)
		current_memory = memory_usage(-1, interval=.2) 
		
		most_mem = np.append(most_mem, max(current_memory))
		num_iters, start, stop = iter_minimize(method, num_iters, start, stop, guess)

	exec_time = stop-start

	# If an algorithm took (-1) iterations, the number of iterations was not returned
	for counter, method in enumerate(methods):

		print '{0} took {1} seconds. The result, {4} was found at ({2}, {3})'.format(method,exec_time[counter],result[counter].x[0],result[counter].x[1],result[counter].fun)
		print '{0} used {1} megabytes and took {2} iterations'.format(method,most_mem[counter],num_iters[counter])
		print


# For custom minimization methods in SciPy, like basinhopping, where the returned object provides more information
def custom_minimize(function, algorithm, bounds = None, guess = None):

	def iter_minimize(): # lightweight version of iter_minimize for a single optimization method

		start = timeit.default_timer()
		
		result = 0
		
		# some minimization techniques do not require an initial guess
		if guess is not None:
			result = algorithm(function, guess) 

		else:
			result = algorithm(function, bounds)

		iterations = -1

		if 'nit' in result.keys():    
			iterations = result.get('nit')

		stop = timeit.default_timer()

		return iterations, start, stop, result

	#tracks amount of memory used  by current process (-1) every interval (.2 seconds)
	current_memory = memory_usage(-1, interval=.2) 
	most_mem = np.append(most_mem, max(current_memory))
	
	num_iters, start, stop, result = iter_minimize()

	exec_time = stop-start

	print '{0} took {1} seconds. The result, {2} was found at ({3})'.format(algorithm.__name__,exec_time,result.fun,result.x)
	print '{0} used {1} megabytes and took {2} iterations'.format(algorithm.__name__,most_mem,num_iters)
	print
	
# Our workaround for evaluating GA performance
def GA_minimize(function, guess):
    
    result = GA(function,[guess, ], minimize=True) # set to minimize by default
    
    start = timeit.default_timer()
    mem = max(memory_usage((result.learn,(),)))
    stop = timeit.default_timer()
    
    print result.learn() #Comment this out for faster performance, i.e. if used purely for evaluation

    exec_time = stop-start

    print '{0} took {1} seconds'.format('Genetic Algorithm',exec_time)
    print '{0} used {1} megabytes'.format('Genetic Algorithm',mem)
    print


