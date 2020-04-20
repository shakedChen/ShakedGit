import geopandas as gpd
import os
# INPUTS -
# layer's folder path
# layers file name (.shp)
# output_path
# fid of building



#  By giving a numerical value of floors(int) for polygon objects (refers to buildings),
#  function returns the height of each building (multiply the number of floors by 3m ),integer output

def FloorsToHeight(input_layer_path,Floors_Field_Name,fid):

    # opening source gdb
    table = gpd.read_file(input_layer_path, encoding='utf-8',driver="OpenFileGDB", errors='ignore',layer=0)

    #creating floors field
    table['Floors'] = 1


    for index, row in table.iterrows():
        # checking if Height field's values are number
        try:
            int(table.loc[index, Floors_Field_Name])
        except(Exception):
            print("Invalid Height Field, Height should be number values, not String")
            exit(0)

        if float(row[Floors_Field_Name]) > 0.0:

            if int(row[Floors_Field_Name])*3 > 0:
                table.loc[index, 'Floors'] = int(row[Floors_Field_Name])*3
        if index == fid:
            try:
                return (table.loc[index, 'Floors'])
            except(Exception):
                print('invalid fid')

