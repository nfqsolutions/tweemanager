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
  tweemanager updatetweets [<startdate> <enddate>]
  tweemanager geotweets [<startdate> <enddate>]
  tweemanager genconfig [<cfgfilepath>]
  tweemanager dumpelastic <indextodump>
  tweemanager loadelastic <dumpedjson>
  tweemanager (-h | --help)
  tweemanager --version

Commands:
  listener      Raise the tweepy listener
  getoldtweets  Access old tweeters (more than a week)
  updatetweets  Will sniff tweets in database and update tweet date
  geotweets     Will sniff tweets and use a "logic" to get geoinfo
  genconfig     Generate the tweemanager.cfg
  dumpelastic   Generate the tweemanager.cfg

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
        configdata.set('TwitterAPIcredentials','consumer_key',"RB4h96LxIM7h0UzAOz8iGUvBX")
        configdata.set('TwitterAPIcredentials','consumer_secret',"GaebMjdmr783zaVqxDmh4H3JtII6hik0YzKcK7aVRC8346S8iv")
        configdata.set('TwitterAPIcredentials','access_key',"868696656-WzV9WWua1CvNDp77VK4YfhuMj5N766s4L3SPc1rr")
        configdata.set('TwitterAPIcredentials','access_secret',"Av3qqc3jpiJtjxiab0iM9tCNwT8iZJbnh1hECbitvWpCx")
        configdata.add_section('TwitterAPITrackQuery')
        configdata.set('TwitterAPITrackQuery','TrackQuery',"caixa")
        configdata.add_section('Elasticsearch')
        configdata.set('Elasticsearch','ES_URL',"http://192.168.80.221")
        configdata.set('Elasticsearch','ES_PORT',"9200")
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
    """
    from tweepywrapper import letsgo
    letsgo(configdata)
    return

def getoldtweets(configdata):
    """
    """
    from tweepywrapper import letsquery
    query = 'lacaixa OR CaixaBank'
    max_tweets = 1000
    letsquery(configdata,query,max_tweets)
    
    return

def getoldertweets(configdata,username=None,since=None,until=None,querySearch=None,maxTweets=None):
    """
    """
    print("debug1")
    try:
        import got
        import json
        from geopy.geocoders import Nominatim
        from tweepywrapper import TweetForElastic,startTweetForElastic
        tweetCriteria = got.manager.TweetCriteria()
        if (username):
            tweetCriteria.username = username
        if (since):
            tweetCriteria.since = since
        if (until):
            tweetCriteria.until = until
        if (querySearch):
            tweetCriteria.querySearch = querySearch
        if (maxTweets):
            tweetCriteria.maxTweets = maxTweets
        else:
            tweetCriteria.maxTweets = 2000

        #geolocator = Nominatim()
        print("debug2")
        startTweetForElastic(configdata)
        print("debug3")
        for t in got.manager.TweetManager.getTweets(tweetCriteria):

#https://twitter.com/agungw132/status/704413977447563264            print t.id
            print t.permalink
            print t.username
            print t.text
            print t.text.replace("# ","#").replace("@ ","@")
            print type(t.date)
            print t.date
            print t.retweets 
            print t.favorites
            print t.mentions 
            print t.hashtags
            print t.geoText
            # tweet = TweetForElastic(meta={'id': t.id})
            # if not hasattr(tweet,"body"):
            #     tweet.body = json.dumps({"text":t.text,"id":t.id},ensure_ascii=False, encoding='utf8')
            #     #tweet._source = json.dumps({"text":t.text,"id":t.id},ensure_ascii=False, encoding='utf8')
            # if not hasattr(tweet,"tweettime"):
            #     tweet.tweettime = t.date
            # else:
            #     if not tweet.tweettime:
            #         tweet.tweettime = t.date
            #         print(t.date)
            # if (t.geoText):
            #     geolocator = Nominatim()
            #     loc = geolocator.geocode(t.geoText)
            #     if loc:
            #         print t.id,t.geoText,(loc.latitude,loc.longitude)
            #         tweet.location =  {"lat" : loc.latitude,"lon" : loc.longitude}
            # tweet.tweettext = json.dumps(t.text)
            # tweet.save()
    except:
        raise



def updatetweets():
    """
    """
    # will try to get more data from tweets.

    return


def geotweets():
    """
    """
    # will try to geolocate the tweet using a basic logic.

    return


def dumpelastic():
    """
    """
    # 
    from elasticsearch import Elasticsearch
    #
    es = Elasticsearch([{"host":"192.168.80.221"}])
    # check the number of dumps and do the 

    # dump in a 5000 records iteration.
    verver = es.search(index="twitter_caixa_v2",doc_type="twitter_twp",scroll="25m")
    valor = True
    while (valor == True):
        try:
            if len(verver['hits']['hits']) > 0:
                for element in verver['hits']['hits']:
                    print element
                verver = es.scroll(scroll_id=verver['_scroll_id'],scroll="25m")
            else:
                valor = False
        except:
            valor = False
            return
    return


def loadelastic(dumpedjson):
    """
    """
    # will try to load data using bulk api in a 5000 records iteration.

    return

# Parse command line arguments
arguments = docopt(__doc__, version='tweemanager 2.0')

if arguments['genconfig']:
    print(arguments)
    configdata = configparserhandler(ReadOrWrite = False,configfilepath=arguments.get('<cfgfilepath>',None))
    exit()

configdata = configparserhandler(ReadOrWrite = True,configfilepath=arguments.get('--cfgfile',None))

if arguments['listener']:
    listener(configdata)
elif arguments['getoldtweets']:
    print('getoldtweets')
    getoldtweets(configdata)
elif arguments['getoldertweets']:
    print('getoldertweets')
    getoldertweets(configdata=configdata,since="2016-02-20",until="2016-03-01",querySearch="lacaixa OR CaixaBank",maxTweets=10)
elif arguments['updatetweets']:
    print('updatetweets')
elif arguments['geotweets']:
    print('geotweets')
elif arguments['dumpelastic']:
    print('dumpelastic')
    dumpelastic()
elif arguments['loadelastic']:
    print('loadelastic')
else:
    pass
