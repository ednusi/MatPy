"""
Loads a stress-strain plot given a filename.

"""

"""Tkinter for GUI"""
import Tkinter as tk
from Tkinter import Entry

"""Library for getting and plotting data"""
import parser
import graph_suite as plot
import material_analytics

"""Display the plot of the file with its yield point"""
def update():
    
    name = enter_text.get()
    model = parser.stress_strain(name).get_experimental_data()
    plot.plotmult2D(model, material_analytics.yield_stress(model), title = 'File: ' + name, xtitle = 'Strain ($\epsilon$)', ytitle= 'Stress ($\sigma$)')

"""Setting window frame""" 
root = tk.Tk()
root.wm_title('Enter the name of your file ')   
root.geometry('500x100')

"""Establishing filename input"""
enter_text = Entry(root)
enter_text.grid(row=0,column=0)
enter_text.place(relx=0.5,rely=0.3,anchor=tk.CENTER)

"""Setting up the button"""
load_file = tk.Button(root, text='Plot Data',command=update)
load_file.grid(row=1, column=0)
load_file.place(relx=0.5,rely=0.7,anchor=tk.CENTER)

"""Start the program"""
root.mainloop()
