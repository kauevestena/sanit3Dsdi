# import subprocess
# import numpy as np
# import json
# import geopandas as gpd
# from shapely.geometry import LineString
# import numpy as np
# import os
# import pymesh
# from copy import deepcopy

# # normalized_v = v/np.linalg.norm(v)

# def normalize_vec(input_vec):
#     try:
#         return input_vec/np.linalg.norm(input_vec)
#     except:
#         print(np.linalg.norm(input_vec),'check for zero norm')
#         return input_vec * 0

# # class plane:

# #     def __init__(self,pt_onplane:np.array,normal:np.array):
# #         self.d = -pt_onplane.dot(normal)
# #         self.a = normal[0]
# #         self.b = normal[1]
# #         self.c = normal[2]


# #     def a_point(self,X,Y,Z):
# #         return self.a*X + self.b*Y + self.c*Z + self.d

# def plane_as_4vec(normal:np.array,pt_onplane:np.array):
#     '''
#         plane as 4vec:

#         - normal vector
#         - point on plane
#     '''
#     return np.array([*normal,-np.dot(normal,pt_onplane)])

# def pt_onplane(plane4vec,X,Y):
#     # plane equation, with z=f(X,Y)
#     if not plane4vec[2] < 0.0001:

#         Z = - (plane4vec[0]*X+plane4vec[1]*Y+plane4vec[3])/plane4vec[2]

#         return np.array([X,Y,Z])

#     else:
#         Z = X + 0.1*X

#         Y = - - (plane4vec[0]*X+plane4vec[2]*Z+plane4vec[3])/plane4vec[1]

#         return np.array([X,Y,Z])


# def gdec2rad(gdec):
#     return gdec * np.pi/180

# def circumference_3D(center_pt,radius,v1,v2,n_points=32):
#     '''
#     a circunference in 3D:

#     - Center Point
#     - The Radius

#     thx: https://math.stackexchange.com/a/1184089/307651

#     '''

#     angles = np.linspace(0,2*np.pi,n_points)

#     point_list = []

#     for angle in angles:
#         # circle_point = center_pt + (radius*np.cos(angle)*v1) + (radius*np.sin(angle)*v2)
#         circle_point = center_pt + radius * (np.cos(angle)*v2 + np.sin(angle)*v1)
#         point_list.append(circle_point)

#     return np.array(point_list)

# def reverse_order_rangelist(a,b):
#     l1 = list(range(-a+1,-b+1))

#     return list(map(abs,l1))

# def segments(curve):
#     '''
#     code from 
#     https://stackoverflow.com/a/62061414/4436950

#     thx Georgy
#     '''
#     return list(map(LineString, zip(curve.coords[:-1], curve.coords[1:])))

# def create_edgeslist(num_vertices,as_np=True):
#     edgelist = []

#     if num_vertices > 0:
#         for i in range(num_vertices-1):
#             edgelist.append([i,i+1])

#     if as_np:
#         return np.array(edgelist)
#     else:
#         return edgelist


# def get_raster_val_at_geoXY(x,y,rasterpath):
#     runstring = f'gdallocationinfo -valonly -geoloc {rasterpath} {x} {y}'

#     ret = subprocess.run(runstring,shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')

#     return float(ret.strip('\n'))

# def pymesh_cylinder_for_cityjson(vertices,radius,zero_index=0,num_edges=16,rounding_places=4,custom_attrs=None,tol_for_simplification=None):
#         '''
#             creates a cylinder using pymesh

#         '''

#         num_vertices = vertices.shape[0]

#         edges_list = create_edgeslist(num_vertices)

#         wire_network = pymesh.wires.WireNetwork.create_from_data(vertices, edges_list)

#         inflator = pymesh.wires.Inflator(wire_network)

#         inflator.set_profile(num_edges)

#         inflator.inflate(radius, per_vertex_thickness=False)

#         mesh = inflator.mesh

#         bbox_min, bbox_max = mesh.bbox

#         mins = bbox_min.tolist()
#         maxs = bbox_max.tolist()

#         points = np.around(mesh.vertices,decimals=rounding_places).tolist()

#         max_vert_idx = np.amax(mesh.faces)

#         faces = deepcopy(mesh.faces) + zero_index
#         faces = faces.tolist()

#         faces = [[face] for face in faces]

#         meshdata = {'mins':mins,'maxs':maxs,'points':points,'faces':faces,'zero_ref':max_vert_idx}

#         if tol_for_simplification:
#             # simplify based on tolerance
#             mesh,info = pymesh.collapse_short_edges(mesh,tol_for_simplification)

#             meshdata['edges_collapsed'] = info["num_edge_collapsed"]

#         if custom_attrs:
#             # for key in custom_attrs:
#             #     meshdata[key] = custom_attrs[key]
#             meshdata['attributes'] = custom_attrs


#         return meshdata



# def city_object_dict(faces,attrs_dict):
#     # TODO: swap between MultiSurface/Solid

#     city_obj = {
#                     "geometry": [
#                     {
#                         "boundaries": [],
#                         "lod": 1,
#                         "type": "MultiSurface"
#                     }
#                     ],
#                     "attributes": {
#                     },
#                     "type": "GenericCityObject"
#                 }


#     city_obj['geometry'][0]['boundaries'] = faces
#     city_obj['attributes'] = attrs_dict

#     return city_obj


















# class cylinder3D:
#     '''
#         DEPRECATED BY 

#         pymesh_cylinder(vertices,radius,num_edges=16,tol_for_simplification=None)


#         manteined only because I don't wanna delete it


#         class to implement a cylinder in 3D to use it in cityjson
#     '''

#     def __init__(self,p1,p2,radius,points_per_circle=32):
#         # first, its handy:
#         self.p_1 = p1
#         self.p_2 = p2
#         self.number_of_points = points_per_circle*2
#         self.circle_points_n = points_per_circle


#         # the axis of the cylinder, is the difference vector:
#         self.axis = p2 - p1
#         # its normalized version will be used as the plane normal
#         self.plane_n = normalize_vec(self.axis)
#         # the plane as a 4 vec of parameters: [a,b,c,d]
#         plane = plane_as_4vec(self.plane_n,p1)
#         # any point on the plane
#         point_on_plane = pt_onplane(plane,p1[0]+0.1*p1[0],p1[1]-0.1*p1[1])
#         # first vector parallel to the plane containing the circle
#         vec1_planeparalel = normalize_vec(point_on_plane-p1)
#         # second vector parallel to the plane containing the circle
#         vec2_planeparalel = normalize_vec(np.cross(vec1_planeparalel,self.plane_n))
#         # first circumference

#         # it must needs to be divisible by 4
#         if points_per_circle % 4 != 0:
#             points_per_circle = (points_per_circle // 4) * 4

#         # the first circumference
#         self.circle1 = circumference_3D(p1,radius,vec1_planeparalel,vec2_planeparalel,points_per_circle)
#         # the second contains basically each point summed up with the axis
#         self.circle2 = self.circle1 + self.axis



#     def check_circles(self):
#         centers = (self.p_1,self.p_2)

#         for i,circle in enumerate((self.circle1,self.circle2)):
#             print('\ncircle ',i+1,':')
#             for point in circle:
#                 print(np.dot(point-centers[i],self.axis))
#                 print(np.linalg.norm(point-centers[i]))


#     def get_vertices_list(self,as_list=False):

#         self.justaposed = np.concatenate((self.circle1,self.circle2))

#         self.mins = np.min(self.justaposed,axis=0)
#         self.maxs = np.max(self.justaposed,axis=0)


#         if as_list:
#             return list(map(list,self.justaposed))
#         else:
#             return self.justaposed


#     def boundaries_list(self,new_zero=0):
#         # first the two circles boundaries
#         zero = new_zero

#         # first circle ending:
#         fce = zero + self.circle_points_n

#         c1 = [list(range(zero,fce))]
#         # c2 = [list(range(fce,fce+self.circle_points_n))]

#         c2 = [reverse_order_rangelist(fce+self.circle_points_n,fce)]

#         # for the rest of the faces:
#         rectangles = []

#         for i in range(zero,fce):
#             print(i,fce)
#             p0 = i
#             p1 = i + fce
#             if i+1 == fce:
#                 p2 = fce
#                 p3 = zero
#             else:
#                 p2 = i + fce + 1
#                 p3 = i + 1

#             # the current face
#             curr = [[p3,p0,p1,p2]]

#             rectangles.append(curr)

#         # rectangles.append(rectangles[0])
#         # rectangles.pop(0)

#         # print(rectangles)

#         # res_list = []

#         # res_list.append(c1)
#         # res_list.append(rectangles)
#         # res_list.append(c2)
        
#         res_list = [c1,rectangles,c2]

#         self.boundaries = res_list

#         return res_list


#     def as_city_object(self,attrs_dict):

#         # city_obj = {name: {
#         #                 "geometry": [
#         #                 {
#         #                     "boundaries": [],
#         #                     "lod": 1,
#         #                     "type": "Solid"
#         #                 }
#         #                 ],
#         #                 "attributes": {
#         #                 },
#         #                 "type": "GenericCityObject"
#         #             }}

#         # city_obj[name]['geometry'][0]['boundaries'].append(self.boundaries)
#         # city_obj[name]['attributes'] = attrs_dict

#         city_obj = {
#                         "geometry": [
#                         {
#                             "boundaries": [],
#                             "lod": 1,
#                             "type": "MultiSurface"
#                         }
#                         ],
#                         "attributes": {
#                         },
#                         "type": "GenericCityObject"
#                     }


#         # city_obj['geometry'][0]['boundaries'].append(self.boundaries)
#         city_obj['geometry'][0]['boundaries'] = self.boundaries


#         city_obj['attributes'] = attrs_dict

#         return city_obj


# # # # # THIS WAS AN ATTEMPT, MANTEINED HERE
# # # # # class city_json_simple2:
# # # # #     base = {
# # # # #             "type": "CityJSON",
# # # # #             "version": "1.0",
# # # # #             "CityObjects": {},
# # # # #             "vertices": [],
# # # # #             "metadata": {
# # # # #             "geographicalExtent": [
# # # # #             ]}}

# # # # # # cjio validation: 
# # # # # # cjio our_test_cylinder.json validate --long > test_cylinder_report.txt

# # # # #     mins = []
# # # # #     maxs = []

# # # # #     point_list = []

# # # # #     def __init__(self,axis_vertex_list,radii_list,attrs_list,pts_per_cicle=32):

# # # # #         # first we will check if two list are equally-sized
# # # # #         # thx: https://stackoverflow.com/a/16720915/4436950

# # # # #         ref_len = len(axis_vertex_list)
# # # # #         if all(len(lst) == ref_len for lst in [radii_list,attrs_list]):

# # # # #             for i,pointpair in enumerate(axis_vertex_list):
# # # # #                 print('processing segment ',i,' of ',ref_len,' segments')

# # # # #                 name = f't{i}'

# # # # #                 p1 = pointpair[0]
# # # # #                 p2 = pointpair[1]

# # # # #                 zero = i * 2 * pts_per_cicle

# # # # #                 cylinder = cylinder3D(p1,p2,radii_list[i],pts_per_cicle)
# # # # #                 self.point_list.append(cylinder.get_vertices_list(True))
# # # # #                 boundaries = cylinder.boundaries_list(zero)

# # # # #                 self.base['CityObjects'][name] = cylinder.as_city_object(attrs_list[i])

# # # # #                 self.mins.append(cylinder.mins)
# # # # #                 self.maxs.append(cylinder.maxs)

# # # # #                 del cylinder

# # # # #             abs_max = np.max(np.array(self.maxs),axis=0)
# # # # #             abs_min = np.min(np.array(self.mins),axis=0)

# # # # #             bbox = [*abs_min,*abs_max]

# # # # #             # filling the bounding box:
# # # # #             self.base['metadata']['geographicalExtent'] = bbox

# # # # #             # filling the vertices:
# # # # #             # self.base['vertices'] = list(map(list,self.point_list))

# # # # #             for i,point in enumerate(self.point_list[0]):
# # # # #                 self.base['vertices'].append(point)

# # # # #             # self.base['vertices'] = [[point.tolist()] for point in self.point_list]

# # # # #             # self.plist = [[point] for point in self.point_list]


# # # # #         else:
# # # # #             print('input lists are in different sizes, check your data!!!')


# # # # #     def dump_to_file(self,outpath):

# # # # #         with open(outpath,'w+') as writer:
# # # # #             json.dump(self.base,writer,indent=2)


# ##### OUR BIG CLASS:
# class city_json_simple:
#     base = {
#             "type": "CityJSON",
#             "version": "1.0",
#             "CityObjects": {},
#             "vertices": [],
#             "metadata": {
#             "geographicalExtent": [
#             ]}}

# # cjio validation: 
# # cjio our_test_cylinder.json validate --long > test_cylinder_report.txt

#     mins = []
#     maxs = []

#     point_list = []


#     def __init__(self,cylinderlist,EPSG):

#         # SETTING epsg
#         self.base["metadata"]["referenceSystem"] = f"urn:ogc:def:crs:EPSG::{EPSG}"

#         # first we will check if two list are equally-sized
#         # thx: https://stackoverflow.com/a/16720915/4436950

#         total_cylinders = len(cylinderlist)

#         for i,cylinder in enumerate(cylinderlist):
#             print('writing cylinder',i,' of ',total_cylinders,' segments')

#             name = f't{i}'

#             self.base['CityObjects'][name] = city_object_dict(cylinder['faces'],cylinder['attributes'])

#             self.mins.append(cylinder['mins'])
#             self.maxs.append(cylinder['maxs'])

#             self.base['vertices'] += cylinder['points']


#         abs_max = np.max(np.array(self.maxs),axis=0)
#         abs_min = np.min(np.array(self.mins),axis=0)

#         bbox = [*abs_min,*abs_max]

#         # filling the bounding box:
#         self.base['metadata']['geographicalExtent'] = bbox

#         # filling the vertices:
#         # self.base['vertices'] = list(map(list,self.point_list))3


        

#         # for i,point in enumerate(self.point_list[0]):
#         #     self.base['vertices'].append(point)

#         # self.base['vertices'] = [[point.tolist()] for point in self.point_list]

#         # self.plist = [[point] for point in self.point_list]


#     def dump_to_file(self,outpath):

#         with open(outpath,'w+') as writer:
#             json.dump(self.base,writer)








# # # ###############################################################

# # # # the points
# # # p1 = np.array([1,1,1])
# # # p2 = np.array([5,5,1])
# # # p3 = np.array([6,7,6])

# # # # c1 = cylinder3D(p1,p2,10)

# # # # p_list = c1.get_vertices_list(False)

# # # # v_list = c1.boundaries_list(64)

# # # # print(v_list[0])

# # # # print(c1.maxs)
# # # # print(c1.mins)
# # # # print(c1.justaposed)

# # # lines_list = [(p1,p2)]
# # # radius_list = [1]
# # # attrs_list = [{"function": "something"}]

# # # builder = city_json_simple(lines_list,radius_list,attrs_list,4)

# # # # print(builder.base)


# # # builder.dump_to_file('our_test_cylinder.json')

# pipes_filepath = '/home/kaue/sanit3Dsdi/tests/sample_rede_agua_tratada.geojson'
# rasterpath = os.path.join(os.environ['HOME'],'sanit3Dsdi/tests/test_vrt_dtm.vrt')

# as_gdf = gpd.read_file(pipes_filepath)

# material_key = 'MATERIAL'

# diameter_key = 'DIAMETRO'

# print(as_gdf[diameter_key].unique())

# meshinfos = []

# n_entities = as_gdf.shape[0]

# zeroindex = 0




# with open('cylinder_report.txt','w+') as writer:
#     for i,feature in enumerate(as_gdf.geometry):
#         if as_gdf[diameter_key][i] != '':
#             if feature.geom_type == 'LineString':
#                 as_array = np.array(feature)
#             else:
#                 lines = []
#                 for line in feature:
#                     lines.append(np.array(line))

#                 as_array = np.concatenate(lines,axis=0)


#             Z_list = []

#             for point in as_array:
#                 Z = get_raster_val_at_geoXY(*point,rasterpath) - 2 
#                 Z_list.append(Z)

#             # as_array = np.concatenate((as_array,np.array(Z_list)[:,-1:]),axis=1)
#             vertices = np.column_stack((as_array,np.array(Z_list)))

#             radius = float(as_gdf[diameter_key][i]) / 200 #200 transforms into radius in centimeters

#             customattrs = {"diametro":as_gdf[diameter_key][i],'material':as_gdf[material_key][i]}

#             try:
#                 print('cylinder',i,' of ',n_entities,' with zero index: ',zeroindex)
#                 cylinder_meshinfo = pymesh_cylinder_for_cityjson(vertices,radius,zero_index=zeroindex,custom_attrs=customattrs)

#                 zeroindex += (cylinder_meshinfo['zero_ref'] + 500 )
#             except Exception as e:
#                 writer.write(f'\n{i}')
#                 writer.write(feature.wkt)
#                 writer.write(str(e))


#             meshinfos.append(cylinder_meshinfo)

#             if i > 50:
#                 break



# # "referenceSystem":"urn:ogc:def:crs:EPSG::31984"


# builder = city_json_simple(meshinfos,31984)

# outpath = os.path.join(os.environ['HOME'],'data/sanit3d_out/pipery01_50.json')
# print(outpath)

# builder.dump_to_file(outpath)





        


