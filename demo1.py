from __future__ import print_function

from googleapiclient import discovery
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from httplib2 import Http
from oauth2client import file, client, tools
from oauth2client.tools import argparser, run_flow
import io
# args = argparser.parse_args()
# args.noauth_local_webserver = True
# credentials = run_flow(flow, storage, args)
def service():
    SCOPES = 'https://www.googleapis.com/auth/drive'
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))
    return DRIVE

service_ = service()
def get_files():
    files = service_.files().list().execute().get('files', [])
    for f in files:
        print(f)
        print(f['name'], f['mimeType'])

# get_files()
def upload_file( file_name, file_path, mimetype):
    file_metadata = {'name': file_name}
    file_metadata['parents'] = ['1ddxaGfU18Yuy4fkt8XoVWWugpR-4riWi']
    #https://drive.google.com/open?id=1ddxaGfU18Yuy4fkt8XoVWWugpR-4riWi
    media = MediaFileUpload(file_path,
                            mimetype=mimetype)
    file = service_.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()

    print('File ID: %s' % file.get('id'))


upload_file('xjpic.jpeg','xjpic.jpeg', 'image/jpeg')


def dowm_load(file_id):
    # file_id = '0BwwA4oUTeiV1UVNwOHItT0xfa2M'
    request = service_.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with open("aa.jpg","wb") as f:
        fh.seek(0)
        f.write(fh.read())
# dowm_load('1EOqiL2V67lVLrILYUH4bGGfMj7-nHah9')


import requests

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            print(value)
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    print(response)
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

# if __name__ == "__main__":
#
#     # file_id = '1EOqiL2V67lVLrILYUH4bGGfMj7-nHah9'
#     # destination = 'aa1.jpg'
#     # download_file_from_google_drive(file_id, destination)
#     chunk = requests.get('https://drive.google.com/uc?export=download&id=1EOqiL2V67lVLrILYUH4bGGfMj7-nHah9')
#     print(chunk)
#     with open("aa1.jpg", "wb") as f:
#             f.write(chunk.content)