#!/usr/bin/env python
# coding: utf-8
#
# MDE_prototype_2.py - Model Data Explorer prototype #2.
#
# Exercise Python interface to OMX files:
#	  1. Sample 'trip tables' OMX file: 'AfterSC_Final_AM_Tables.omx'
#	  2. Sample 'skims' OMX file: 'AM_SOV_Skim.omx'
# 
# Sample tasks to perform:
#	  1. Calculate link VMT by functional class
#	  2. Calculate trip length distribution by mode
#     3. Render the TAZes in a map
#     4. Render the links in a map
#
# Author: Ben Krepp

import openmatrix as omx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas
import folium

# Prototype generating maps using the folium library
#
center = [42.27, -71.73]

# (6.0) Render an OpenStretMap map of the model area
m = folium.Map(location=center, zoom_start=8)
m

# (6.1) Plot the TAZes with no symbolization/styling, for starters
#       TAZ data is in GeoJson format
base = r'C:/Users/ben_k/work_stuff/tdm/datastore/reference_data/'
taz_geojson_file = base + 'candidate_CTPS_TAZ_STATE_2019.geojson'
taz_geojson = open(taz_geojson_file).read()
folium.GeoJson(taz_geojson).add_to(m)
m
# Rendering completed in just under 37 seconds.

# Note: Folium supports reading data in TopoJson format.
#       Use of this format will reduce the size of the file read in,
#       but will increase the time required to load and "inflate" it.

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
# Rendering completed in just under 23 seconds - not clear why this was faster than above.

# (6.4) Plot the model links with no symbolization/styling, for starters
#       The data is in GeoJson format
#
links_geojson_file = base + 'Statewide_Links_2018_BK_EPSG26986.geojson'
links_geojson = open(links_geojson_file).read()
m = folium.Map(location=center, zoom_start=8)
folium.GeoJson(links_geojson).add_to(m)
m
# Rendering completed in just under 56 seconds, but the notebook crashed shortly thereafter
# with an out-of-memory error when it was run on PC with 6 GB of RAM.
