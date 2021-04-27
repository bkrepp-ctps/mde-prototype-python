#!/usr/bin/env python
# coding: utf-8
#
# MDE_prototype_6.py - Model Data Explorer prototype #6.
# Exploring use of the hvplot library.
#
#
# Author: Ben Krepp

import openmatrix as omx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
# Import statements unique to Prototype #6 begin here
import xarray as xr
import hvplot.pandas
import hvplot.xarray
import cartopy.crs as ccrs
import bokeh
import datashader as ds
# import spatialpandas as spd -- not sure if we want or need this, at least at this point.


# For starters, we will work with sample data provided with the bokeh library.
# Most of the next section of code is taken verbatim from the holoviews documentation and demo "galleries":
# https://hvplot.holoviz.org/user_guide/Geographic_Data.html
# https://hvplot.holoviz.org/reference/geopandas/polygons.html#geopandas-gallery-polygons
#
# Be sure to download the bokeh sample data, if you don't already have it.
bokeh.sampledata.download()

from bokeh.sampledata.airport_routes import airports
airports.head(3)
airports.hvplot.points('Longitude', 'Latitude', geo=True, color='red', alpha=0.2,
                       xlim=(-180, -30), ylim=(0, 72), tiles='ESRI')

cities = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))  
cities.hvplot(global_extent=True, frame_height=450, tiles=True)

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world.hvplot(geo=True) * cities.hvplot(geo=True, color='orange')

world.hvplot(geo=True) + world.hvplot(c='continent', geo=True)

# Now, render some sample polygon data.
countries = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
countries.sample(5)
countries.hvplot(geo=True)
countries.hvplot.polygons(geo=True, c='pop_est', hover_cols='all')
countries.hvplot.polygons(geo=True, c=countries.pop_est/countries.area, clabel='pop density')

###############################################################################
# The following code has been copied to the appropriate place below.
# It is retained here only for the time being during development.
#
# Now some real polygon data - the TAZ shapefile 
# (5) Do some (very) simple mapping

base = r'C:/Users/ben_k/work_stuff/tdm/datastore/reference_data/'
taz_shpfile = 'candidate_CTPS_TAZ_STATE_2019.shp'
fn = base + taz_shpfile
gdf = gpd.read_file(fn)
gdf.set_index("id")
# (5.0) Generate a map of the TAZes, using a single color symbology
gdf.hvplot()


# (5.1) Generate a map of the TAZes, symbolized by state, 
#       and with a tooltip that displays all columns of data
gdf.hvplot(c='state', hover_cols='all')

# The following will also work, but is not needed
# because hvplot will figure out the type of the underlyting data
gdf.hvplot.polygons(c='state', hover_cols='all')

# (5.1.1) Generate a map of the TAZes, symbolized by state,  
#         but with a legend label, and a tooltip that displays
#         a subset of the column (i.e., attributes)
gdf.hvplot(c='state', hover_cols=['taz', 'town', 'state', 'taz_type'], clabel='State')


###############################################################################
# This is the model for generating bar charts.

data_tuples = list(zip(names, values))
mydf = pd.DataFrame(data_tuples, columns=['Mode', 'Trips'])
mydf.hvplot.bar(x = 'Mode', y = 'Trips')

###############################################################################
# Here, we begin working with sample model data.
# The calculations are as in Prototype #1, which uses matplotlib, 
# but in this prototype we (attempt to) use hvplot to render the data graphically.

# Work with the trip tables OMX file

trip_tables_file = r'C:/Users/ben_k/work_stuff/tdm/datastore/sample_data/AfterSC_Final_AM_Tables.omx'
trip_tables_omx = omx.open_file(trip_tables_file, 'r')
trip_tables_omx.list_matrices()
# Returns: ['Bike', 'DAT_Boat', 'DAT_CR', 'DAT_LB', 'DAT_RT', 'DET_Boat', 'DET_CR', 'DET_LB', 'DET_RT', 
#			'HOV', 'HOV2p', 'HOV3p', 'HOV_Person_Trips', 'Heavy_Truck', 'Heavy_Truck_HazMat', 'Light_Truck', 
#			'Medium_Truck', 'Medium_Truck_HazMat', 'SOV', 'WAT', 'Walk']
trip_tables_omx.shape()
# Returns: (5839, 5839)

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
#			'LT_Toll (Skim)', 'Length (Skim)', 'TerminalTimes', 'Total_Cost']
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
	# print(s)
	trip_length_by_mode[mode]= tmp2
# end_for

# (2) Plot the data as a bar chart
names = trip_length_by_mode.keys()
values = trip_length_by_mode.values()
scaled_values = []
for value in values:
	scaled_values.append(value / 10e6)
# end_for
data_tuples = list(zip(names, values))
mydf = pd.DataFrame(data_tuples, columns=['Mode', 'Trips'])
mydf.hvplot.bar(x = 'Mode', y = 'Trips')


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
fc_names = df_links.groupby(['SCEN_00_FU']).groups.keys()

pruned_fc_names = []
pruned_total_flow_by_fc = [] 

# Here ASERT len(fc_names) == len(total_flow_by_fc)
if len(fc_names) != len(total_flow_by_fc):
	print("Something is wrong:")
	s = '	 Length of fc_names = ' + str(len(fc_names))
	print(s)
	s = '	 Length of total_flow_by_fc' + str(len(total_flow_by_fc))
	print(s)

# Do the actual pruning
for (x,y) in zip(fc_names, total_flow_by_fc):
	if x < 10:
		pruned_fc_names.append(x)
		pruned_total_flow_by_fc.append(y)
    # end_if
# end_for

# (4) Generate the plot of link VMT by functional class	
scaled_values = []
for value in pruned_total_flow_by_fc:
	scaled_values.append(value / 10e6)
# end_for

# plt.title('Link VMT by Functional Class')
# plt.xlabel('Functional Class')
# plt.ylabel('Link VMT in 10^7 Miles')
# plt.bar(pruned_fc_names, scaled_values)
# The following line is not needed in the IPython Notebook environment
# plt.show()
#
# *** TBD: Plot using hvplot



# (5) Do some simple mapping
#
# (5.0) Generate a map of the TAZes, using a single color symbology
base = r'C:/Users/ben_k/work_stuff/tdm/datastore/reference_data/'
taz_shpfile = 'candidate_CTPS_TAZ_STATE_2019.shp'
fn = base + taz_shpfile
gdf = geopandas.read_file(fn)
gdf.set_index("id")
gdf.hvplot()

# (5.1) Generate a map of the TAZes, symbolized by state,
#       and with a tooltip that displays all columns of data
gdf.hvplot(c='state', hover_cols='all')

# The following will also work, but is not needed
# because hvplot will figure out the type of the underlyting data
gdf.hvplot.polygons(c='state', hover_cols='all')

# (5.1.1) Generate a map of the TAZes, symbolized by state,  
#         but with a legend label, and a tooltip that displays
#         a subset of the column (i.e., attributes)
gdf.hvplot(c='state', hover_cols=['taz', 'town', 'state', 'taz_type'], clabel='State')


# (5.2) Generate a map of ALL the links, symbolized by functional class
links_shpfile = 'Statewide_Links_2018_BK_EPSG26986.shp'
fn2 = base + links_shpfile
gdf2 = geopandas.read_file(fn2)
gdf2.set_index("ID")
# gdf2.plot("SCEN_00_FU", figsize=(10.0,8.0), legend=True)
# The following line is not needed in the IPython Notebook environment
# plt.show()
#
# *** TBD: Plot using hvplot

# (5.3) Generate a map of all links with a "reasonable" functional class
real_roads = gdf2[gdf2["SCEN_00_FU"] < 10]
# real_roads.plot(column="SCEN_00_FU", categorical=True, legend=True, figsize=(10.0,8.0))
# The following line is not needed in the IPython Notebook environment
# plt.show()
#
# *** TBD: Plot using hvplot

# (5.4) Join links data for "real roads" to flow data on 'ID'/'ID1' fields,
#		and generate a (very crude) map of relative flow by link.
real_roads_joined = real_roads.set_index('ID').join(df_flow.set_index('ID1'))
# real_roads_joined.plot(column='Tot_Flow', legend=True, figsize=(10.0,8.0))
#
# *** TBD: Plot using hvplot

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
# real_roads_joined2.plot(column="flow_class", categorical=True, legend=True, figsize=(10.0,8.0))
#
# *** TBD: Plot using hvplot

# (5.6) Generate a map of the geometrically "simplified" TAZes, symbolized by state,
#       and with a tooltip that displays all columns of data
simp_taz_shpfile = 'candidate_CTPS_TAZ_STATE_2019_simp_10m.shp'
fn3 = base + simp_taz_shpfile
gdf3 = geopandas.read_file(fn3)
gdf3.set_index("id")
gdf3.hvplot(c='state', hover_cols='all

# (5.7) Generate a map of ALL the geometrically "simplified" links, symbolized by functional class
simp_links_shpfile = 'Statewide_Links_2018_BK_EPSG26986_simp_10m.shp'
fn4 = base + simp_links_shpfile
gdf4 = geopandas.read_file(fn4)
# gdf4.plot("SCEN_00_FU", figsize=(10.0,8.0), legend=True)
# The following line is not needed in the IPython Notebook environment
# plt.show()
# 
# *** TBD: Plot using hvplot

##########################################

# (5.8) Generate a map of all the "simplified" links with a "reasonable" functional class
real_roads_simp = gdf4[gdf4["SCEN_00_FU"] < 10]
# real_roads_simp.plot(column="SCEN_00_FU", categorical=True, legend=True, figsize=(10.0,8.0))
# The following line is not needed in the IPython Notebook environment
# plt.show()
# 
# *** TBD: Plot using hvplot

# (5.9) Join links data for simplified "real roads" to flow data on 'ID'/'ID1' fields,
#		and generate a map of 6-way classifcation of flow by link
real_roads_simp_joined = real_roads_simp.set_index('ID').join(df_flow.set_index('ID1'))
real_roads_simp_joined2 = real_roads_simp_joined.assign(flow_class=0)
real_roads_simp_joined2['flow_class'] = real_roads_simp_joined2.apply(lambda row: classify_flow(row['Tot_Flow']), axis=1)
# real_roads_simp_joined2.plot(column="flow_class", categorical=True, legend=True, figsize=(10.0,8.0))
# The following line is not needed in the IPython Notebook environment
# plt.show()
#
# ***TBD: Plot using hvplot


# *** CAN BE IGNORED FOR NOW - (5.10) Same as 5.9, but using a somewhat more meaningful symbolization.
cmap = plt.get_cmap('jet', 7)
# real_roads_simp_joined2.plot(column="flow_class", categorical=True, cmap=cmap, legend=True, figsize=(10.0,8.0))
# The following line is not needed in the IPython Notebook environment
# plt.show()

# *** CAN BE IGNORED FOR NOW - (5.11) Same as 5.9, but using a colormap of our own.
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
col_dict = { 1 : "gray", 2 : "blue", 3 : "green", 4 : "goldenrod", 5 : "orangered", 6 : "red" }
cmap2 = ListedColormap([col_dict[x] for x in col_dict.keys()])
# real_roads_simp_joined2.plot(column="flow_class", categorical=True, cmap=cmap2, legend=True, figsize=(10.0,8.0))
