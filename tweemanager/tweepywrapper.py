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
        # No need for Get or Create while listening
        tweet = TweetForElastic(meta={'id': json_data["id"]})

        for k,v in json_data.iteritems():
            tweet[k] = v
        
        # Time
        try:
            tweet.tweettime = datetime.datetime.strptime(json_data['created_at'],'%a %b %d %H:%M:%S +0000 %Y');
        except:
            tweet.tweettime = datetime.datetime.fromtimestamp(int(json_data["timestamp_ms"])/1000)
        
        # Geolocation
        try:
            if json_data["place"]:
                geolocator = Nominatim()
                loc = geolocator.geocode(json_data["place"]["full_name"],timeout = 1000000)
                if loc:
                    tweet.location =  {"lat" : loc.latitude,"lon" : loc.longitude}
        except:
            pass

        # Text
        texto = t['text']
        try:
        # Remove URLs
            try:
                texto_sin_url = re.sub(r'htt[^ ]*', '', texto)
            except:
                texto_sin_url = re.sub(r'htt\w+:\/{2}[\d\w-]', '', texto)

            tweet.text = texto_sin_url
        except:
            tweet.text = texto

        ## If you want to show the tweet, uncomment this
        # try:
        #     print(json_data["id"])
        #     print tweet["text"]
        # except:
        #     pass        

        ## Filter
        try:
            text_low = tweet.text
            text_low = text_low.lower()
            idioma = text['lang']
            toexclude = configdata.get('Patterns','toexclude')
            toinclude = configdata.get('Patterns','toinclude')
            languagetoinclude = configdata.get('Patterns','languagetoinclude')

            toexclude = eval(toexclude)
            for word in toexclude:
                word = word.decode('utf-8')
                if word in text_low:
                    filtro = False
                    break

            toinclude = eval(toinclude)
            for word in toinclude:
                word = word.decode('utf-8')
                if word in text_low:
                    filtro = True

            languagetoinclude = eval(languagetoinclude)
            for language in languagetoinclude:
                language = language.decode('utf-8')
                if json_data["lang"] == language:
                    filtro = True               

        except Exception as e:
            print e
            filtro = False


        # # Filter (not sure it works)
        # try:
        #     text_low = tweet.text
        #     text_low = text_low.lower()

        #     for word in self.toexclude:
        #         if word in text_low:
        #             filtro = False

        #     for word in self.toinclude:
        #         if word in text_low:
        #             filtro = True


        #     for language in self.languagetoexclude:
        #         if json_data["lang"] == language:
        #             filtro = False

        #     for language in self.languagetoinclude:
        #         if json_data["lang"] == language:
        #             filtro = True

        # except Exception as e:
        #     print e
        #     filtro = False

        if filtro == True:      
            try:
                tweet.save()
            except:
                raise        


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
    myStreamListener.toexclude = configdata.get('Patterns','toexclude')
    myStreamListener.toinclude = configdata.get('Patterns','toinclude')
    myStreamListener.languagetoexclude = configdata.get('Patterns','languagetoexclude')
    myStreamListener.languagetoinclude = configdata.get('Patterns','languagetoinclude')
    api = tweepy.API(auth)
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    listapalabras = list()
    listapalabras.append(configdata.get('TwitterAPITrackQuery','trackquery'))
    myStream.filter(track=listapalabras)

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
    try:
        query = configdata.get("TwitterAPITrackQuery","trackquery")
    except:
        query = None
    #

    try:
        since = configdata.get("TwitterAPITrackQuery","since")
        since = 'since:' + since
        query = query + ' ' + since
    except:
        pass

    try:
        until = configdata.get("TwitterAPITrackQuery","until")
        until = 'until:' + until
        query = query + ' ' + until
    except:
        pass

    startTweetForElastic(configdata)
    #
    contador = 0
    searched_tweets = tweepy.Cursor(api.search, q=query).items(max_tweets)
    for status in searched_tweets:
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
        # if json_data["place"]:
        #     geolocator = Nominatim()
        #     loc = geolocator.geocode(json_data["place"]["full_name"],timeout = 1000000)
        #     if loc:
        #         tweet.location =  {"lat" : loc.latitude,"lon" : loc.longitude}

        # ## Text
        # texto = json_data['text']
        # try:
        # # Remove URLs
        #     try:
        #         texto_sin_url = re.sub(r'htt[^ ]*', '', texto)
        #     except:
        #         texto_sin_url = re.sub(r'htt\w+:\/{2}[\d\w-]', '', texto)

        #     tweet.text = texto_sin_url
        # except:
        #     tweet.text = texto

        # # Filter
        filtro=True
        # try:
        #     text_low = tweet.text
        #     text_low = text_low.lower()
        #     idioma = text['lang']
        #     toexclude = configdata.get('Patterns','toexclude')
        #     toinclude = configdata.get('Patterns','toinclude')
        #     languagetoinclude = configdata.get('Patterns','languagetoinclude')

        #     toexclude = eval(toexclude)
        #     for word in toexclude:
        #         word = word.decode('utf-8')
        #         if word in text_low:
        #             filtro = False
        #             break

        #     toinclude = eval(toinclude)
        #     for word in toinclude:
        #         word = word.decode('utf-8')
        #         if word in text_low:
        #             filtro = True

        #     languagetoinclude = eval(languagetoinclude)
        #     for language in languagetoinclude:
        #         language = language.decode('utf-8')
        #         if json_data["lang"] == language:
        #             filtro = True               

        # except Exception as e:
        #     print e
        #     filtro = False


        # # Filter (not sure it works)
        # try
        #     text_low = tweet.text
        #     text_low = text_low.lower()
        #     idioma = text['lang']
        #     toexclude = configdata.get('Patterns','toexclude')
        #     toinclude = configdata.get('Patterns','toinclude')
        #     languagetoinclude = configdata.get('Patterns','languagetoinclude')

        #     for word in self.toexclude:
        #         word = word.decode('utf-8')
        #         if word in text_low:
        #             filtro = False

        #     for word in self.toinclude:
        #         word = word.decode('utf-8')
        #         if word in text_low:
        #             filtro = True

        #     for language in self.languagetoinclude:
        #         language = language.decode('utf-8')
        #         if json_data["lang"] == language:
        #             filtro = True

        # except Exception as e:
        #     print e
        #     filtro = False

        if filtro == True:      
            try:
                print tweet.text
                contador += 1
                print contador
                tweet.save()
            except:
                raise  
