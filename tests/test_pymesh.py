
import enum
import pymesh
import numpy as np
import json


def create_edgeslist(num_vertices,as_np=True):
    edgelist = []

    if num_vertices > 0:
        for i in range(num_vertices-1):
            edgelist.append([i,i+1])

    if as_np:
        return np.array(edgelist)
    else:
        return edgelist

# worked!!!


#                        0       1      2         3      4       5
vertices = np.array([[1, 1,1],[2,1,1],[2,2,1]],dtype='float64') * 10

# edges = np.array([[0, 1],[1,2],[3,4],[4,5]])

# edges = create_edgeslist(vertices.shape[0])


# wire_network = pymesh.wires.WireNetwork.create_from_data(vertices, edges)


# inflator = pymesh.wires.Inflator(wire_network)

# inflator.set_profile(16)

# inflator.inflate(1, per_vertex_thickness=False)



# mesh = inflator.mesh

# bbox_min, bbox_max = mesh.bbox

# mins = bbox_min.tolist()
# maxs = bbox_max.tolist()

# points = mesh.vertices.tolist()
# faces = mesh.faces.tolist()

# faces = [[face] for face in faces]

# # mesh,info = pymesh.collapse_short_edges(mesh,0.1)


# meshdata = {'mins':mins,'maxs':maxs,'points':points,'faces':faces}

# try:
#     print(info)

#     meshdata['edges_collapsed'] = info["num_edge_collapsed"]

# except:
#     pass

# with open('meshdata.json','w+') as handle:
#     json.dump(meshdata,handle)


#mesh.write_to_file("debug.obj")


# pymesh.save_mesh('canos.obj',mesh)

pipe1 = pymesh.generate_cylinder(p0=vertices[0,:], p1=vertices[1,:], r0=0.19, r1=0.19, num_segments=32)

pipe1_outer = pymesh.generate_cylinder(p0=vertices[0,:], p1=vertices[1,:], r0=0.2, r1=0.2, num_segments=32)

pipe2 = pymesh.generate_cylinder(p0=vertices[1,:], p1=vertices[2,:], r0=0.19, r1=0.19, num_segments=32)

pipe2_outer = pymesh.generate_cylinder(p0=vertices[1,:], p1=vertices[2,:], r0=0.2, r1=0.2, num_segments=32)

joint_sphere = pymesh.generate_icosphere(0.195,vertices[1,:],refinement_order=2)

joint_sphere_outer = pymesh.generate_icosphere(0.205,vertices[1,:],refinement_order=2)

inner_tree = pymesh.CSGTree({"union": [{"mesh": pipe1}, {"mesh": joint_sphere}, {"mesh": pipe2}]})

outer_tree = pymesh.CSGTree({"union": [{"mesh": pipe1_outer}, {"mesh": joint_sphere_outer}, {"mesh": pipe2_outer}]})

pipe_tree = pymesh.CSGTree({"difference": [outer_tree, inner_tree]})

pymesh.save_mesh('pipes.obj',pipe_tree.mesh)


# for i,point in enumerate(vertices):
#     print(i,point)

def one_pipe_making(pointlist,diameter,thickness,pipenumber=0,extra_safe_percent=0.05,joint_ampliation=0.01):

    # lists to store geometries
    inner_geometries = []
    outer_geometries = []

    number_of_points = pointlist.shape[0]


    # radius for inner and outer geometries
    outer_radius = diameter/2
    inner_radius = outer_radius - thickness

    # a little bit bigger for joints
    outer_radius_sphere = outer_radius + outer_radius * joint_ampliation
    inner_radius_sphere = inner_radius + inner_radius * joint_ampliation

    for i,point in enumerate(pointlist):
        print(i,point)

        # calculating the joint spheres:
        # first and last points does not have any joint
        if (i > 0) and (i < (number_of_points - 1)):

            joint_sphere = pymesh.generate_icosphere(inner_radius_sphere,point,refinement_order=2)

            joint_sphere_outer = pymesh.generate_icosphere(outer_radius_sphere,point,refinement_order=2)

            inner_geometries.append(joint_sphere)

            outer_geometries.append(joint_sphere_outer)

        if i < (number_of_points - 1):
            # the outer pipe must not have the safe margin
            p2 = pointlist[i+1,:] # except for the last inner segment, it will always be this point


            outer_pipe = pymesh.generate_cylinder(p0=point, p1=p2, r0=outer_radius, r1=outer_radius, num_segments=32)
            outer_geometries.append(outer_pipe)


            # we neeed to apply some safe margin, to avoid thin triangles
            if i == 0: # b_a is vector from B to A
                b_a = point - p2
                point += b_a * extra_safe_percent

            if i == (number_of_points - 2):
                a_b = p2 - point

                p2 += a_b * extra_safe_percent

            inner_pipe = pymesh.generate_cylinder(p0=point, p1=p2, r0=inner_radius, r1=inner_radius, num_segments=32)

            inner_geometries.append(inner_pipe)

    # now the  inner and outer trees for combinations
    print('joining from geometries')

    innerlist = [{'mesh':geometry} for geometry in inner_geometries]

    outerlist = [{'mesh':geometry} for geometry in outer_geometries]

    inner_tree = pymesh.CSGTree({"union": innerlist})

    outer_tree = pymesh.CSGTree({"union": outerlist})

    pipe_tree = pymesh.CSGTree({"difference": [outer_tree, inner_tree]})

    ret_mesh = pipe_tree.mesh

    # we tried to add per mesh attibute, no sucess
    # ret_mesh.add_attribute('number')
    # vals = np.ones(ret_mesh.num_vertices) * pipenumber
    # ret_mesh.set_attribute('number',vals)
    print(ret_mesh.get_attribute_names())
    print(ret_mesh.get_attribute('source'))

    return ret_mesh

def merge_meshlist(meshlist,print_info=True):

    if print_info:
        print('joining ',len(meshlist),' meshes')

    mergelist = [{'mesh':geometry} for geometry in meshlist]

    merging_tree = pymesh.CSGTree({"union": mergelist})

    return merging_tree.mesh




test_pipe1 = one_pipe_making(vertices,1,0.01,1)
test_pipe2 = one_pipe_making(vertices+5,2,0.5,2)
test_pipe3 = one_pipe_making(vertices+10,1.5,0.1,3)

meshlist = [test_pipe1,test_pipe2,test_pipe3]

test_pipe = merge_meshlist(meshlist)

# print(test_pipe.get_attribute_names())
# print(len(test_pipe.get_attribute('source').tolist()))
# print(test_pipe.num_faces)

src_mesh_list = test_pipe.get_attribute('source').astype(np.int_).tolist()

max_mesh_index = max(src_mesh_list)

meshindexlist = list(range(0,max_mesh_index+1))

# print(src_mesh_list.index(1))

# # for i,face in enumerate(test_pipe.faces):
# #     print(face,int(src_mesh_list[i]))

# dict comprehension, thx https://stackoverflow.com/a/44593994/4436950
ind = {x: [i for i, value in enumerate(src_mesh_list) if value == x] for x in meshindexlist}

# print(ind)

edgeslist = []

for i,faceindex in enumerate(ind[0]):
    edgeslist.append([test_pipe.faces[faceindex].tolist()])


print(edgeslist)
pymesh.save_mesh('pipes.ply',test_pipe, *test_pipe.get_attribute_names(), ascii=True)
