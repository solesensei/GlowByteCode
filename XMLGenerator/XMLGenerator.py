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

# --------- pattern file ----------- #
file = 'pattern.xml'
# ------------ variables ----------- #
app_id = 'SERV-TEST-NEW-XSD'
client_id = 'test_client_id'
request_type = 'SGCheck'
inn_size = [10, 12]
app_dt = '2018-04-07T03:40:35Z'
service_extra_info = 'Generated with XMLGenerator.py v1.0' 
# ----------- parametrs ----------- #
apps_number = 10
start_from = 1

def create_num_size(size):
    rand.seed(datetime.now())
    inn = ''
    size = rand.choice(size) 
    for i in range(size):
        a = rand.randint(0,9)
        inn += str(a)
    return inn


def get_app_name(i):
    return app_id + '-' + str(i)


def add_header(header, filename, i):
    with open(filename, 'r+') as f:
            content = f.readlines()
            content[0] = header
            f.seek(0,0)
            f.write('<!-- Generated with XMLGenerator.py v1.0 | ' + get_app_name(i) + ' -->\n')
            f.writelines(content)


def modify(f, n):
    tree = ET.parse(file)
    root = tree.getroot()
    for child in root.findall('Application'):
        for field in child:
            if field.tag == 'App_ID':
                field.text = get_app_name(n)
            if field.tag == 'INN':
                field.text = create_num_size(inn_size)
            if field.tag == 'Client_ID':
                field.text = client_id
            if field.tag == 'App_DT':
                field.text = app_dt
            if field.tag == 'Service_Extra_Info':
                field.text = service_extra_info
    tree.write(f)


def generator(header):
    print('Starting generator!')
    print('Number of apps:', apps_number)
    print('Starts from:', start_from)
    if not path.isdir('./apps'):
        mkdir('./apps')
    if not path.isdir(f'./apps/{app_id}'):
        mkdir(f'./apps/{app_id}')
    for i in range(start_from, start_from+apps_number):
        print(f'{i*100//apps_number}% processed', end='\r')
        filename = f'./apps/{app_id}/{get_app_name(i)}.xml'
        modify(filename, i)
        add_header(header, filename, i)
    print(f'Finished! Apps created in ./apps/{app_id}' )


def main():
    header = ''
    if not path.exists(file):
        print('No pattern file exist!')
        print('Create one app by hands: pattern.xml')
        exit(1)
    start_cleaning('./database/export-base.csv')
    inn_list = get_company_inn('./database/export-base.csv')
    with open(file, 'r') as f:
        header = f.readline()
    generator(header)

if __name__ == ('__main__'):
    main()
