"""
material_analytics.py
06-27-16

Contains all functionality needed to
automatically determine the yield stress
of a material, even with noisy data, given
a stress-strain curve in the form
[Strain|Stress] in each row.

Edward Alexander Nusinovich
"""

"""Basic libs"""
import numpy as np
import math
from DataModelDict import DataModelDict as dmd

"""For optimization and model training"""
from scipy.optimize import curve_fit
from sklearn.linear_model import LinearRegression
from sklearn.cluster import MiniBatchKMeans as mbkmeans
from sklearn.cluster import KMeans

# returns the model after any readings greater than 0.025, any smaller are considered noise/error-prone
def delete_noise(model,cutoff = 0.025):
    
    cur_index = 0

    # deleting noisy values (possible inaccuracies up to .025 by default)
    for index, num in enumerate(model[:,0]):
        
        if num >= cutoff: 
              
             return model[index:]   
             
# makes all values positive in order to be able to take logarithms
def adjust(model):
    
    for index, num in enumerate(model[:,1]):
        
        if num<=0:
            model[index,1] = 1
        
    return model

# gives the value that is halfway through the list, left mid if there are an odd number of points
def midpoint(lst):
    
    length = len(lst)
    return lst[int(length)/2]

# clusters the data into groups and returns the split data
def kmeanssplit(data, numclusters=2):
    
    return splitdata(data,kcluster(data,numclusters=numclusters).predict(data[:,0][:,None]))

# creates a linear model based on data and predicts its values over the domain
def predictlinear(data, step = 0.5):
    
    est = linfit(data)
    x_pred = np.arange(min(data[:,0]),max(data[:,0]+1), step)
    y_pred = est.predict(x_pred[:,None])
    
    return combine_data(x_pred,y_pred)

# given a function and an interval (two-element list) and a number of points, applies it to the function and gets some sample points
def samplepoints(function, interval, numpoints):

    x_dom = np.linspace(interval[0],interval[1],numpoints)
    y_range = np.zeros(numpoints)
    
    for index, point in enumerate(x_dom):
        y_range[index] = function(point)
        
    return combine_data(x_dom,y_range)

# fits a linear regression to the data and returns it
def linfit(data, start=None):

    return LinearRegression().fit(*format_data(data,start))
    
# clusters the data using mini batch kmeans
def kminicluster(data, numclusters, start=None):
    
    return mbkmeans(n_clusters=numclusters).fit(*format_data(data,start))
    
# same as above but without mini batch (runs slower, should be more accurate)
def kcluster(data,numclusters,start=None):
    
    return KMeans(n_clusters=numclusters).fit(*format_data(data,start))
    
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
    
# takes the approximate derivative of the model by taking slopes
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
    
# finds the yield stress of a dataset automatically using kmeans clustering and covariance analysis
def yield_stress(model, numpoints=1000, cutoff=0.025, startx=None, endx=None, decreasingend=False):

    """Default interval values"""
    if startx is None:
        startx=min(model[:,0])+0.1
    if endx is None:
        endx=max(model[:,0])

    """We get rid of the noise in the data, and select only positive values (so that logarithms can be taken)"""
    model = delete_noise(model,cutoff=cutoff)
    model = adjust(model)

    """a and c are parameters"""
    def fit(x, a,c):
        return a*np.log(x)+c

    strain = model[:,0]
    stress = model[:,1]

    """We are fitting a logarithmic curve as closely as possible to the dataset"""
    optimal_params, cov_matrix = curve_fit(fit,strain,stress)
    a, c = optimal_params

    """The fitted version of the dataset"""
    def bestfit(x):
        return a*np.log(x)+c

    """
    We look for the place where the slope is average over
    the domain by taking sample points of the logarithmic curve
    """
    gap_len = (endx-startx)/numpoints

    xs = np.linspace(startx,endx,numpoints)
    ys = bestfit(xs)

    pred_data = combine_data(xs,ys)
    pred_slope = get_slopes(pred_data)

    ave_slope = 0

    """If the slope decreases at the end, we cluster the data to avoid referencing the end of the dataset"""
    if decreasingend is True:
        
        """Defining average slope by observing clusters in data"""
        left, right = kmeanssplit(model)
        leftmid, rightmid = midpoint(left)[None,:], midpoint(right)[None,:]
        ave_slope = (rightmid[0,1]-leftmid[0,1])/(rightmid[0,0]-leftmid[0,0])
            
    else:
        """Otherwise, we get the slope over the whole interval to find where slope begins to decrease overall"""    
        ave_slope = (stress[-1]-stress[0])/(strain[-1]-strain[0])
    
    """As soon as the slope at a point is less than the average slope, we stop"""
    for ind, slope in enumerate(pred_slope):
        if slope<ave_slope:
            break

    """
    We must take into account that we may not have a 
    data point in the experimental set where we have found a result,
    so we find the nearest neighbor in our dataset
    """
    datapointind = ind*gap_len

    """Here we find the nearest neighbor in the dataset"""
    for ind, stra in enumerate(model[:,0]):

        if stra > datapointind:
            return model[ind][None,:]

    raise ValueError("The data does not seem to have a yield")     
      

