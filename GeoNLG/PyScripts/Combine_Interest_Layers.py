import geopandas as gpd
import pandas as pd
import osr
from osgeo import ogr
import shapely.wkt

# function combine all interest point layers
# OUTPUT ----> create new layer with one field- 'data' string field
#  interest_layers_paths= [r'C:\Users\Shaked Chen\Desktop\Geo NLG\interest_layers\PublicPlaces_Buisnesses_Points.shp',r'C:\Users\Shaked Chen\Desktop\Geo NLG\interest_layers\BusStations.shp',r'C:\Users\Shaked Chen\Desktop\Geo NLG\interest_layers\Gardens_And_Sites_Points.shp',r'C:\Users\Shaked Chen\Desktop\Geo NLG\interest_layers\Edu_HighSchool.shp',r'C:\Users\Shaked Chen\Desktop\Geo NLG\interest_layers\Edu_JunSchool.shp']
def Combine(outputName,layers_list=[]):


    srs = osr.SpatialReference()  # create output spatial reference, ISRAEL ESPG 2039
    srs.ImportFromEPSG(2039)


    outTable= pd.DataFrame()

    outTable['data']=''
    outTable['x'] =None
    outTable['y'] = None

    i=0
    for layer_path in layers_list:
        table = gpd.read_file(layer_path, driver="ESRI Shapefile", errors='ignore',encode='utf-8')
        if i==0:
            for index, row in table.iterrows():

                feature_geom = shapely.wkt.loads(str(table.loc[index, 'geometry']))
                data_string= ''
                if table.loc[index, 'descriptio'] != '' and table.loc[index, 'descriptio'] != None:
                    data_string= str(table.loc[index, 'descriptio'])
                elif table.loc[index, 'sub_class'] != '' and table.loc[index, 'sub_class'] != None:
                    data_string = str(table.loc[index, 'sub_class'])
                elif table.loc[index, 'CLASS'] != '' and table.loc[index, 'CLASS'] != None:
                    data_string = str(table.loc[index, 'CLASS'])


                outTable = outTable.append({'x': feature_geom.x,'y': feature_geom.y, 'data':data_string }, ignore_index=True)

            row=None
            index=0

        elif i==1:
            for index, row in table.iterrows():
                feature_geom = shapely.wkt.loads(str(table.loc[index, 'geometry']))
                data_string= ''
                data_string = 'תחנת אוטובוס: '+ str(table.loc[index, 'stop_name'])
                outTable = outTable.append({'x': feature_geom.x, 'y': feature_geom.y, 'data': data_string},ignore_index=True)

            row = None
            index = 0

        elif i == 2:
            for index, row in table.iterrows():
                feature_geom = shapely.wkt.loads(str(table.loc[index, 'geometry']))
                data_string = ''
                data_string = table.loc[index, 'entity']
                outTable = outTable.append({'x': feature_geom.x, 'y': feature_geom.y, 'data': data_string},ignore_index=True)

            row = None
            index = 0

        elif i==3 or i==4:
            for index, row in table.iterrows():
                feature_geom = shapely.wkt.loads(str(table.loc[index, 'geometry']))
                data_string= ''
                data_string= str(table.loc[index, 'NAME'])
                outTable = outTable.append({'x': feature_geom.x, 'y': feature_geom.y, 'data': data_string},ignore_index=True)

            row = None
            index = 0

        i+=1


    geomOutTable = gpd.GeoDataFrame(outTable, crs=srs, geometry=gpd.points_from_xy(outTable.x, outTable.y))
    geomOutTable.crs= {'init': 'epsg:2039'}

    geomOutTable.to_file(outputName,driver='ESRI Shapefile',encoding='utf-8')

    # Save and close the data source
    data_source = None
Combine('Combined_Interest_Points.shp',layers_list=[r'C:\Users\Shaked Chen\Desktop\Geo NLG\interest_layers\PublicPlaces_Buisnesses_Points.shp',r'C:\Users\Shaked Chen\Desktop\Geo NLG\interest_layers\BusStations.shp',r'C:\Users\Shaked Chen\Desktop\Geo NLG\interest_layers\Gardens_And_Sites_Points.shp',r'C:\Users\Shaked Chen\Desktop\Geo NLG\interest_layers\Edu_HighSchool.shp',r'C:\Users\Shaked Chen\Desktop\Geo NLG\interest_layers\Edu_JunSchool.shp'])