import os

import ez
import ymd

import argparse

if __name__ == '__main__':
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Decompile .ez and convert .ymd to .obj")
    parser.add_argument("input_folder", help="path to the folder containing ez or ymd files")
    parser.add_argument("output_folder", help="path to store your objs")  # Corrected spelling of 'output_folder'

    # Parse command-line arguments
    args = parser.parse_args()
    input_folder = os.path.normpath(args.input_folder)  # Corrected variable name
    output_folder = os.path.normpath(args.output_folder)

    # Iterate over files in the input folder
    for file_name in os.listdir(input_folder):
        input_file = os.path.join(input_folder, file_name)

        # Process .ez files
        if file_name.endswith(".ez"):
            print("Processing .ez file: {}".format(input_file))
            
            # Convert .ez to .zip
            ez.ToZip(input_file, output_folder)
                
            # Set up paths for the new .ymd file and output folder
            filename = os.path.splitext(os.path.basename(input_file))[0]
            new_output_folder = os.path.join(output_folder, filename)
            new_input_file = os.path.join(new_output_folder, filename + '.ymd')
                
            # Convert .ymd to .obj
            if ymd.to_obj(new_input_file, new_output_folder):
                print("Conversion of {} to obj succeeded".format(input_file))
            else:
                print("Can't convert {} to obj".format(input_file))
        # Process .ymd files
        elif file_name.endswith(".ymd"):
            print("Processing .ymd file: {}".format(input_file))
            # Convert .ymd to .obj
            if ymd.to_obj(input_file, output_folder):
                print("Conversion of {} to obj succeeded".format(input_file))
            else:
                print("Can't convert {} to obj".format(input_file))
