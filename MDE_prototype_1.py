#!/usr/bin/env python
# coding: utf-8
#
# MDE_prototype_1.py - Model Data Explorer prototype #1.
#
# Exercise Python interface to OMX files:
#     1. Sample 'trip tables' OMX file: 'AfterSC_Final_AM_Tables.omx'
#     2. Sample 'skims' OMX file: 'AM_SOV_Skim.omx'
# 
# Sample tasks to perform:
#     1. Calculate link VMT by functional class
#     2. Calculate trip length distribution by mode
#     3. Render the TAZes in a map
#     4. Render the links in a map
#
# Author: Ben Krepp

import openmatrix as omx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas

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
# (1) Get A.M. trip length distribution by mode [SOV, HOV, Bike, Walk]
trip_length_by_mode = {}
modes = [ 'SOV', 'HOV', 'Bike', 'Walk']
for mode in modes:
    tmp1 = np.multiply(skim_omx['Length (Skim)'], trip_tables_omx[mode])
    tmp2 = np.sum(tmp1)
    s = mode + ' trip length = ' + str(tmp1)
    print(s)
    trip_length_by_mode[mode]= tmp2
# end_for

# Cause matplotlib to display all "plots" in an external window:
%matplotlib

# (2) Plot the data as a bar chart
names = trip_length_by_mode.keys()
values = trip_length_by_mode.values()
for value in values:
    scaled_values.append(value / 10e6)
plt.title('Trip Length Distribution by Mode')
plt.xlabel('Transportation Mode')
plt.ylabel('Trip Length in 10^6 miles')
plt.bar(names, scaled_values)
plt.show()


###############################################################
# Now, let's do what Marty _really_ asked us to do:
# For each mode, make a plot of trip-length distribution
#
# t_lengths: TAZ-to-TAZ distance, no?
t_lengths = skim_omx['Length (Skim)']

# Let's find out a  bit about TAZ-to-TAZ distances
np.min(t_lengths)
np.max(t_lengths)
np.mean(t_lengths)
np.std(t_lengths)

# Brute-force display of distribution of TAZ-to-TAZ trip-lengths
plt.hist(t_lengths, bins=6)

# (1a) Trip length distribution for SOV mode
tt_sov = trip_tables_omx['SOV']

# 'bins' for trip length distribution histograms
bins =       [ 1.0,      5.0,      10.0,       20.0,       50.0,      100.0,        np.max(t_lengths) ]
bin_labels = [ '< 1 mi', '1-5 mi', '5-10 mi', '10-20 mi', '20-50 mi', '50-100 mi', '> 100 mi' ]

sov_product = np.multiply(tt_sov, t_lengths)
sov_hist, bin_edges = np.histogram(sov_product, bins)

# Scale sov_hist for display purposes
sov_hist_scaled = np.divide(sov_hist, 10e5)
plt.title('Trip Length Distribution for SOV Mode')
# plt.xlabel(bin_labels[:-1])
plt.ylabel('Number of Trips x 10^5')
plt.bar(bin_edges[:-1], sov_hist_scaled)

# (1b) Trip length distribution for HOV mode
tt_hov = trip_tables_omx['HOV']
hov_product = np.multiply(tt_hov, t_lengths)
hov_hist, bin_edges = np.histogram(hov_product, bins)
hov_hist_scaled = np.divide(hov_hist, 10e5)
plt.title('Trip Length Distribution for HOV Mode')
plt.ylabel('Number of Trips x 10^5')
plt.bar(bin_edges[:-1], hov_hist_scaled)

# (1c) Trip length distribution for Bike mode
tt_bike = trip_tables_omx['Bike']
bike_product = np.multiply(tt_bike, t_lengths)
bike_hist, bin_edges = np.histogram(bike_product, bins)
bike_hist_scaled = np.divide(bike_hist, 10e5)
plt.title('Trip Length Distribution for Bike Mode')
plt.ylabel('Number of Trips x 10^5')
plt.bar(bin_edges[:-1], bike_hist_scaled)

# (1d) Trip length distribution for Walk mode
tt_walk = trip_tables_omx['Walk']
walk_product = np.multiply(tt_walk, t_lengths)
walk_hist, bin_edges = np.histogram(walk_product, bins)
walk_hist_scaled = np.divide(walk_hist, 10e5)
plt.title('Trip Length Distribution for Walk Mode')
plt.ylabel('Number of Trips x 10^5')
plt.bar(bin_edges[:-1], walk_hist_scaled)



# (3) Calculate link VMT by functional class of road
#
flow_fn = r'C:/Users/ben_k/work_stuff/tdm/datastore/sample_data/AM_MMA_LinkFlow.csv'
# The following CSV contains a mapping from link ID ('ID') to functional class ('SCEN_00_FU')
links_fn = r'C:/Users/ben_k/work_stuff/tdm/datastore/sample_data/statewide_links_pruned.csv'

df_flow = pd.read_csv(flow_fn, usecols=['ID1', 'Tot_Flow'], dtype={'ID1':np.int32, 'Tot_Flow':np.float64})
df_links = pd.read_csv(links_fn, usecols=['ID', 'SCEN_00_FU'])

# Join links data to flow data on 'ID'/'ID1' fields:
joined_data = df_links.set_index('ID').join(df_flow.set_index('ID1'))

# Get sum of total flow, aggregated by functional class
total_flow_by_fc = joined_data.groupby('SCEN_00_FU')['Tot_Flow'].sum()

# The following statement gets the (somewhat funky) list of the functional classes found in the data:
fc_names = df_links.groupby(['SCEN_00_FU']).groups.keys()
# for fc_name in fc_names:
    # print(fc_name)

# Prep to prune weird FC's from 'fc_names' (and prune corresponding value from total_flow_by_fc)
pruned_fc_names = []
pruned_total_flow_by_fc = [] 

# Here ASERT len(fc_names) == len(total_flow_by_fc)
if len(fc_names) != len(total_flow_by_fc):
    print("Something is wrong:")
    s = '    Length of fc_names = ' + str(len(fc_names))
    print(s)
    s = '    Length of total_flow_by_fc' + str(len(total_flow_by_fc))
    print(s)

# Do the actual pruning
for (x,y) in zip(fc_names, total_flow_by_fc):
    if x < 10:
        pruned_fc_names.append(x)
        pruned_total_flow_by_fc.append(y)
        
# (4) Generate the plot of link VMT by functional class        
scaled_values = []
for value in pruned_total_flow_by_fc:
    scaled_values.append(value / 10e7)

plt.title('Link VMT by Functional Class')
plt.xlabel('Functional Class')
plt.ylabel('Link VMT in 10^7 Miles')
plt.bar(pruned_fc_names, scaled_values)
# The following line is not needed in the IPython Notebook environment
plt.show()

# (DIGRESSION) Export data from table in OMX file in CSV format
# This is trivial, as the numpy library supports a function for this very purpose:
#     np.savetxt(csv_filename, nparray, delimiter=",")
#
# Example: Export the SOV trip table
output_csv = r'C:/Users/ben_k/work_stuff/tdm/datastore/sample_data/sov_tt.csv'
trip_tables = openmatrix.open_file(trip_tables_file, 'r') 
np.savetxt(output_csv, trip_tables['SOV'], delimiter=",")


# (5) Do some simple mapping
#
# (5.1) Generate a map of the TAZes, symbolized by state
base = r'C:/Users/ben_k/work_stuff/tdm/datastore/reference_data/'

taz_shpfile = 'candidate_CTPS_TAZ_STATE_2019.shp'
fn = base + taz_shpfile
gdf = geopandas.read_file(fn)
gdf.set_index("id")
gdf.plot("state", figsize=(10.0,8.0), legend=True)
# The following line is not needed in the IPython Notebook environment
plt.show()

# (5.2) Generate a map of ALL the links, symbolized by functional class
links_shpfile = 'Statewide_Links_2018_BK_EPSG26986.shp'
fn2 = base + links_shpfile
gdf2 = geopandas.read_file(fn2)
gdf2.set_index("ID")
gdf2.plot("SCEN_00_FU", figsize=(10.0,8.0), legend=True)
# The following line is not needed in the IPython Notebook environment
plt.show()

# (5.3) Generate a map of all links with a "reasonable" functional class
real_roads = gdf2[gdf2["SCEN_00_FU"] < 10]
real_roads.plot(column="SCEN_00_FU", categorical=True, legend=True, figsize=(10.0,8.0))
# The following line is not needed in the IPython Notebook environment
plt.show()

# (5.4) Join links data for "real roads" to flow data on 'ID'/'ID1' fields,
#       and generate a (very crude) map of relative flow by link.
real_roads_joined = real_roads.set_index('ID').join(df_flow.set_index('ID1'))
real_roads_joined.plot(column='Tot_Flow', legend=True, figsize=(10.0,8.0))
# The following line is not needed in the IPython Notebook environment
plt.show()

# A very simple flow-level classification function
def classify_flow(flow):
	retval = 0
	if flow == None:
		retval = 0
	elif flow < 100.0:
		retval = 1
	elif flow < 500.0:
		retval = 2
	elif flow < 1000.0:
		retval = 3
	elif flow < 5000.0:
		retval = 4
	elif flow < 10000.0:
		retval = 5
	else:
		retval = 6
	# end_if
	return retval
# end_def 

# (5.5) Generate a map of 6-way classifcation of flow by link
real_roads_joined2 = real_roads_joined.assign(flow_class=0)
real_roads_joined2['flow_class'] = real_roads_joined2.apply(lambda row: classify_flow(row['Tot_Flow']), axis=1)
real_roads_joined2.plot(column="flow_class", categorical=True, legend=True, figsize=(10.0,8.0))
# The following line is not needed in the IPython Notebook environment
plt.show()

# (5.6) Generate a map of the geometrically "simplified" TAZes, symbolized by state
simp_taz_shpfile = 'candidate_CTPS_TAZ_STATE_2019_simp_10m.shp'
fn3 = base + simp_taz_shpfile
gdf3 = geopandas.read_file(fn3)
gdf3.set_index("id")
gdf3.plot("state", figsize=(10.0,8.0), legend=True)
# The following line is not needed in the IPython Notebook environment
plt.show()

# (5.7) Generate a map of ALL the geometrically "simplified" links, symbolized by functional class
simp_links_shpfile = 'Statewide_Links_2018_BK_EPSG26986_simp_10m.shp'
fn4 = base + simp_links_shpfile
gdf4 = geopandas.read_file(fn4)
gdf4.plot("SCEN_00_FU", figsize=(10.0,8.0), legend=True)
# The following line is not needed in the IPython Notebook environment
plt.show()

# (5.8) Generate a map of all the "simplified" links with a "reasonable" functional class
real_roads_simp = gdf4[gdf4["SCEN_00_FU"] < 10]
real_roads_simp.plot(column="SCEN_00_FU", categorical=True, legend=True, figsize=(10.0,8.0))
# The following line is not needed in the IPython Notebook environment
plt.show()

# (5.9) Join links data for simplified "real roads" to flow data on 'ID'/'ID1' fields,
#		and generate a map of 6-way classifcation of flow by link
real_roads_simp_joined = real_roads_simp.set_index('ID').join(df_flow.set_index('ID1'))
real_roads_simp_joined2 = real_roads_simp_joined.assign(flow_class=0)
real_roads_simp_joined2['flow_class'] = real_roads_simp_joined2.apply(lambda row: classify_flow(row['Tot_Flow']), axis=1)
real_roads_simp_joined2.plot(column="flow_class", categorical=True, legend=True, figsize=(10.0,8.0))
# The following line is not needed in the IPython Notebook environment
plt.show()

# (5.10) Same as 5.9, but using a somewhat more meaningful symbolization.
cmap = plt.get_cmap('jet', 7)
real_roads_simp_joined2.plot(column="flow_class", categorical=True, cmap=cmap, legend=True, figsize=(10.0,8.0))
# The following line is not needed in the IPython Notebook environment
plt.show()

# (5.11) Same as 5.9, but using a colormap of our own.
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
col_dict = { 1 : "gray", 2 : "blue", 3 : "green", 4 : "goldenrod", 5 : "orangered", 6 : "red" }
cmap2 = ListedColormap([col_dict[x] for x in col_dict.keys()])
real_roads_simp_joined2.plot(column="flow_class", categorical=True, cmap=cmap2, legend=True, figsize=(10.0,8.0))
