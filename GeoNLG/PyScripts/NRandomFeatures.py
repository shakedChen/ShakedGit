import geopandas as gpd

#  function creates layer from n random features of source layer(.gdb)

def GetNRandom(layer_path,output_path, n=0):
    table = gpd.read_file(layer_path, driver="OpenFileGDB", errors='ignore', encode='utf-8', layer=0)
    print(len(table))




GetNRandom(layer_path=r'C:\Users\Shaked Chen\Desktop\Geo NLG\NewBuildngLayer', output_path=r'C:\Users\Shaked Chen\Desktop\Geo NLG\interest_layers\Random30Buildings.gdb', n=30)