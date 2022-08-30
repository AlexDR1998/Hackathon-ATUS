import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yaml
%matplotlib inline

data_dir = "TeamTime/"

def load_yaml(name):
    with open(name) as f:
        value_codes = yaml.safe_load(f)
    return value_codes

def make_chart_pie(x, values, data):
    """
    Count the occurrence of all entries for each column
    
    
    x: A key of the data frame
    values: the value yaml file
    data: the data frame
    
    returns: A dictionary with the counting
    """
    
    #Count the occurency of all values
    counted = data[x].value_counts()
    labels_id = counted.index.tolist()
    
    #Get total 
    total_labels = list(values[x].values())
    final_labels = [total_labels[i] for i in labels_id]
    plt.figure(figsize = (10,10))
    plt.pie(list(counted), labels = final_labels)
    
    output = {}
    for i, x in enumerate(final_labels):
        output[x] = list(counted)[i]
    return output