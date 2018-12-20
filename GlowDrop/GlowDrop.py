"""
GlowDrop.py
Script for sending files to strict firewall locations via GlowByte Network
Author: Goncharenko Dmitriy
"""
import requests
import smtplib
import getpass
import os
import sys
import yaml
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep

# --------------- GBC URL ---------------
base_url = 'https://wiki.glowbyteconsulting.com'
url = base_url + '/rest/api/content/110496705/child/attachment'
headers = {"X-Atlassian-Token": "nocheck"}


def usage():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', metavar='file', type=str, help='specified file sending to GBC')
    parser.add_argument('-g', metavar='file', nargs='?', help='download file from GBC. Get last file if not specified', const=True)
    parser.add_argument('-e', '--email', help='send email', action='store_true')
    parser.add_argument('-c', metavar='config', help='config file', default='config.yaml')
    parser.add_argument('--make_conf', help='create config file template', action='store_true')
    parser.add_argument('--about', help='about author', action='store_true')
    return parser.parse_args()

def soft_exit(code=0):
    input('Press any key to exit...')
    sys.exit(code)

def create_template_conf(config):
    if os.path.exists(config):
        print(config, 'file already exists')
        soft_exit(0)
    
    print('Creating config template...')
    with open(config, 'w') as conf:
        conf.write('# Config file for GlowDrop.py \n')
        conf.write('# ----------------------------------- # \n')
        conf.write('# if all specified - no need arguments provide # \n\n')
        conf.write('# ---------- Required args ---------- #\n')
        conf.write('gbc_username: \'YOUR GBC USERNAME\' # exm: name:surname \n\n')
        conf.write('# ---------- Optional args ---------- #\n')
        conf.write('gbc_pass: \'YOUR GBC PASSWORD\' \n')
        conf.write('email_from: \'YOUR EMAIL\' # Not working with GBC, you can set forward if you want\n')
        conf.write('email_pass: \'YOUR EMAIL PASSWORD\' \n')
        conf.write('email_to: \'EMAIL TO SEND DOWNLOAD LINK\' \n\n')
        conf.write('# --------- Additional args --------- # \n')
        conf.write('send_file: \'PATH TO FILE TO SEND\' \n')
        conf.write('get_file: \'FILE NAME TO DOWNLOAD FROM GBC\' # specifie \'LAST\' for last file download \n')
        conf.write('email: \'True\' # \'True\' | \'False\' to send message \n')
    print('Created config template', config)

def get_config(config):
    if not os.path.exists(config):
        print('No config file', config, 'found!')
        r = input('Create template config [y|n]')
        if r == 'y':
            create_template_conf(config)
        soft_exit(1)

    with open(config, 'r') as stream:
        return yaml.load(stream)
    
args = usage()

if args.about:
    print('GlowDrop.py v1.0')
    print('Script for sending files to strict firewall locations via GlowByte Network')
    print('Author: Goncharenko Dmitriy')
    soft_exit(0)

if args.make_conf:
    create_template_conf(args.c)
    soft_exit(0)

config = get_config(args.c)

if args.email:
    subject = 'GlowDrop.py | Download Link'
    try:
        emailto = config['email_to']
    except:
        print('No email_to: specified in', config, 'file!')
        soft_exit(1)

args.s = config['send_file'] if not args.s and 'send_file' in config.keys() else args.s
args.g = config['get_file'] if not args.g and 'get_file' in config.keys() else args.g
args.email = config['email'] if not args.email and 'email' in config.keys() else args.email

if args.email or args.g or args.s:
    try:
        username = config['gbc_username']
    except:
        print('No gbc_username: specified in', config, 'file!')
        soft_exit(1)

    try:
        password = config['gbc_pass']
    except:
        password = getpass.getpass('Enter your ' +  username + '@glowbyteconsulting.com password: ')
else:
    print('No options specified: use --help option for more information...')
    soft_exit(0)

if args.email:
    if 'email_from' in config.keys():
        emailme = config['email_from']
    else:
        emailme = input('Enter your email: ')
    if 'email_pass' in config.keys():
        epass = config['email_pass']
    else:
        epass = getpass.getpass('Enter your ' +  emailme + ' password: ')

if args.s:
    if os.path.exists(args.s):
        print('Sending file', args.s)
        files = {'file' : open(args.s, 'rb')}
        send = requests.post(url, auth=(username, password), headers=headers, files=files)
        print ('Sended!' if send.status_code == 200 else send.text + str(send.status_code))
    else:
        print('Error: No \'' + args.s + '\' file found!')
        soft_exit(1)

if args.g:
    print('Downloading', 'last' if args.g == True else args.g, 'file to download/')

    if not os.path.isdir('download/'):
        os.mkdir('download/')
    
    read = requests.get(url, auth=(username, password), headers=headers)
    print ('Got attach page!' if read.status_code == 200 else read.text + str(read.status_code))

    i = 0
    if not args.g == True:
        found_flg = False
        last_page = False
        while not last_page and not found_flg:
            for i, name in enumerate(read.json()['results']):
                if args.g.upper() == name['title'].upper():
                    found_flg = True
                    break
            if not found_flg:
                try:
                    url = base_url + read.json()['_links']['next']
                    read = requests.get(url, auth=(username, password), headers=headers)
                    print('Got next attach page')
                except:
                    last_page = True
        if not found_flg:
            print('No found', args.g, 'in GBC attachments. Check name and try again')
            soft_exit(1)

    download_url = base_url + read.json()['results'][i]['_links']['download']
    local_filename =  read.json()['results'][i]['title']
    print('Downloading file:', local_filename)
    d = requests.get(download_url, auth=(username, password), headers=headers)
    print ('Downloaded file download/' + local_filename + '!' if d.status_code == 200 else d.text + str(d.status_code))

    with open('./download/'  + local_filename, 'wb') as f:
        f.write(d.content)

if args.email:
    print('Sending email to', emailto)
    read = requests.get(url, auth=(username, password), headers=headers)
    print ('Got attach page' if read.status_code == 200 else read.text + str(read.status_code))

    download_url = base_url + read.json()['results'][0]['_links']['download']

    msg = MIMEMultipart()
    msg['From'] = emailme
    msg['To'] = emailto
    msg['Subject'] = subject
    
    body = download_url
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(emailme, epass)
        server.sendmail(emailme, emailto, msg.as_string())
    except:
        print('Email auth error: go to https://stackabuse.com/how-to-send-emails-with-gmail-using-python/')
    
    print('Sent!')
    server.quit()


print('Completed!')
soft_exit(0)
