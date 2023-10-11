# [YKWPPModelConverter](https://github.com/Tiniifan/YKWPPModelConverter/releases/latest) (Puni Puni Model Converter)

YKWPP Model Converter is a tool that allows you to decompile `.ez` files and convert `.ymd` files to `.obj`.  

The tool comes in two versions: 
- a Graphical User Interface (GUI) version 
- a Command-Line Interface (CMD) version.
  
For the time being, only the OBJ export functionality is available.

## Requirements
- Python 3: https://www.python.org/downloads/
- Crypto: https://pypi.org/project/pycrypto/
- tkinter: https://docs.python.org/3/library/tkinter.html

## GUI Version

The GUI version provides a user-friendly interface for selecting input files and setting the output folder. It can be run by executing the following command:

```bash
python YKWPPModelConverterGUI.py
````

## CMD Version
The CMD version is designed for command-line use and requires invocation with the following syntax:

```bash
python YKWPPModelConverter.py [input_folder] [output_folder]
````

Example

  `python YKWPPModelConverter.py ./ymds ./objs`

## Arguments
    usage: YKWPPModelConverter.py [-h]  input_path output_path

    Decompile .ez and convert .ymd to .obj

    positional arguments:
      input_path        path to the folder containing ez or ymd files
      output_folder     path to store your objs

    optional arguments:
      -h, --help    show this help message and exit

## Notes
Yo-Kai Watch Puni Puni is an older game with varying YMD structures between the initial and final versions. As a result, the script may encounter difficulties converting all YMD files.

Occasionally, when applying textures in a 3D tool such as Blender, you might notice texture damage. In such cases, navigate to the UV mapping and perform a 'Mirror Y' operation to restore the correct UVs.

Furthermore, there may be instances where certain faces are inexplicably missing.
