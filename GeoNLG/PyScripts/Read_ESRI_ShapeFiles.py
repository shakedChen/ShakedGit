import geopandas as gpd
import os



#reading all source DATA (.shp form) from source folder
#return value: list with all source .shp paths
def read_shp_data():

    #source data path
    folder_path = r"C:\Users\Shaked Chen\Desktop\Geo NLG\Source_Layers"
    #all .shp files in source folder
    files_list = os.listdir(folder_path)

    #files names
    shp_files_names = []
    #removing files extensions
    # remove duplicated file names from list
    for file in files_list:
        if file.split('.')[0] not in shp_files_names:
            shp_files_names.append(file.split('.')[0])

    #creating list with all layer objects
    gdf_layers = []
    for name in shp_files_names:
        print(name)
        try:
            table = gpd.read_file(folder_path + "\\" + name + ".shp", driver= "ESRI Shapefile",errors='ignore')
            gdf_layers.append(table)

        except(Exception):
            print("exception")
    return gdf_layers
