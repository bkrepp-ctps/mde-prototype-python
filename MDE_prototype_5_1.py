# Model Data Explorer Prototype #5 
# Pre-prototype #1
# Using plotly.express to render geographic data
#

import json
import pandas as pd
import geopandas
import plotly.express as px

# Let's start with something that is (or at least should be) simple:
# rendering a map of the towns in Massachusetts.

base = r'C:/Users/ben_k/work_stuff/tdm/datastore/reference_data/'
towns_geojson_file = base + 'MGIS_TOWNSSURVEY_POLYM.geojson'

# Load towns geojson file into an in-core GeoJSON object.
# This will be used by plotly.exrepss to render GEOMETRY.
#
towns_geojson = open(towns_geojson_file).read()
towns = json.loads(towns_geojson)

# Load towns geojson file into a (geo-) data frame.
# This data frame (which _need not_ be a GEO data frame
# has a column with the attribute whose value to be symbolized.
gdf = geopandas.read_file(towns_geojson_file)

# Join the data frame to the geojson in preparation for rendering.
#
# The basic idea in plotly.express is that the GEOMETRY to be rendered
# is given by the value of the 'geojson' parameter. This is an in-core
# GeoJSON object.
# The 'data_frame' parameter provides an attribute table contiaing the attribute to symbolize.
# (That the geojson might _also_ contain attribute(s) data is besides the point.)
#
# The "join" between the geometry and attribute table is defined by
#    data_frame.<locations> = geojson.<featureidkey>
#
# That is to say the column named by the 'locations' parameter in the 'data_frame' parameter
# is used to join the records in the data frame with the feature in the GeoJSON with an
# identical value in its properties._featureidkey_ property.
#
# The column in the 'data_frame' parameter on which to symbolize the corresponding geometry
# is given by the 'color' parameter.
#
# Please read the above again, at least once, as it is not made nearly as clear as it should
# be in the plotly.express documentation.

# Example 1
#
# This call doesn't render the map using the indicated color palette,
# (apparently) because 'fourcolor' is an integer (numeric) field, which plotly regards
# as requiring a continuous color scale. 
fig = px.choropleth(gdf, geojson=towns, locations='town_id', featureidkey='properties.town_id',
                    color='fourcolor',
                    scope='usa', projection='albers usa', fitbounds='geojson')
fig.show()

# Yes, we know that the map is using Albers USA projection, and the symbolization uses
# a continuous scale. Addressing these two points are the next steps.

# Example 2
#
# Mostly the same comments as for Example 1,
# but also note that the dictionary keys are integers which doesn't pass muster.
# Even if these are changed to string, it still doesn't work.
fig = px.choropleth(gdf, geojson=towns, locations='town_id', featureidkey='properties.town_id',
					color='fourcolor',
					# color_discrete_map={1 : "red", 2 : "green", 3 : "blue", 3 : "goldenrod"},
					scope='usa', projection='albers usa', fitbounds='geojson')
fig.show()

# Example 3 - the first really "working" example
#
# The field 'type' is non-numeric, and so specifying a color_discrete_map works.
fig = px.choropleth(gdf, geojson=towns, locations='town_id', featureidkey='properties.town_id',
					color='type',
					color_discrete_map={ "T" : "red", "C" : "green", "TC" : "blue" },
					scope='usa', projection='albers usa', fitbounds='geojson')
fig.show()

# Example 4
#
# If we want to symbolize on 'fourcolor', we'll need to create a string-valued
# field in the data frame on which to use for discrete colormap symbolization.
def fourcolor_to_string(row):
	return str(row['fourcolor'])

gdf['fourcolor_str'] =  gdf.apply(fourcolor_to_string, axis=1)
fig = px.choropleth(gdf, geojson=towns, locations='town_id', featureidkey='properties.town_id',
					color='fourcolor_str',
					color_discrete_map={ "1" : "red", "2" : "green", "3" : "blue", "4" : "goldenrod" },
					scope='usa', projection='albers usa', fitbounds='geojson')
fig.show()


# Example 5
#
# Render the (simplified) TAZes.
#
# Load simplified TAZ geojson file into an in-core GeoJSON object.
# This will be used by plotly.express to render GEOMETRY.
#
taz_geojson_file = base + 'candidate_CTPS_TAZ_STATE_2019_simp_10m.geojson'
taz_geojson = open(taz_geojson_file).read()
tazes = json.loads(taz_geojson)
# Load the TAZ 'attributes' from a CSV file into a pandas data frame.
taz_attributes_csv = base + 'taz_attributes.csv'
taz_attr_df = pd.read_csv(taz_attributes_csv)

fig = px.choropleth(taz_attr_df, geojson=tazes, locations='id', featureidkey='properties.id',
					color='state',
					scope='usa', projection='albers usa', fitbounds='geojson')
fig.show()
