import os
from osgeo import ogr
from PyScripts import CreateFishnetGrid

def Directional_9 (input_layer_path, pointX,pointY):
    """
    Essence
    -------
    Function calculates the relative position of the point with respect to polygon

    Inputes
    -------
    :param input_layer_path: Polygon objects layer (street layer), .shp file format
    :type String

    :param pointX: The X value of out object
    :type float

    :param pointY: The Y value of out object
    :type float

    Returns
    --------

    :return:
    return tuple with:
    ---- 1 -----
    • Relative direction word (string type)

    output in hebrew:
צפון מזרח, מזרח, דרום מזרח, צפון, מרכז, דרום, צפון מערב, מערב, דרום מערב

    Method: Divide the polygon into 9 cells (Fishnet) and examine them
    The function adds a new column to source layer, indicating the direction
    of each polygon which intersects with input point

    ---- 2 -----
    The street name (string type)

    :type tuple (String,String)
    """
    directions = ['בצפון מערב', 'במערב', 'בדרום מערב', 'בצפון', 'במרכז', 'בדרום' ,'בצפון מזרח', 'במזרח', 'בדרום מזרח']

    # for english output ---> ['North-East','East','Southeast','North','Center','South','North-West','West','South-West']

    #setting final direction output string
    output_direction = ""
    min_distance = None

    #opening source input layer, Polygon type layer
    daShapefile = input_layer_path
    driver = ogr.GetDriverByName('ESRI Shapefile')
    dataSource = driver.Open(daShapefile, 1)  # 0 means read-only. 1 means writeable.
    source_layer = dataSource.GetLayer()
    layerDefinition = source_layer.GetLayerDefn()

    # field_list = []
    # # Add an 'Direction' field to output layer, if field does not exist
    # for i in range(layerDefinition.GetFieldCount()):
    #     fieldName = layerDefinition.GetFieldDefn(i).GetName()
    #     field_list.append(fieldName)
    #
    # if "Direction" not in field_list:
    #     directionField = ogr.FieldDefn("Direction", ogr.OFTString)
    #     source_layer.CreateField(directionField)

    #  getting XY values of reference point
    try:
        pointX = float(pointX)
        pointY = float(pointY)


    except(Exception):
        print("Invalid xy coordinates or fid")
        exit(0)

    # creating point object
    point_obj = ogr.Geometry(ogr.wkbPoint)
    point_obj.AddPoint(pointX, pointY)


    for feature in source_layer:
        # print('st_name',st_name)
        fishnet = None
        feature_geom = feature.GetGeometryRef()
        # print(feature_geom)

        if point_obj.Intersects(feature_geom):
            street_name= feature.GetField("nane")
            feature_envelope= feature_geom.GetEnvelope()
            envelope_width= (feature_envelope[1] - feature_envelope[0])/3
            envelope_height= (feature_envelope[3] - feature_envelope[2])/3

            fishnet_path = 'PolygonFishnetGrid.shp'
            if os.path.exists(fishnet_path):
                os.remove(fishnet_path)

            #  creating polygon fishnet grid
            CreateFishnetGrid.CreateFishnetGrid(fishnet_path, feature_envelope[0], feature_envelope[1] ,feature_envelope[2],feature_envelope[3],envelope_height,envelope_width)


            #  opening fishnet .shp file
            gridShapefile = fishnet_path
            grid_driver = ogr.GetDriverByName('ESRI Shapefile')
            grid_dataSource = grid_driver.Open(gridShapefile, 1)  # 0 means read-only. 1 means writeable.
            grid_layer = grid_dataSource.GetLayer()


            for squere in grid_layer:
                squere_id = squere.GetFID()
                #print("fid: ", squere_id)
                squere_geom = squere.GetGeometryRef()
                if point_obj.Intersects(squere_geom):
                    output_direction = directions[squere_id]
                    grid_dataSource.Destroy()
                    tup= (output_direction,street_name)
                    return (tup)


            # feature.SetField("Direction", output_direction)
            # source_layer.SetFeature(feature)


            #reset all values



    # Close DataSource
    dataSource.Destroy()








