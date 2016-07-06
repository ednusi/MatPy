"""
optimization_suite.py
07-06-2016

This contains methods to optimize functions using SciPy
and evaluate the methods' performance in terms of memory,
algorithmic iterations, and runtime. 

Edward Alexander Nusinovich
"""

"""Basic libs"""
import numpy as np

"""Optimization"""
from scipy.optimize import minimize
from pybrain.optimization import GA

"""Evaluation"""
import timeit
from memory_profiler import memory_usage

# takes specific methods provided by scipy.optimize (Nelder-Mead, L-BFGS-B, CG, etc...)
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

            # if the number of iterations is contained in the result object
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

    most_mem = np.zeros(0)

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
    
# Our workaround for evaluating GA performance, needs its own method because it is separate in the SciPy class and takes different parameters
# FORMAT IS CRUCIAL HERE OR THIS WILL NOT WORK (NOT MY FAULT, BLAME THE AUTHORS OF PYBRAIN):
# FUNCTION MUST TAKE A TUPLE (EVEN IF OF ONLY ONE ELEMENT) AND GUESS MUST BE A LIST (EVEN IF OF ONLY ONE ELEMENT)
def GA_minimize(function, guess):
    
    result = GA(function, guess, minimize=True) # set to minimize by default
    
    start = timeit.default_timer()
    mem = max(memory_usage(-1,interval=.1))
    
    print "The result is: ", result.learn()
    stop = timeit.default_timer()
    
    exec_time = stop-start

    print '{0} took {1} seconds'.format('Genetic Algorithm',exec_time)
    print '{0} used {1} megabytes'.format('Genetic Algorithm',mem)
    print
