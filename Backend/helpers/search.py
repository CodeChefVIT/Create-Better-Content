from helpers.senti import *
import urllib.parse
warnings.filterwarnings("ignore")

# build the YT api using the api key and use the youtube data -> v3 api
config=dotenv_values('helpers/.env')
api_key = config['API_KEY']

youtube = build('youtube', 'v3', developerKey=api_key)


def searcher(search):
    """
    * search-search is the keyword entered by the user
    * function returns a list of the comments of 15 videos in the form of a list
    """
    # try :
    response = youtube.search().list(part='snippet', q=search, maxResults=15, type='video').execute()
    # except:
    #     print('comments were turned off for this video')
    l = []
    for i in response['items']:
        l.append(i['id']['videoId'])
    return l


def keyword_s(search):
    a = []
    for i in searcher(search):
        if calc(i) != None:
            #check if theres an item in the dtring => but we would ned to chk if comments are on
            a.append(calc(i))
    a = sorted(a, key=lambda i: i['rating'], reverse=True)
    print(a)
    return a


def link(url):
    url_data = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(url_data.query)
    vId = query["v"][0]
    print(calc(vId))
    return calc(vId)
