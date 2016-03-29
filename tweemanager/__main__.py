#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hugo M. Marrão Rodrigues
# @Date:   2016-03-02 20:20:57
# @Last Modified by:   hmarrao
# @Last Modified time: 2016-03-02 23:53:54

from docopt import docopt

__doc__ = """tweemanager.
NFQ Solutions: this package is at alpha stage.

Usage:
  tweemanager listener [options]
  tweemanager getoldtweets
  tweemanager getoldertweets [<username> <since> <until> <querySearch> <maxTweets>]
  tweemanager genconfig [<cfgfilepath>]
  tweemanager dumpelastic <indextodump>
  tweemanager loadelastic <dumpedjson>
  tweemanager (-h | --help)
  tweemanager --version

Commands:
  listener       Raise the tweepy listener
  getoldtweets   Access old tweeters (less than 10 days)
  getoldertweets Access old tweeters (unofficial API)
  genconfig      Generate the tweemanager.cfg
  dumpelastic    Download tweets from Elasticsearch into a json
  loadelastic    Upload tweets to Elasticsearch from a json

Options:
  -h --help                      Show this screen
  --version                      Show version
  --cfgfile=<configfilepath>     add config file path to be used

"""

import ConfigParser

def configparserhandler(ReadOrWrite = True,configfilepath = None):
    """
    ReadOrWrite = True will read or use default config data
    ReadOrWrite = False will write the tweemanager.cfg if it doesn't exists
    """
    configdata = ConfigParser.ConfigParser()

    def configdefaultdata():
        """
        if no data is given use this as default
        """
        configdata = ConfigParser.ConfigParser()
        configdata.add_section('TwitterAPIcredentials')
        configdata.set('TwitterAPIcredentials','consumer_key',"una_consumer_key")
        configdata.set('TwitterAPIcredentials','consumer_secret',"una consumer_secret")
        configdata.set('TwitterAPIcredentials','access_key',"una access_key")
        configdata.set('TwitterAPIcredentials','access_secret',"una access_secret")
        configdata.add_section('TwitterAPITrackQuery')
        configdata.set('TwitterAPITrackQuery','TrackQuery',"palabra")
        configdata.add_section('Elasticsearch')
        configdata.set('Elasticsearch','ES_URL',"URL_de_ES")
        configdata.set('Elasticsearch','ES_PORT',"Puerto_para_ES")
        return configdata


    if ReadOrWrite:
        # Read tweem.cfg or given config file
        try:
            if configfilepath:
                if os.path.isfile(configfilepath):
                    configdata.read(configfilepath)
            else:
                configdata.read("tweem.cfg")
                print "reading tweem.cfg"
                print configdata.sections()
        except:
            raise
        finally:
            return configdata
    else:
        # write config file tweem.cfg with default information
        try:
            if configfilepath is None:
                configfilepath = "tweem.cfg"
            import os.path
            if not os.path.isfile(configfilepath):
                configdata = configdefaultdata()
                with open(configfilepath,"w") as fichero:
                    configdata.write(fichero)
                print("Done::"+configfilepath+" is ready to me modified")
            else:
                print("Warning::"+configfilepath+".cfg already exists")
                print("Warning::delete it repeat command")
        except:
            raise
        finally:
            return configdata


def listener(configdata):
    """
    Set up a listener which save tweets from a query
    """
    from tweepywrapper import letsgo
    letsgo(configdata)
    return

def getoldtweets(configdata,max_tweets):
    """
    Get old tweets with the official API. Limited to 10 days
    """
    from tweepywrapper import letsquery
    letsquery(configdata,max_tweets)
    
    return

def getoldertweets(configdata,maxTweets=None):
    """
    Get old tweets with an unofficial API. Just limited by Twitter servers' capacity
    """
    try:
        import got
        import json
        from geopy.geocoders import Nominatim
        from tweepywrapper import TweetForElastic,startTweetForElastic
        tweetCriteria = got.manager.TweetCriteria()
        
        if (username):
            tweetCriteria.username = configdata.get("TwitterAPITrackQuery","username")
        if (since):
            tweetCriteria.since = configdata.get("TwitterAPITrackQuery","since")
        if (until):
            tweetCriteria.until = configdata.get("TwitterAPITrackQuery","until")
        if (querySearch):
            # The query is the same as the listener. Otherwise, change it
            tweetCriteria.querySearch = configdata.get("TwitterAPITrackQuery","trackquery")
        if (maxTweets):
            tweetCriteria.maxTweets = maxTweets
        else:
            tweetCriteria.maxTweets = 2000

        #geolocator = Nominatim()
        startTweetForElastic(configdata)

        for t in got.manager.TweetManager.getTweets(tweetCriteria):
            ## If you want to show the tweet, uncomment this
            # print t.permalink
            # print t.username
            # print t.text
            # print t.text.replace("# ","#").replace("@ ","@")
            # print type(t.date)
            # print t.date
            # print t.retweets 
            # print t.favorites
            # print t.mentions 
            # print t.hashtags
            # print t.geoText

            tweet = TweetForElastic(meta={'id': t.id})
            tweet.text = t.text.replace("# ","#").replace("@ ","@")
            tweet.favorite_count = t.favorites
            tweet.retweet_count = t.retweets
            tweet.user = {"name": "None"}
            tweet.user.name = t.username

            if not hasattr(tweet,"tweettime"):
                tweet.tweettime = t.date
            else:
                if not tweet.tweettime:
                    tweet.tweettime = t.date
                    print(t.date)

            if (t.geoText):
                geolocator = Nominatim()
                loc = geolocator.geocode(t.geoText)
                if loc:
                    print t.id,t.geoText,(loc.latitude,loc.longitude)
                    tweet.location =  {"lat" : loc.latitude,"lon" : loc.longitude}
            tweet.text = json.dumps(t.text,ensure_ascii=False, encoding='utf8')

            ## Filter
            try:
                text_low = tweet.text
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

    except:
        raise

def dumpelastic(NombreArchivo,indextodump):
    """
    Dump tweets from an index into a json in a bulk of 500 tweets
    """
    import json
    from elasticsearch import Elasticsearch
    import io

    es = Elasticsearch([{'host':configdata.get("Elasticsearch","ES_URL")}])
    outputFile = io.open(NombreArchivo, "w+", encoding='utf8')

    res = es.search(index=indextodump, size=500, doc_type="tweet_for_elastic", body={"query": {"match_all": {}}}, scroll='10m')
    
    tweets = res['hits']['hits']

    for hit in tweets:
        hit["_source"]['text'] = hit["_source"]['text'].replace("\n"," ").replace("# ","#").replace("@ ","@")
        outputFile.write('%s\n' % (json.dumps(hit,ensure_ascii=False, encoding='utf8')))

       
    while (len(tweets)>0):
        # Keep with the search until no more tweets are found
        sid = res['_scroll_id']
        res = es.scroll(scroll_id = sid, scroll = '10m')
        tweets = res['hits']['hits']

        for hit in tweets:
            hit["_source"]['text'] = hit["_source"]['text'].replace("\n"," ").replace("# ","#").replace("@ ","@")
            outputFile.write('%s\n' % (json.dumps(hit,ensure_ascii=False, encoding='utf8')))

    outputFile.close()

    return

def loadelastic(configdata,dumpedjson):
    """
    This function try to load data to the Elasticsearch server by importing tweets from a json
    """
    try:
        import got
        import json
        import datetime
        from geopy.geocoders import Nominatim
        from tweepywrapper import TweetForElastic,startTweetForElastic


        # Streaming
        startTweetForElastic(configdata)

        tweets = open(dumpedjson, "r")

        contador = 0

        for t in tweets:
            t = json.loads(t)

            tweet = TweetForElastic(meta={'id': t['_source']['id']})
            
            for key, value in t["_source"].iteritems():
                try:
                    tweet[key] = eval(value)
                except:
                    tweet[key] = value

            try:
                tweet.tweettime = t['_source']['tweettime']
                print t['_source']['tweettime']
            except:
                tweet.tweettime = datetime.datetime.strptime(t['_source']['created_at'],'%a %b %d %H:%M:%S +0000 %Y');
                print t['_source']['created_at']

            try:
                tweet.location = t['_source']['location']
                # print tweet.location
            except Exception as e:
                loc = None

            try:
                urls = t['_source']['entities']['urls']
                # This script just save the first url
                url = urls[0]
                ex_url = url['expanded_url']
                tweet.url = ex_url
            except:
                pass

            try:
                tweet["text"] = t['_source']['text']
            except:
                raise

            ## Filter
            try:


                toexclude = configdata.get('Patterns','toexclude')
                toinclude = configdata.get('Patterns','toinclude')
                languagetoexclude = configdata.get('Patterns','languagetoexclude')
                languagetoinclude = configdata.get('Patterns','languagetoinclude')

                ## if we want to include tweets from a date
                # anno = configdata.get('Patterns','year')
                # mes = configdata.get('Patterns','month')
                # dia = configdata.get('Patterns','day')
                # fecha = datetime.datetime(year=anno,mont=mes,day=dia)

                # Format fields to compare
                time = tweet.tweettime
                time_naive = time.replace(tzinfo=None)
                text_low = tweet["text"]
                text_low = text_low.lower()

                for word in toexclude:
                    print word
                    print text_low
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

                # if time < fecha:
                #     filtro = False

            except Exception as e:
                print e
                filtro = False
                raise

            if filtro == True:      
                try:
                    tweet.save()
                    print("tweet saved")
                    print contador
                    contador += 1
                except:
                    raise      
        
    except:
        raise


# Parse command line arguments
arguments = docopt(__doc__, version='tweemanager 2.0')

if arguments['genconfig']:
    print(arguments)
    configdata = configparserhandler(ReadOrWrite = False,configfilepath=arguments.get('<cfgfilepath>',None))
    exit()

configdata = configparserhandler(ReadOrWrite = True,configfilepath=arguments.get('--cfgfile',None))
print configdata.get('TwitterAPIcredentials','consumer_key')

if arguments['listener']:
    listener(configdata)
elif arguments['getoldtweets']:
    print('getoldtweets')
    getoldtweets(configdata)
elif arguments['getoldertweets']:
    print('getoldertweets')
    getoldertweets(configdata=configdata,maxTweets=10)
elif arguments['dumpelastic']:
    print('dumpelastic')
    dumpelastic(NombreArchivo,indextodump)
elif arguments['loadelastic']:
    print('loadelastic')
    loadelastic(configdata,arguments['<dumpedjson>'])
else:
    pass
