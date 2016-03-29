import json
import datetime
import tweepy
import random
from geopy.geocoders import Nominatim
from elasticwrapper import TweetForElastic, startTweetForElastic

class MyStreamListener(tweepy.StreamListener):

    """
    """

    def on_status(self, status):
        """
        """
        json_data = status._json
        # No need for Get or Create while listening
        tweet = TweetForElastic(meta={'id': json_data["id"]})

        for k,v in json_data.iteritems():
            tweet[k] = v
        
        try:
            tweet.tweettime = datetime.datetime.strptime(json_data['created_at'],'%a %b %d %H:%M:%S +0000 %Y');
        except:
            tweet.tweettime = datetime.datetime.fromtimestamp(int(json_data["timestamp_ms"])/1000)
        
        try:
            if json_data["place"]:
                print json_data["place"]
                geolocator = Nominatim()
                loc = geolocator.geocode(json_data["place"]["full_name"])
                if loc:
                    tweet.location =  {"lat" : loc.latitude,"lon" : loc.longitude}
        except:
            pass

        ## If you want to show the tweet, uncomment this
        # try:
        #     print(json_data["id"])
        #     print tweet["text"]
        # except:
        #     pass        

        ## Filter
        try:
            text_low = tweet["text"]
            text_low = text_low.lower()
            toexclude = configdata.get('Patterns','toexclude')
            toinclude = configdata.get('Patterns','toinclude')
            languagetoexclude = configdata.get('Patterns','languagetoexclude')
            languagetoinclude = configdata.get('Patterns','languagetoinclude')


            for word in toexclude:
                if word in text_low:
                    filtro = False

            for word in toinclude:
                if word in text_low:
                    filtro = True


            for language in languagetoexclude:
                if json_data["lang"] == language:
                    filtro = False

            for language in languagetoinclude:
                if json_data["lang"] == language:
                    filtro = True

        except:
            filtro = False

        if filtro == True:      
            try:
                tweet.save()
            except:
                raise        


def letsgo(configdata):
    """
    """
    #
    print configdata._dict()
    startTweetForElastic(configdata)
    #
    auth = tweepy.OAuthHandler(configdata.get("TwitterAPIcredentials","consumer_key") ,
        configdata.get("TwitterAPIcredentials","consumer_secret"))
    auth.set_access_token(configdata.get("TwitterAPIcredentials","access_key")
        , configdata.get("TwitterAPIcredentials","access_secret"))
    myStreamListener = MyStreamListener()
    api = tweepy.API(auth)
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    myStream.filter(track=configdata.get("TwitterAPITrackQuery","trackquery"))

def letsquery(configdata,max_tweets):
    """
    """
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
    for status in tweepy.Cursor(api.search, q=query).items(max_tweets):
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
            loc = geolocator.geocode(json_data["place"]["full_name"])
            if loc:
                tweet.location =  {"lat" : loc.latitude,"lon" : loc.longitude}
        #
        tweet.save()
