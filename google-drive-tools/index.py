from __future__ import print_function
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from httplib2 import Http
from oauth2client import file, client, tools
import os, io
import subprocess
import platform

try:
    from tkinter import *
except:
    from Tkinter import *

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'

def downloadFile(downloadLocation, filename, autoOpen=False):
    """Download specified file inside my google drive account to the specified working directory
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    # use contains instead of = to allow user don't specify file extention 
    queryString = """name contains '{0}'""".format(filename)
    request = service.files().list(pageSize=10, fields="*" ,q=queryString)
    results = request.execute()
    items = results.get('files', [])
    if len(items) == 0:
        print('no such file')
    elif len(items) > 1:
        print('more than 1 such file')
    else:
        fullname = items[0]['name']
        file_id = items[0]['id']
        mime_type = items[0]['mimeType']
        targeLocation = os.path.join(downloadLocation, fullname)
        #print(fullname)
        #print(downloadPath)
        request = service.files().get_media(fileId=file_id)
        fh = io.FileIO(targeLocation, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        if done:
            fh.close()
            if autoOpen:
                if platform.system() == 'Mac':
                    subprocess.call(['open', targeLocation], shell=True)
                elif platform.system() == 'Windows':
                    subprocess.call(['start', targeLocation], shell=True)

class MyFirstGUI:
    def __init__(self, master):
        self.autoOpen = False
        self.master = master
        master.title("Download file from Google Drive")
        self.locationLabel = Label(master, text="Download Location")
        self.locationLabel.pack()
        self.location = Text(master, height="2", width="100")
        self.location.pack()
        self.label = Label(master, text="Filename")
        self.label.pack()
        self.text = Text(master, height="2", width="100")
        self.text.pack()
        self.download_button = Button(master, text="Download", command=self.download)
        self.download_button.pack()
        self.autoOpenLabel = Label(master, text="auto open after download?")
        self.autoOpenLabel.pack()
        self.autoOpen = Checkbutton(master, variable=self.autoOpen)
        self.autoOpen.pack()
        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def download(self):
        # use tkinter index system to get whole text content
        filename = self.text.get('1.0', 'end-1c')
        downloadLocation = self.location.get('1.0', 'end-1c')
        # print("text:"+filename+":")
        try:
            downloadFile(downloadLocation, filename, self.autoOpen)
        except err:
            print("Download failed. Please check network, authentication and permission and try again")

if __name__ == '__main__':
    root = Tk()
    my_gui = MyFirstGUI(root)
    root.mainloop()