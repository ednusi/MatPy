This is a toolbox that can be used to plot and analyze mechanical properties of materials.

There are a few modules, (usable, but still under work) that can be used to plot data (graph_suite.py), optimize functions (optimization_suite.py),
and analyze data (material_analytics.py).

To my understanding, there are no tools currently available to automatically determine the yield stress of a material. 
This is a huge drawback for large datasets, and so the yield_stress() function seeks to create a universal tool to do so, using ML clustering, as well as basic regression analysis.

-Edward Nusinovich
 July 7th, 2016