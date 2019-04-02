# 
# Tiny tool for fast recursive files encoding 
# by Sole
import os
import html
from chardet import detect

# --------- Variables ---------
__ue_path__ = ''
__ue_ext__ = ''
# -----------------------------
__start_log_line__ = '-------------- start processing --------------'


def to_log(*text):
    """ Logging `text` to `log.txt` file """
    print(*text)
    with open('log.txt', 'a') as log:
        print(*text, file=log)


def print_log():
    """ Printing `log.txt` """
    print('Errors log:')
    with open('log.txt', 'r') as log:
        text = log.readlines()
    last_count = sum(1 for line in text if line.strip() == __start_log_line__)
    count = 0
    for line in text:
        line = line.strip()
        if line == __start_log_line__:
            count += 1
        if count >= last_count:
            print(line)
        

def get_encoding_type(file):
    """ Detect `file` encoding codec """ 
    with open(file, 'rb') as f:
        rawdata = f.read()
    return detect(rawdata)['encoding']


def encode(path, tocodec, default_codec='windows-1251', unescape=False, force_encode=False):
    """ Change encoding codec from source to target
        --
        path : str - path to file \n
        tocodec : str - target codec to encode \n
        default_codec : str - try this codec as source if error detection
        unescape : bool - fix ascii html codes
        force_encode : bool - force encode if input codec matches output and if possible detection error 
    """
    fromcodec = get_encoding_type(path)
    
    if fromcodec == tocodec:
        print(f"Already {tocodec}: {path}")
        if not force_encode and not unescape:
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
            if unescape:
                text = html.unescape(text)
            e.write(text)
        os.remove(path)
        os.rename(tmp_file, path) 
    except UnicodeDecodeError:
        to_log(f'[{fromcodec}] → [{tocodec}] - Decoding Error: {path}')
    except UnicodeEncodeError:
        to_log(f'[{fromcodec}] → [{tocodec}] - Encoding Error: {path}')
    print(f'Converted!')


def change_encoding(path, ext='any', codec='utf-8'):
    """ Recursively encoding files in directory 
        --
        path : str - directory path to process \n
        ext : str - file extension to process, *any* for insensitivity to file extensions
    """
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


def main():
    path = __ue_path__
    if not path:
        path = input('Enter path for directory: ')

    ext = __ue_ext__
    if not ext:
        ext = input('Enter file extension: ')
        if ext == 'any' or ext == 'all':
            ext = 'any'
        elif ext[0] != '.':
            ext = '.' + ext
    
    # Loging start line
    to_log(__start_log_line__)

    # Change Encoding
    change_encoding(path, ext)

    # Print Errors
    print_log()


if __name__ == "__main__":
    main()
