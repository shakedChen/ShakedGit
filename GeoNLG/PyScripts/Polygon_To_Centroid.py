import geopandas as gpd

# make Centroid Point gpd layer from gpd polygon layer
# input ---> polygon layer path (gdb) & output path(.shp)

def Polygon_To_Centroid(input_layer_path,output_path):

    polys = gpd.read_file(input_layer_path,encoding='utf-8',driver="OpenFileGDB", errors='ignore',layer=0)
    # copy GeoDataFrame
    points = polys.copy()
    # change geometry
    points['geometry'] = points['geometry'].centroid
    points.to_file(output_path,driver='ESRI Shapefile',crswkt=polys.crs,encoding='utf-8')

