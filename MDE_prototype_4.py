#!/usr/bin/env python
# coding: utf-8
#
# MDE_prototype_4.py - Model Data Explorer prototype #4.
# 
# Sample tasks to perform:
#	  0. Render simple chart in IPython notebook using bokeh library
#     1. Render the TAZes in a map using bokeh
#     2. Render the links in a map using bokeh
#
# Author: Ben Krepp

import openmatrix as omx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas
from bokeh.plotting import figure, show, ColumnDataSource
from bokeh.io import output_notebook, output_file

# The following line directs bokeh to render output to an IPython notebook:
output_notebook()

# Very simple kick-the-tires test of bokeh
x = [1, 2, 3, 4, 5]
y = [6, 7, 2, 4, 5]
TOOLS = "pan,wheel_zoom,reset,hover,save"
p = figure(title="Simple line example", x_axis_label='x', y_axis_label='y', tools=TOOLS)
p.line(x, y, legend_label="Temp.", line_width=2)
output_notebook()
show(p)


# Create a geopandas dataframe of the TAZes
base = r'C:/Users/ben_k/work_stuff/tdm/datastore/reference_data/'
taz_geojson_file = base + 'candidate_CTPS_TAZ_STATE_2019.geojson'
tazes = geopandas.read_file(taz_geojson_file)

# *** TBD: Pull in function(s) to convert geopandas dataframe to form suitable for use by bokeh
# ??? tazes_4_bokeh = convert_GeoPandas_to_Bokeh_format(tazes)
