from scipy.spatial import distance
# function return distance between 2 points in km (int)

# INPUTS -->
# 2 points coords ((x,y) form)

def km_dis(coords_1, coords_2):
    return (int(distance.euclidean(coords_1, coords_2)))
