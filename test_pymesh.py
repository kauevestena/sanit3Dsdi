import pymesh
import numpy as np
import json


# worked!!!

vertices = np.array([[1, 1, 1],[5, 5, 1],[5, 5, 5]])

edges = np.array([[0, 1],[1,2]]);


wire_network = pymesh.wires.WireNetwork.create_from_data(vertices, edges)


inflator = pymesh.wires.Inflator(wire_network)

inflator.set_profile(16)

inflator.inflate(0.5, per_vertex_thickness=False)



mesh = inflator.mesh

bbox_min, bbox_max = mesh.bbox

mins = bbox_min.tolist()
maxs = bbox_max.tolist()

points = mesh.vertices.tolist()
faces = mesh.faces.tolist()

faces = [[face] for face in faces]

meshdata = {'mins':mins,'maxs':maxs,'points':points,'faces':faces,}

with open('meshdata.json','w+') as handle:
    json.dump(meshdata,handle)


#mesh.write_to_file("debug.obj")


pymesh.save_mesh('canos.obj',mesh)
