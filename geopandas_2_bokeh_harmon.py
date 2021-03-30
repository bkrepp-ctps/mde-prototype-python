# Convert geopandas dataframe format to bokeh format
# Written by Michael Harmon (mdh266@gmail.com)
# Source: http://michael-harmon.com/blog/IntroToBokeh.html

def convert_GeoPandas_to_Bokeh_format(gdf):
	"""
	Function to convert a GeoPandas GeoDataFrame to a Bokeh
	ColumnDataSource object.
	
	:param: (GeoDataFrame) gdf: GeoPandas GeoDataFrame with polygon(s) under
								the column name 'geometry.'
								
	:return: ColumnDataSource for Bokeh.
	"""
	gdf_new = gdf.drop('geometry', axis=1).copy()
	gdf_new['x'] = gdf.apply(getGeometryCoords, 
							 geom='geometry', 
							 coord_type='x', 
							 shape_type='polygon', 
							 axis=1)
	
	gdf_new['y'] = gdf.apply(getGeometryCoords, 
							 geom='geometry', 
							 coord_type='y', 
							 shape_type='polygon', 
							 axis=1)
	
	return ColumnDataSource(gdf_new)


def getGeometryCoords(row, geom, coord_type, shape_type):
	"""
	Returns the coordinates ('x' or 'y') of edges of a Polygon exterior.
	
	:param: (GeoPandas Series) row : The row of each of the GeoPandas DataFrame.
	:param: (str) geom : The column name.
	:param: (str) coord_type : Whether it's 'x' or 'y' coordinate.
	:param: (str) shape_type
	"""
	
	# Parse the exterior of the coordinate
	if shape_type == 'polygon':
		exterior = row[geom].geoms[0].exterior
		if coord_type == 'x':
			# Get the x coordinates of the exterior
			return list( exterior.coords.xy[0] )	
		
		elif coord_type == 'y':
			# Get the y coordinates of the exterior
			return list( exterior.coords.xy[1] )

	elif shape_type == 'point':
		exterior = row[geom]
	
		if coord_type == 'x':
			# Get the x coordinates of the exterior
			return	exterior.coords.xy[0][0] 

		elif coord_type == 'y':
			# Get the y coordinates of the exterior
			return	exterior.coords.xy[1][0]