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
from bokeh.models import ColumnDataSource, GeoJSONDataSource

# The following line directs bokeh to render output to an IPython notebook:
output_notebook()

# Very simple kick-the-tires test of bokeh
x = [1, 2, 3, 4, 5]
y = [6, 7, 2, 4, 5]
TOOLS_1 = "pan,wheel_zoom,reset,hover,save"
p = figure(title="Simple line example", x_axis_label='x', y_axis_label='y', tools=TOOLS_1)
p.line(x, y, legend_label="Temp.", line_width=2)
show(p)

TOOLS_2 = "pan,wheel_zoom,reset,save"
p2 = figure(title="Simple line example", x_axis_label='x', y_axis_label='y', tools=TOOLS_2)
p2.line(x, y, legend_label="Temp.", line_width=2)
show(p2)
#
hover2 = HoverTool()
hover2.tooltips = [ ( "temperature = ", "@y" ) ] 
p2.add_tools(hover2)
show(p2)

# Here: Use external function "getCoords" to transform data in dataframe
#       "geometry" column to "x's" and "y's" required by bokeh plotting package.

# (2) Let's try mapping the links first (I got lucky with it first)
#
links_geojson_file = base + 'Statewide_Links_2018_BK_EPSG26986.geojson'
links = geopandas.read_file(links_geojson_file)
links['x'] = links.apply(getCoords, geom_col="geometry", coord_type="x", axis=1)
links['y'] = links.apply(getCoords, geom_col="geometry", coord_type="y", axis=1)

# To clear the lowest bar, only try to render the geometry.
# So, prune all columns other than 'x' and 'y' from the links dataframe.
pruned_links_df = links[['x','y']]
pruned_links_dfsource = ColumnDataSource(data=pruned_links_df)
p_links = figure(plot_width=600, plot_height=300)
p_links.multi_line(xs='x', ys='y', source=pruned_links_dfsource)
show(p_links)

# Render a map of all the links using a data frame that includes
# both the geometry and one attribute ("STREETNAME");
# include an "on-hover" tooltip that will show "STREETNAME".
# Note: Rendering completed in 17.5 seconds.
pruned_links_df2 = links[['x', 'y', 'STREETNAME']]
TOOLTIPS_1 = [ ( "streetname = ", "@STREETNAME" ) ]
p_links2 = figure(plot_width=600, plot_height=300, tooltips=TOOLTIPS_1)
p_links2.multi_line(xs='x', ys='y', source=pruned_links_df2)
show(p_links2)

# It is possible to add a "hover tool" that displays a tooltip,
# after creating a plot.
# The following code is not yet known-to-work.
from bokeh.models.tools import HoverTool
hover = HoverTool()
hover.tooltips = [ ( "streetname = ", "@STREETNAME" ) ]
# Next TBD: plot_name.add_tools(hover)

##############################################################################################
#
# (1) The code below this point represents thus-far unsuccessful attempts to render the TAZes.
#
# Create a geopandas dataframe of the TAZes
base = r'C:/Users/ben_k/work_stuff/tdm/datastore/reference_data/'
taz_geojson_file = base + 'candidate_CTPS_TAZ_STATE_2019.geojson'
tazes = geopandas.read_file(taz_geojson_file)
tazes['x'] = tazes.apply(getCoords, geom_col="geometry", coord_type="x", axis=1)
tazes['y'] = tazes.apply(getCoords, geom_col="geometry", coord_type="y", axis=1)

# Include only coordinates from tazes (exclude 'geometry' column)
tazs_df = tazes[['x','y']]
taz_dfsource = ColumnDataSource(data=tazs_df)

p2 = figure(title="TAZes in model region", tools=TOOLS_1,
            plot_width=650, plot_height=500, active_scroll = "wheel_zoom" )

# Try bokeh's "patches" plotter  ... it does not work...
#
taz_poly = p2.patches('x', 'y', source=taz_dfsource, name="TAZ",
         # fill_color={'field': 'pt_r_tt_ud', 'transform': color_mapper},
         fill_alpha=1.0, line_color="black", line_width=0.03, legend="my_legend")

# Try bokeh's "multi_polygons" plotter ... this also doesn't work...
#
p3 = figure(title="TAZes in model region", tools=TOOLS_1,
            plot_width=650, plot_height=500, active_scroll = "wheel_zoom" )
            
taz_mpoly = p3.multi_polygons(xs='x', ys='y', source=taz_dfsource, name="TAZ", line_color="black", line_width=0.03)
