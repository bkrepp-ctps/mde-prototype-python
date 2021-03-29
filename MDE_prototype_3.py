#!/usr/bin/env python
# coding: utf-8
#
# MDE_prototype_3.py - Model Data Explorer prototype #3.
#
# Sample tasks to perform:
#
#     1. Render the TAZes in a map
#     2. Attempt to render the links in a map
#
# Author: Ben Krepp

import openmatrix as omx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas
from keplergl import KeplerGl 

# Do some (very) simple mapping using the keplergl library
#
# *** NOTES: (1) keplergl cannot be installed from within Anaconda Navigator; 
#                it has to be installed using pip.
#            (2) In order to install keplergl with pip successfully, I had to run the anaconda3 
#                shell in *Administrator* mode.
#
base = r'C:/Users/ben_k/work_stuff/tdm/datastore/reference_data/'

# (1) Map the TAZes with no symbolization/styling
#       TAZ data is in GeoJson format
taz_geojson_file = base + 'candidate_CTPS_TAZ_STATE_2019.geojson'
taz_geojson = open(taz_geojson_file).read()

map_1 = KeplerGl(height=600)
map_1.add_data(data=taz_geojson,name="taz_layer")
map_1
# The map renders in 5 to 6 seconds

# (2) Attempt to map the links with no symbolization/styling
#       Links data is in a geopandas dataframe
links_shpfile = 'Statewide_Links_2018_BK_EPSG26986.shp'
fn2 = base + links_shpfile
gdf2 = geopandas.read_file(fn2)
gdf2.set_index("ID")
map_2 = KeplerGl(height=600)
map_2.add_data(data=gdf2,name="links_layer")
map_2
# *** The map fails to render at all. ***
# Prototype abandoned.








# (6) Prototype generating maps using the folium library
#
import folium
center = [42.27, -71.73]

# (6.0) Render an OpenStretMap map of the model area
m = folium.Map(location=center, zoom_start=8)
m

# (6.1) Plot the TAZes with no symbolization/styling, for starters
#       TAZ data is in GeoJson format
taz_geojson_file = base + 'candidate_CTPS_TAZ_STATE_2019.geojson'
taz_geojson = open(taz_geojson_file).read()
folium.GeoJson(taz_geojson).add_to(m)
m

# *** TBD: Convert the data to TopoJson format for faster loading

# A simple function to style the TAZ polygons
def my_style_function(feature):
	state = feature['properties']['state']
	retval = { 'color' : '#FFFFFF' }
	if state == 'CT':
		retval = { 'color' : '#1F77B4' }
	elif state == 'MA':
		retval = { 'color' : '#FF7F0E'}
	elif state == 'ME':
		retval = { 'color' : 'D62728' }
	elif state == 'NH':
		retval = { 'color' : '#8C564B' }
	elif state == 'NY':
		retval = { 'color' : '#E377C2' }
	elif state == 'RI':
		retval = { 'color' : '#BCBD22' }
	elif state == 'VT':
		retval = { 'color' : '#17BECF' }
	else:
		retval = { 'color': '#FFFFFF' }
	# end_if
	return retval
# end_def

# (6.3) Plot TAZes, symbolized by state
folium.GeoJson(taz_geojson, style_function=my_style_function).add_to(m)
m

# (6.4) Plot the model links with no symbolization/styling, for starters
#       The data is in GeoJson format
# *** NOTE: The links load successfully, but fail to render.
#
# links_geojson_file = base + 'Statewide_Links_2018_BK_EPSG26986.geojson'
# links_geojson = open(links_geojson_file).read()
# folium.GeoJson(links_geojson).add_to(m)
# m

