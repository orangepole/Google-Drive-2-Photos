#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Script Name	: drive2photos.py
# Author		: Jagadeesan
# Author Email	: myscoreisone@gmail.com
# Created		: April 2016
# Version		: 1.0
# Description	: Online transfer of images from google drive to google photos


import httplib2
import os
import sys
import io

import oauth2client
from oauth2client import client
from oauth2client import tools

from apiclient import errors
from apiclient import discovery
from apiclient.http import MediaIoBaseDownload

import requests
import json
import time

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


''' --------------------------------------
####            GOOGLE DRIVE              ###
    --------------------------------------'''


SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'GOOGLE : Drive to Photos'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    credential_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,'drive-to-photos.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print 'Storing credentials to ' + credential_path
    return credentials

''' ---------------------------------------
####            GOOGLE PHOTOS              ###
    ---------------------------------------'''
h1 = { "Host":" photos.google.com","User-Agent":" Mozilla/5.0 (Windows NT 10.0; rv:44.0) Gecko/20100101 Firefox/44.0","Accept":" text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language":" en-US,en;q=0.5","Accept-Encoding":" gzip, deflate, br","DNT":" 1","Referer":" https://photos.google.com","Cookie":"","Connection":" keep-alive","X-GUploader-Client-Info": "","Content-Type": "application/x-www-form-urlencoded;charset=utf-8" }
h2 = { "Host":" photos.google.com","User-Agent":" Mozilla/5.0 (Windows NT 10.0; rv:44.0) Gecko/20100101 Firefox/44.0","Accept":" text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language":" en-US,en;q=0.5","Accept-Encoding":" gzip, deflate, br","DNT":" 1","Referer":" https://photos.google.com","Cookie":"","Connection":" keep-alive" ,"X-HTTP-Method-Override":" PUT","Content-Type":" application/octet-stream","X-GUploader-No-308":" yes"}

global p1
p1='{"protocolVersion":"0.8","createSessionRequest":{"fields":[{"external":{"name":"file","filename":"=====","put":{},"size":@@@@@}},{"inlined":{"name":"auto_create_album","content":"camera_sync.active","contentType":"text/plain"}},{"inlined":{"name":"auto_downsize","content":"true","contentType":"text/plain"}},{"inlined":{"name":"storage_policy","content":"use_manual_setting","contentType":"text/plain"}},{"inlined":{"name":"disable_asbe_notification","content":"true","contentType":"text/plain"}},{"inlined":{"name":"client","content":"photosweb","contentType":"text/plain"}},{"inlined":{"name":"effective_id","content":"?????","contentType":"text/plain"}},{"inlined":{"name":"owner_name","content":"?????","contentType":"text/plain"}},{"inlined":{"name":"timestamp_ms","content":"+++++","contentType":"text/plain"}}]}}'

global count
count = 1

def upload_initialise():  
    
    INPUTfile = os.path.join(os.path.dirname(os.path.abspath(__file__)),'INPUT.json')
    
    if os.path.exists(INPUTfile):
        with open(INPUTfile,'r') as file :
            inputs = json.loads(file.read())    
        if not inputs['Cookie'] or not inputs['X-GUploader-Client-Info'] or not inputs['effective_id'] :
            print "Enter all required details in INPUT.json file"
            print "and re run the program\n"
            print "Refer ReadMe for help.\nProgram now terminates"
            print " ----------------------------------------------------------"
            raise SystemExit
        else :
            h1['Cookie']                    = inputs['Cookie']
            h1['X-GUploader-Client-Info']   = inputs['X-GUploader-Client-Info']
            global p1 
            p1= p1.replace('?????',inputs['effective_id'])


def banner1():
    print """                       
                         *(                
                         *(((              
                         *(((((            
                         *(((((((          
                *********/(((((((((        
              ,,,,*******/(((((((%%        
            ,,,,,,,,*****/(((((%%%%        
          ,,,,,,,,,,,,*** (((%%%%%%        
        ,,,,,,,,,,,,,,,,   %%%%%%%%        
                ((((((((   ((((((((((((((((
                ((((((/** ###((((((((((((  
                ((((/****/#####((((((((    
                ((/******/#######((((      
                /********/########(        
                  *******.                 
                    *****.                 
                      ***.                 """
def banner2():

    print " =========================================================="
    print "                 Drive to Photos Uploader                 "
    print " ----------------------------------------------------------"
    print ' %s | %s | %s | %s '%('s.no'.ljust(5),'Filename'.ljust(30),'Size'.ljust(7),'Status'.ljust(12))
    print " =========================================================="
                

def main():
    banner1()
    try:
        upload_initialise()

        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('drive', 'v3', http=http)
        banner2()

        page_token = None
        while True:
            try:
                param = {"orderBy":"recency desc","pageSize":1000,"fields":"nextPageToken, files(fullFileExtension,id,name,size)"}
                if page_token:
                    param['pageToken'] = page_token
                
                results = service.files().list(**param).execute()
                items = results.get('files', [])
                if not items:
                    print 'End of File List'
                else:
                    for item in items:
						getPhotosfromDrive(item,service)
                
                page_token = results.get('nextPageToken')
                if not page_token:
                    break
            except errors.HttpError, error:
                print 'An error occurred: %s' % error
                break
    except KeyboardInterrupt:
        print "\n"
        print " ----------------------------------------------------------"
        print "       CAUGHT KILL SIGNAL . TERMINATING GRACEFULLY         "
        print " ----------------------------------------------------------"
        sys.exit(1)

    print "\n"
    print " ----------------------------------------------------------"
    print "          ALL FILES UPLOADED . PEACE OF MIND               "
    print " ----------------------------------------------------------"
    sys.exit(0)

def getPhotosfromDrive(item,service):
    
    fileID   = item['id']
    filename = item['name'].strip('')
    size     = item['size']
    filetype = item['fullFileExtension']

    if filetype == 'jpg' or 'png':
        if size >= 100000:
            request = service.files().get_media(fileId=fileID)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                #print "Downloading  %d%%." %(int(status.progress() * 100))
            
            MoveToGphotos(filename,size,fh.getvalue())
            # To save image to Disk
            #with open(filename,'wb') as file:
                #file.write(fh.getvalue())

def MoveToGphotos(filename,size,content):
    global count

    timestamp_ms = int(time.time() * 1000)
    p = p1 # MAKES A COPY SO AS NOT TO DISTURB THROUGHT ITERATION OF EACH OBJECT
    p = p.replace('=====',filename)
    p = p.replace('@@@@@',str(size))
    p = p.replace('+++++',str(timestamp_ms))
    
    p2 = content
    up = 1
    if up == 1:
        u1 = "https://photos.google.com/_/upload/photos/resumable?authuser=0"
        # Initial Request to get the Upload - ID from google
        r  = requests.post(u1,headers=h1,data=p)
        print ' %s | %s | %s |'%((str(count).zfill(3)).ljust(5),filename.ljust(30),str(size).ljust(7)),
        count=count + 1
        
        try :
            u2 = json.loads(r.content)['sessionStatus']['externalFieldTransfers'][0]['putInfo']['url']
            r2 = requests.post(u2,headers=h2,data=p2)
            status = json.loads(r2.content)['sessionStatus']['state']
            if status == 'FINALIZED' :
                print '%s'%('SUCCESS'.ljust(12))
                
            else:
                print '%s'%('FAILED'.ljust(12))
        except KeyError:
            print "Google Photos Authentication Error\n\
            Check the Values added in th INPUT.json file\n\
            and run the program again"

          
if __name__ == '__main__':
    main()
    
    