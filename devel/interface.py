"""
Loads a stress-strain plot given a filename.
"""

"""Tkinter for GUI"""
import Tkinter as tk
from Tkinter import Entry
import tkFileDialog

"""Library for getting and plotting data"""
import parser
import graph_suite as plot
import material_analytics

"""Data handlers"""
import irreversible_stressstrain
from irreversible_stressstrain import StressStrain as strainmodel
import optimization_suite
from scipy.optimize import basinhopping
from scipy.optimize import brute
from pybrain.optimization import GA

def update():
"""Display the plot of the file with its yield point"""

	"""Opens file browser and gets selection"""
	name = tkFileDialog.askopenfilename()
	
	"""Creates model for data"""
	if 'xml' in name:
	    model = strainmodel(name, type='xml')
	    
	else:
	    model = strainmodel(name)
	
	data = model.get_experimental_data()
	
	"""Will need to be set to user-input guess"""	    
	guess = [-150,1]
	
	yieldpoint = None
	
	"""Gets radio button input as to which method to use to optimize"""
	if yield_method.get() == 1:
	    yieldpoint = material_analytics.yield_stress_classic_unfitted(data)
	    
	elif yield_method.get() == 2:
	    yieldpoint = material_analytics.yield_stress_classic_fitted(data)
	    
	elif yield_method.get() == 3:
	    yieldpoint = material_analytics.yield_stress(data)
	    
	else:
	    elastic, plastic = material_analytics.kmeanssplit(data)
	    yieldpoint = plastic[0][None,]
	
	"""Displays the found yield stress"""
	plot.plotmult2D(data, yieldpoint, title = 'File', xtitle = 'Strain ($\epsilon$)', ytitle= 'Stress ($\sigma$)')

	"""[0,1] is the first row, second column, which is the stress values"""
	SS_stress = yieldpoint[0,1]

	model_training_methods = ['Nelder-Mead','Powell','CG','Newton-CG','BFGS','L-BFGS-B','SLSQP','COBYLA','TNC','Basinhopping','Brute Force','Genetic Algorithm']
	
	"""Because basinhopping, brute force, and GA are all in separate libraries, they are handled as separate cases."""
	optmethod = optimization_method.get()-1
	if optmethod<9:
	    model_params = optimization_suite.minimize_suite(model.mcfunc, methods=[model_training_methods[optmethod],], guess = guess ,SS_stress=SS_stress)

	elif optmethod==9:
	    model_params = optimization_suite.minimize_suite(model.mcfunc, methods=[basinhopping,], guess = guess ,SS_stress=SS_stress)

	elif optmethod==10:
		model_params = optimization_suite.minimize_suite(model.mcfunc, methods=[brute,], guess = guess ,SS_stress=SS_stress)

	else:
		model_params = optimization_suite.GA_minimize(model.mcfunc, guess)

	"""Plots the data versus the fitted irreversible model data"""
	plot.plotmult2D(data, model.irreversible_model(model_params,SS_stress), title = 'Fitted Thermodynamics', xtitle = 'Strain ($\epsilon$)', ytitle= 'Stress ($\sigma$)')

"""Setting window frame""" 
root = tk.Tk()
root.resizable(width=False, height=True)
root.wm_title('Select your data file')   
root.geometry('500x280')

"""Analysis selection radio buttons"""

"""(Selection Variable)"""
lbl1 = tk.Label(root, text='Yield point selection')
lbl1.grid(row=0, column=0, sticky='W')
yield_method = tk.IntVar()

"""(Buttons)"""
b1 = tk.Radiobutton(root, text='Classic Unfitted', variable=yield_method, value=1)
b2 = tk.Radiobutton(root, text='Classic Fitted', variable=yield_method, value=2)
b3 = tk.Radiobutton(root, text='Custom', variable=yield_method, value=3)
b4 = tk.Radiobutton(root, text='Clustering', variable=yield_method, value=4)

"""(Button Placement)"""
b1.grid(row=1, column=0, sticky='W')
b2.grid(row=2, column=0, sticky='W')
b3.grid(row=3, column=0, sticky='W')
b4.grid(row=4, column=0, sticky='W')

"""Setting up the file selection button"""
load_file = tk.Button(root, text='Open a file!',command=update)
load_file.place(relx=0.4,y=230,anchor=tk.NW)

spacer = tk.Label(root, text='                                                            ')
spacer.grid(row=0, column=3)

"""Model fitting method radio buttons"""

"""(Selection Variable)"""
lbl2 = tk.Label(root, text='Optimization Technique')
lbl2.grid(row=0, column=5, sticky='E')
optimization_method = tk.IntVar()

"""(Buttons)"""
m1 = tk.Radiobutton(root, text='Nelder-Mead', variable=optimization_method, value=1)
m2 = tk.Radiobutton(root, text='Powell', variable=optimization_method, value=2)
m3 = tk.Radiobutton(root, text='CG', variable=optimization_method, value=3)
m4 = tk.Radiobutton(root, text='Newton-CG', variable=optimization_method, value=4)
m5 = tk.Radiobutton(root, text='BFGS', variable=optimization_method, value=5)
m6 = tk.Radiobutton(root, text='L-BFGS-B', variable=optimization_method, value=6)
m7 = tk.Radiobutton(root, text='SLSQP', variable=optimization_method, value=7)
m8 = tk.Radiobutton(root, text='COBYLA', variable=optimization_method, value=8)
m9 = tk.Radiobutton(root, text='TNC', variable=optimization_method, value=9)
m10 = tk.Radiobutton(root, text='Basinhopping', variable=optimization_method, value=10)
m11 = tk.Radiobutton(root, text='Brute Force', variable=optimization_method, value=11)
m12 = tk.Radiobutton(root, text='Genetic Algorithm', variable=optimization_method, value=12)

"""(Button Placement)"""
m1.grid(row=1, column=5, sticky='E')
m2.grid(row=2, column=5, sticky='E')
m3.grid(row=3, column=5, sticky='E')
m4.grid(row=4, column=5, sticky='E')
m5.grid(row=5, column=5, sticky='E')
m6.grid(row=6, column=5, sticky='E')
m7.grid(row=7, column=5, sticky='E')
m8.grid(row=8, column=5, sticky='E')
m9.grid(row=9, column=5, sticky='E')
m10.grid(row=10, column=5, sticky='E')
m11.grid(row=11, column=5, sticky='E')
m12.grid(row=12, column=5, sticky='E')

"""Start the program"""
root.mainloop()
