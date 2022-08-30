import pandas as pd
import yaml
import matplotlib.pyplot as plt
from plotting_module import *
from statistics_module import *
respondents = pd.read_csv("TEAM-TIME/respondents/atusresp_0321.csv.gz")
activity = pd.read_csv("TEAM-TIME/activity/atusact_0321.csv.gz")
roster = pd.read_csv("TEAM-TIME/roster/atusrost_0321.csv.gz")
"""
with open("TEAM-TIME/roster/value_codes.yaml") as f:
    r_vc = yaml.safe_load(f)
with open("TEAM-TIME/roster/column_codes.yaml") as f:
    r_cc = yaml.safe_load(f)
    
with open("TEAM-TIME/activity/value_codes.yaml") as f:
    a_vc = yaml.safe_load(f)
with open("TEAM-TIME/activity/column_codes.yaml") as f:
    a_cc = yaml.safe_load(f)
    
with open("TEAM-TIME/respondents/value_codes.yaml") as f:
    re_vc = yaml.safe_load(f)
with open("TEAM-TIME/respondents/column_codes.yaml") as f:
    re_cc = yaml.safe_load(f)
"""
for col in respondents.columns:
    print(col)

print(respondents.head(10))
#print(activity.head(10))
#print(roster.head(10))

def time_series(df):
    """
    Returns a dataframe, sorted in chronological order

    Parameters
    ----------
    df - pandas dataframe
        any dataframe that includes the TUDIARYDATE variable
    Returns
    -------
    df_sorted - pandas dataframe
        dataframe sorted by TUDIARYDATE variable
    """
    df_sorted = df.sort_values("TUDIARYDATE")
    #df_subset = df_sorted[label]
    return df_sorted



"""
df = (time_series(respondents))
print(df)
df.plot(x="TUDIARYDATE",y="TEHRUSL1",kind="scatter")
plt.show()
"""
df = outliers_NaNs(respondents)
plt.imshow(df.corr(method ='kendall'))
plt.colorbar()
plt.show()