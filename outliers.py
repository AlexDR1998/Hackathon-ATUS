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
    
    arr_replace = arr.replace(outliers, value=np.nan)
    
    return arr_replace


    
    