from googleapiclient.discovery import build
import pprint
import pickle
import re
import numpy
import warnings
warnings.filterwarnings("ignore")
import urllib.parse
from senti import *




api_key = 'AIzaSyB99vDvUQUO8qWZ7QDb2l5UvO1QEzDAErQ'
youtube = build('youtube', 'v3', developerKey=api_key)



# def sorter(b):
#     c=0
#     for i in b:
#         for j in b:
#             if j['rating']>i['rating']:
#                 c=i
#                 i=j
#                 j=c
#                 # print('chala')
#     print(b)
#     return b


def searcher(search):
    response = youtube.search().list(part='snippet',q=search,maxResults=15,type='video').execute()
    l=[]
    for i in response['items']:
        l.append(i['id']['videoId'])

    # print(l)

    return l



def keyword_s(search):
    a=[]
    for i in searcher(search):
        if calc(i)!=None:
            a.append(calc(i))
    # print(a)
    a=sorted(a,key=lambda i:i['rating'],reverse=True)
    print(a)

    return a


def link(url):

    url_data = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(url_data.query)
    vId = query["v"][0]
    print(calc(vId))
    return (calc(vId))

