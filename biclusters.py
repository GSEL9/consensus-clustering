# -*- coding: utf-8 -*-
#
# _biclusters.py
#

"""
A bicluster representation.
"""

__author__ = 'Severin E. R. Langberg'
__email__ = 'Langberg91@gmail.no'


import numpy as np
import pandas as pd


class Biclusters:
    """Representation of predicted biclusters."""

    def __init__(self, rows, cols, data):

        self.rows = rows
        self.cols = cols
        self.data = data

        # NOTE: Sets attributes.
        self._setup()

    @property
    def nbiclusters(self):

        return self._nbiclusters

    @nbiclusters.setter
    def nbiclusters(self, value):

        if np.shape(self.rows)[0] == np.shape(self.cols)[0]:
            self._nbiclusters = value
        else:
            raise RuntimeError('Sample clusters: {}, ref clusters {}'
                               ''.format(sample, ref))

    def _setup(self):

        self.nrows, self.ncols = np.shape(self.data)
        self.nbiclusters = np.shape(self.rows)[0]

        return self

    @property
    def indicators(self):
        """Determine coordiantes of row and column indicators
        for each bicluster.
        """

        row_idx, col_idx = [], []
        for cluster_num in range(self.nbiclusters):

            rows_bools = self.rows[cluster_num, :] != 0
            cols_bools = self.cols[cluster_num, :] != 0

            rows = [index for index, elt in enumerate(rows_bools) if elt]
            cols = [index for index, elt in enumerate(cols_bools) if elt]

            row_idx.append(rows), col_idx.append(cols)

        return row_idx, col_idx

    @property
    def labels(self):
        """Assign row and column labels to biclusters."""

        genes = np.array(self.data.columns, dtype=object)
        cpgs =  np.array(self.data.index, dtype=object)

        row_idx, col_idx = self.indicators

        row_labels, col_labels = [], []
        for num in range(self.nbiclusters):
            row_labels.append(cpgs[row_idx[num]])
            col_labels.append(genes[col_idx[num]])

        return row_labels, col_labels
    
    
def biclusters(model, raw_data):
    """Create bicluster representations
    
    Args:
        model (sklearn.bicluster): The model used to predict biclusters.
        raw_data (pandas.DataFrame): The raw data.
    
    Returns:
        (Biclusters): A bicluster representation.
    
    """

    # Extract result.
    rows, cols = model.rows_, model.columns_
    
    assert np.shape(rows)[0] == np.shape(cols)[0]

    # Collect Bicluster instances 
    biclusters = Biclusters(
        rows=rows, cols=cols, data=raw_data
    )
    return biclusters
