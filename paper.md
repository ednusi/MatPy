---
title: 'MatPy: A toolbox for intelligent material design, and automatic yield stress determination'
tags:
- materials
- toolbox
- design
- stress
- strain
- nonconvex optimization
- design
authors:
- name: Edward Alexander Nusinovich
 orcid: 0000-0002-7527-4474
 affiliation: 1
- name: Sheng-Yen Li
 affiliation: 1
- name: Steven P. Mates
 affiliation: 1
- name: Carelyn Campbell
 affiliation: 1
affiliations:
- name: U.S. National Institute of Standards and Technology
 index: 1
date: 3 March 2017
---

  # Summary

  MatPy analyzes stored data files, visualizes the data, 
  and applies optimization techniques to discover material parameters in phase-based models
  and statistical models that best fit the data. The data from the Kolsky Bar mechanical testing device can be saved 
  to a variety of data schemas, including but not limited to .data and XML file schemas, and 
  had to be parsed from each of these. Parsing these data schemas is a complex and nuanced 
  task, because each data format comes with unique features in the representation of a set 
  of data by a separate encoding mechanism. 
  
  A parser program was written that would allow for a mechanical data file to be input with 
  stress-strain information, as well as strain rate data, and that would extract the information 
  into a workable format. In addition, the data is filtered as it is parsed, in order to remove 
  non-physical recorded values that are merely an artifact of wave refraction. Furthermore, 
  a visualization feature was developed that allows a user to automatically view the results 
  of input data in the form of an interactive stress-strain plot. The parsed data could then 
  be analyzed using either statistical methods that were built into the program, such as 
  logarithmic regression, or using aforementioned Optimization Techniques, that allow the user 
  to gauge the parameters of the material design.


  # References
  
  The repository: https://github.com/ednusi/MatPy
  The releases: https://pypi.python.org/pypi/MatPy
  The docs: http://pythonhosted.org/MatPy/
  
  Papers used to write the software and to validate the need for it:

	[1]	"Fact Sheet: Progress on Materials Genome Initiative," Executive Office of the President, May 14, 2012.
	[2]	S. Barron et al., "NIST Materials Genome Initiative," 2015. [Online]. Available: https://mgi.nist.gov/high-throughput-combinatorial-foundry-inorganic-materials-data-demand. Accessed: Nov. 2, 2016.
	[3]	M. Grujicic, J. S. Snipes, and S. Ramaswami, "Application of the materials-by-design methodology to redesign a new grade of the high-strength low-alloy class of steels with improved mechanical properties and Processability," Journal of Materials Engineering and Performance, vol. 25, no. 1, pp. 165–178, Dec. 2015.
	[4]	D. A. Morrow, T. Haut Donahue, G. M. Odegard, and K. R. Kaufman, "A method for assessing the fit of a constitutive material model to experimental stress–strain data," Computer Methods in Biomechanics and Biomedical Engineering, vol. 13, no. 2, pp. 247–256, Apr. 2010.
	[5]	S. P. Mates, R. Rhorer, E. Whitenton, T. Burns, and D. Basak, "A pulse-heated Kolsky bar technique for measuring the flow stress of metals at high loading and heating rates," Experimental Mechanics, vol. 48, no. 6, pp. 799–807, Apr. 2008.
	[6]	B. Song, B. R. Antoun, and H. Jin, "Dynamic tensile characterization of a 4330-V steel with Kolsky bar techniques," Experimental Mechanics, vol. 53, no. 9, pp. 1519–1529, Jun. 2013.
	[7]	Z. Huang, L. Gao, Y. Wang, and F. Wang, "Determination of the Johnson-Cook Constitutive model parameters of materials by cluster global optimization algorithm," Journal of Materials Engineering and Performance, vol. 25, no. 9, pp. 4099–4107, Jun. 2016.
	[8]	P. Bosetti, C. Maximiliano Giorgio Bort, and S. Bruschi, "Identification of Johnson–Cook and Tresca’s parameters for numerical modeling of AISI-304 machining processes," Journal of Manufacturing Science and Engineering, vol. 135, no. 5, p. 051021, Sep. 2013.

  