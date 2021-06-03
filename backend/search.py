import os
import warnings
warnings.filterwarnings("ignore")
import urllib.parse
from senti import *
from dotenv import dotenv_values


# build the YT api using the api key and use the youtube data -> v3 api
# print(os.environ)
config=dotenv_values('.env')
api_key = config['API_KEY']
youtube = build('youtube', 'v3', developerKey=api_key)



def searcher(search):
    """
    * search-search is the keyword entered by the user
    * function returns a list of the comments of 15 videos in the form of a list
    """
    response = youtube.search().list(part='snippet',q=search,maxResults=15,type='video').execute()
    l=[]
    for i in response['items']:
        l.append(i['id']['videoId'])
    return l

def keyword_s(search):
    '''
    It is used when the user enters a keyword to search and returns the information about top 15 videos realted to that keyword
    * search-keyword entered by the user
    * returns the list of information of different videos sorting according to the descending order of videos (with respect to their ratings)
    '''
    a=[]
    for i in searcher(search):
        if calc(i)!=None:
            a.append(calc(i))
    a=sorted(a,key=lambda i:i['rating'],reverse=True)
    print(a)
    return a

def link(url):
    """
    It is used when the user enters a link to search and returns the information about the video given by the link.
    * url-url entered by the user
    * returns the details of the specific video ,whose link is entered by the user
    """
    url_data = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(url_data.query)
    vId = query["v"][0]
    print(calc(vId))
    return (calc(vId))
