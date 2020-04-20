from PyScripts import HeightToBuildingType
from PyScripts import FloorsToHeight
from PyScripts import Foundation_Year
from PyScripts import Directional_9
import geopandas as gpd

import fiona
from PyScripts import Km_Distance
from PyScripts import Polygon_To_Centroid
from PyScripts import Identify_All
from PyScripts import ReleativeDistance
from PyScripts import Building_RelativePos
from PyScripts import SelectCandidate
from PyScripts import Find_N_Nearest_Neighbours
from PyScripts import NewHeightToBuildingType
from osgeo import ogr
import os


def main():
    # inputes
    #print(fiona.supported_drivers)
    output_path= 'output.xlsx'
    buildings_path= r'C:\Users\Shaked Chen\Desktop\Geo NLG\interest_layers\NEW30TestBuildings.gdb'
    road_path= r'C:\Users\Shaked Chen\Desktop\Geo NLG\Source_Layers\Roads.shp'
    streets_polygons_path= r'C:\Users\Shaked Chen\Desktop\Geo NLG\Source_Layers\Area_Fixed\Area_Fixed.shp'
    street_field= 'STREET_NAM'
    category_field= 'entity'

    interest_points_number= 5
    # category2_field= 'NAME'
    # description_field= 'descriptio'
    floors_field='NUM_FLOORS'
    founding_field= 'year'
    cent_layer_name= 'Centroid.shp'
    interest_places_name= 'NEW_Combined_Interest_Points.shp'


    # creating p
    centroids= Polygon_To_Centroid.Polygon_To_Centroid(input_layer_path=buildings_path, output_path=cent_layer_name)

    table = gpd.read_file(buildings_path, driver="OpenFileGDB", errors='ignore',encode = 'utf-8',layer=0)

    #creating x,y and id fields in output csv
    table['x']= None
    table['y'] = None
    table['id'] = None

    # print(fiona.supported_drivers)
    centroid_table= gpd.read_file(cent_layer_name, driver="ESRI Shapefile", errors='ignore',encode = 'utf-8')

    interest_places_table = gpd.read_file(interest_places_name, driver="ESRI Shapefile", errors='ignore', encode='utf-8')

    # creating new output field if not existing
    if 'main' not in table.columns:
        table['main'] = ''

    for index, row in table.iterrows():
        feature_geom= table.loc[index,'geometry']

        total_string = ''

        # centroid of source feature
        Xcenter= centroid_table.loc[index,'geometry'].x
        Ycenter = centroid_table.loc[index,'geometry'].y

        table[index,'x'] = Xcenter
        table[index, 'y'] = Ycenter
        table[index, 'id'] = index

        # adding building type and floors number
        #building_type= HeightToBuildingType.HeightToBuildingType(input_layer_path=buildings_path, Height_Field_Name=floors_field,fid=index)
        #unmark if you want to add floors to final string
        building_height= FloorsToHeight.FloorsToHeight(input_layer_path=buildings_path,Floors_Field_Name=floors_field,fid=index)

        building_type= NewHeightToBuildingType.NewHeightToBuildingType(building_height)
        #' עם '+ str(floors_number) +' קומה\ות.'
        type_and_floors_string= 'זהו ' +building_type+ ' '
        total_string += type_and_floors_string

        # is there is category fields in source layer, add it to the final string
        cat_string= ''
        cat1= table.loc[index,category_field]
        # cat2= table.loc[index, category2_field]
        if (cat1 != None and cat1 != ''):

            # if((cat2 != None and cat2 != '')):
            #     cat_string= cat1 + ',' + cat2
            cat_string= cat1
            category_string='המשמש כ' + cat_string + '.'+'\n'
            total_string+=category_string
        # elif (cat2 != None and cat2 != ''):
        #     cat_string= cat2

        # adding foundation year to total string, if existing in source layer fields
        foundation_year= Foundation_Year.Foundation_Year(input_layer_path=buildings_path,founding_Field_Name=founding_field,fid=index)
        if foundation_year == '':
            year_string=''
        else:
            year_string='הוקם ב' + foundation_year + '.\n'
            total_string += year_string
        # print('field', street_field)
        # print('name', table.loc[index,street_field])

        # getting the relative location of source feature in its neighborhood
        tup= Directional_9.Directional_9(input_layer_path=streets_polygons_path, pointX=Xcenter,pointY=Ycenter)
        relative_location= tup[0]
        street_name= tup[1]
        # getting street name (string type) of source feature, if existing
        # print('relative',relative_location)
        if street_name != '' and street_name != None:
            if street_name == 'במרכז':
                relative_string = "נמצא " + str(
                    relative_location) + ' השכונה ' + street_name + '.'+'\n\n'
                total_string += relative_string

            else:
                relative_string = "נמצא " + str(
                    relative_location) + ' השכונה ' + street_name+ '.'+'\n\n'
                total_string += relative_string
        elif(street_name == 'במרכז'):
            relative_string = "נמצא " + str(relative_location) + 'השכונה בה הוא ממוקם.' + '\n\n'
            total_string += relative_string

        else:
            relative_string = "נמצא " + str(relative_location) + 'השכונה בה הוא ממוקם.' + '\n\n'
            total_string += relative_string



        # see if source feature is more than just a building (has more than one use)
        another_uses= Identify_All.Identify_All(layers_paths_list=[interest_places_name], pointX=Xcenter,pointY=Ycenter)
        if another_uses!= None and another_uses!= '':
            another_uses_string= 'משמש גם כ- ' + str(another_uses) + '.'
            total_string+= another_uses_string

        very_far= []
        far= []
        close= []
        very_close= []
        front= []
        null=[]
        # finding relevant interest points for source feature (from potential interest points layer)
        # point coords
        tup2= SelectCandidate.SelectCandidate(input_layer_path=interest_places_name, pointX=Xcenter, pointY=Ycenter, point_output_number=interest_points_number)
        interest_points = tup2[0]
        # point data string
        interest_points_data = tup2[1]
        closest_features = Find_N_Nearest_Neighbours.N_Closest(x= Xcenter,y= Ycenter,layer_name= interest_places_name,interest_point_dict=interest_points,n=interest_points_number)
        # closest_and_interest_table= gpd.read_file('closest_and_interest.shp', driver="ESRI Shapefile", errors='ignore', encode='utf-8')

        for key in interest_points:
            coords= interest_points[key]

            relative_object = ReleativeDistance.RelativeDistance(input_layer_path='closest_and_interest.shp',temp_coords=coords,pointX=Xcenter,pointY=Ycenter)
            relative_pos= Building_RelativePos.Building_RelativePos(building_layer_path=buildings_path, road_layer_path=road_path, first_building_fid=index , tempX=interest_points[key][0], tempY=interest_points[key][1])

            #calculating distance between interest point to building
            #distance_from_building= Km_Distance.km_dis(coords_1=coords, coords_2=(Xcenter,Ycenter))

            if relative_object == 'Very Far':
                very_far.append(interest_points_data[key])
            elif relative_object == 'Far':
                far.append(interest_points_data[key])
            elif relative_object == 'Close':
                close.append(interest_points_data[key])
            elif relative_object == 'Very Close':
                very_close.append(interest_points_data[key])
            if relative_pos == 'Front':
                front.append(interest_points_data[key])
            if relative_object == 'NULL':
                null.append(interest_points_data[key])
            # elif relative_pos == 'Near':
            #     near.append(key)
        if very_far != []:
            total_string += 'נמצא רחוק מאוד מ- ' + '\n'
            for a in very_far:
                if "תחנת אוטובוס" in a:
                    a= a.replace("תחנת אוטובוס", "ציר")
                total_string+= str('* '+str(a))+ '\n'
        if far != []:
            total_string+= 'נמצא רחוק מ- ' + '\n'
            for b in far:
                if "תחנת אוטובוס" in b:
                    b= b.replace("תחנת אוטובוס", "ציר")
                total_string += str('* '+str(b))+ '\n'

        if close != []:
            total_string += 'נמצא קרוב ל- ' + '\n'
            for c in close:
                if "תחנת אוטובוס" in c:
                    c= c.replace("תחנת אוטובוס", "ציר")
                total_string += str('* '+str(c))+ '\n'
        if very_close != []:
            total_string += 'נמצא קרוב מאוד ל- ' + '\n'
            for d in very_close:
                if "תחנת אוטובוס" in d:
                    d= d.replace("תחנת אוטובוס", "ציר")
                total_string += str('* '+str(d))+ '\n'

        if null != []:
            total_string += 'נמצא בקרבת- ' + '\n'
            for f in null:
                if "תחנת אוטובוס" in f:
                    f= f.replace("תחנת אוטובוס", "ציר")
                total_string += str('* '+str(f))+ '\n'
        #
        # if near != []:
        #     total_string += 'Found near interest point\s: ' + str(near)+'\n'
        if front != []:
            total_string+= 'נמצא מול- ' + '\n'
            for e in front:
                if "תחנת אוטובוס" in e:
                    e= e.replace("תחנת אוטובוס", "ציר")
                total_string += str('* '+str(e))+ '\n'
        table.loc[index,'x'] = Xcenter
        table.loc[index,'y'] = Ycenter
        table.loc[index,'id'] = index

        print(total_string)
        table.loc[index,'main'] = total_string
    out_table= table[['id','x', 'y', 'main']]

    out_table.to_excel(output_path, index=None, header=True)
main()