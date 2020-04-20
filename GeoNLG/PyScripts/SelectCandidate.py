import os
from osgeo import ogr
from scipy.spatial import distance
from scipy.spatial import Voronoi
from PyScripts import Voronoi_Polygons_Geom
import osr
from collections import Counter
import math

# Essence: Gong Algorithm - Performs an Intelligent Selection of a Minimal
# Set of Candidate References for Object Description

# Inputs:

# • Target Object XY (TO).
# • input layer path- A layer of reference objects (Point type)(.shp)
# •	A threshold value(integer)

# check point --->
# pointX = float(34.8289199)
# pointY = float(32.0721959)
# point_output_number = int(5)

# Outputs:
# list of two dictionaries:
    # • Dictionary of reference objects relevant to the description of the object
    # •Dictionary 1: key ---> fid, value ---> point coords
    # •Dictionary 2: key ---> fid, value ----> data string



# function adds "Score" field to source layer (Float type) (you need to remove mark to create that field)
# function creats layer, containing all of interest points

def SelectCandidate(input_layer_path,pointX,pointY,point_output_number):
    # opening reference objects layer, Point type
    daShapefile = input_layer_path
    driver = ogr.GetDriverByName('ESRI Shapefile')
    dataSource = driver.Open(daShapefile, 1)  # 0 means read-only. 1 means writeable.
    source_layer = dataSource.GetLayer()
    layerDefinition = source_layer.GetLayerDefn()

    field_list = []
    # Add an 'Score' field to output layer, if field does not exist
    for i in range(layerDefinition.GetFieldCount()):
        fieldName = layerDefinition.GetFieldDefn(i).GetName()
        field_list.append(fieldName)
    # if "Score" not in field_list:
    #     directionField = ogr.FieldDefn("Score", ogr.OFSTFloat32)
    #     source_layer.CreateField(directionField)

    #  getting XY values of reference point
    # Point output number
    try:
        pointX = float(pointX)
        pointY = float(pointY)
        point_output_number = int(point_output_number)

    except(Exception):
        print("Invalid xy coordinates or point output number")
        exit(0)

    # creating point object
    point_obj = ogr.Geometry(ogr.wkbPoint)
    point_obj.AddPoint(pointX, pointY)
    point_coord = (pointX, pointY)

    #  Sum of all Euclidean distances
    total_distance = 0
    #  Dictionary of all Euclidean distances for input layer  ---> key ---> feature coords
    distance_list = {}
    # tuple containint all features xy coords
    layer_coords = []

    for feature in source_layer:
        if(feature.GetGeometryRef().GetX() != pointX and feature.GetGeometryRef().GetY() != pointY):
            feature_coord = (feature.GetGeometryRef().GetX(), feature.GetGeometryRef().GetY())

            dst = math.pow(distance.euclidean(feature_coord, point_coord),2)

            total_distance += (1 / dst)
            distance_list[feature_coord] = (1 / dst)
            layer_coords.append(feature_coord)

    source_layer.ResetReading()
    #  Calculate the probability rate for each object in the layer
    for key in distance_list:
        distance_list[key] = float(distance_list[key] / total_distance)

    #  creating first voronoi polygons, before adding the reference input point
    first_voronoi = Voronoi_Polygons_Geom.voronoi_polygons_geom(layer_coords)

    #  creating second voronoi polygons, after adding the reference input point
    second_layer_coords = layer_coords
    second_layer_coords.append((pointX, pointY))
    second_voronoi = Voronoi_Polygons_Geom.voronoi_polygons_geom(second_layer_coords)


    #  calculating final score for each point base on stole area and Euclidean distances
    total_score = {}
    sigma = 0
    #  calculating sigma
    for j in distance_list:
        if j in first_voronoi:
            sigma+= (first_voronoi[j] * distance_list[j])

    #  calculating score per point
    for key in distance_list:
        if key in second_voronoi:
            score = (second_voronoi[key] * distance_list[key])/sigma
            total_score[key] = score


    #the output dictionary, key ---> FID, value ---> Feature geometry
    interest_points = {}
    # the second output dictionary, key ---> FID, value ---> data string
    interest_points2 = {}

    max_values = dict(Counter(total_score).most_common(point_output_number))

    #  inserting scores into source layer
    for feat in source_layer:
        feature_coord = (feat.GetGeometryRef().GetX(), feat.GetGeometryRef().GetY())
        if feature_coord in max_values:
            interest_points[feat.GetFID()] = feature_coord
            interest_points2[feat.GetFID()] = str(feat.GetField("data"))
        # if feature_coord in total_score:
        #     feat.SetField("Score", total_score[feature_coord])
        #     source_layer.SetFeature(feat)

    return ([interest_points,interest_points2])
