import os
from osgeo import ogr
import math
from collections import Counter
from collections import OrderedDict
from skfuzzy import fuzzy_or,trimf
from scipy.spatial import distance
import numpy as np

#Essence: Gahegan Algorithm - tests the distance between 2 objects in space
# (close, far, very far, etc.)
# by measuring considering the other elements around it and using the Fuzzy function

#  Inputs:
# • Target Object XY (TO).
# • Point coords (temp coords) from source layer
# • Relative Objects layer - n objects in it, (Point layer)
# Outputs:
#  preposition(string type) for interest points:
# 0-0.1  very far
# 0.1-0.3 far
# 0.3-0.7 NULL
# 0.7-0.9 close
# 0.9-1 very close

def RelativeDistance(input_layer_path,temp_coords,pointX,pointY):

    # opening reference objects layer, Point type
    daShapefile = input_layer_path
    driver = ogr.GetDriverByName('ESRI Shapefile')
    dataSource = driver.Open(daShapefile, 1)  # 0 means read-only. 1 means writeable.
    source_layer = dataSource.GetLayer()
    layerDefinition = source_layer.GetLayerDefn()

    #  getting XY values of reference point
    # Point output number
    try:
        pointX = float(pointX)
        pointY = float(pointY)
        source_point_coords= (temp_coords)

    except(Exception):
        print("Invalid xy coordinates or none existing fid")
        exit(0)

    # creating point object
    point_obj = ogr.Geometry(ogr.wkbPoint)
    point_obj.AddPoint(pointX, pointY)
    point_coord = (pointX, pointY)

    # calculating the diagonal of bounding rectangle of source layer
    envelope_coords = source_layer.GetExtent()
    side1 = envelope_coords[0] - envelope_coords[1]  # x's
    side2 = envelope_coords[3] - envelope_coords[2]  # y's
    diagonal = math.sqrt((math.pow(side1,2)+math.pow(side2,2)))



    #  Dictionary of all Euclidean distances for input layer ---> key ---> feature coords
    distance_list = {}

    #  calculating Euclidean distances from input point for each feature in layer
    for feature in source_layer:
        feature_coord = (feature.GetGeometryRef().GetX(), feature.GetGeometryRef().GetY())
        dst = distance.euclidean(feature_coord, point_coord)
        distance_list[feature_coord] = dst

    source_layer.ResetReading()

    #  Calculate the probability by a straight line equation
    prob = {}
    i=0
    for key in distance_list:
        prob[key] = 1-(distance_list[key]/diagonal)



    #  Calculate the probability based on the distance rating
    #  sorting distionary from max prob to low
    sorted_distance = dict(sorted(distance_list.items(),reverse=True))

    # finding source point index in dictionary
    position_index= 1-(list(sorted_distance.keys()).index(source_point_coords)/len(sorted_distance))

    # finding the highest prob for the source point
    final_score= max(prob[source_point_coords],position_index)


    if final_score<0.1:
        return ("Very Far")
    elif final_score>0.1 and final_score<0.3:
        return("Far")
    elif final_score>0.3 and final_score<0.7:
        return("NULL")
    elif final_score>0.7 and final_score<0.9:
        return("Close")
    elif final_score>0.9 and final_score<1:
        return("Very Close")
    else:
        return("NULL")



