#
# XML Generator - small tool to generate xml from template
# 
# XSD to XML (http://xsd2xml.com/)
#

import xml.etree.ElementTree as ET
import random as rand
from datetime import datetime
from os import path, mkdir
from modules.clean_base import start_cleaning
from modules.inn import get_company_inn

__ver__ = 'v1.1' 

# -------- database file ----------- #
database = './database/export-base.csv'
# --------- pattern file ----------- #
pattern_path = 'pattern.xml'
# ------------ variables ----------- #
app_id = 'SERV-TEST-XSD'
client_id = 'test_client_id'
request_type = 'SGCheck'
inn_size = [10, 12]
app_dt = '2018-04-07T03:40:35Z'
service_extra_info = 'Generated with XMLGenerator.py ' + __ver__
# ----------- parametrs ----------- #
apps_number = 100
start_from = 1

def create_num_size(size):
    """ Creating number with random `size` of random digits 
        --
        size : list - list of sizes, get one randomly
    """
    rand.seed(datetime.now())
    num = ''
    size = rand.choice(size) 
    for _ in range(size):
        a = rand.randint(0,9)
        num += str(a)
    return num


def get_app_name(i):
    """ Get concatenation of `app_id` and `i` """
    return app_id + '-' + str(i)


def get_header(file):
    """ Get first line of the `file` """
    with open(file, 'r') as f:
        return f.readline()


def add_header(header, filename, i):
    """ Insert `header` to top of the `filename` """
    with open(filename, 'r+') as f:
            content = f.readlines()
            content[0] = header
            f.seek(0,0)
            f.write(f'<!-- Generated with XMLGenerator.py {__ver__} | {get_app_name(i)} -->\n')
            f.writelines(content)


def modify(f, n, pattern, inn):
    """ Changing pattern to create new xml """
    tree = ET.parse(pattern)
    root = tree.getroot()
    for child in root.findall('Application'):
        for field in child:
            if field.tag == 'App_ID':
                field.text = get_app_name(n)
            if field.tag == 'INN':
                field.text = inn
            if field.tag == 'Client_ID':
                field.text = client_id
            if field.tag == 'Request_Type':
                field.text = request_type
            if field.tag == 'App_DT':
                field.text = app_dt
            if field.tag == 'Service_Extra_Info':
                field.text = service_extra_info
    tree.write(f)


def start_generation(pattern, data):
    """ Input function where generation begins """
    print('XML Generation starts!')
    print('Number of apps:', apps_number)
    print('Starts from:', start_from)
    # Creating apps folders
    if not path.isdir('./apps'):
        mkdir('./apps')
    if not path.isdir(f'./apps/{app_id}'):
        mkdir(f'./apps/{app_id}')

    # Get first line of file
    header = get_header(pattern)
    inn_list = []
    if data:
        inn_list = get_company_inn(data)

    for i in range(start_from, start_from+apps_number):
        print(f'{i*100//apps_number}% processed', end='\r')
        
        filename = f'./apps/{app_id}/{get_app_name(i)}.xml'
        # if no inns from database then generate random
        if len(inn_list) == 0:
            inn = create_num_size(inn_size)
        else:
            inn = inn_list[(i - start_from) % len(inn_list)]

        modify(filename, i, pattern, inn)
        
        add_header(header, filename, i)
    
    print(f'Finished! Apps created in ./apps/{app_id}' )


def main():
    if not path.exists(pattern_path):
        print('No pattern file exist!')
        print('Create one app by hands: pattern.xml')
        exit(1)

    if database:
        start_cleaning(database)

    start_generation(pattern_path, database)

if __name__ == ('__main__'):
    main()
