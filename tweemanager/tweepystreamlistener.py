# -*- coding: utf-8 -*-
import tweepy
from tweepy.utils import import_simplejson
from bson import json_util

import utilities

json = import_simplejson()

class nfqTwitterStreamListener(tweepy.StreamListener):
    """nfqlistener
    """
    # class attribute containing some configdata
    configdata = None
    

    def on_error(self,code):
        """On error it won't stop the listener.
        """
        print("Error while listening with code:"+code)

    def on_status(self, status):
        """Handle recevied tweet:

        This status will put candidate in a MQ.
        """
        print("data from twitter")
        data = status._json
        # Avoid manual parsing datetime and use the one on the Status object.
        data[u'created_at'] = status.created_at
        utilities.resultshandler.putresult(data)


class nfqTwitterAuth(object): 
    """ 
    class to manage the twitter authorization 
    """ 
    
    def __init__(self,configdata): 
        self.auth = tweepy.OAuthHandler(configdata.getTwitterAPIcredentials("consumer_key"),
                    configdata.getTwitterAPIcredentials("consumer_secret")) 
        self.auth.set_access_token(configdata.getTwitterAPIcredentials("access_key"),
                  configdata.getTwitterAPIcredentials("access_secret")) 
        self.api = tweepy.API(self.auth) 
    
    def get_auth(self): 
        return self.auth 
    
    def get_api(self): 
        return self.api 


def letslisten(api,track):
    """Set 
    """
    NFQlistener = nfqTwitterStreamListener()
    thecurrentstream = tweepy.Stream(auth = api.auth, listener=NFQlistener)
    thecurrentstream.filter(track=track)


def letssearch(api,query,maxtweets=10):
    """
    """
    for status in tweepy.Cursor(api.search, q=query).items(maxtweets):
        # Verver
        # 
        data = status._json
        data[u'created_at'] = status.created_at
        utilities.resultshandler.putresult(data)
