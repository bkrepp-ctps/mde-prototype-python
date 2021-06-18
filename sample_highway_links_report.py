#!/usr/bin/env python
# coding: utf-8

# In[65]:


# Sample highway links flow, V/C, and speeds notebook

import openmatrix as omx
import numpy as np
import pandas as pd
import geopandas as gp
from io import StringIO
import matplotlib.pyplot as plt
import bokeh
import xarray as xr
import hvplot.pandas
import hvplot.xarray
import cartopy.crs as ccrs
import csv


# In[60]:


# Base directory for MoDX output for "base year" model results.
base_dir = r'G:/Regional_Modeling/1A_Archives/LRTP_2018/2016 Scen 00_08March2019_MoDXoutputs/'


# In[61]:


# Base directory for MoDX output for "comparison scenario" model results.
# Unused in the current version of this notebook
comparison_base_dir = r'G:/Regional_Modeling/1A_Archives/LRTP_2018/2040 NB Scen 01_MoDXoutputs/'


# In[62]:


# Directory containing link flow CSVs
link_flow_dir = base_dir + 'out/'


# In[63]:


# Individual link-flow CSV tables:
am_flow_fn = link_flow_dir + 'AM_MMA_LinkFlow.csv'
md_flow_fn = link_flow_dir + 'MD_MMA_LinkFlow.csv'
pm_flow_fn = link_flow_dir + 'PM_MMA_LinkFlow.csv'
nt_flow_fn = link_flow_dir + 'NT_MMA_LinkFlow.csv'
#
# *** TO BE DETERMINED: Do we also have to *add* in the data from the "Truck" LinkFlow CSVs?
#


# In[137]:


# Read these into pandas dataframes
temp_am_df = pd.read_csv(am_flow_fn, delimiter=',')
temp_md_df = pd.read_csv(md_flow_fn, delimiter=',')
temp_pm_df = pd.read_csv(pm_flow_fn, delimiter=',')
temp_nt_df = pd.read_csv(nt_flow_fn, delimiter=',')


# In[138]:


# Directory containing CSVs with the IDs of the sample links to use for this prototype
sample_links_dir = r'G:/Data_Resources/modx/sample_model_links/'
# CSV files with sample highway and transit links for this prototype
highway_links_csv = sample_links_dir + 'highway_links.csv'
transit_links_csv = sample_links_dir + 'transit_links.csv'
# Load the above into dataframes
highway_links_df = pd.read_csv(highway_links_csv, delimiter=",")
transit_links_df = pd.read_csv(transit_links_csv, delimiter=",")
# And convert the column with the link ID in each dataframe to a Python list
highway_links_list = highway_links_df['TC_Link_ID'].tolist()
transit_links_list = transit_links_df['Route_ID'].tolist()


# In[141]:


# Filter the links dataframes to only include rows for the "selected" highway links
am_df = temp_am_df[temp_am_df['ID1'].isin(highway_links_list)]
md_df = temp_md_df[temp_md_df['ID1'].isin(highway_links_list)]
pm_df = temp_pm_df[temp_pm_df['ID1'].isin(highway_links_list)]
nt_df = temp_nt_df[temp_nt_df['ID1'].isin(highway_links_list)]


# In[ ]:


# Filter these dataframes to only only include the columns containing 'Tot_Flow' (and 'ID1')
am_vol_df = am_df[['ID1', 'Tot_Flow']]
md_vol_df = md_df[['ID1', 'Tot_Flow']]
pm_vol_df = pm_df[['ID1', 'Tot_Flow']]
nt_vol_df = nt_df[['ID1', 'Tot_Flow']]


# In[143]:


# Convert these into numpy arrays in preparation for summing 'Tot_Flow'
am_vol_np = am_vol_df.to_numpy()
md_vol_np = md_vol_df.to_numpy()
pm_vol_np = pm_vol_df.to_numpy()
nt_vol_np = nt_vol_df.to_numpy()


# In[145]:


# Sum these 4 arrays to get the total daily flow (and ID1 muliplied by 4 - ugh!)
total_vol_np = am_vol_np + md_vol_np + pm_vol_np + nt_vol_np


# In[151]:


# Convert this to a pandas dataframe
total_vol_df = pd.DataFrame(total_vol_np, columns=['Link_ID_scaled', 'Total_Volume'])


# In[154]:


# Calculate the 'real' link ID for each row
total_vol_df['Link_ID'] = total_vol_df['Link_ID_scaled']/4


# In[155]:


total_vol_df


# In[ ]:





# In[103]:


# Read each of the link flow CSVs into Python lists - these will be converted to numpy arrays later
#
# AM flow
#
temp_list = []
with open(am_flow_fn, newline='') as csvfile:
    myreader = csv.reader(csvfile, delimiter=',')
    for row in myreader:
        temp_list.append(row)
#
# Save the column names in a separate list, and remove them from 'temp_list'
column_names = temp_list[0]
temp_list.pop(0)
pass


# In[107]:


# Convert all the data to floating point type, so it can be loaded into a numpy array
#
r_ix = 0
retval_list = []
for r in temp_list:
    r_ix += 1
    new_row = []
    # print("Row = " + str(r_ix))
    c_ix = 0
    for c in r:
        c_ix += 1
        # *** WARNING: HACK! to work around cells with no data
        temp = float(c) if c != '' else 0.0
        new_row.append(temp)
    #
    retval_list.append(new_row)
#

# Load retval_list into a numpy array
temp_np = np.array(retval_list)


# In[ ]:





# In[111]:


# Function: csv_to_np_array(csv_fn)
# 
# Summary: Given the full pathname to a CSV file,
#                read the CSV file, extracting the column headers,
#                and converting the data in the remaining rows into
#                a numpy array.
#
# Assumption: The "cells" of the CSV file have uniform floating-point data type
#
# Return value: Python 'dict' containing:
#     column_names - Python list of column names
#     np_array - numpy array of values in the CSV file, excluding the column headers
#
def csv_to_np_array(csv_fn):
    temp_list = []
    with open(csv_fn, newline='') as csvfile:
        myreader = csv.reader(csvfile, delimiter=',')
        for row in myreader:
            temp_list.append(row)
    #
    # Save the column names in a separate list, and remove them from 'temp_list'
    column_names = temp_list[0]
    temp_list.pop(0)

    # Convert all the data in temp_list (which is of string type) to floating point type, 
    # so it can be loaded into a numpy array.
    # We accumulate the converted data in a "parallel" list/array, retval_list.
    #
    retval_list = []
    for r in temp_list:
        new_row = []
        for c in r:
            # *** WARNING: HACK! to work around cells with no data.
            temp = float(c) if c != '' else 0.0
            new_row.append(temp)
        #
        retval_list.append(new_row)
    #

    # Load retval_list into a numpy array, the function's return value.
    np_array = np.array(retval_list)
    #
    # Function return value is a dict consisting of:
    #     column_names - Python list of column names
    #     np_array - numpy array of values in the CSV file, excluding the column headers
    #
    retval = { 'column_names' : column_names, 'np_array' : np_array }
    return retval
# end_def csv_to_np_array


# In[ ]:




