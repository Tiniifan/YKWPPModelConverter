import os
import struct

def write_obj(objects, output_path):
    """
    Writes mesh data to .obj files based on the provided objects dictionary.

    Args:
    - objects (dict): Dictionary containing object and mesh data.
    - output_path (str): Path to the directory where the .obj files will be written.
    """
    
    for object_name, meshes in objects.items():
        for mesh_name, mesh_data in meshes.items():
            file_name = f"{output_path}/{object_name}_{mesh_name}.obj"
            
            # Extract the directory from the file path
            directory = os.path.dirname(file_name)  
            
            # If the directory does not exist, create it
            if not os.path.exists(directory):
                os.makedirs(directory)    
            
            positions = mesh_data["positions"]
            uvs = mesh_data["uvs"]
            normals = mesh_data["normals"]
            faces = mesh_data["faces"]
            
            with open(file_name, 'w', encoding='utf-8') as obj_file:
                for position in positions:
                    obj_file.write("v %f %f %f\n" % (position[0], position[1], position[2]))
                for uv in uvs:
                    obj_file.write("vt %f %f\n" % (uv[0], uv[1]))
                for normal in normals:
                    obj_file.write("vn %f %f %f\n" % (normal[0], normal[1], normal[2])) 

                for face in faces:
                    obj_file.write("f %i/%i/%i %i/%i/%i %i/%i/%i\n" % (face[0]+1, face[0]+1, face[0]+1, face[1]+1, face[1]+1, face[1]+1, face[2]+1, face[2]+1, face[2]+1)) 

def get_geometries(data):
    """
    Extracts mesh geometries from binary data.

    Args:
    - data (io.BufferedReader): Binary data stream.

    Returns:
    Tuple containing positions, uvs, normals, and faces.
    """
    
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
        for i in range(0, faces_count, 3):
            faces.append([i, i+1, i+2])

        # Skip bytes
        data.seek(data.tell() + (faces_count) * 4)

        # Create .obj
        return positions, uvs, normals, faces

patterns = ["geometries", "skin"]
            
def to_obj(file_path, output_path):
    """
    Reads an EZ file, extracts mesh data, and writes .obj files.

    Args:
    - file_path (str): Path to the input EZ file.
    - output_path (str): Path to the directory where the .obj files will be written.

    Returns:
    True if successful, False otherwise.
    """
    
    objects = {}
    can_be_opened = False
    
    geometrie_offset = 0   
    file_name = os.path.basename(file_path).split(".")[0].strip()
    
    with open(file_path, 'rb') as file:
        # Read the first 300 bytes of the file
        data = file.read(300)

        for pattern in patterns:
            # Find all occurrences of the text in the data
            positions = [pos for pos in range(len(data)) if data.startswith(pattern.encode(), pos)]
            
            if positions:
                geometrie_offset = positions[0] - 8
                can_be_opened = True
                break
             
        if can_be_opened:
            file.seek(geometrie_offset)
            meshes_count = struct.unpack("<i", file.read(4))[0]

            for i in range(meshes_count):
                mesh_name = "unnamed_mesh_" + str(i)
                mesh_lentgh = struct.unpack("<i", file.read(4))[0]
                
                if mesh_lentgh == 1:
                    file.read(4)
                    object_name = file.read(struct.unpack("<i", file.read(4))[0]).decode()
                    file.read(4)
                else:
                    mesh_name = file.read(mesh_lentgh).decode()
                    
                    file.read(12)
                    object_name = file.read(struct.unpack("<i", file.read(4))[0]).decode()
                    file.read(4)
                    
                positions, uvs, normals, faces = get_geometries(file)
                
                if object_name not in objects:
                    objects[object_name] = {}

                if mesh_name not in objects[object_name]:
                    objects[object_name][mesh_name] = {}

                objects[object_name][mesh_name].setdefault("positions", []).extend(positions)
                objects[object_name][mesh_name].setdefault("uvs", []).extend(uvs)
                objects[object_name][mesh_name].setdefault("normals", []).extend(normals)
                objects[object_name][mesh_name].setdefault("faces", []).extend(faces)
                
            write_obj(objects, output_path + "/" + file_name + "/")
            return True
        else:
            return False
