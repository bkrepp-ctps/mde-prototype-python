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

fig = px.choropleth(gdf, geojson=towns, locations='town_id', featureidkey='properties.town_id',
                    color='fourcolor',
                    scope='usa', projection='albers usa', fitbounds='geojson')
fig.show()

# Yes, we know that the map is using Albers USA projection, and the symbolization uses
# a continuous scale. Addressing these two points are the next steps.
