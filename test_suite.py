import numpy as np
import scipy as sp
import matplotlib
from matplotlib import pyplot as plot

from scipy.optimize import minimize

import timeit
from memory_profiler import memory_usage


def IntervalPlot3D(function, x_domain, y_domain, xlabel="",ylabel="",zlabel="",title="",fontsize=14):

    fig = plot.figure()
    ax = fig.gca(projection='3d')
    plot.title(title)
    matplotlib.rcParams.update({'font.size': fontsize})

    x = np.zeros(0)
    y = np.zeros(0)

    for y_val in y_domain:

        x = np.append(x,x_domain)

        for x_val in x_domain:

            y = np.append(y,y_val)

    z = np.zeros(0)

    for index, value in enumerate(x):

        model_params = (x[index],y[index])
        z = np.append(z,function(model_params))

    ax.plot(x,y,z,"p")

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)

    plot.show()
    
def barGraph(data, ylabel='', title='', xticklabels=None):

	N = len(data) # Number of data points
		
	width = 0.50       # the width of the bars
	offset = width/2.
	ind = np.arange(N)+offset  # the x locations for the groups

	matplotlib.rcParams.update({'font.size': 18})
	fig, ax = plot.subplots(figsize=(20,10))
	rects1 = ax.bar(ind, data, width, color='r')

	# add some text for labels, title and axes ticks
	ax.set_ylabel(ylabel)
	ax.set_title(title)
	ax.set_xticks(ind + offset)
	
	if xticklabels is not None:
		ax.set_xticklabels(xticklabels)

	# puts graph labels above bars
	def autolabel(rects):
		# attach some text labels
		for index, rect in enumerate(rects):
			
			height = rect.get_height()
			
			if data[index] == -1.0:
				ax.text(rect.get_x() + offset, 1.01*height,
					'Not given\n by algorithm',
					ha='center', va='bottom')
			else:    
				ax.text(rect.get_x() + offset, 1.01*height,
					'%d' % int(height),
					ha='center', va='bottom')

	autolabel(rects1)
	plot.ylim(0,max(data)*1.5) # enforces limits on axis range
	plot.show()
    
# conveniently creates a plot with the attributes given
def plotSingle2D(comp,xtitle,ytitle,xscale,yscale):
	
	global exp
	exp = []                           # ***** target 
	exp = np.loadtxt('ref/HSRS/22')

	fig, ax = plot.subplots(figsize=(9,6))

	ax.plot(comp[:,0],comp[:,1],lw=3)
	ax.plot(exp[:,0], exp[:,1],'o',zorder=5,markevery=5)

	ax.set_xlabel(xtitle, fontsize=35, labelpad=15)
	ax.set_ylabel(ytitle, fontsize=35, labelpad=15)
	ax.tick_params(axis='x', labelsize=25, pad = 10)
	ax.tick_params(axis='y', labelsize=25, pad = 10)

	# we maintain only positive x&y values
	ax.set_xscale(xscale, nonposx='clip')
	ax.set_yscale(yscale, nonposx='clip')
	
	ax.set_xlim(0,exp[-1,0]+1) # margin
	ax.grid(True)
	fig.tight_layout()
	plot.show()
        
"""Takes specific methods provided by scipy.optimize"""
def minimize_suite(function, methods, guess):

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


# For custom minimization methods in SciPy, like basinhopping, where the returned object provides more information
def custom_minimize(function, algorithm, guess):

	def iter_minimize(): # lightweight version of iter_minimize for a single optimization method

		start = timeit.default_timer()

		result = algorithm(function, guess) # calls the minimizer

		iterations = -1

		if 'nit' in result.keys():    
			iterations = result.get('nit')

		stop = timeit.default_timer()

		return iterations, start, stop, result

	#tracks amount of memory used
	most_mem = max(memory_usage((iter_minimize, (),)))
	num_iters, start, stop, result = iter_minimize()

	exec_time = stop-start

	print '{0} took {1} seconds. The result, {2} was found at ({3})'.format(algorithm.__name__,exec_time,result.fun,result.x)
	print '{0} used {1} megabytes and took {2} iterations'.format(algorithm.__name__,most_mem,num_iters)
	print
	
# Our workaround for evaluating GA performance
def GA_minimize(function, guess):
    
    from pybrain.optimization import GA
    
    result = GA(function,[guess, ], minimize=True) # set to minimize by default
    
    start = timeit.default_timer()
    mem = max(memory_usage((result.learn,(),)))
    stop = timeit.default_timer()
    
    print result.learn() #Comment this out for faster performance, i.e. for evaluation

    exec_time = stop-start

    print '{0} took {1} seconds'.format('Genetic Algorithm',exec_time)
    print '{0} used {1} megabytes'.format('Genetic Algorithm',mem)
    print

	

