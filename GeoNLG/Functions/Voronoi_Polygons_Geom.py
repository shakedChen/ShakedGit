from osgeo import ogr
import pytess
from shapely.geometry import MultiPoint, Point, Polygon,MultiPolygon,LineString
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np
import geopandas as gpd

def voronoi_polygons_geom(layer_coords):
    """
    Essence
    -------
    Function creates dictionary of voronoi polygons geom

    Inputes
    -------

    :param layer_coords: list of coords tuples
    :type List of tuples [(),(),....]

    Returns
    -------

    :return: list of voronoi areas
    :type list of shapely.geometry Polygons
    """
    voronoi_polys = pytess.voronoi(layer_coords)
    #key = coord, value = dis
    voronoi_areas = {}
    voronoi_shapefile= gpd.GeoDataFrame()
    voronoi_shapefile['geometry']= None
    points_to_polygon = gpd.GeoDataFrame()
    points_to_polygon['geometry'] = None

    concave= gpd.read_file(r'C:\Users\Shaked Chen\Desktop\Geo NLG\screenshots\Concave_hull\concave_hull.shp', driver='ESRI Shapefile')

    points = np.array(layer_coords)

    vor = Voronoi(points)

    regions, vertices = voronoi_finite_polygons_2d(vor)

    pts = MultiPoint([Point(i) for i in points])
    mask = pts.convex_hull
    new_vertices = []
    counter=0
    for region in regions:
        polygon = vertices[region]
        shape = list(polygon.shape)
        shape[0] += 1
        p = Polygon(np.append(polygon, polygon[0]).reshape(*shape)).intersection(mask)
        poly = np.array(list(zip(p.boundary.coords.xy[0][:-1], p.boundary.coords.xy[1][:-1])))
        new_vertices.append(poly)
        intersect= p.intersection(concave.loc[0,'geometry'])
        voronoi_shapefile= voronoi_shapefile.append({'geometry':intersect},ignore_index=True)
        temp = ogr.CreateGeometryFromWkt(intersect.wkt)
        voronoi_areas[layer_coords[counter]]= temp.GetArea()
        counter+=1

    voronoi_shapefile.to_file('voronoi_shapefile3.shp', driver='ESRI Shapefile')
    #plt.plot(points[:, 0], points[:, 1], 'ko')
    #plt.title("Clipped Voronois")
    #plt.show()


    return voronoi_areas



def voronoi_finite_polygons_2d(vor, radius=None):
    """
    Reconstruct infinite voronoi regions in a 2D diagram to finite
    regions.
    Parameters
    ----------
    vor : Voronoi
        Input diagram
    radius : float, optional
        Distance to 'points at infinity'.
    Returns
    -------
    regions : list of tuples
        Indices of vertices in each revised Voronoi regions.
    vertices : list of tuples
        Coordinates for revised Voronoi vertices. Same as coordinates
        of input vertices, with 'points at infinity' appended to the
        end.
    """

    if vor.points.shape[1] != 2:
        raise ValueError("Requires 2D input")

    new_regions = []
    new_vertices = vor.vertices.tolist()

    center = vor.points.mean(axis=0)
    if radius is None:
        radius = vor.points.ptp().max()*2

    # Construct a map containing all ridges for a given point
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    # Reconstruct infinite regions
    for p1, region in enumerate(vor.point_region):
        vertices = vor.regions[region]

        if all(v >= 0 for v in vertices):
            # finite region
            new_regions.append(vertices)
            continue

        # reconstruct a non-finite region
        ridges = all_ridges[p1]
        new_region = [v for v in vertices if v >= 0]

        for p2, v1, v2 in ridges:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                # finite ridge: already in the region
                continue

            # Compute the missing endpoint of an infinite ridge

            t = vor.points[p2] - vor.points[p1] # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # normal

            midpoint = vor.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = vor.vertices[v2] + direction * radius

            new_region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())

        # sort region counterclockwise
        vs = np.asarray([new_vertices[v] for v in new_region])
        c = vs.mean(axis=0)
        angles = np.arctan2(vs[:,1] - c[1], vs[:,0] - c[0])
        new_region = np.array(new_region)[np.argsort(angles)]

        # finish
        new_regions.append(new_region.tolist())

    return new_regions, np.asarray(new_vertices)

# make up data points
np.random.seed(1234)
points = np.random.rand(15, 2)

# compute Voronoi tesselation
vor = Voronoi(points)

# plot
regions, vertices = voronoi_finite_polygons_2d(vor)


# colorize
for region in regions:
    polygon = vertices[region]

