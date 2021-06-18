from typing_extensions import Concatenate
import numpy as np


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

    Z = - (plane4vec[0]*X+plane4vec[1]*Y+plane4vec[3])/plane4vec[2]

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


class cylinder3D:
    '''
        class to implement a cylinder in 3D to use it in cityjson
    '''

    def __init__(self,p1,p2,radius,points_per_circle=32):
        # first, its handy:
        self.p_1 = p1
        self.p_2 = p2
        self.number_of_points = points_per_circle*2
        self.half_points = points_per_circle


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

    def get_vertices_list(self):

        # justaposed = np.concatenate((self.c1,self.c2))

        return list(map(list,self.c1)) + list(map(list,self.c2))






###############################################################

# the points
p1 = np.array([1,1,1])
p2 = np.array([5,5,5])

difV = p2-p1

difV_normalized = normalize_vec(difV)

plane1_normal = difV_normalized

plane_p1 = plane_as_4vec(difV_normalized,p1)

point_plane_p1 = pt_onplane(plane_p1,p1[0]+1,p1[1]-1)

vec1_paralelplane = point_plane_p1 - p1

vec1_paralelplane = normalize_vec(vec1_paralelplane)

vec2_paralelplane = np.cross(vec1_paralelplane,plane1_normal)

vec2_paralelplane = normalize_vec(vec2_paralelplane)

circle1 = circumference_3D(p1,10,vec1_paralelplane,vec2_paralelplane)

# for point in circle1:
#     print(np.dot(point-p1,difV))
#     print(np.linalg.norm(point-p1))
#     print()

# print(vec1_paralelplane)
# print(vec2_paralelplane)
# print(np.dot(vec1_paralelplane,vec2_paralelplane))


c1 = cylinder3D(p1,p2,10)

print(c1.get_vertices_list())

