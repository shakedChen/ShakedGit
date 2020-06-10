import geopandas as gpd

def Polygon_To_Centroid(input_layer_path,output_path):

    """
    Essence
    -------
    Function make Centroid Point .gdb layer from .gdb polygon layer

    Inputes
    -------

    :param input_layer_path: Buildings layer path .gdb format
    :type String

    :param output_path: Centroids buildings layer output saving path .gdb format
    :type String

    Returns
    -------
    :return: None
    :type None
    """

    polys = gpd.read_file(input_layer_path,encoding='utf-8',driver="OpenFileGDB", errors='ignore',layer=0)
    # copy GeoDataFrame
    points = polys.copy()
    # change geometry
    points['geometry'] = points['geometry'].centroid
    points.to_file(output_path,driver='ESRI Shapefile',crswkt=polys.crs,encoding='utf-8')
