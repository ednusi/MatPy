import setuptools
from distutils.core import setup

setup(name='Intelligent Material Design',
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
      long_description=open('README.txt').read(),
      )
