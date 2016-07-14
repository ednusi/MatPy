"""
Optimization Suite
******************

This contains methods to optimize functions using SciPy
and evaluate the methods' performance in terms of memory,
algorithmic iterations, and runtime. 
"""

"""Basic libs"""
import numpy as np

"""Optimization"""
from scipy.optimize import minimize
from pybrain.optimization import GA

"""Evaluation"""
import timeit
from memory_profiler import memory_usage

def minimize_suite(function, methods, guess):
    """
    This method takes any method provided by http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html.

   | This method takes a function, strings representing the method to test it with, and an initial guess for the optimal solution.
   | Every minimizer in this package is a local optimization algorithm, so it will get trapped in convexities of a dataset.
   | In running, this function will display the amount of memory, the runtime, and the number of algorithmic iterations required to
   | achieve an optimal result.
    """

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


def custom_minimize(function, algorithm, bounds = None, guess = None):
    """
    This is similar to the minimize_suite, but is defined for functions like basinhopping or brute_force (in scipy.optimize), so the second parameter is a user-provided algorithm for optimization.

    Arguments:
       | algorithm - has been tested with things like scipy.optimize.basinhopping, and bruteforce, but should work with a user-defined algorithm as well.
    Keyword Arguments:
       | bounds - Limits the search domain
       | guess - an initial guess at an optimal solution
    
	| Which keyword arguments are required or optional depends on the provided algorithm.
    """

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

# Our workaround for evaluating GA performance, needs its own method because it is separate in the PyBrain module and takes different parameters
def GA_minimize(function, guess):
    """
    This function runs the genetic algorithm from PyBrain (http://pybrain.org/docs/api/optimization/optimization.html) on a function, provided with an initial guess.

   | NOTE: Format is **CRUCIAL** here or this will not work (blame the authors of PyBrain, sorry):
   | Function must take a **TUPLE** (**EVEN** if of only one element (in the form (a, )) and guess **MUST BE A LIST** (even if only with one element)
    """
    
    result = GA(function, guess, minimize=True) # set to minimize by default
    
    start = timeit.default_timer()
    mem = max(memory_usage(-1,interval=.1))
    
    print "The result is: ", result.learn()
    stop = timeit.default_timer()
    
    exec_time = stop-start

    print '{0} took {1} seconds'.format('Genetic Algorithm',exec_time)
    print '{0} used {1} megabytes'.format('Genetic Algorithm',mem)
    print
