# ymd_to_obj
Python scrip to convert some .ymd (Yo-Kai Watch Puni Puni model) to .obj

## Requirements
- Python 3: https://www.python.org/downloads/

## Usage
Assuming Python has been installed, you can invoke this script with the following in a command line/terminal:

  `python ymd_to_obj.py [path to folder containing .ymd files]`

You should put all yours .ymd files on one folder like "ymds" because I'm not sure that the application can read subfolders

## Arguments
    usage: ymd_to_obj.py [-h]  ymd_path

    Converts .ymd into .obj

    positional arguments:
      ymd_path      path to the folder containing ymd files

    optional arguments:
      -h, --help    show this help message and exit

## Notes
Yo-Kai Watch Puni Puni is an old game, the ymd are different between the first and the last, the script isn't able to convert all ymds.  
Sometimes when you go to apply your texture in a 3D tool, your texture will be dammaged, go to the UV and do Miror Y to restore the right UVS  
Sometimes some faces are missing without any reasons.
