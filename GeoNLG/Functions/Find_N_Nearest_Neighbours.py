from scipy.spatial import KDTree
import geopandas as gpd
import numpy as np

def N_Closest(x, y, layer_name, interest_point_dict, n):
    """
    Essence
    -------
    Function create layer, containing interest points of point input (building center coordinates), and
    the n closest points to input point, using KDTree algorithm

    Inputs
    ------

    :param x: the X value of input point (building's center)
    :type float

    :param y: the Y value of input point (building's center)
    :type float

    :param layer_name: Interest points layer path, as .shp format
    :type String

    :param interest_point_dict: Dictionary of interest points for our reference object
    key= FID of interest point, from layer_name layer.  value= Interest point's coordinates
    :type Dictionary {}

    :param n: The number of output points
    :type Integer

    Returns
    --------

    :return: None
    :type None
    """
    # reading source layer
    table = gpd.read_file(layer_name, driver="ESRI Shapefile", errors='ignore', encode='utf-8')
    points_list = []
    dict_index= []
    input_point_list = [x,y]


    for key in interest_point_dict:
        dict_index.append(key)
    for index, row in table.iterrows():
        tempX = table.loc[index, 'geometry'].x
        tempY = table.loc[index, 'geometry'].y
        temp_list = [tempX,tempY]
        if index not in dict_index:
            points_list.append(temp_list)

    # finding n closest points
    tree = KDTree(points_list,leafsize=2)
    # ind- the indexes we need
    dist, ind = tree.query(input_point_list, k=n)

    index_calculate= []
    for index, row in table.iterrows():
        tempX2 = table.loc[index, 'geometry'].x
        tempY2 = table.loc[index, 'geometry'].y
        temp_list2 = [tempX2,tempY2]
        # adding all of the closest points indexes to final indexes list
        for point in points_list:
            if points_list.index(point) in ind:
                if point == temp_list2:
                    index_calculate.append(index)

    # we only need the n closest points and interest point indexes
    needed_index= list(np.array(index_calculate))+ list(np.array(dict_index))
    total_index= list(range(0, table.count(axis=0)[0]))
    # remove all of the points, which not interest points or n closest points
    not_included_index= [idx for idx in total_index if idx not in needed_index]
    table= table.drop(table.index[not_included_index])

    table.to_file(filename='closest_and_interest.shp',driver='ESRI Shapefile',encoding = "utf-8")
