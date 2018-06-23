'''
Created on 9 Sep 2017

@author: kylefarinas_Main
'''
#OS
import os
from os import chdir, listdir, stat
from pathlib  import Path
#HTTP
import httplib2
#PYDRIVE
import pydrive as drive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import GoogleDriveFile
#GOOGLEAPI
import googleapiclient
from googleapiclient import discovery
from googleapiclient import errors
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
#GSPREAD
import gspread
from gspread import utils
from gspread import Spreadsheet
from gspread import Worksheet
from gspread.exceptions import SpreadsheetNotFound

#GLOBALSTART
try:
    import argparse
    flags = argparse.ArgumentParser(parents = [tools.argparser]).parse_args()
except ImportError:
    flags = None

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.install']
CLIENT_SECRET_FILE = 'client_secrets.json'
APPLICATION_NAME = 'Google Drive Auditing System by KFPy'
JSONS = ['drive-python-quickstart.json', 'sheets.googleapis.com-python-quickstart.json']
#GLOBALEND

###FUNCTIONS###

#GET CREDENTIALS START
def get_credentials():
    home_dir = os.path.expanduser('~')
    cred_dir = os.path.join(home_dir, 'credentials')
    
    if not os.path.exists(cred_dir):
        os.makedirs(cred_dir)
    
    for qs in JSONS:
        cred_path = os.path.join(cred_dir, qs)
    
    store = Storage(cred_path)
    cred = store.get()
    
    if not cred or cred.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agenr = APPLICATION_NAME
        if flags:
            cred = tools.run_flow(flow, store, flags)
        else:
            cred = tools.run_flow(flow, store)
        print('Storing credentials to ' + cred_path)
    return cred
#GET CREDENTIALS END

#LIST DRIVE FILES GLOBAL
arr = []
arr2 = []
filelist = []
check = 0
ax = "root"
#LIST DRIVE FILES START
def listDriveFiles(root, ax):
    fList = drive.ListFile({'q': "'%s' in parents and trashed=false" % root}).GetList()
    
    for f in fList:
        p = f['title']
        if f['mimeType'] == 'application/vnd.google-apps.folder':
            print("Folder: %s" % p)
            ax = ax + "> %s >" %p
            filelist.append('%s|%s|%s|%s|%s|%s|%s' % (f['createdDate'], f['modifiedDate'], f['title'], f['mimeType'], f['alternateLink'], ax , f['ownerNames']))
            listDriveFiles(f['id'], f['title'])
        else:
            print(p)
            ax = ax + "> %s " %p
            arr.append("%s" %(ax))
            filelist.append('%s|%s|%s|%s|%s|%s|%s' % (f['createdDate'], f['modifiedDate'], f['title'], f['mimeType'], f['alternateLink'], ax , f['ownerNames']))

#LIST DRIVE FILES END

#PROCESS CSV GLOBAL
arrFiles = []
#TO CSV START

def toCSV():
    text_file = open("aupy.csv", "w")
    for i in filelist:
        text_file.write("%s \n " %i.encode('utf-8'))
    text_file.close()

def processCSV():
    #desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\aupy.csv')
    tf = open("aupy.csv", "r")
    lines = tf.read().split('\n')
    for j in lines:
        arrFiles.append(j.split('|'))
#TO CSV END

#TO SHEETS START
def toSheets(gc):
    try:
        sh = gc.open('Google Drive Auditing System by KFPy')
    except SpreadsheetNotFound:
        sh = gc.create('Google Drive Auditing System by KFPy')
    #sh = gc.create('AUPY')
    print("opened Google Drive Auditing System by KFPy")
    wks = sh.sheet1
    print("opened Sheet 1")
   
    ccount = 1
    rcount = 1

    for i in arrFiles:
        for j in i:
            wks.update_cell(ccount, rcount, '%s' %j)
            rcount += 1
        ccount += 1
        rcount = 1
#TO SHEETS END

#MAIN FUNCTION GLOBAL
lidir = []
#MAIN FUNCTION START
def main():
    print('#MAIN START')

    cred = get_credentials()
    http = cred.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http = http)
    
    listDriveFiles('root', ax)
    print("#FILES APPENDED")
    toCSV()
    processCSV()
    print("#CSV Processed")
    gc = gspread.authorize(cred)
    toSheets(gc)
    print("#SHEETS Processed")
    print('#MAIN END')
#MAIN FUNCTION END 
    

#MAINSTART
if __name__ == '__main__':
    main()
#MAINEND
