"""
Material Analytics
******************

Contains all functionality needed to
**automatically determine the yield stress**
of a material (see *yield_stress()*), even with noisy data, given
a stress-strain curve in the form
[Strain|Stress] in each row. Also automatically
creates a phenomenological model for the material's behavior under
stress and can return Young's Modulus for the elastic deformation
of the material.

This works for alloys that exhibit the yield point
phenomenon as well.
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

def young_modulus(data):
    """
    Given a stress-strain dataset, returns Young's Modulus.
    """
    
    yielding = yield_stress(data)[0]

    """Finds the yield index"""
    yield_index = 0
    for index, point in enumerate(data):

        if (point == yielding).all():
            yield_index = index
            break

    """Finds data in elastic region"""
    elastic = data[:yield_index+1]

    """
    Finds the upper yield point (lower yield point is the *yielding* variable). 
    We're taking the first element ([0]) because it returns the 
    first element that meets the criteria in parentheses.
    
    It's a two-dimensional array so we have to do this twice.
    """
    upperyieldpoint_index = np.where(elastic==max(elastic[:,1]))[0][0]
    upperyieldpoint = elastic[upperyieldpoint_index]

    """We estimate the region until the first upper yield point with a linear model"""
    lin_elastic_region = elastic[:upperyieldpoint_index+1]
    
    """The slope of this region is Young's Modulus"""
    return (lin_elastic_region[-1,1]-lin_elastic_region[0,1])/(lin_elastic_region[-1,0]-lin_elastic_region[0,0])

def yield_stress(model, numpoints=1000, cutoff=0.0, startx=None, endx=None, decreasingend=False):
    """
    Finds the yield stress of a dataset **automatically** using kmeans clustering and covariance analysis.

    In order to use this function, you just need to provide it with a stress/strain curve as a numpy array
    where the data is formatted as a two-column array. The first column is all of the stress values,
    and the second column is all of the strain values.

    This works by fitting a logarithmic model as closely as possible to the experimental data (to reduce noise)
    and then to analyze where the slope begins to be decrease relative to the average slope. In other words,
    where :math:`\partial \sigma/ \partial \epsilon < (f(b)-f(a))/(b-a)` where a and b are the beginning and
    end of the interval, respectively. For the purposes of this method, it is important that we have data up
    until the point of failure of a given material.
    """

    """Default interval values"""
    if startx is None:
        startx=min(model[:,0])+0.1
    if endx is None:
        endx=max(model[:,0])

    """We get rid of the noise in the data, and select only positive values (so that logarithms can be taken)"""
    model = log_prep(model,cutoff = cutoff)

    """Fitting a log function to our data, bestfit is that function"""
    bestfit = log_approx(model)

    """
    We look for the place where the slope is average over
    the domain by taking sample points of the logarithmic curve
    """
    gap_len = (endx-startx)/numpoints

    xs = np.linspace(startx,endx,numpoints)
    ys = bestfit(xs)

    """Find the slope of sample points from our log curve"""
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
        ave_slope = (ys[-1]-ys[0])/(xs[-1]-xs[0])
    
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
  
def yield_stress_classic_fitted(data_original, cutoff = 0.0, offset = 0.002):

    """Fit a log curve"""
    data = log_prep(data_original, cutoff = cutoff)
    logapprox = log_approx(data)

    """Take sample data points"""
    data_x = np.linspace(min(data[:,0]),max(data[:,0]),1001)
    data_y = logapprox(data_x)
    data = combine_data(data_x,data_y)

    """Determine average slope"""
    av_slope = (data[-1,1]-data[0,1])/(data[-1,0]-data[0,0]) #rise over run
    closest_index = lambda data, value: (np.abs(data-value)).argmin()
    deriv1st = combine_data(data[:,0], get_slopes(data))

    """Determine where slope is closest to average"""
    bend = closest_index(deriv1st[:,1],av_slope)

    """Fitted this offset line to the left side"""
    young_modulus = (data[bend,1]-data[0,1])/(data[bend,0]-data[0,0])
    def linear_estimation(x):
    return data[0,1] + young_modulus*(x-offset)

    """Sample linear points"""
    linear_y = linear_estimation(data_x)

    """Find closest point in fitted curve"""
    difference_bw_est = np.abs(data_y-linear_y)
    intersection = data[np.where(difference_bw_est==min(difference_bw_est))[0]]

    """Find closest point in original dataset"""
    data = data_original
    intersect_x = intersection[0,0]
    intersect_index = closest_index(data[:,0],intersect_x)

    return data[intersect_index][None,]
    
def yield_stress_classic_unfitted(data, cutoff = 0.0, offset = 0.002):

    """Determine average slope"""
    av_slope = (data[-1,1]-data[0,1])/(data[-1,0]-data[0,0])
    closest_index = lambda data, value: (np.abs(data-value)).argmin()
    deriv1st = combine_data(data[:,0],get_slopes(data))

    """Determine where slope is closest to average"""
    bend = closest_index(deriv1st[:,1],av_slope)

    """Fitted this offset line to the left side"""
    young_modulus = (data[bend,1]-data[0,1])/(data[bend,0]-data[0,0])
    def linear_estimation(x):
        return data[0,1] + young_modulus*(x-offset)

    """Sample linear points"""
    linear_y = linear_estimation(data[:,0])

    """Find closest point in fitted curve"""
    difference_bw_est = np.abs(data[:,1]-linear_y)
    intersection = data[np.where(difference_bw_est==min(difference_bw_est))[0]]

    """Find closest point in original dataset"""
    intersect_x = intersection[0,0]
    intersect_index = closest_index(data[:,0],intersect_x)

    return data[intersect_index][None,]
    
def stress_model(data, yielding = None, strain = None):
    """
    Returns a two-element array with the strain value as the first
    item, and the expected stress as the second if a strain value is provided.
    Otherwise returns a function that will predict stress given a strain value.
    
    Given a dataset and a strain value, predicts what the stress will be at that point.
    As the first parameter, data should be an array with a bunch of entries
    [strain, stress]. 
    The second parameter, strain should be the value for which you wish to estimate 
    stress.
    
    This effectively constructs a physical model for the stress-strain 
    behavior of any material on-the-fly. If no expected strain value is
    provided, this function will simply return the physical model function
    that automatically computes expected stress. This is the preferred use-case 
    for large datasets where the stress-strain curve will need to be predicted repeatedly,
    because otherwise the entire model is recalculated each time, which
    is hugely inefficient.    
    """
    if yielding is None:
        yielding = yield_stress(data)[0]

    """Finds the yield index"""
    yield_index = 0
    for index, point in enumerate(data):

        if (point == yielding).all():
            yield_index = index
            break

    """Separates data into plastic and elastic regions"""
    elastic = data[:yield_index+2]
    plastic = data[yield_index+1:]

    """
    Finds the upper yield point (lower yield point is the *yielding* variable). 
    We're taking the first element ([0]) because it returns the 
    first element that meets the criteria in parentheses.
    
    It's a two-dimensional array so we have to do this twice.
    """
    upperyieldpoint_index = np.where(elastic==max(elastic[:,1]))[0][0]
    upperyieldpoint = elastic[upperyieldpoint_index]

    """We estimate the region until the first upper yield point with a linear model"""
    lin_elastic_region = elastic[:upperyieldpoint_index+1]
    
    """Creating a function that will linearly fit the data"""
    def lin_elastic_model(x):
        m = (lin_elastic_region[-1,1]-lin_elastic_region[0,1])/(lin_elastic_region[-1,0]-lin_elastic_region[0,0])
        return m*x + lin_elastic_region[0,1]
    
    """
    If the upper yield point is the only yield point, 
    then the material doesn't exhibit the yield point phenomenon.

    Otherwise, we establish the domain in which the yield point 
    phenomenon occurs, within which we will be selecting nearest
    neighbors as a method of approximation. The yield point pheno-
    menon occurs when there are two distinct yield points, and 
    that when plastic deformation begins, stress is immediately 
    relieved.
    """
    yieldpointphenom_region = None
    yieldpointphenom = True

    if upperyieldpoint_index==yield_index:
        yieldpointphenom = False        

    if yieldpointphenom:
        yieldpointphenom_region = [upperyieldpoint_index,yield_index]

    """We must determine which domain contains the strain point requested"""
    
    start_yield = upperyieldpoint[0]

    """If we had lists previously, we have an extra dimension we need to get rid of for processing"""
    if yielding.ndim == 2:
        yielding = yielding[0]
    
    def stress_value(strain):
    
        if strain < 0 or strain > max(data[:,0]):
            
            """(Out of range)"""
            return np.nan
        
        elif strain < start_yield:

            """Linear approximation (elastic region)"""
            return [strain, lin_elastic_model(strain)]

        elif yieldpointphenom and strain >= start_yield and strain < yielding[0]:
            
            """Picks the nearest neighbor in this zone"""
            yieldpoints_inregion = elastic[np.where(np.logical_and(elastic[:,0] >= start_yield, elastic[:,0] < yielding[0]) )]

            """As soon as we find a neighbor, we return its value"""
            for val in yieldpoints_inregion:
                if val[0] > strain:
                    return [strain,val [1]]
            
            return yieldpoints_inregion[-1]
            
        elif not yieldpointphenom or strain >= yielding[0]:
               
            """We fit a logarithmic curve to approximate the plastic region"""
            plastic_reg = log_approx(plastic)
            return np.array([strain,plastic_reg(strain)])
            
    """If we should evaluate the function at a point, we'll do so, otherwise we return the function itself"""
    if strain is None:
        return stress_value
        
    else:
        return stress_value(strain)
                 

def log_approx(model):
    """
    Given a dataset with two columns,
    this function returns the logarithmic
    function that best fits that data.
    """
    
    """a and c are parameters"""
    def fit(x, a, c):
        return a*np.log(x)+c

    strain = model[:,0]
    stress = model[:,1]

    """We are fitting a logarithmic curve as closely as possible to the dataset"""
    optimal_params, cov_matrix = curve_fit(fit,strain,stress)
    a, c = optimal_params

    """The fitted version of the fit function"""
    def bestfit(x):
        return a*np.log(x)+c
        
    return bestfit

def log_prep(model, cutoff = 0.025):
    """
    Makes data ready for logarithmic 
    approximation. Deletes data components that
    we know are inaccurate and sets all to be
    positive because logs can only be taken of
    positive values.
    """
    
    model = delete_noise(model,cutoff=cutoff)
    model = adjust(model)
    return model

def delete_noise(model,cutoff = 0.025):
    """
    Takes an array (assuming it's roughly sorted) and returns it after
    a certain value (cutoff), useful for removing early values which may
    contain high levels of noise.
    """

    cur_index = 0

    # deleting noisy values (possible inaccuracies up to .025 in the strain by default)
    for index, num in enumerate(model[:,0]):
        
        if num >= cutoff: 
              
             return model[index:]   
             
def adjust(model):
    """
    Written for convenience because
    it makes all values positive in
    order to be able to take logarithms.
    """
    
    for index, num in enumerate(model[:,1]):
        
        if num<=0:
            model[index,1] = 1
        
    return model

def midpoint(lst):
    """
    Returns the value that is halfway through the
    list (index-wise), left midpoint if
    there are an odd number of points.
    """
    
    length = len(lst)
    return lst[int(length)/2]

def kmeanssplit(data, numclusters=2):
    """Clusters the data into groups (k-means) and returns the split data."""
    
    return splitdata(data,kcluster(data,numclusters=numclusters).predict(data[:,0][:,None]))

def splitdata(data, predictions):
    """Takes predictions from kmeans clustering and split the table into two groups."""
    
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

def predictlinear(data, step = 0.5):
    """Creates a linear model based on data and predicts its values over the domain, returning the predictions."""
    
    est = linfit(data)
    x_pred = np.arange(min(data[:,0]),max(data[:,0]), step)
    y_pred = est.predict(x_pred[:,None])
    
    return combine_data(x_pred,y_pred)

def samplepoints(function, interval, numpoints):
    """Given a function and an interval (two-element list) and a number of points, applies it to the function and gets sample points at even intervals."""

    x_dom = np.linspace(interval[0],interval[1],numpoints)

    """
    If the function returns lists, then we have to convert them to numpy arrays
    This is necessary for our statistical model prediction method.
    """
    if isinstance(function(0), list):

        nums = np.zeros(2)

        """We convert to numpy arrays"""
        for val in x_dom:
            nextval = np.asarray(function(val))

            """
            If we go out of bounds, the model methods will begin to return nan, so at that point
            we just need to return what we have so far.
            """
            if np.isnan(nextval).any():
                break
            
            nums = np.vstack((nums, nextval[None,:]))

        """Ignoring the first element which is 2 zeros (needed for size consistency when stacking)"""    
        return nums[1:]

    else:
        return combine_data(x_dom,function(x_dom))

def linfit(data, start=None):
    """Fits a linear regression to the data and returns it."""

    return LinearRegression().fit(*format_data(data,start))
    
def kminicluster(data, numclusters, start=None):
    """Clusters the data using mini batch kmeans."""
    
    return mbkmeans(n_clusters=numclusters).fit(*format_data(data,start))
    
def kcluster(data,numclusters,start=None):
    """Clusters the data using regular kmeans clustering."""
    
    return KMeans(n_clusters=numclusters).fit(*format_data(data,start))
    
def format_data(data, start=None):
    """This method will put data in the appropriate format for regression (Scikit-Learn)."""
    
    return (expToTrain(data, start),data[start:,1])
    
def combine_data(data1,data2):
    r"""Given two arrays, returns a combined list where each element is :math:`x_i,y_i`."""

    return np.array([list(a) for a in zip(data1,data2)])

def regularize(data):
    """Converts every non-numerical list value to zero which is useful for analysis later."""
    
    for index, val in enumerate(data):
        if math.isinf(val) or math.isnan(val):
            data[index]=0
        
    return data
    
def get_slopes(model):
    """
    Takes the approximate derivative of a two-column dataset by taking slopes between all of the points.

    The data should be formatted
    [x,y] for each row.
    """
    
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

def expToTrain(exp,start=None):
    """Converts a bunch of individual domain values to lists, because each domain value must be iterable for training data."""
    
    x_train = []
    
    for data in exp[start:,0]:
        x_train.append([data, ])
    
    return x_train

