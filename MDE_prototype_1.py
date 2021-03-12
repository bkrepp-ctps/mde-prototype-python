# MDE_prototype_1.py - Model Data Explorer prototype #1.
#
# Exercise Python interface to OMX files:
#     1. Sample 'trip tables' OMX file: 'AfterSC_Final_AM_Tables.omx'
#     2. Sample 'skims' OMX file: 'AM_SOV_Skim.omx'
# 
# Sample tasks to perform:
#     1. Calculate link VMT by functional class
#     2. Calculate trip length distribution by mode
#
# Author: Ben Krepp and Margaret Atkinson

import openmatrix as omx
import numpy as np
import matplotlib.pyplot as plt
import csv


# Work with the trip tables OMX file

trip_tables_file = r'C:/Users/ben_k/work_stuff/tdm/datastore/sample_data/AfterSC_Final_AM_Tables.omx'
trip_tables_omx = omx.open_file(trip_tables_file, 'r')
trip_tables_omx.list_matrices()
# Returns: ['Bike', 'DAT_Boat', 'DAT_CR', 'DAT_LB', 'DAT_RT', 'DET_Boat', 'DET_CR', 'DET_LB', 'DET_RT', 
#           'HOV', 'HOV2p', 'HOV3p', 'HOV_Person_Trips', 'Heavy_Truck', 'Heavy_Truck_HazMat', 'Light_Truck', 
#           'Medium_Truck', 'Medium_Truck_HazMat', 'SOV', 'WAT', 'Walk']
trip_tables_omx.shape()
# Returns: (5839, 5839)

# Very crude way to get the # of SOV trips from TAZ[1] to TAZ[1]
trip_tables_omx['SOV'][0][0]

# A more elegant way to do the same thing, using TAZ IDs rather than OMX table indices
trip_tables_omx.list_mappings()
# Returns: ['CTPS', 'ID', 'MAPC', 'extZ', 'intZ']
taz_to_omxid = trip_tables_omx.mapping('ID')
trip_tables_omx['SOV'][taz_to_omxid[1]][taz_to_omxid[1]]

#####

# Work with the skims OMX file

skim_file = r'C:/Users/ben_k/work_stuff/tdm/datastore/sample_data/AM_SOV_Skim.omx'
skim_omx = omx.open_file(skim_file, 'r')
skim_omx.list_matrices()
# Returns: ['Auto_Toll (Skim)', 'CongTime', 'CongTime_wTerminalTimes', 'Drive_Cost', 
#           'LT_Toll (Skim)', 'Length (Skim)', 'TerminalTimes', 'Total_Cost']
skim_omx.shape()
# Returns: (5839, 5839)
skim_omx.list_mappings()
# Returns: ['Destination', 'Origin', 'extZ', 'inCTPS', 'intZ']


# Do some real work!
#
# (1) Get A.M. trip length distribution by mode [SOV, HOV, Bike, Walk])
trip_length_by_mode = {}
modes = [ 'SOV', 'HOV', 'Bike', 'Walk']
for mode in modes:
    tmp1 = np.multiply(skim_omx['Length (Skim)'], trip_tables_omx[mode])
    tmp2 = np.sum(tmp1)
    s = mode + ' trip length = ' + str(tmp1)
    print(s)
    trip_length_by_mode[mode]= tmp2
# end_for

# (2) Plot the data as a bar chart
names = trip_length_by_mode.keys()
values = trip_length_by_mode.values()
plt.figure(figsize=(9,3))
plt.title('A.M. Trip Length Distribution by Mode')
plt.xlabel('Mode')
plt.ylabel('Trip Length')
plt.bar(names, values)
plt.show()

# (3) Get link VMT by functional class of road
flow_fn = r'C:/Users/ben_k/work_stuff/tdm/datastore/sample_data/AM_MMA_LinkFlow.csv'
links_fn = r'C:/Users/ben_k/work_stuff/tdm/datastore/sample_data/statewide_links.csv'

df_flow = pd.read_csv(flow_fn, usecols=['ID1', 'Tot_Flow'], dtype={'ID1':np.int32, 'Tot_Flow':np.float64})
df_links = pd.read_csv(links_fn, usecols=['ID', 'SCEN_00_FU'])

# Join links data to flow data on 'ID'/'ID1' fields:
joined_data = df_links.set_index('ID').join(df_flow.set_index('ID1'))

# Get sum of total flow, aggregated by functional class
total_flow_by_fc = joined_data.groupby('SCEN_00_FU')['Tot_Flow'].sum()

# The following statement gets the (somewhat funky) list of the functional classes found in the data:
names = df_links.groupby(['SCEN_00_FU']).groups.keys()
values = total_flow_by_fc
plt.figure(figsize=(9,3))
plt.title('Link VMT by Functional Class')
plt.xlabel('Functional Class')
plt.ylabel('Link VMT')
plt.bar(names, values)
plt.show()
