"""
Module to get inn from database
"""
import csv
from os.path import exists

def get_company_inn(datapath, delimiter=';', quotechar='"'):
    """
    Returns 'INN' list from database
    ----
    datapath : str - path to database with 'INN' column
    """ 
    if not exists(2):
        print(f"Base path: {datapath} doesn't exists!")
        exit(0)
    with open(datapath, 'r') as base:
        reader = csv.reader(base, delimiter=delimiter, quotechar=quotechar)
        inn_column_num = -1
        inn_list = []
        for first_row in reader:
            for i, f in enumerate(first_row):
                if f.strip().upper() in ('ИНН', 'INN'):
                    inn_column_num = i
                    break
            break
        for row in reader:
            inn = row[inn_column_num]
            if inn:
                if ', ' in inn:
                    inn_list += inn.split(', ') 
                else:
                    inn_list.append(inn)
        print(f'Parsed {len(inn_list)} INNs!')
        return inn_list
