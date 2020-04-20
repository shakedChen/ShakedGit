import geopandas as gpd
import os

# INPUTS -
# layers file name (.gdb)
# height field name (string type)
# fid of building (int type)

#  By giving a numerical value of height returns the type of building
#  function returns 'Building_Type' String
#  There are four types of buildings --->

# * Normal building (building) - up to 12.90 meters from the entrance level בניין רגיל
# * Tall building - its height is 13 meters to 28.90 meters from the entry level בניין גבוה
# * High-rise building - its height is 29 meters to 41.90 meters from the entry level בניין רב קומות
# * Skyscraper building - from 42 meters from the entry level גורד שחקים


#
def HeightToBuildingType(input_layer_path,Height_Field_Name,fid):

    # opening source gdb
    table = gpd.read_file(input_layer_path, encoding='utf-8',driver="OpenFileGDB", errors='ignore',layer=0)

    # creating Building_Type field
    table['Building_Type'] = "בניין"



    for index, row in table.iterrows():
        #checking if Height field's values are number
        try:
            int(table.loc[index, Height_Field_Name])
        except(Exception):
            print("Invalid Height Field, Height should be number values, not String")
            exit(0)

        #  Tall building
        if float(row[Height_Field_Name]) >  13 and float(row[Height_Field_Name]) >  28.90:
            table.loc[index, 'Building_Type'] = "בניין גבוה"

        #  High-rise building
        elif float(row[Height_Field_Name]) > 29 and float(row[Height_Field_Name]) > 41.90:
            table.loc[index, 'Building_Type'] = "בניין רב קומות"

        #  Skyscraper building
        elif float(row[Height_Field_Name]) > 42:
            table.loc[index, 'Building_Type'] = "גורד שחקים"

        if index == fid:
            try:
                return (table.loc[index, 'Building_Type'])
            except(Exception):
                print('invalid fid')




