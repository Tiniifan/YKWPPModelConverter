import os
import struct

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
    mesh_length = struct.unpack('i', data.read(4))[0]
    if mesh_length > 0:
        for i in range(mesh_length):
            positions.append(list(struct.unpack("<%df" % 3, data.read(12))))
            normals.append(list(struct.unpack("<%df" % 3, data.read(12))))
            uvs.append(list(struct.unpack("<%df" % 2, data.read(8))))

        # Create triangle according to number of faces
        faces_count = struct.unpack('i', data.read(4))[0]    
        for i in range(0, faces_count-3, 3):
            faces.append([i, i+1, i+2])

        # Skip bytes
        data.seek(data.tell() + (faces_count+1) * 4)

        # Create .obj
        write_obj(file_name, positions, uvs, normals, faces)
    
def to_obj(file_path):
    # Open ymd file
    with open(file_path, 'rb') as f:
        file_name = os.path.basename(f.name).split(".")[0].strip()
        directory = os.path.dirname(file_path)

        # Try to find object name
        f.seek(8)
        found_object = False
        name = ''
        for i in range(10):
            name_size = struct.unpack("<i", f.read(4))[0]
            if (name_size < 5):
                pass
            elif (name_size < 20):
                name = f.read(name_size).decode()
                if name.endswith("_01") and not name.endswith("_01_01"):
                    found_object = True
                    break
        
        if found_object:
            # Valid ymd file
            valid_meshes_names = ['geometries', 'skinShape']
            mesh_number = 1
            
            for i in range(20):
                name_size = struct.unpack("<i", f.read(4))[0]
                if (name_size < 5):
                    pass
                elif (name_size < 20):
                    name = f.read(name_size).decode()
                    
                    for valid_mesh_name in valid_meshes_names:
                        if name.startswith(valid_mesh_name):
                            # Valid mesh name
                            for i in range(10):
                                name_size = struct.unpack("<i", f.read(4))[0]
                                if (name_size < 5):
                                    pass
                                elif (name_size < 20):
                                    f.read(name_size).decode()
                                else:
                                    # Valid geometre
                                    geometries_to_obj(directory + '/' + file_name + '_' + str(mesh_number) + '.obj', f)
                                    mesh_number += 1
                                    f.seek(f.tell()-4)
                                    break
                                    
            print('Successful ' + file_name + '.ymd converted to .obj')
        else:
            print("Unable to convert "  + file_name + ".ymd to .obj")