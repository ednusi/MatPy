import setuptools
from distutils.core import setup

setup(name='MatPy',
      version='1.0.2',
      packages=['MatPy',],
      author='Edward Alexander Nusinovich',
      author_email='edward.nusinovich@gmail.com',
      install_requires=[
          'matplotlib',
          'numpy',
          'scipy',
          'sklearn',
          'DataModelDict',
          'pybrain',
          'memory_profiler'
      ],
	  url='https://github.com/ednusi/MatPy/tree/master/evening_build/matpy',
	  description='A toolbox for intelligent material design, automatic yield stress determination, and automatic construction of a mechanical behavior model based on experimental stress-strain data.',
      long_description=open('README').read(),
      )
