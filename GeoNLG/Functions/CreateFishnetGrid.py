from osgeo import ogr
from math import ceil
import osr

def CreateFishnetGrid(outputGridfn,xmin,xmax,ymin,ymax,gridHeight,gridWidth):
    """
    Essence
    -------
    Function creates fishnet grid for each polygon (3X3)

    Inputs
    ------

    :param outputGridfn: Output's save grid path (.shp file)
    :type String

    :param xmin: the x min value of object's bounds
    :type float

    :param xmax: the x max value of object's bounds
    :type float

    :param ymin: the y min value of object's bounds
    :type float

    :param ymax: the y max value of object's bounds
    :type float

    :param gridHeight: object's bounds height / 3
    :type float

    :param gridWidth: object's bounds width / 3
    :type float

    Returns
    --------

    :return: None
    :type None
    """

    # convert sys.argv to float
    xmin = float(xmin)
    xmax = float(xmax)
    ymin = float(ymin)
    ymax = float(ymax)
    gridWidth = float(gridWidth)
    gridHeight = float(gridHeight)

    # get rows
    rows = ceil((ymax - ymin) / gridHeight)
    # get columns
    cols = ceil((xmax - xmin) / gridWidth)

    # start grid cell envelope
    ringXleftOrigin = xmin
    ringXrightOrigin = xmin + gridWidth
    ringYtopOrigin = ymax
    ringYbottomOrigin = ymax-gridHeight

    # create output file


    # try:
    #     os.remove(outputGridfn)
    #
    # except(Exception):
    #     print('no')
    outDriver = ogr.GetDriverByName('ESRI Shapefile')
    srs = osr.SpatialReference()  # create output spatial reference, ISRAEL ESPG 2039
    srs.ImportFromEPSG(2039)
    outDataSource = outDriver.CreateDataSource(outputGridfn)
    outLayer = outDataSource.CreateLayer(outputGridfn,srs)
    featureDefn = outLayer.GetLayerDefn()

    # create grid cells
    countcols = 0
    while countcols < 3:
        countcols += 1

        # reset envelope for rows
        ringYtop = ringYtopOrigin
        ringYbottom =ringYbottomOrigin
        countrows = 0

        while countrows < 3:
            countrows += 1
            ring = ogr.Geometry(ogr.wkbLinearRing)
            ring.AddPoint(ringXleftOrigin, ringYtop)
            ring.AddPoint(ringXrightOrigin, ringYtop)
            ring.AddPoint(ringXrightOrigin, ringYbottom)
            ring.AddPoint(ringXleftOrigin, ringYbottom)
            ring.AddPoint(ringXleftOrigin, ringYtop)
            poly = ogr.Geometry(ogr.wkbPolygon)
            poly.AddGeometry(ring)

            # add new geom to layer
            outFeature = ogr.Feature(featureDefn)
            outFeature.SetGeometry(poly)
            outLayer.CreateFeature(outFeature)
            outFeature = None

            # new envelope for next poly
            ringYtop = ringYtop - gridHeight
            ringYbottom = ringYbottom - gridHeight

        # new envelope for next poly
        ringXleftOrigin = ringXleftOrigin + gridWidth
        ringXrightOrigin = ringXrightOrigin + gridWidth

    # Save and close DataSources
    outDataSource.Destroy()

