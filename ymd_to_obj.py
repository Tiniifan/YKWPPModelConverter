# ymd_to_obj.py 1.0

import os
import zlib
import argparse
from struct import *

def write_obj(filename, positions, uvs, normals, faces):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    f = open(filename, 'w', encoding='utf-8')
    
    for position in positions:
        f.write("v %f %f %f\n" % (position[0], position[1], position[2]) )

    for uv in uvs:
        f.write("vt %f %f\n" % (uv[0], uv[1]) )

    for normal in normals:
        f.write("vn %f %f %f\n" % (normal[0], normal[1], normal[2]) )

    for face in faces:
        f.write("f %i/%i/%i %i/%i/%i %i/%i/%i \n" % (face[0]+1, face[0]+1, face[0]+1, face[1]+1, face[1]+1, face[1]+1, face[2]+1, face[2]+1, face[2]+1) )   
    
def geometries_to_obj(file_name, data):
    positions = []
    uvs = []
    normals = []
    faces = []

    # Get mesh data
    mesh_length = unpack('i', data.read(4))[0]
    for i in range(mesh_length):
        positions.append(list(unpack("<%df" % 3, data.read(12))))
        normals.append(list(unpack("<%df" % 3, data.read(12))))
        uvs.append(list(unpack("<%df" % 2, data.read(8))))

    # Create triangle according to number of faces
    faces_count = unpack('i', data.read(4))[0]    
    for i in range(0, faces_count-3, 3):
        faces.append([i, i+1, i+2])

    # Skip bytes
    data.seek(data.tell() + (faces_count+1) * 4)

    # Create .obj
    write_obj(file_name, positions, uvs, normals, faces)
    
def ymd_to_obj(file_path):
    # Open ymd file
    with open(file_path, 'rb') as f:
        file_name = os.path.basename(f.name).split(".")[0]

        # Load header of file
        header = f.read(200)
        searches = {b'geometries': 45, b'skin1Shape':40}
        successful = False

        # Try all searches
        for key in list(searches.keys()):
            if successful == True:
                break
            
            s = header.find(key)
            # Found! the .ymd contains 3D data
            if s > -1:
                f.seek(s - 8)
                meshes_count = unpack("<i", f.read(4))[0]
                f.seek(f.tell() + 4)

                for i in range(meshes_count):
                    f.seek(f.tell() + searches[key])
                    geometries_to_obj(os.path.splitext(file_path)[0] + "/" + file_name + "_" + str(i) + ".obj", f)
                    successful = True
            else:
                successful = False

        if successful == True:
            print("Successful", file_name, ".ymd converted to .obj")
        else:
            print("Unable to convert", file_name, ".ymd to .obj")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Converts .ymd into .obj")
    parser.add_argument("ymd_path", help="path to the folder containing ymd files")

    args = parser.parse_args()
    indir = os.path.normpath(args.ymd_path)

    for f in os.listdir(indir):
        if f.endswith(".ymd"):
            print("Load ", indir+os.path.sep+f)
            ymd_to_obj(indir+os.path.sep+f)
