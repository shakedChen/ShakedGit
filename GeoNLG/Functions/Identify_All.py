from osgeo import ogr
import os

def Identify_All(layers_paths_list,pointX,pointY):
    """
    Essence
    -------
    Function returns objects from all layers that are in the above reference
    (returns another uses(string) for the input feature from
    interest layer from fields "entity" and "NAME")

    Inputs
    ------

    :param layers_paths_list: all of layers paths which we want to examine
    :type List of .shp path Strings

    :param pointX: The X value of out selected point
    :type float

    :param pointY: The Y value of out selected point
    :type float

    Returns
    --------
    :return: Function returns objects from all layers that are in the above reference
    (returns another uses(string) for the input feature from
    interest layer from fields "entity" and "NAME")

    :type String
    """

    #  getting XY values of reference point
    try:
        pointX = float(pointX)
        pointY = float(pointY)
    except(Exception):
        print("Invalid xy coordinates")
        exit(0)

    # creating point object
    point_obj = ogr.Geometry(ogr.wkbPoint)
    point_obj.AddPoint(pointX, pointY)

    #output dictionary
    uses = ""

    # iterating each input layer
    for layer_path in layers_paths_list:
        try:
            layer_name = os.path.basename(layer_path).strip(".shp")
            # opening reference objects layer
            daShapefile = layer_path
            driver = ogr.GetDriverByName('ESRI Shapefile')
            dataSource = driver.Open(daShapefile, 1)  # 0 means read-only. 1 means writeable.
            source_layer = dataSource.GetLayer()
            layerDefinition = source_layer.GetLayerDefn()

            for feature in source_layer:
                feature_geom = feature.GetGeometryRef()
                if feature_geom.Intersects(point_obj):
                    if uses != '':
                        uses+= ', '+ feature.GetField("data")
                    else:
                        uses += feature.GetField("data")
            dataSource.Destroy()
            source_layer = None
            daShapefile = None
        except Exception:
            pass


    return(uses)

