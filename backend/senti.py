from googleapiclient.discovery import build
import pickle
import re
import warnings
warnings.filterwarnings("ignore")
api_key = 'AIzaSyB99vDvUQUO8qWZ7QDb2l5UvO1QEzDAErQ'
youtube = build('youtube', 'v3', developerKey=api_key)
NON_ALPHANUM = re.compile(r'[\W]')
NON_ASCII = re.compile(r'[^a-z0-1\s]')

def normalize_texts(text):
    """

    * text: the text passed as a comment here
    * function returns the normalised form of the text
    -converts the input to lower case
    - removes all punctuations as well as non-ascii characters
    """
    lower = text.lower()
    no_punctuation = NON_ALPHANUM.sub(r' ', lower)
    no_non_ascii = NON_ASCII.sub(r'', no_punctuation)
    return no_non_ascii

def calc(vId):
    """
    *vID is the vidoe id of that particular video
    This function
    -calculates the positive comments
    -calculates the negative comments
    -finds the number of likes
    -finds the number of dislikes
    -finds the views of a video
    * returns a list of dictionaries having :
    -title
    -rating(out of 10)
    -views
    -number of positive comments
    -number of negative comments
    -number of likes
    -number of dislikes
    -link of the video
    """
    response = youtube.commentThreads().list(part='snippet',videoId=vId,textFormat='plainText').execute()
    #opening the logistic regression and count vectoizer models
    lr = pickle.load(open('model.pkl', 'rb'))
    cv = pickle.load(open('cv.pkl', 'rb'))
    l=list()
    d=dict()

    for i in response['items']:
        comment=i['snippet']['topLevelComment']['snippet']['textDisplay']
        l.append(comment)
        comment=normalize_texts(comment)
        normalized = cv.transform([comment])
        result = lr.predict(normalized)
        d[comment]=result
    pc=0
    nc=0

    for i in d:
        if d[i][0] ==1:
            pc=pc+1
        else:
            nc=nc+1

    #try if there are any comments for the video, except return
    try:
        r_c=((pc)/(pc+nc))*10
    except :
        print('\n','this video has no comments','\n')
        return

    #Get like and dislike count for the video
    response2 = youtube.videos().list(part='statistics',id=vId).execute()
    likes=(int)(response2['items'][0]['statistics']['likeCount'])
    dislikes=(int)(response2['items'][0]['statistics']['dislikeCount'])
    #Get viewcountof the video
    views=(int)(response2['items'][0]['statistics']['viewCount'])

    r_l=(likes/(likes+dislikes))*10
    sum=(r_l+r_c)/2
    f = youtube.videos().list(part='snippet',id=vId).execute()
    # get the title of the video
    title=f['items'][0]['snippet']['title']
    l2 = {'title':title,'rating': sum,'views':views ,'positive_comments':pc,'negative_comments':nc,'likes':likes,'dislikes':dislikes,'link': ("https://www.youtube.com/watch?v=" + vId)}
    return (l2)
