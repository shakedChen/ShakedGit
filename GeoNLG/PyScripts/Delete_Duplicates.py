import geopandas as gpd

def delete_duplicates(layer_path,output_path):
    table = gpd.read_file(layer_path, driver="ESRI Shapefile", errors='ignore', encode='utf-8')
    table.drop_duplicates(subset=['geometry', 'data'], keep='first',inplace=True)
    table.to_file(output_path,driver='ESRI Shapefile', encoding='utf-8')

delete_duplicates('Combined_Interest_Points.shp','NEW_Combined_Interest_Points.shp')
