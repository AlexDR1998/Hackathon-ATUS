import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yaml

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

def plot_all_histograms(data, column_codes, value_codes, output_folder):
    """Plots a histogram of responses to each question (column column_code) asked in the survey.
    Saves the results to a output_folder.

    Args:
        data (Pandas dataframe): Dataframe containing the responses to the survey
        column_codes (dict): Dictionary of the question (column) codes and the full description
        value_codes (dict): Dictionary of the response (value) codes for questions with discrete answers
        output_folder (str): Folder to save plots to
    """
    # Iterate over each of the questions in the survey
    for column_code in column_codes:
        fig, ax = plt.subplots(figsize=(11.75, 8.25))
        # If the column_code exists in values_codes.yaml then the data is discrete
        if column_code in value_codes:
            # Get the list of value codes
            val_codes = np.array([int(code) for code in value_codes[column_code].keys()])
            # Explicitly state the number of bins to avoid different response codes being grouped together
            bins = np.linspace(min(val_codes), max(val_codes), len(val_codes)+1)

            ax.hist(data[column_code], color='tab:orange',
                    bins=bins,
                    align='mid')
            ax.set_xticks(val_codes + 0.5,
                          labels=value_codes[column_code].values(),
                          rotation=90)
        else:
            ax.hist(data[column_code])

        ax.set_title(f"{column_code:}: {column_codes[column_code]:}")
        ax.set_xlabel('Response')
        ax.set_ylabel('Number of responses')
        plt.savefig(f"{output_folder:}/{column_code:}.png")
        plt.close()
        
def plot_histogram(data, column_code, value_codes):
    """Plots a histogram of responses to each question (column column_code) asked in the survey.
    Saves the results to a output_folder.

    Args:
        data (Pandas dataframe): Dataframe containing the responses to the survey
        column_codes (str): Question (column) code
        value_codes (dict): Dictionary of the response (value) codes for questions with discrete answers
        output_folder (str): Folder to save plots to
    """
    fig, ax = plt.subplots(figsize=(11.75, 8.25))
    # If the column_code exists in values_codes.yaml then the data is discrete
    if column_code in value_codes:
        # Get the list of value codes
        val_codes = np.array([int(code) for code in value_codes[column_code].keys()])
        # Explicitly state the number of bins to avoid different response codes being grouped together
        bins = np.arange(min(val_codes), max(val_codes)+2, 1) - 0.5

        ax.hist(data[column_code], color='tab:orange',
                bins=bins,
                align='mid',
                rwidth=0.9)
        ax.set_xticks(val_codes,
                        labels=value_codes[column_code].values(),
                        rotation=90)
    else:
        ax.hist(data[column_code])

    ax.set_title(f"{column_code:}")
    ax.set_xlabel('Response')
    ax.set_ylabel('Number of responses')
    fig.tight_layout()
    plt.show()
        
        
if __name__ == "__main__":
    datasets = ['activity', 'respondents', 'roster']

    column_codes = {}
    value_codes = {}

    for dataset in datasets:
        with open(f"{dataset:}/value_codes.yaml") as val_codes, open(f"{dataset:}/column_codes.yaml") as col_codes:
            value_codes[dataset] = yaml.safe_load(val_codes)
            column_codes[dataset] = yaml.safe_load(col_codes)

    responses= pd.read_csv(f"roster/atusrost_0321.csv")
    
    plot_histogram(responses, 'TERRP', value_codes['roster'])
