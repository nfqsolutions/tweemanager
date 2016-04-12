#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hugo M. Marrão Rodrigues, Carlos Perales Gonz
# @Date:   2016-03-02 20:20:57
# @Last Modified by:   cperales
# @Last Modified time: 2016-04-08

from docopt import docopt

__doc__ = """tweemanager.
NFQ Solutions: this package is at alpha stage.

Usage:
  tweemanager listener [options]
  tweemanager getoldtweets
  tweemanager getoldertweets
  tweemanager genconfig [<cfgfilepath>]
  tweemanager dumpelastic <namefile> <indextodump>
  tweemanager loadelastic <dumpedjson>
  tweemanager dumptocsv <dumpedjson> <csvfile>
  tweemanager (-h | --help)
  tweemanager --version

Commands:
  listener       Raise the tweepy listener
  getoldtweets   Access old tweeters (less than 10 days)
  getoldertweets Access old tweeters (unofficial API)
  genconfig      Generate the tweemanager.cfg
  dumpelastic    Download tweets from Elasticsearch into a json
  loadelastic    Upload tweets to Elasticsearch from a json
  dumptocsv      Load tweets from a json to a CSV

Options:
  -h --help                      Show this screen
  --version                      Show version
  --cfgfile=<configfilepath>     add config file path to be used
  --username=<username>     add config file path to be used

Comments:


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
        configdata.set('TwitterAPITrackQuery','username',"palabra")
        configdata.set('TwitterAPITrackQuery','since',"fecha-desde")
        configdata.set('TwitterAPITrackQuery','until',"fecha-hasta")
        configdata.add_section('Elasticsearch')
        configdata.set('Elasticsearch','ES_URL',"URL_de_ES")
        configdata.set('Elasticsearch','ES_PORT',"Puerto_para_ES")
        configdata.add_section('Patterns')
        configdata.set('Patterns','toexclude','[]')
        configdata.set('Patterns','toinclude','[]')
        configdata.set('Patterns','languagetoinclude','[]')
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

def getoldtweets(configdata):
    """
    Get old tweets with the official API. Limited to 10 days
    """
    from tweepywrapper import letsquery
    max_tweets = int(configdata.get("TwitterAPITrackQuery","maxTweets"))
    letsquery(configdata,max_tweets)
    
    return

def getoldertweets(configdata):
    """
    Get old tweets with an unofficial API. Just limited by Twitter servers' capacity
    """
    try:
        import got
        import json
        from geopy.geocoders import Nominatim
        from tweepywrapper import TweetForElastic,startTweetForElastic
        tweetCriteria = got.manager.TweetCriteria()


        try:
            tweetCriteria.username = configdata.get("TwitterAPITrackQuery","username")
            print tweetCriteria.username
        except:
            print "no usuario"

        try:
            tweetCriteria.since = configdata.get("TwitterAPITrackQuery","since")
            print tweetCriteria.since
        except:
            print "no since"
            pass

        try:
            tweetCriteria.until = configdata.get("TwitterAPITrackQuery","until")
            print tweetCriteria.until 
        except:
            print "no until"
            pass

        try:
            # The query is the same as the listener. Otherwise, change it
            tweetCriteria.querySearch = configdata.get("TwitterAPITrackQuery","trackquery")
            print tweetCriteria.querySearch
        except:
            print "no query"
            pass

        try:
            tweetCriteria.maxTweets = int(configdata.get("TwitterAPITrackQuery","maxTweets"))
            print tweetCriteria.maxTweets
        except:
            print "no maxTweets"
            tweetCriteria.maxTweets = 1



        geolocator = Nominatim()
        searched_tweets = got.manager.TweetManager.getTweets(tweetCriteria)
        startTweetForElastic(configdata)
        contador = 0
        for t in searched_tweets:
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
                try:
                    geolocator = Nominatim()
                    loc = geolocator.geocode(t.geoText, timeout=1000000)
                    if loc:
                        print t.id,t.geoText,(loc.latitude,loc.longitude)
                        tweet.location =  {"lat" : loc.latitude,"lon" : loc.longitude}
                except:
                    pass

            ## Text
            try:
                texto = json.dumps(t.text,ensure_ascii=False, encoding='utf8')
                texto = re.sub(r'# ', '#', texto)
                texto = re.sub(r'/ ', '/', texto)
                texto = re.sub(r'@ ', '@', texto)
                tweet.text = texto
            except Exception as e:
                print e
                tweet.text = json.dumps(t.text,ensure_ascii=False, encoding='utf8')

            print tweet.text

            texto = tweet.text
            try:
            # Remove URLs
                try:
                    texto_sin_url = re.sub(r'htt[^ ]*', '', texto)
                except:
                    texto_sin_url = re.sub(r'htt\w+:\/{2}[\d\w-]', '', texto)

                tweet.text = texto_sin_url
            except:
                pass

            # Filter
            filtro = True
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


            if filtro == True:      
                try:
                    contador += 1
                    print contador
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
            try:
                hit["_source"]['text'] = hit["_source"]['text'].replace("\n"," ").replace("# ","#").replace("@ ","@")
                outputFile.write('%s\n' % (json.dumps(hit,ensure_ascii=False, encoding='utf8')))
            except:
                pass

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


            ## Text
            texto = t['_source']['text']
            try:
            # Remove URLs
                try:
                    texto_sin_url = re.sub(r'htt[^ ]*', '', texto)
                except:
                    texto_sin_url = re.sub(r'htt\w+:\/{2}[\d\w-]', '', texto)

                tweet.text = texto_sin_url
            except:
                tweet.text = texto


            # Filter
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

            if filtro == True:      
                try:
                    tweet.save()
                except:
                    raise  


            ## Filter
            try:
                text_low = tweet.text
                text_low = text_low.lower()
                toexclude = configdata.get('Patterns','toexclude')
                toinclude = configdata.get('Patterns','toinclude')
                languagetoexclude = configdata.get('Patterns','languagetoexclude')
                languagetoinclude = configdata.get('Patterns','languagetoinclude')

                toexclude = eval(toexclude)
                for word in toexclude:
                    word = word.decode('utf-8')
                    if word in text_low:
                        filtro = False
                        break

                toinclude = eval(toinclude)
                for word in toinclude:
                    if word in text_low:
                        filtro = True

                print ""


            except Exception as e:
                print e
                filtro = False

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


# def dumptoCSV(dumpedjson,csvfile):
#     """
#     Dump JSON fields to a CSV file. Comment/Uncomment to pass all the data or just the text message
#     """
#     import codecs
#     import json

#     infile = codecs.open(dumpedjson, "r",encoding='utf8')

#     outputFile = codecs.open(csvfile, "w+",encoding='utf8')
#     outputFile.write('texto\n')

#     # outputFile.write('contributors\ttruncated\ttext\tis_quote_status\tin_reply_to_status_id\tid\tfavorite_count\tsource\tretweeted\tcoordinates\ttimestamp_ms\tin_reply_to_screen_name\tin_reply_to_user_id\tretweet_count\tid_str\tfavorited\tgeo\tpossibly_sensitive\tlang\tcreated_at\tfilter_level\tin_reply_to_status_id_str\tplace\tUsuario verificado\tNum amigos\tNombre de usuario\n') #] (t.contributors, t.truncated, t.text, t.is_quote_status, t.in_reply_to_status_id, t.id, t.favourite_count, t.source, t.retweeted, t.coordinates, t.timestamp_ms, t.in_reply_to_screen_name, t.in_reply_to_user_id, t.retweet_count, t.id_str, t.favorited, t.geo, t.in_reply_to_user_id_str, t.possibly_sensitive\tlang, t.created_at, t.filter_level, t.in_reply_to_status_id_str, t.place))

#     i = 1
#     for t in infile:

#         line_as_dict = json.loads(t.rstrip())
#         entero = line_as_dict
#         line_as_dict = line_as_dict["_source"]
#         texto  = line_as_dict['text'].strip()
#         texto = texto.rstrip('\n')
#         print texto
#         outputFile.write('%s\n' % (texto)



#         # geoloc = line_as_dict.get('geo')

#         # if not geoloc:
#         #   geoloc = "NA"


#         # entities = line_as_dict.get('entities','NA')
#         # # url = entities.get('urls','[NA]')
#         # usuario_nul = {'name':'NA', 'friends_count':0}
#         # user = line_as_dict.get('user',usuario_nul)

#         # print ""
#         # try:
#         #     iden = line_as_dict['id']
#         # except:
#         #     iden = entero["_id"]

#         # try:
#         #     fecha = line_as_dict['tweettime']
#         # except:
#         #     fecha = line_as_dict['created_at']

#         # print(line_as_dict.get('contributors','NA'), 
#         # line_as_dict.get('truncated','NA'), texto, line_as_dict.get('is_quote_status','NA'), line_as_dict.get('in_reply_to_status_id','NA'), iden,
#         # line_as_dict.get('favorite_count',0), line_as_dict.get('source','NA'), line_as_dict.get('retweeted','False'), line_as_dict.get('coordinates','NA'), line_as_dict.get('timestamp_ms','NA'),
#         # line_as_dict.get('in_reply_to_screen_name','NA'), line_as_dict.get('in_reply_to_user_id','NA'), line_as_dict.get('retweet_count',0), line_as_dict.get('id_str','NA'), line_as_dict.get('favorited','NA'),
#         # geoloc, line_as_dict.get('possibly_sensitive','False'), line_as_dict.get('lang','NA'), fecha,
#         # line_as_dict.get('filter_level','NA'), line_as_dict.get('in_reply_to_status_id_str','NA'), line_as_dict.get('place','NA'), user.get('verified','False'), user.get('friends_count',0),
#         # user.get('name','NA'))

#         # outputFile.write('%s\t %s\t %s\t %s\t %s\t %s\t %f\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\n' % (line_as_dict.get('contributors','NA'), 
#         # line_as_dict.get('truncated','NA'), texto, line_as_dict.get('is_quote_status','NA'), line_as_dict.get('in_reply_to_status_id','NA'), iden,
#         # line_as_dict.get('favorite_count',0), line_as_dict.get('source','NA'), line_as_dict.get('retweeted','False'), line_as_dict.get('coordinates','NA'), line_as_dict.get('timestamp_ms','NA'),
#         # line_as_dict.get('in_reply_to_screen_name','NA'), line_as_dict.get('in_reply_to_user_id','NA'), line_as_dict.get('retweet_count',0), line_as_dict.get('id_str','NA'), line_as_dict.get('favorited','NA'),
#         # geoloc, line_as_dict.get('possibly_sensitive','False'), line_as_dict.get('lang','NA'), fecha,
#         # line_as_dict.get('filter_level','NA'), line_as_dict.get('in_reply_to_status_id_str','NA'), line_as_dict.get('place','NA'), user.get('verified','False'), user.get('friends_count',0),
#         # user.get('name','NA')  ))

#         #except:
#         #g  print line_as_dict
#         # outputFile.write('%s\t%s\t%s\t%d\t%s\t%s\t%f\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (line_as_dict['contributors'], line_as_dict['truncated'], line_as_dict['text'], line_as_dict['is_quote_status'], line_as_dict['in_reply_to_status_id'], line_as_dict['id'], line_as_dict['favorite_count'], line_as_dict['source'], line_as_dict['retweeted'], line_as_dict['coordinates'], line_as_dict['timestamp_ms'], line_as_dict['in_reply_to_screen_name'], line_as_dict['in_reply_to_user_id'], line_as_dict['retweet_count'], line_as_dict['id_str'], line_as_dict['favorited'], line_as_dict['in_reply_to_user_id_str'], line_as_dict['possibly_sensitive'], line_as_dict['lang'], line_as_dict['created_at'], line_as_dict['filter_level'], line_as_dict['in_reply_to_status_id_str'], line_as_dict['place']))

#         # (t.me, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions, t.hashtags, t.id, t.permalink)

#         i += 1
#         print i

#     outputFile.close()



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
    getoldtweets(configdata=configdata)
elif arguments['getoldertweets']:
    print('getoldertweets')
    getoldertweets(configdata=configdata)
elif arguments['dumpelastic']:
    print('dumpelastic')
    dumpelastic(arguments['<namefile>'],arguments['<indextodump>'])
elif arguments['loadelastic']:
    print('loadelastic')
    loadelastic(configdata,arguments['<dumpedjson>'])
elif arguments['dumptocsv']:
    dumptocsv(arguments['dumpedjson'],arguments['csvfile'])
else:
    pass
