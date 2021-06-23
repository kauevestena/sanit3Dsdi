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

#                         0        1        2         3      4       5
vertices = np.array([[1, 1, 1],[1, 2, 2],[2,2,1],[5,2,1.5],[8,5,3],[8,8,2],[7,6,1],[7,7,7],[5,6,4],[5,6,5],[5,5,5],[7,6,6]])

# edges = np.array([[0, 1],[1,2],[3,4],[4,5]])

edges = create_edgeslist(vertices.shape[0])


wire_network = pymesh.wires.WireNetwork.create_from_data(vertices, edges)


inflator = pymesh.wires.Inflator(wire_network)

inflator.set_profile(16)

inflator.inflate(0.2, per_vertex_thickness=False)



mesh = inflator.mesh

bbox_min, bbox_max = mesh.bbox

mins = bbox_min.tolist()
maxs = bbox_max.tolist()

points = mesh.vertices.tolist()
faces = mesh.faces.tolist()

faces = [[face] for face in faces]

# mesh,info = pymesh.collapse_short_edges(mesh,0.1)


meshdata = {'mins':mins,'maxs':maxs,'points':points,'faces':faces}

try:
    print(info)

    meshdata['edges_collapsed'] = info["num_edge_collapsed"]

except:
    pass

with open('meshdata.json','w+') as handle:
    json.dump(meshdata,handle)


#mesh.write_to_file("debug.obj")


pymesh.save_mesh('canos.obj',mesh)
