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
        
def Minutes_year_loc(location_id, data, title = None, xs = range(2006, 2021)):
    """Plot the average minutes per day people spend doing activities at some specific location.
    The options are:

    1: "Respondent's home or yard",
    2: "Respondent's workplace",
    3: "Someone else's home",
    4: 'Restaurant or bar',
    5: 'Place of worship',
    6: 'Grocery store',
    7: 'Other store/mall',
    8: 'School',
    9: 'Outdoors away from home',
    10: 'Library',
    11: 'Other place',
    12: 'Car, truck, or motorcycle (driver)',
    13: 'Car, truck, or motorcycle (passenger)',
    14: 'Walking',
    15: 'Bus',
    16: 'Subway/train',
    17: 'Bicycle',
    18: 'Boat/ferry',
    19: 'Taxi/limousine service',
    20: 'Airplane',
    21: 'Other mode of transportation',
    30: 'Bank',
    31: 'Gym/health club',
    32: 'Post Office',


    Args:
        activity_id (int): An integer associated to a specific location
        data (_type_): The activity DataFrame
        title (string, optional): A string to be used as the title of the plot. Defaults to None.
        xs (iterable, optional): A range iterable with the years you want to plot the data. Defaults
        is range(2006, 2021).
    """


    #Filter the data based on some location
    filtered_df = data.query("TEWHERE == @location_id")

    #Group many entries by the same person in a day to get the total time that person spent
    grouped_df = filtered_df.groupby("TUCASEID")["TUACTDUR24"].sum()

    #Get the entries per year and take an average
    entry_id = grouped_df.index.tolist()
    values = np.asarray(list(grouped_df))
    years = np.asarray([int(str(x)[0:4]) for x in entry_id])
    result = []
    for i in xs:
        mask = years==i
        result.append(np.mean(values[mask]))
        
    #Make the plot
    plt.figure(figsize = (8,5))
    plt.plot(xs,result, color = "black", marker = "o")
    plt.xlabel("year", size = 20)
    plt.ylabel("minutes per day", size = 20)
    if title is not None:
        plt.title(title)
    plt.show()
    plt.close()
       
def Minutes_year_precise(activity_id, data, title = None, xs = range(2006, 2021)):
    """Plot the average minutes per day people spend doing a specific activity.
    The options can be found at the columns yaml file.

    Args:
        activity_id (int): An integer associated to a specific activity
        data (_type_): The activity DataFrame
        title (string, optional): A string to be used as the title of the plot. Defaults to None.
        xs (iterable, optional): A range iterable with the years you want to plot the data. Defaults
        is range(2006, 2021).
    """

    #Filter the data by some activity
    filtered_df = data.query("TRCODEP == @activity_id")

    #Group many entries by the same person in a day to get the total time that person spent
    grouped_df = filtered_df.groupby("TUCASEID")["TUACTDUR24"].sum()

    #Get the entries per year and take an average
    entry_id = grouped_df.index.tolist()
    values = np.asarray(list(grouped_df))
    years = np.asarray([int(str(x)[0:4]) for x in entry_id])
    result = []

    for i in xs:
        mask = years==i
        result.append(np.mean(values[mask]))

    #Make the plot
    plt.figure(figsize = (8,5))
    plt.plot(xs,result, color = "black", marker = "o")
    plt.xlabel("year", size = 20)
    plt.ylabel("minutes per day", size = 20)
    if title is not None:
        plt.title(title)
    plt.show()
    plt.close()

def Minutes_year_coarse(group_id, data, title = None, xs = range(2006, 2021)):
    """Plot the average minutes per day people spend doing a specific activity.
    The options are:

    1: Personal care 
    2: Household
    3: Caring for and helping household members
    4: Caring For & Helping Nonhousehold (NonHH) Members
    5: Work & Work-Related Activities
    6: Education
    7: Consumer Purchases
    8: Professional and Personal Care Services
    9: Household activities
    10:Government Services and Civic Oblitations 
    11: Eating and Drinking
    12: Socializing, relaxing and leisure
    13: Sports, Exercise and Recreation
    14: Religious and Spiritual Activities
    15: Volunteer Activities
    16: Telephone calls 
    18: Traveling

    Args:
        activity_id (int): An integer associated to a specific activity
        data (_type_): The activity DataFrame
        title (string, optional): A string to be used as the title of the plot. Defaults to None.
        xs (iterable, optional): A range iterable with the years you want to plot the data. Defaults
        is range(2006, 2021).
    """

    #Filter the data by activity category
    filtered_df = data.query("TRTIER1P == @group_id")

    #Group many entries by the same person in a day to get the total time that person spent
    grouped_df = filtered_df.groupby("TUCASEID")["TUACTDUR24"].sum()

    #Get the entries per year and take an average
    entry_id = grouped_df.index.tolist()
    values = np.asarray(list(grouped_df))
    years = np.asarray([int(str(x)[0:4]) for x in entry_id])
    result = []
            
    for i in xs:
        mask = years==i
        result.append(np.mean(values[mask]))
        
    plt.figure(figsize = (8,5))
    plt.plot(xs,result, color = "black", marker = "o")
    plt.xlabel("year", size = 20)
    plt.ylabel("minutes per day", size = 20)

    if title is not None:
        plt.title(title)
    plt.show()
    plt.close()

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
