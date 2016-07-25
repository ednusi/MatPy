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

"""Display the plot of the file with its yield point"""
def update():

	name = tkFileDialog.askopenfilename()
	
	"""Uses radio buttons to establish file type"""
	if 'xml' in name:
	    model = parser.stress_strain(name, type='xml').get_experimental_data()

	else:
	    model = parser.stress_strain(name).get_experimental_data()
	    
	plot.plotmult2D(model, material_analytics.yield_stress(model), title = 'File', xtitle = 'Strain ($\epsilon$)', ytitle= 'Stress ($\sigma$)')

"""Setting window frame""" 
root = tk.Tk()
root.wm_title('Enter the name of your file ')   
root.geometry('500x100')

"""Analysis selection radio buttons


(TBD)"""


"""Setting up the update button"""
load_file = tk.Button(root, text='Open a file!',command=update)
load_file.grid(row=1, column=0)
load_file.place(relx=0.5,rely=0.7,anchor=tk.CENTER)

"""Start the program"""
root.mainloop()
