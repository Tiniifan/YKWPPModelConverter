import os

from Crypto.Cipher import AES
from zipfile import ZipFile

# Encryption key for EZ files
ez_key = b'\x2a\xb5\x11\xf4\x77\x97\x7d\x25\xcf\x6f\x7a\x8a\xe0\x49\xa1\x25'

def decrypt_file(key, input_file, output_file=None, chunksize=64*1024):
    """
    Decrypts a file using AES encryption in CBC mode.

    Args:
    - key (bytes): The encryption key.
    - input_file (str): Path to the input encrypted file.
    - output_file (str): Path to the output decrypted file.
                        If not provided, a default output file with a .zip extension is used.
    - chunksize (int): Size of the chunks to read and decrypt at a time.
    """
    
    if not output_file:
        output_file = os.path.splitext(input_file)[0] + '.zip'

    filesize = os.path.getsize(input_file)

    # Initialize AES cipher in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, b'0000000000000000')

    with open(input_file, 'rb') as infile:
        with open(output_file, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                # Decrypt the chunk using the AES cipher
                outfile.write(cipher.decrypt(chunk))

            outfile.truncate(filesize)

def ToZip(file_path, output_path=None):
    """
    Decrypts an EZ file and extracts its contents to a zip file.

    Args:
    - file_path (str): Path to the input EZ file.
    - object_name (str): Name of the object.
    - output_path (str): Path to the directory where the contents will be extracted.
    """
    
    directory = os.path.dirname(file_path)
    filename = os.path.splitext(os.path.basename(file_path))[0]    
    
    output_path += '/' + filename + '/' + filename + '.zip'  
    if output_path and not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
    
    # Open the decrypted zip file and extract its contents
    with ZipFile(output_path, 'r') as zf:
        zf.extractall(os.path.dirname(output_path))
