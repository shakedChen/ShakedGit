import geopandas as gpd
import os

# INPUTS -
# layer's folder path
# layers file name (.shp)
# output_path

#  Function returns GeoDataFrame with 'FieldsToString' field, containing
#  string for all of the field's fields and values.


def ToString(folder_path,output_path,building_layer_name):

    table = gpd.read_file(os.path.join(folder_path, building_layer_name), driver="ESRI Shapefile", errors='ignore',encode='utf-8')

    # list of table fields names
    fields_names = table.columns

    # creating FieldsToString field
    table['FieldsToString'] = ""



    for index, row in table.iterrows():
        table_string = ""

        for field in fields_names:
            #if string is empty
            if table_string == "":
                if str(table.loc[index, field]) == "":
                    table_string = "field " + field + " is -->  " + "None"
                else:
                    table_string = "field " + field + " is -->  " + str(table.loc[index, field])

            elif str(table.loc[index, field]) == "":
                table_string += ", field " + field + " is -->  " + "None"

            else:
                table_string += ", field " + field + " is -->  " + str(table.loc[index, field])




        print(table_string)
        table.loc[index, 'FieldsToString'] = table_string



    # saving new building GeoDataFrame
    table.to_file(output_path, driver="ESRI Shapefile",encoding='utf-8')

ToString()
