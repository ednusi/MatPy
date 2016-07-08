import setuptools
from distutils.core import setup

setup(name='Intelligent_Material_Design',
      version='0.5',
      packages=['intelligent_materials',],
      author='Edward Alexander Nusinovich',
      author_email='edward.nusinovich@gmail.com',
      install_requires=[
          'matplotlib',
          'numpy',
          'scipy',
          'math',
          'sklearn',
          'DataModelDict',
          'pybrain',
          'timeit',
          'memory_profiler'
      ],
	  url='https://github.com/ednusi/notebooks/tree/master/evening_build/Intelligent%20Material%20Design',
	  description='A toolbox for intelligent material design, and automatic yield stress determination',
      long_description=open('README.txt').read(),
      )
