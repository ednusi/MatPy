
all:
	clear
	python mc.py

fortran:
	clear
	f2py -c -m irreverisble irreverisble.f90
