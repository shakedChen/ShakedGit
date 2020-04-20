from osgeo import ogr
import numpy as np
import math
from PyScripts import Find_Angle
# Essence: Function returns the relative state between the buildings
# Inputs:
# • Road layer (Line) path
# • Layer of buildings (points layer) path
# • Two structures you want to examine (features FID of source point and coords of temp building center point)
# Output:
# • Relative mode (Front, Near, NULL)

def Building_RelativePos(building_layer_path, road_layer_path,first_building_fid,tempX,tempY):

    # opening source input layer(buildings), Polygon type layer
    daShapefile = building_layer_path
    driver = ogr.GetDriverByName('OpenFileGDB')
    dataSource = driver.Open(daShapefile, 0)  # 0 means read-only. 1 means writeable.
    source_layer = dataSource.GetLayerByIndex(0)
    layerDefinition = source_layer.GetLayerDefn()

    # opening source input layer(roads), Line type layer
    road_daShapefile =  road_layer_path
    road_driver = ogr.GetDriverByName('ESRI Shapefile')
    road_dataSource = road_driver.Open(road_daShapefile, 1)  # 0 means read-only. 1 means writeable.
    road_layer = road_dataSource.GetLayer()
    road_layerDefinition = road_layer.GetLayerDefn()

    feature_num = source_layer.GetFeatureCount()


    if first_building_fid > feature_num or first_building_fid <0:
        print("Please enter valid FID")
        exit(0)

    i=0
    #  getting center coords of building
    for feature1 in source_layer:
        if first_building_fid == i:
            first_geom= feature1.GetGeometryRef()
            break
        i+=1


    #first building center
    first_center = first_geom.Centroid()

    # second building center
    second_center = (tempX,tempY)

    #  creating line feature between two centers
    line = ogr.Geometry(ogr.wkbLineString)
    line.AddPoint(first_center.GetX(), first_center.GetY())
    line.AddPoint(tempX,tempY)

    #  Checking whether the line crosses another object from the buildings layer
    for feature in source_layer:
        feature_fid = feature.GetFID()
        feature_geom = feature.GetGeometryRef()

        if line.Touches(feature_geom):
            if feature_fid != first_building_fid and ((tempX,tempY) !=feature_geom.Centroid()):
                print("touches")
                return None
    source_layer.ResetReading()


    #  Check how many times the line connecting the two buildings crosses the road layer
    # key----> random point on the road. value----> the intersection point
    intersection_points = {}
    for road in road_layer:
        road_geom = road.GetGeometryRef()
        if line.Intersects((road_geom)):
            i=0
            temp= road_geom.GetPoint(i)
            # checking that the key is not as same as the intersection point
            while(temp in line.Intersection(road_geom)):
                temp = road_geom.GetPoint(i)
                i+=1


    #  Check whether the angles between the road line and the line between
    #  the two buildings is in range of 60-120 degrees

    if intersection_points is not {}:
        counter= 0
        for point1 in intersection_points:
            if intersection_points[point1].GetGeometryName() == "MULTIPOINT":
                for single_point in intersection_points[point1]:
                    angle= Find_Angle.ang(((first_center.GetX(), first_center.GetY()),(single_point.GetX(),single_point.GetY())),((temp.GetX(), temp.GetY()),(single_point.GetX(),single_point.GetY())))
                    if angle>60 and angle<120:
                        counter+=1
                        return ("Front")

            else:
                angle= Find_Angle.ang(((first_center.GetX(), first_center.GetY()),(intersection_points[point1][0],intersection_points[point1][1])),((temp.GetX(), temp.GetY()),(intersection_points[point1][0],intersection_points[point1][1])))
                if angle > 60 and angle < 120:
                    counter+=1
                    return ("Front")
        # if(counter>0):
        #     return ("Front")

    return(None)





