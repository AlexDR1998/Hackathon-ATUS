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
    """Plots a histogram of responses to each question (column tag) asked in the survey.
    Saves the results to a output_folder.

    Args:
        data (Pandas dataframe): Dataframe containing the responses to the survey
        column_codes (dict): Dictionary of the question (column) codes and the full description
        value_codes (dict): Dictionary of the response (value) codes for questions with discrete answers
        output_folder (str): Folder to save plots to
    """
    # Iterate over each of the questions in the survey
    for tag in column_codes:
        fig, ax = plt.subplots(figsize=(11.75, 8.25))
        # If the tag exists in values_codes.yaml then the data is discrete
        if tag in value_codes:
            # Get the list of value codes
            val_codes = np.array([int(code) for code in value_codes[tag].keys()])
            # Explicitly state the number of bins to avoid different response codes being grouped together
            bins = np.linspace(min(val_codes), max(val_codes), len(val_codes)+1)

            ax.hist(data[tag], color='tab:orange',
                    bins=bins,
                    align='mid')
            ax.set_xticks(val_codes + 0.5,
                          labels=value_codes[tag].values(),
                          rotation=90)
        else:
            ax.hist(data[tag])

        ax.set_title(f"{tag:}: {column_codes[tag]:}")
        ax.set_xlabel('Response')
        ax.set_ylabel('Number of responses')
        plt.savefig(f"{output_folder:}/{tag:}.png")
        plt.close()
        
        
if __name__ == "__main__":
    datasets = ['activity', 'respondents', 'roster']

    column_codes = {}
    value_codes = {}

    for dataset in datasets:
        with open(f"TEAM-TIME/{dataset:}/value_codes.yaml") as val_codes, open(f"TEAM-TIME/{dataset:}/column_codes.yaml") as col_codes:
            value_codes[dataset] = yaml.safe_load(val_codes)
            column_codes[dataset] = yaml.safe_load(col_codes)

    responses= pd.read_csv(f"TEAM-TIME/respondents/atusresp_0321.csv")
    
    plot_all_histograms(responses, column_codes['respondents'], value_codes['respondents'], 'histograms')