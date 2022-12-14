#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 11:12:59 2022

@author: charlie
"""

import pandas as pd
import yaml
import numpy as np

def outliers_NaNs(arr, outliers=[-3, -2, -1]):
    """
    Parameters
    ----------
    arr : Panda DataFrames array
    outliers : float/int,
        DESCRIPTION. Values in the array to replace with NaN. The default is [-3, -2, -1].

    Returns
    -------
    arr_replace : TYPE
        DESCRIPTION.
    """
    
    arr_replace = arr.replace(outliers, value=np.nan)
    
    return arr_replace


    
    