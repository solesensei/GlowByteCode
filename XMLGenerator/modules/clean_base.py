"""
Tool for cleaning csv from export-base
"""
import csv
from os.path import exists

def start_cleaning(datapath, delimiter=';', quotechar='"'):
    """
        Returns filename of clean version of input base

        base : str - path to base.csv
    """
    if not exists(datapath):
        print(f"Base path: {datapath} doesn't exists!")
        exit(0)
    with open(datapath, 'r') as csvfile, open('clean_base.txt', 'w') as clean:
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
        set_width={}
        for first_row in reader:
            for i, f in enumerate(first_row):
                set_width[i] = len(f)
            break
        for row in reader:
            for i, f in enumerate(row):
                if set_width[i] < len(f):
                    set_width[i] = len(f)
        csvfile.seek(0,0)
        for row in reader:
            print(file=clean)
            for i, field in enumerate(row):
                print('{:<{width}}'.format(field, width=set_width[i]), end=' | ', file=clean)
    print("Cleaned! Saved to clean_base.txt")
    return 'clean_base.txt'
