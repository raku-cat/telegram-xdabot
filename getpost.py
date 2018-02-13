import requests
from urllib.parse import urlparse, parse_qs
import json
import regex

apibase = 'https://api.xda-developers.com/v1/posts/bypostid/'
def getpost(posturl):
    parsedurl = urlparse(posturl)
    try:
        pq = parse_qs(parsedurl.query)
        #try:
        postid = pq['p'][0]
        #except KeyError:
        #    return
    except:
        try:
            if len(parsedurl.fragment) > 0:
                postid = regex.sub('[^0-9]', '', parsedurl.fragment)
            elif len(parsedurl.path) > 0 and 'post' in parsedurl.path.split('/')[-1]:
                postid = regex.sub('[^0-9]', '', parsedurl.path.split('/')[-1])
            try:
                if len(postid) == 0:
                    raise ValueError('No post ID')
            except (UnboundLocalError, ValueError) as e:
                return
        except KeyError:
            return
    idparam = { 'postid' : postid }
    post_request = requests.get(apibase, params=idparam)
    if (post_request.status_code == requests.codes.ok):
        try:
            post_json = post_request.json()['results']
            post = (post['pagetext'] for post in post_json if post['postid'] == postid).__next__()
        except:
            return
        post = post.replace('\n',' ').replace('\r','')
        return post
    else:
        return
