from os import removexattr
import numpy as np
import json

# normalized_v = v/np.linalg.norm(v)

def normalize_vec(input_vec):
    try:
        return input_vec/np.linalg.norm(input_vec)
    except:
        print(np.linalg.norm(input_vec),'check for zero norm')
        return input_vec * 0

# class plane:

#     def __init__(self,pt_onplane:np.array,normal:np.array):
#         self.d = -pt_onplane.dot(normal)
#         self.a = normal[0]
#         self.b = normal[1]
#         self.c = normal[2]


#     def a_point(self,X,Y,Z):
#         return self.a*X + self.b*Y + self.c*Z + self.d

def plane_as_4vec(normal:np.array,pt_onplane:np.array):
    '''
        plane as 4vec:

        - normal vector
        - point on plane
    '''
    return np.array([*normal,-np.dot(normal,pt_onplane)])

def pt_onplane(plane4vec,X,Y):
    # plane equation, with z=f(X,Y)
    if not plane4vec[2] < 0.0001:

        Z = - (plane4vec[0]*X+plane4vec[1]*Y+plane4vec[3])/plane4vec[2]

        return np.array([X,Y,Z])

    else:
        Z = X + 0.1*X

        Y = - - (plane4vec[0]*X+plane4vec[2]*Z+plane4vec[3])/plane4vec[1]

        return np.array([X,Y,Z])


def gdec2rad(gdec):
    return gdec * np.pi/180

def circumference_3D(center_pt,radius,v1,v2,n_points=32):
    '''
    a circunference in 3D:

    - Center Point
    - The Radius

    thx: https://math.stackexchange.com/a/1184089/307651

    '''

    angles = np.linspace(0,2*np.pi,n_points)

    point_list = []

    for angle in angles:
        # circle_point = center_pt + (radius*np.cos(angle)*v1) + (radius*np.sin(angle)*v2)
        circle_point = center_pt + radius * (np.cos(angle)*v2 + np.sin(angle)*v1)
        point_list.append(circle_point)

    return np.array(point_list)

def reverse_order_rangelist(a,b):
    l1 = list(range(-a+1,-b+1))

    return list(map(abs,l1))


class cylinder3D:
    '''
        class to implement a cylinder in 3D to use it in cityjson
    '''

    def __init__(self,p1,p2,radius,points_per_circle=32):
        # first, its handy:
        self.p_1 = p1
        self.p_2 = p2
        self.number_of_points = points_per_circle*2
        self.circle_points_n = points_per_circle


        # the axis of the cylinder, is the difference vector:
        self.axis = p2 - p1
        # its normalized version will be used as the plane normal
        self.plane_n = normalize_vec(self.axis)
        # the plane as a 4 vec of parameters: [a,b,c,d]
        plane = plane_as_4vec(self.plane_n,p1)
        # any point on the plane
        point_on_plane = pt_onplane(plane,p1[0]+0.1*p1[0],p1[1]-0.1*p1[1])
        # first vector parallel to the plane containing the circle
        vec1_planeparalel = normalize_vec(point_on_plane-p1)
        # second vector parallel to the plane containing the circle
        vec2_planeparalel = normalize_vec(np.cross(vec1_planeparalel,self.plane_n))
        # first circumference

        # it must needs to be divisible by 4
        if points_per_circle % 4 != 0:
            points_per_circle = (points_per_circle // 4) * 4

        # the first circumference
        self.circle1 = circumference_3D(p1,radius,vec1_planeparalel,vec2_planeparalel,points_per_circle)
        # the second contains basically each point summed up with the axis
        self.circle2 = self.circle1 + self.axis



    def check_circles(self):
        centers = (self.p_1,self.p_2)

        for i,circle in enumerate((self.circle1,self.circle2)):
            print('\ncircle ',i+1,':')
            for point in circle:
                print(np.dot(point-centers[i],self.axis))
                print(np.linalg.norm(point-centers[i]))


    def get_vertices_list(self,as_list=False):

        self.justaposed = np.concatenate((self.circle1,self.circle2))

        self.mins = np.min(self.justaposed,axis=0)
        self.maxs = np.max(self.justaposed,axis=0)


        if as_list:
            return list(map(list,self.justaposed))
        else:
            return self.justaposed


    def boundaries_list(self,new_zero=0):
        # first the two circles boundaries
        zero = new_zero

        # first circle ending:
        fce = zero + self.circle_points_n

        c1 = [list(range(zero,fce))]
        # c2 = [list(range(fce,fce+self.circle_points_n))]

        c2 = [reverse_order_rangelist(fce+self.circle_points_n,fce)]

        # for the rest of the faces:
        rectangles = []

        for i in range(zero,fce):
            print(i,fce)
            p0 = i
            p1 = i + fce
            if i+1 == fce:
                p2 = fce
                p3 = zero
            else:
                p2 = i + fce + 1
                p3 = i + 1

            # the current face
            curr = [[p3,p0,p1,p2]]

            rectangles.append(curr)

        # rectangles.append(rectangles[0])
        # rectangles.pop(0)

        # print(rectangles)

        # res_list = []

        # res_list.append(c1)
        # res_list.append(rectangles)
        # res_list.append(c2)
        
        res_list = [c1,rectangles,c2]

        self.boundaries = res_list

        return res_list


    def as_city_object(self,attrs_dict):

        # city_obj = {name: {
        #                 "geometry": [
        #                 {
        #                     "boundaries": [],
        #                     "lod": 1,
        #                     "type": "Solid"
        #                 }
        #                 ],
        #                 "attributes": {
        #                 },
        #                 "type": "GenericCityObject"
        #             }}

        # city_obj[name]['geometry'][0]['boundaries'].append(self.boundaries)
        # city_obj[name]['attributes'] = attrs_dict

        city_obj = {
                        "geometry": [
                        {
                            "boundaries": [],
                            "lod": 1,
                            "type": "MultiSurface"
                        }
                        ],
                        "attributes": {
                        },
                        "type": "GenericCityObject"
                    }


        # city_obj['geometry'][0]['boundaries'].append(self.boundaries)
        city_obj['geometry'][0]['boundaries'] = self.boundaries


        city_obj['attributes'] = attrs_dict

        return city_obj


##### OUR BIG CLASS:
class city_json_simple:
    base = {
            "type": "CityJSON",
            "version": "1.0",
            "CityObjects": {},
            "vertices": [],
            "metadata": {
            "geographicalExtent": [
            ]}}

# cjio validation: 
# cjio our_test_cylinder.json validate --long > test_cylinder_report.txt

    mins = []
    maxs = []

    point_list = []

    def __init__(self,axis_vertex_list,radii_list,attrs_list,pts_per_cicle=32):

        # first we will check if two list are equally-sized
        # thx: https://stackoverflow.com/a/16720915/4436950

        ref_len = len(axis_vertex_list)
        if all(len(lst) == ref_len for lst in [radii_list,attrs_list]):

            for i,pointpair in enumerate(axis_vertex_list):
                print('processing segment ',i,' of ',ref_len,' segments')

                name = f't{i}'

                p1 = pointpair[0]
                p2 = pointpair[1]

                zero = i * 2 * pts_per_cicle

                cylinder = cylinder3D(p1,p2,radii_list[i],pts_per_cicle)
                self.point_list.append(cylinder.get_vertices_list(True))
                boundaries = cylinder.boundaries_list(zero)

                self.base['CityObjects'][name] = cylinder.as_city_object(attrs_list[i])

                self.mins.append(cylinder.mins)
                self.maxs.append(cylinder.maxs)

                del cylinder

            abs_max = np.max(np.array(self.maxs),axis=0)
            abs_min = np.min(np.array(self.mins),axis=0)

            bbox = [*abs_min,*abs_max]

            # filling the bounding box:
            self.base['metadata']['geographicalExtent'] = bbox

            # filling the vertices:
            # self.base['vertices'] = list(map(list,self.point_list))

            for i,point in enumerate(self.point_list[0]):
                self.base['vertices'].append(point)

            # self.base['vertices'] = [[point.tolist()] for point in self.point_list]

            # self.plist = [[point] for point in self.point_list]


        else:
            print('input lists are in different sizes, check your data!!!')


    def dump_to_file(self,outpath):

        with open(outpath,'w+') as writer:
            json.dump(self.base,writer,indent=2)










###############################################################

# the points
p1 = np.array([1,1,1])
p2 = np.array([5,5,1])
p3 = np.array([6,7,6])

# c1 = cylinder3D(p1,p2,10)

# p_list = c1.get_vertices_list(False)

# v_list = c1.boundaries_list(64)

# print(v_list[0])

# print(c1.maxs)
# print(c1.mins)
# print(c1.justaposed)

lines_list = [(p1,p2)]
radius_list = [1]
attrs_list = [{"function": "something"}]

builder = city_json_simple(lines_list,radius_list,attrs_list,4)

# print(builder.base)


builder.dump_to_file('our_test_cylinder.json')