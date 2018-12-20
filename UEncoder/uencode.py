# 
# Tiny tool for fast recursive files encoding 
# by Sole
import os
from chardet import detect

# --------- Variables ---------
path = ''
ext = ''
# -----------------------------

with open('log.txt', 'a') as log:
    print('--------------', file=log)

def get_encoding_type(file):
    with open(file, 'rb') as f:
        rawdata = f.read()
    return detect(rawdata)['encoding']

def encode(path, tocodec):
    fromcodec = get_encoding_type(path)
    if fromcodec == 'MacCyrillic': fromcodec = 'windows-1251' # fix error detections
    if fromcodec == tocodec :
        print(f"Already {tocodec}: {path}")
        return
    print(f"Convert from {fromcodec} to {tocodec}: {path}")
    tmp_file = 'text.txt'
    try:
        with open(path, 'r', encoding=fromcodec) as f, open(tmp_file, 'w', encoding=tocodec) as e:
            text = f.read()
            e.write(text)
        os.remove(path)
        os.rename(tmp_file, path) 
    except UnicodeDecodeError:
        with open('log.txt', 'a') as log:
            print(f'[{fromcodec}] → [{tocodec}] - Decoding Error: {path}', file=log)
    except UnicodeEncodeError:
        with open('log.txt', 'a') as log:
            print(f'[{fromcodec}] → [{tocodec}] - Encoding Error: {path}', file=log)

def change_encoding(path, ext='any', codec='utf-8'):
    if not os.path.exists(path):
        print(f'No {path} found!')
        exit(0)
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d[0] != '.']
            dirname = root[root.rfind('\\')+1:]
            print('-' * 100)
            print(f"Process directory: {dirname}")
            print('-' * 100)
            for file in files:
                if ext == 'any' or file.rfind(ext) != -1:
                    file = os.path.join(root, file)
                    encode(file, codec)
    else:
        encode(path, codec)
    print('Converted!')


if not path:
    path = input('Enter path for directory: ')

if not ext:
    ext = input('Enter file extension: ')
    if ext[0] != '.':
        ext = '.' + ext

change_encoding(path, ext)
