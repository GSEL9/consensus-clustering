# -*- coding: utf-8 -*-
#
# io.py
#
# This module is part of emQTL biclustering analysis.
#

"""
Read raw data from file or save detected biclusters.
"""

__author__ = 'Severin E. R. Langberg'
__email__ = 'Langberg91@gmail.no'


# Import external Python packages.
import numpy as np
import pandas as pd


def read_data(path_to_file, log_transform=True):
    """Reads a file of raw data.

    Args:
        path_to_file (str): A reference to the location of the data.

    Kwargs:
        log_transform (bool): Determine to apply -log10(*) transform to data.

    Returns:
        (pandas.DataFrame): Formatted raw data.

    """
    # Read raw data as pandas.DataFrame.
    raw_data = pd.read_csv(
        path_to_file, delim_whitespace=True, index_col=0
    )
    # Infer dtypes.
    data = raw_data.infer_objects()

    # Apply negative base-10 logarithm to values.
    if log_transform:
        transf_data = data.apply(lambda val: -np.log10(val))
        # Replace NaNs with zeros.
        transf_data.fillna(0, inplace=True)
        return transf_data
    else:
        # Replace NaNs with zeros.
        data.fillna(0, inplace=True)
        return data
    
    
def write_data(path_to_file, biclusters, threshold=1):
    """Saves bicluster labels to disk.
    
    Args:
        path_to_file (str): Reference to location for storing file.
        biclusters (array-like): The bicluster members.
        
       
    Kwargs:
        threshold (int): The minimum number of members allowed in each 
            bicluster.
        
    """
    with open(path_to_file, 'w') as outfile:
        num = 1

        for bicluster in biclusters:
            
            outfile.write('clusternum_{0}\n'.format(num))
            if len(bicluster) < threshold:
                outfile.write('\n')
            else:
                for item in bicluster:
                    outfile.write('{}\n'.format(item))

            num += 1
            
    return None
