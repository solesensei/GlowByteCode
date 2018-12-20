# 
# Tiny tool for fast recursive files encoding 
# by Sole
import os
from chardet import detect

# --------- Variables ---------
path = ''
ext = ''
force_encode = False
default_codec = 'windows-1251'
# -----------------------------

start_log_line = '-------------- start processing --------------'

def to_log(*text):
    print(*text)
    with open('log.txt', 'a') as log:
        print(*text, file=log)

def print_log():
    print('Errors log:')
    with open('log.txt', 'r') as log:
        text = log.readlines()
    last_count = sum(1 for line in text if line.strip() == start_log_line)
    count = 0
    for line in text:
        line = line.strip()
        if line == start_log_line:
            count += 1
        if count >= last_count:
            print(line)
        

def get_encoding_type(file):
    with open(file, 'rb') as f:
        rawdata = f.read()
    return detect(rawdata)['encoding']

def encode(path, tocodec):
    fromcodec = get_encoding_type(path)
    
    if fromcodec == tocodec:
        print(f"Already {tocodec}: {path}")
        if not force_encode:
            return
            
    # fix error detections (RU region)
    if fromcodec not in ('windows-1251', 'ascii') and fromcodec.lower().find('utf') == -1: 
        to_log('Possible Detect dismiss: ' + fromcodec + ' in ' +  path)
        if not force_encode:
            to_log('Try default:', default_codec)
            fromcodec = default_codec
        else:
            to_log('Force encode:', fromcodec)
    
    print(f"Convert from {fromcodec} to {tocodec}: {path}")
    tmp_file = 'text.txt'
    try:
        with open(path, 'r', encoding=fromcodec) as f, open(tmp_file, 'w', encoding=tocodec) as e:
            text = f.read()
            e.write(text)
        os.remove(path)
        os.rename(tmp_file, path) 
    except UnicodeDecodeError:
        to_log(f'[{fromcodec}] → [{tocodec}] - Decoding Error: {path}')
    except UnicodeEncodeError:
        to_log(f'[{fromcodec}] → [{tocodec}] - Encoding Error: {path}')

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


to_log(start_log_line)

if not path:
    path = input('Enter path for directory: ')

if not ext:
    ext = input('Enter file extension: ')
    if ext == 'any' or ext == 'all':
        ext = 'any'
    elif ext[0] != '.':
        ext = '.' + ext

# Change Encoding
change_encoding(path, ext)

# Print Errors
print_log()
