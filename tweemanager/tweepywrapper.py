# -*- coding: utf-8 -*-
import json
import datetime
import tweepy
import random
from geopy.geocoders import Nominatim
from elasticwrapper import TweetForElastic, startTweetForElastic

class MyStreamListener(tweepy.StreamListener):

    """
    """

    toexclude = None;
    toinclude = None;
    languagetoexclude = None;
    languagetoinclude = None;

    def on_error(self,code):
        print code

    def on_status(self, status):
        """
        """
        json_data = status._json
        print json_data
        # No need for Get or Create while listening
        # tweet = TweetForElastic(meta={'id': json_data["id"]})

        # for k,v in json_data.iteritems():
        #     tweet[k] = v
        
        # try:
        #     tweet.tweettime = datetime.datetime.strptime(json_data['created_at'],'%a %b %d %H:%M:%S +0000 %Y');
        # except:
        #     tweet.tweettime = datetime.datetime.fromtimestamp(int(json_data["timestamp_ms"])/1000)
        
        # try:
        #     if json_data["place"]:
        #         geolocator = Nominatim()
        #         loc = geolocator.geocode(json_data["place"]["full_name"],timeout = 1000000)
        #         if loc:
        #             tweet.location =  {"lat" : loc.latitude,"lon" : loc.longitude}
        # except:
        #     pass

        # ## If you want to show the tweet, uncomment this
        # try:
        #     print(json_data["id"])
        #     print tweet["text"]
        # except:
        #     pass        

        # ## Filter
        # try:
        #     text_low = tweet["text"]
        #     text_low = text_low.lower()

        #     for word in self.toexclude:
        #         # print "pasa por aquí 1"
        #         if word in text_low:
        #             # print "pasa por aquí 2 (false)"
        #             filtro = False

        #     for word in self.toinclude:
        #         # print "pasa por aquí 3"
        #         if word in text_low:
        #             # print "pasa por aquí 4 (true)"
        #             filtro = True


        #     for language in self.languagetoexclude:
        #         # print "pasa por aquí 5"
        #         if json_data["lang"] == language:
        #             # print "pasa por aquí 6 (false)"
        #             filtro = False

        #     for language in self.languagetoinclude:
        #         # print "pasa por aquí 7"
        #         if json_data["lang"] == language:
        #             # print "pasa por aquí 8 (true)"
        #             filtro = True

        # except Exception as e:
        #     print e
        #     filtro = False

        # if filtro == True:      
        #     try:
        #         # print "pasa por aquí 9"
        #         print tweet.text
        #         tweet.save()
        #     except:
        #         raise        


def letsgo(configdata):
    """
    """
    #
    # print configdata._dict()
    startTweetForElastic(configdata)
    #
    auth = tweepy.OAuthHandler(configdata.get("TwitterAPIcredentials","consumer_key") ,
        configdata.get("TwitterAPIcredentials","consumer_secret"))
    auth.set_access_token(configdata.get("TwitterAPIcredentials","access_key")
        , configdata.get("TwitterAPIcredentials","access_secret"))
    myStreamListener = MyStreamListener()
    try:
        myStreamListener.toexclude = configdata.get('Patterns','toexclude')
    except:
        myStreamListener.toinclude = []
    try:
        myStreamListener.toinclude = configdata.get('Patterns','toinclude')
    except:
        myStreamListener.toinclude = []
    try:
        myStreamListener.languagetoexclude = configdata.get('Patterns','languagetoexclude')
    except:
        myStreamListener.languagetoexclude = []
    try:
        myStreamListener.languagetoinclude = configdata.get('Patterns','languagetoinclude')
    except:
        myStreamListener.languagetoinclude = []
    api = tweepy.API(auth)
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    listapalabras = list()
    listapalabras.append(configdata.get('TwitterAPITrackQuery','trackquery'))
    print listapalabras
    myStream.filter(track=['la+caixa'])

def letsquery(configdata,maxTweets=100):
    """
    """
    try:
        #
        # assuming twitter_authentication.py contains each of the 4 oauth elements (1 per line)

        auth = tweepy.OAuthHandler(configdata.get("TwitterAPIcredentials","consumer_key"),
            configdata.get("TwitterAPIcredentials","consumer_secret"))
        auth.set_access_token(configdata.get("TwitterAPIcredentials","access_key")
            , configdata.get("TwitterAPIcredentials","access_secret"))

        api = tweepy.API(auth)
        query = configdata.get("TwitterAPITrackQuery","trackquery")
        #
        startTweetForElastic(configdata)
        #
        verver = tweepy.Cursor(api.search, q=query)
        for status in tweepy.Cursor(api.search, q=query).items(maxTweets):
            #
            print "el for"
            #
            json_data = status._json
            #
            tweet = TweetForElastic(meta={'id': json_data["id"]},)
            #
            for k,v in json_data.iteritems():
                tweet[k] = v
            #
            tweet.tweettime = datetime.datetime.strptime(json_data['created_at'],'%a %b %d %H:%M:%S +0000 %Y');
            #
            tweet.location =  None
            #
            if json_data["place"]:
                geolocator = Nominatim()
                loc = geolocator.geocode(json_data["place"]["full_name"],timeout = 1000000)
                if loc:
                    tweet.location =  {"lat" : loc.latitude,"lon" : loc.longitude}
            #
            tweet.save()
    except:
        #print "Exception"
        raise
