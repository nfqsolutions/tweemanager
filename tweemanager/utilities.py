# -*- coding: utf-8 -*-

import sys
import datetime
import codecs
import re
import string
import unicodedata
import logging
from bson import json_util as json


resultshandler = None

repunctuacion = re.compile('[%s]' % re.escape(string.punctuation + '¿¡'))
sourceprocessor = re.compile(r'<a.*?>(.*?)</a>', re.S | re.M)


def avg(items):
    return float(sum(items)) / len(items)


def cleantweet(rawtweet):
    """
    """
    finetweet = ""
    try:
        # Proceso original pero se estaba perdiendo alguna información:
        # Quita los RT's:
        text_clean = rawtweet.replace('RT ', '')
        # todo en letras pequeñas:
        text_clean = text_clean.lower()
        # reemplaza urls por URL:
        text_clean = re.sub(
            '((www\.[^\s]+)|(https?://[^\s]+))', 'URL', text_clean)
        # Quita mentions y pone AT_MENTION
        text_clean = re.sub('@[^\s]+', 'AT_MENTION', text_clean)
        # Reemplaza #palabra por palabra:
        text_clean = re.sub(r'#([^\s]+)', r'\1', text_clean)
        # Limpia puntuacion:
        text_clean = repunctuacion.sub('', text_clean)
        # quita acentos:
        try: # Python 2
            text_clean = unicode(text_clean)
        except: # Python 3
            pass
        text_clean = ''.join((c for c in unicodedata.normalize(
            'NFD', text_clean) if unicodedata.category(c) != 'Mn'))
        # Limpia palabras repetidas y consecutivas:
        text_clean = re.sub(r'\b(\w+)( \1\b)+', r'\1', text_clean)
        # Reemplaza espacios extra
        text_clean = re.sub('[\s]+', ' ', text_clean)
        # y añade un trimzito
        finetweet = text_clean.strip('\'"')
    except:
        raise
    finally:
        return finetweet


class outputhandler(object):

    """
    This Handler perform the processing needed from obtained tweet.
    """

    def __init__(self, outputtype=None):
        """
        """
        if outputtype is None:
            if (sys.version_info) > (3, 4):
                self.output = sys.stdout
            else:
                self.output = codecs.getwriter('utf8')(sys.stdout)
            self.tipo = "stdout"
        if outputtype == "mongodb":
            from tweetdocument import TweetDocument
            self.tipo = "mongodb"
            self.output = TweetDocument
        elif isinstance(outputtype, str):
            self.tipo = "file"
            self.output = codecs.open(outputtype, "a", encoding='utf8')

    def putresult(self, result):
        """
        """
        # validate and complement tweet information:
        #

        # add location:
        logging.info("start final process on tweetid: {}".format(result['id']))
        try:
            if result.get('geo', None):
                if result['geo']['type'] == 'Point':
                    result['location'] = {
                        'lat': result['geo']['coordinates'][0],
                        'lon': result['geo']['coordinates'][1]}
            elif result.get("place", None):
                if result.get('place',
                              {}).get('bounding_box',
                                      {}).get('type', None) == 'Polygon':
                    # calculate polygon centroid.
                    transposed = zip(
                        *result['place']['bounding_box']['coordinates'][0])
                    # sums = map(sum, transposed)
                    averages = map(avg, transposed)
                    result['location'] = {
                        'lat': averages[1], 'lon': averages[0]}
                else:
                    if result.get('place', {}).get('full_name', None):
                        from geopy.geocoders import Nominatim
                        geolocator = Nominatim()
                        loc = geolocator.geocode(result['place']['full_name'])
                        if loc:
                            result['location'] = {
                                "lat": loc.latitude, "lon": loc.longitude}
        except:
            logging.debug("couldn't manage to find location for tweetid: {} ".format(result['id']))
        # add clean text for unique count and training:
        try:
            result['text_clean'] = cleantweet(result['text'])
        except:
            logging.debug("couldn't manage to clean text for tweetid: {} ".format(result['id']))
        # Adding other kind of info: the tweet permalink
        try:
            if not result.get('permalink', None):
                result['permalink'] = u'https://twitter.com/' + \
                    result['user']['screen_name'] + \
                    u'/status/' + str(result['id_str'])
        except:
            pass
        # Processing source to track devices/apps/pages that access twitter:
        try:
            result['source'] = sourceprocessor.match(
                result['source']).groups()[0]
        except:
            logging.debug("couldn't process source for tweetid: {} ".format(result['id']))
        if self.tipo == "file":
            # self.output.write(json.dumps(
            #    result, default=json_util.default,
            #    ensure_ascii=False, encoding='utf8'))
            self.output.write(json.dumps(
                result, default=json.default,
                ensure_ascii=False))
            # and add a new line
            self.output.write("\n")
            logging.info("saving tweetid: {} to json".format(result['id']))
        # elif isinstance(self.output,type(TweetDocument)):
        elif self.tipo == "mongodb":
            # if not a file it is assumed that is a mongodocument
            mongodoc = self.output(id=int(result['id_str']))
            result.pop('id')
            if (sys.version_info) > (3, 4):
                for key, value in result.items():
                    mongodoc[key] = value
            else:
                for key, value in result.iteritems():
                    mongodoc[key] = value
            # and add a new line
            mongodoc.save()
            logging.info("saving tweetid: {} to mongo".format(result['id']))
        elif self.tipo == "stdout":
            # self.output.write(json.dumps(
            #    result, default=json_util.default,
            #    ensure_ascii=False, encoding='utf8'))
            self.output.write(json.dumps(
                result, default=json.default,
                ensure_ascii=False))
            # and add a new line
            self.output.write("\n")
            logging.info("saving tweetid: {} to json".format(result['id']))


def importToMongo(jsonline, directimport=True):
    """
    """
    # if not a file it is assumed that is a mongodocument
    try:
        jsontodict = json.loads(jsonline)
        logging.debug("Starting importing tweetid {} to mongo".format(jsontodict['id']))
        # Check if created_at exists and try to parse it properly:
        if not isinstance(jsontodict['created_at'], datetime.datetime):
            # must parse date
            jsontodict['created_at'] = datetime.datetime.strptime(
                jsontodict['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        else:
            # no need to parse date
            pass
        if directimport:
            from tweetdocument import TweetDocument
            mongodoc = TweetDocument(id=int(jsontodict["id_str"]))
            if (sys.version_info) > (3, 4):
                for key, value in jsontodict.items():
                    mongodoc[key] = value
            else:
                for key, value in jsontodict.iteritems():
                    mongodoc[key] = value
            # and add a new line
            mongodoc.save()
        else:
            resultshandler.putresult(jsontodict)
        logging.debug("Saved tweetid {} to mongo".format(jsontodict['id']))
    except:
        raise
