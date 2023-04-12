import os
import ymd
import struct
import argparse

from Crypto.Cipher import AES
from zipfile import ZipFile

def decrypt_file(key, input_file, output_file=None, chunksize=64*1024):
    if not output_file:
        output_file = os.path.splitext(input_file)[0] + '.zip'

    filesize = os.path.getsize(input_file)

    cipher = AES.new(key, AES.MODE_CBC, b'0000000000000000')

    with open(input_file, 'rb') as infile:
        with open(output_file, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(cipher.decrypt(chunk))

            outfile.truncate(filesize)

if __name__ == '__main__':
    key = b'\x2a\xb5\x11\xf4\x77\x97\x7d\x25\xcf\x6f\x7a\x8a\xe0\x49\xa1\x25'
    
    parser = argparse.ArgumentParser(description="Decompile .ez and convert .ymd to .obj")
    parser.add_argument("ez_path", help="path to the folder containing ez files")

    args = parser.parse_args()
    indir = os.path.normpath(args.ez_path)

    for f in os.listdir(indir):
        if f.endswith(".ez"):
            # Get file
            input_file = indir+os.path.sep+f
            filename = os.path.splitext(os.path.basename(input_file))[0]
            directory = os.path.dirname(input_file)
            print("Load", filename)
            
            # Decrypt and extract file
            decrypt_file(key, input_file)
            zf = ZipFile(directory + '/' + filename + '.zip', 'r')
            zf.extractall(directory + '/' + filename)
            zf.close()
            
            # Convert .ymd to .obj
            ymd.to_obj(directory + '/' + filename + '/' + filename + '.ymd')
