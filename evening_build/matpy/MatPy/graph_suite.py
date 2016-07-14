"""
Graph Suite
***********

Contains all functionality needed to plot functions easily.
Uses pyplot from matplotlib.

IntervalPlot3D -- takes a function in R3, an x domain, and a y domain, and plots the function at all points on those domains.\n
barGraph -- takes some data points and plots them as a series of bars, with optionally specifiable tick labels.\n
plot2D -- takes a set of data with two columns and plots the data, where markers for the data set can be specified.\n
plotmult2D -- takes two data sets and plots each, where each data set is like the input for plot2D.\n
"""

import matplotlib
from matplotlib import pyplot as plot
matplotlib.rcParams.update({'font.size': 16}) # default font size

def IntervalPlot3D(function, x_domain, y_domain, xlabel="",ylabel="",zlabel="",title="",fontsize=14):
    """
    Plots a function over a given domain, allowing the user to provide labels for the axes.

    Requires a user to provide a function, and x_domain, and a y_domain.
    Keyword args:
        | **The three labels for the axes**
        | xlabel
        | ylabel
        | zlabel
        |  
        | title - The title of the chart
        | fontsize - Override the default font size, which is 14
    """

    fig = plot.figure()
    ax = fig.gca(projection='3d')
    plot.title(title)
    matplotlib.rcParams.update({'font.size': fontsize})

    x = np.zeros(0)
    y = np.zeros(0)

    # evenly traverses the entire domain and adds all points to the list of points to be evaluated
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
    """
    Displays all of the data points in data as a series of bars.

    Optionally a user can provide a label for the y-axis, a title, and
    tick labels for the bars.
    """

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
            
            # special case for data that is not found
            if data[index] == -1.0:
                ax.text(rect.get_x() + offset, 1.01*height,
                    'Not given\n by algorithm',
                    ha='center', va='bottom')

            # labels all of the data 
            else:    
                ax.text(rect.get_x() + offset, 1.01*height,
                    '%d' % int(height),
                    ha='center', va='bottom')

    autolabel(rects1)
    plot.ylim(0,max(data)*1.5) # enforces limits on axis range
    plot.show()
    
def plot2D(data, xtitle='', ytitle='', title='', marker='b-'):
    """
    Takes two columns for data, and plots it.

    Keyword arguments (optional):
       | axes titles 
       | plot title
       | marker (uses pyplot's standard markers)
    """
    
    # default font size
    matplotlib.rcParams.update({'font.size': 16}) 
    fig, ax = plot.subplots(figsize=(12, 9))

    # plot stress vs strain
    ax.plot(data[:,0],data[:,1],marker) 
    ax.set_xlabel(xtitle)
    ax.set_ylabel(ytitle)
    ax.set_title(title)
    
    # set the limits to entire domain and range
    plot.xlim(min(data[:,0]),max(data[:,0])*1.05)
    plot.ylim(min(data[:,1]),max(data[:,1])*1.05)

    ax.grid(True)
    fig.tight_layout()
    plot.show()
    
    
def plotmult2D(data1, data2, xtitle='', ytitle='', title='', marker1='b-', marker2='r^'):
    """
    Similar to plot2D, but plots 2 data sets.

    Takes two datasets, each consisting of two columns.

    Keyword arguments (optional):
       | axes labels
       | plot title
       | markers
    """
    
    # default font size
    matplotlib.rcParams.update({'font.size': 16}) 
    fig, ax = plot.subplots(figsize=(12, 9))

    # plot stress vs strain
    ax.plot(data1[:,0],data1[:,1],marker1)
    ax.plot(data2[:,0],data2[:,1],marker2) 
 
    ax.set_xlabel(xtitle)
    ax.set_ylabel(ytitle)
    ax.set_title(title)
    
    # ensuring that data is visible on the plot
    x_min = min((min(data1[:,0]),min(data2[:,0])))
    y_min = min((min(data1[:,1]),min(data2[:,1])))
    
    x_max = max((max(data1[:,0]),max(data2[:,0])))
    y_max = max((max(data1[:,1]),max(data2[:,1])))
    
    # (UNCOMMENT TO VIEW ALL DATA)
    #plot.xlim(x_min,x_max*1.05)
    #plot.ylim(y_min,y_max*1.05)

    # (UNCOMMENT TO VIEW ALL POSITIVE DATA)
    plot.xlim(0,x_max*1.05)
    plot.ylim(0,y_max*1.05)

    ax.grid(True)
    fig.tight_layout()
    plot.show()
