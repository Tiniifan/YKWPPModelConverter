# ez_to_obj
Python scrip to decompile .ez to .zip and Convert .ymd (Yo-Kai Watch Puni Puni model) to .obj

## Requirements
- Python 3: https://www.python.org/downloads/
- Crypto: https://pypi.org/project/pycrypto/

## Usage
Assuming Python has been installed, you can invoke this script with the following in a command line/terminal:

  `python ez.py [path to folder containing .ez files]`

You should put all yours .ez files on one folder like "ezs"

Example

  `python ez.py ./ezs`

## Arguments
    usage: ez.py [-h]  ez_path

    Decompile .ez and convert .ymd to .obj

    positional arguments:
      ez_path      path to the folder containing ez files

    optional arguments:
      -h, --help    show this help message and exit

## Notes
Yo-Kai Watch Puni Puni is an old game, the ymd are different between the first and the last, the script isn't able to convert all ymds.  

Sometimes when you go to apply your texture in a 3D tool like Blender, your texture will be dammaged, go to the UV and do Miror Y to restore the right UVS    

Sometimes some faces are missing without any reasons.
