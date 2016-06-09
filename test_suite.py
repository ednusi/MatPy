def minimize_suite(function, methods, guess):

	import numpy as np
	import scipy as sp
	from matplotlib import pyplot as plot

	from scipy.optimize import minimize

	import timeit
	from memory_profiler import memory_usage

	start = np.zeros(0)
	stop = np.zeros(0)
	num_iters = np.zeros(0)
	most_mem = np.zeros(0)
	result = []

#runtime code goes here

#testing every minimization method
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

		#tracks amount of memory used
		most_mem = np.append(most_mem, max(memory_usage((iter_minimize, (method, num_iters, start, stop, guess),))))
		num_iters, start, stop = iter_minimize(method, num_iters, start, stop, guess)

	exec_time = stop-start

# If an algorithm took (-1) iterations, the number of iterations was not returned
	for counter, method in enumerate(methods):

		print '{0} took {1} seconds. The result, {4} was found at ({2}, {3})'.format(method,exec_time[counter],result[counter].x[0],result[counter].x[1],result[counter].fun)
		print '{0} used {1} megabytes and took {2} iterations'.format(method,most_mem[counter],num_iters[counter])
		print
