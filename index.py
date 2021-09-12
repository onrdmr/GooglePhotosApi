from pprint import pprint
from init_photo_service import service
import pandas as pd
import sys

# wget envden sslinecek
#import wget
# urlib extra ahve renaming option wget is exception thowing big named file
from urllib import request

import os

def response_media_items_by_filter(request_body: dict):
    try:
        response_search = service.mediaItems().search(body=request_body).execute()
        lstMediaItems = response_search.get('mediaItems')
        nextPageToken = response_search.get('nextPageToken')

        while nextPageToken:
            request_body['pageToken'] = nextPageToken
            response_search = service.mediaItems().search(body=request_body).execute()

            if not response_search.get('mediaItem') is None:
                lstMediaItems.extend(response_search.get('mediaItems'))
                nextPageToken = response_search.get('nextPageToken')
            else:
                nextPageToken = ''
        return lstMediaItems
    except Exception as e:
        print(e)
        return None


"""
search method (by date)
"""

print("arg count is " + str(len(sys.argv)))
print("link to this file path is " + sys.argv[0])

if len(sys.argv) > 1:
    request_body = {
        'pageSize': 100,
        'filters': {
            'dateFilter': {
                 'ranges': [
                     {
                         'startDate': {
                             'year': sys.argv[3],
                             'month': sys.argv[2],
                             'day': sys.argv[1]
                         },
                         'endDate': {
                             'year': sys.argv[6],
                             'month': sys.argv[5],
                             'day': sys.argv[4]
                         }
                     }
                 ]


            }
        }
    }


"""
list method
"""
response = service.mediaItems().list(pageSize=25).execute()

lst_medias = response.get('mediaItems')
nextPageToken = response.get('nextPageToken')

while nextPageToken:
    response = service.mediaItems().list(
        pageSize=25,
        pageToken=nextPageToken
    ).execute()

    lst_medias.extend(response.get('mediaItems'))
    nextPageToken = response.get('nextPageToken')

df_media_items = pd.DataFrame(lst_medias)


image_folder_name = 'images'
if not os.path.isdir(image_folder_name):
    os.mkdir(image_folder_name)

i = 0
named_rim = "cmsModel1"

print(df_media_items)

for index, item in df_media_items.iterrows():
    item_url = item['baseUrl']
    local_file = item['filename'] #named_rim + str(i)
    if local_file in os.listdir(image_folder_name):
        print("resmi atla ")
        continue;
    if i == 10:
        break

    print(item_url)
    # Define the remote file to retrieve
    remote_url = item_url
    # Define the local filename to save data
    # local_file = filename  
    # Download remote and save locally
    request.urlretrieve(remote_url,
                        os.path.join(image_folder_name, local_file))
    i += 1

# here get some filter use machine learning




# here function for model renaming

# albummise all images

"""
get method
"""
media_id = df_media_items['id'][108]
response = service.mediaItems().get(mediaItemId=media_id).execute()

pprint(response)




