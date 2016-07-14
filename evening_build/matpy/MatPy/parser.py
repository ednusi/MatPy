"""

Stress-Strain Data Parser
*************************

Given a file containing experimental stress-strain
data, this class parses it and turns it into a
numpy array.

If the data is in a text file, it just needs
to be two columns, the first one strain, and
the second one stress.

If the data is in an XML file, it should have
a stressStrain tag where the relevant data begins
and then rows and columns with data as follows::

    <headers>
	<column id="1">True Strain</column>
	<column id="2">True Stress [MPa]</column>
	<column id="3">True Strain Rate [1/s]</column>
    </headers>
    <rows>
	<row id="1">
	    <column id="1">0.000303349228225</column>
	    <column id="2">-10.3437455647</column>
	    <column id="3">0.0</column>
	</row>
	<row id="2">
	    <column id="1">4.86122562637e-06</column>
	    <column id="2">9.89667339963</column>
	    <column id="3">-596.976005197</column>
	</row>
    </rows>

"""


"""To parse the data"""
from DataModelDict import DataModelDict as dmd
import numpy as np

class stress_strain:
    """
    This class will contain the relevant data from a file   
      
    For the constructor:
    Takes in a file name, by default assuming it's a text file.

    data_file is the name of the file with the data
    (must be in your directory).

    Include the full file name, with the extension
    (if applicable).
    If you wish to parse an xml file, specify type="xml"
    as a keyword argument.
    """
    
    def __init__(self,data_file,type='txt'): 
                
        if type is 'txt':
            self.exp = np.loadtxt(data_file)            
            
        elif type is 'xml':
            """Uses DataModelDict to parse XML"""

            table = dmd(open(data_file, "r")).find('stressStrain')
            distable = []

            for row in table['rows'].iteraslist('row'):
                disrow = []
                    
                for column in row.iteraslist('column'):
                    """Adds every column entry for each row"""
                    disrow.append(column['#text'])
                
                distable.append(disrow)

            del distable[0] # gets rid of header
            self.exp = np.array(distable)

    def get_experimental_data(self):
        """
        Returns experimental data gathered from initialization.

        If you are using the other methods in this package to
        automatically determine yield stress, call this method after
        creating an instance of this class to be able to use the
        data with those methods.        
        """
        return self.exp
