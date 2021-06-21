import geopandas as gpd
from shapely.geometry.linestring import LineString
from shapely import wkt


file_gpd = gpd.read_file('/home/ubuntu/sanit3Dsdi/tests/clipped_31984.geojson')

outpath = '/home/ubuntu/sanit3Dsdi/tests/clipped_31984_with_id.geojson'
outpath2 = '/home/ubuntu/sanit3Dsdi/tests/clipped_31984_with_id.shp'


si = file_gpd.shape[0]

ids = list(range(si))

ids = list(map(str,ids))

file_gpd['id'] = ids

print(file_gpd)

file_gpd.to_file(outpath,driver='GeoJSON')

file_gpd.to_file(outpath2)


# gpol2 = gpd.read_file('/home/ubuntu/sanit3Dsdi/tests/ground_pol_31984.geojson')


###################### part2

small_bbox_wkt = 'POLYGON((-40.3397827083 -20.3176282943, -40.3353356058 -20.3176282943, -40.3353356058 -20.3214263926, -40.3397827083 -20.3214263926, -40.3397827083 -20.3176282943))'

bbox_polygon = wkt.loads(small_bbox_wkt)

crs_proj = 'EPSG:31984'

data2 = {'name':['bbox'],'geometry':[bbox_polygon]}

bbox_gdf = gpd.GeoDataFrame(data2,crs="EPSG:4326")

bbox_proj = bbox_gdf.to_crs(crs_proj)

bbox_proj['id'] = ['0']


ground_pol = bbox_proj.symmetric_difference(file_gpd.unary_union)

# ground_pol['id'] = ['0']

print(ground_pol)

outpath3 = '/home/ubuntu/sanit3Dsdi/tests/ground_pol_31984.shp'
outpath4 = '/home/ubuntu/sanit3Dsdi/tests/ground_pol_31984B.geojson'


ground_pol.to_file(outpath3)
ground_pol.to_file(outpath4,driver='GeoJSON')

