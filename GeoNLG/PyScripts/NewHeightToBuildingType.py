import geopandas as gpd
import os
#  By giving a numerical value of height returns the type of building
#  function returns 'Building_Type' String
#  There are four types of buildings --->

# * Normal building (building) - up to 12.90 meters from the entrance level בניין רגיל
# * Tall building - its height is 13 meters to 28.90 meters from the entry level בניין גבוה
# * High-rise building - its height is 29 meters to 41.90 meters from the entry level בניין רב קומות
# * Skyscraper building - from 42 meters from the entry level גורד שחקים


#
def NewHeightToBuildingType(floors_num):

    #  Tall building
    if floors_num >  13 and floors_num <  28.90:
        return("בניין גבוה")

    #  High-rise building
    elif floors_num > 29 and floors_num < 41.90:
        return("בניין רב קומות")

    #  Skyscraper building
    elif floors_num > 42:
        return("גורד שחקים")

    else:
        return('בניין')





