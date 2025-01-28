#!/usr/bin/env python

"""
Functions to read and write data from/to files
"""

import numpy as np 
import pandas as pd


def extract_precursor_sets(precursor_sets):
    # Get all possible precursors
    precursors = set()
    for k, v in precursor_sets.items():
        for p in v:
            precursors.update(p)
    precursors = list(precursors)
          

    # Create a dataframe to store the information
    df = pd.DataFrame(index=precursor_sets.keys(), columns=precursors)

    # Fill the dataframe
    for k, v in precursor_sets.items():
        for p in v:
            df.loc[k, list(p)] = True
    # Fill the rest with False
    df = df.fillna(False)
    
    return df