import subprocess

""" Compiles the Fortran code """
bashCommand = "make fortran"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)