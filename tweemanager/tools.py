# -*- coding: utf-8 -*-
import sys

import re
import codecs
import string
import unicodedata
import logging

from bson import json_util as json


repunctuacion = re.compile('[%s]' % re.escape(string.punctuation + '¿¡'))


def avg(items):
    """
    """
    return float(sum(items)) / len(items)


def textclean(rawtext):
    """
    """
    finetweet = ""
    try:
        # Proceso original pero se estaba perdiendo alguna información:
        # Quita los RT's:
        text_clean = rawtext.replace('RT ', '')
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
        logging.debug("unable to clean text {}".format(rawtext))
    finally:
        return finetweet


class GenericTweetProcessor(object):
    """
    """
    SOURCEPROCESSOR = re.compile(r'<a.*?>(.*?)</a>', re.S | re.M)
    PATTERNSTOEXCLUDE = None
    PATTERNSTOINCLUDE = None
    LANGTOINCLUDE = None

    def __init__(self, tweetdata):
        """
        """
        self.tweetdata = tweetdata
        self._setgeo()
        self._buildpermalink()
        self._processsource()
        self._textclean()

    def _setgeo(self):
        """
        """
        logging.debug("checking geo info for tweet id: {}".format(self.tweetdata['id']))
        try:
            if self.tweetdata.get('geo', None):
                if self.tweetdata['geo']['type'] == 'Point':
                    self.tweetdata['location'] = {
                        'lat': self.tweetdata['geo']['coordinates'][0],
                        'lon': self.tweetdata['geo']['coordinates'][1]}
            elif self.tweetdata.get("place", None):
                if self.tweetdata.get('place', {}).get('bounding_box', {}).get('type', None) == 'Polygon':
                    # calculate polygon centroid.
                    transposed = zip(
                        *self.tweetdata['place']['bounding_box']['coordinates'][0])
                    # sums = map(sum, transposed)
                    averages = map(avg, transposed)
                    self.tweetdata['location'] = {
                        'lat': averages[1], 'lon': averages[0]}
                else:
                    if self.tweetdata.get('place', {}).get('full_name', None):
                        from geopy.geocoders import Nominatim
                        geolocator = Nominatim()
                        loc = geolocator.geocode(self.tweetdata['place']['full_name'])
                        if loc:
                            self.tweetdata['location'] = {
                                "lat": loc.latitude, "lon": loc.longitude}
        except:
            logging.debug("couldn't manage to find location for tweetid: {} ".format(self.tweetdata['id']))

    def _buildpermalink(self):
        """
        """
        logging.debug("building permalink for tweet id: {}".format(self.tweetdata['id']))
        try:
            if not self.tweetdata.get('permalink', None):
                self.tweetdata['permalink'] = u'https://twitter.com/' + \
                    self.tweetdata['user']['screen_name'] + \
                    u'/status/' + str(self.tweetdata['id_str'])
        except:
            logging.debug("no permalink set for for tweetid: {} ".format(self.tweetdata['id']))

    def _processsource(self):
        """
        """
        logging.debug("processing source for tweet id: {}".format(self.tweetdata['id']))
        try:
            self.tweetdata['source'] = self.SOURCEPROCESSOR.match(
                self.tweetdata['source']).groups()[0]
            logging.debug("source processed for tweet id: {}".format(self.tweetdata['id']))
        except:
            logging.debug("couldn't process source for tweetid: {} ".format(self.tweetdata['id']))

    def _textclean(self):
        logging.debug("Building text_clean field for tweet id: {} with text {}".format(self.tweetdata['id'], self.tweetdata['text'].encode('utf-8')))
        self.tweetdata['text_clean'] = textclean(self.tweetdata['text'])
        logging.debug("text_clean field set tweet id: {}".format(self.tweetdata['id']))

    def _checkpatterns(self):
        """
        """
        result = True
        logging.debug("checking patterns for tweet id: {}".format(self.tweetdata['id']))
        if (self.PATTERNSTOEXCLUDE is None) and (self.PATTERNSTOINCLUDE is None) and (self.LANGTOINCLUDE is None):
            # All tweets are good to go:
            logging.debug("No patterns to check for tweet id: {}".format(self.tweetdata['id']))
            return result
        else:
            if self.PATTERNSTOEXCLUDE:
                logging.debug("PATTERNSTOEXCLUDE")
                for pattern in self.PATTERNSTOEXCLUDE:
                    if textclean(pattern) in self.tweetdata['text_clean']:
                        logging.debug("patternstoexclude {} found in tweet id: {}".format(pattern,self.tweetdata['id']))
                        result = False
                # checking patterns:
            elif self.PATTERNSTOINCLUDE:
                logging.debug("PATTERNSTOINCLUDE")
                result = False
                for pattern in self.PATTERNSTOINCLUDE:
                    if textclean(pattern) in self.tweetdata['text_clean']:
                        logging.debug("patternstoinclude {} found in tweet id: {}".format(pattern, self.tweetdata['id']))
                        result = True
                # checking patterns:
            if self.LANGTOINCLUDE:
                logging.debug("LANGTOINCLUDE")
                for pattern in self.LANGTOINCLUDE:
                    if textclean(pattern) in self.tweetdata.get('lang',''):
                        logging.debug("langtoinclude {} found in tweet id: {}".format(pattern, self.tweetdata['id']))
                        result = True
        return result

    def sendtooutput(self):
        """
        """
        raise NotImplementedError


class StdoutTweetProcessor(GenericTweetProcessor):
    """
    """
    OUTPUT = None

    def __init__(self, tweetdata):
        """
        """
        GenericTweetProcessor.__init__(self, tweetdata)
        if (sys.version_info) > (3, 4):
            self.OUTPUT = sys.stdout
        else:
            self.OUTPUT = codecs.getwriter('utf8')(sys.stdout)

    def sendtooutput(self):
        """
        """
        if self._checkpatterns():
            logging.debug("writing data to stdout tweet id: {}".format(self.tweetdata['id']))
            self.OUTPUT.write(json.dumps(self.tweetdata,
                                         default=json.default,
                                         ensure_ascii=False))
            self.OUTPUT.write('\n')


class FileTweetProcessor(GenericTweetProcessor):
    """
    """
    OUTPUT = None
    OUTPUT_FILE = None

    def __init__(self, tweetdata):
        """
        """
        GenericTweetProcessor.__init__(self, tweetdata)
        self.OUTPUT = codecs.open(self.OUTPUT_FILE, "a", encoding='utf8')

    def sendtooutput(self):
        """
        """
        if self._checkpatterns():
            logging.debug("writing data to output file tweet id: {}".format(self.tweetdata['id']))
            self.OUTPUT.write(json.dumps(self.tweetdata,
                                         default=json.default,
                                         ensure_ascii=False))
            self.OUTPUT.write('\n')


class MongoTweetProcessor(GenericTweetProcessor):
    """
    """

    def __init__(self, tweetdata):
        """
        """
        GenericTweetProcessor.__init__(self, tweetdata)

    def sendtooutput(self):
        """
        """
        # Import done here due to cfg.
        from dbdocuments import MongoDocument
        if self._checkpatterns():
            logging.debug("writing tweet id: {} in mongodb".format(self.tweetdata['id']))
            # upsert to mongo
            mongodoc = MongoDocument(id=int(self.tweetdata["id_str"]))
            if (sys.version_info) > (3, 4):
                for key, value in self.tweetdata.items():
                    mongodoc[key] = value
            else:
                for key, value in self.tweetdata.iteritems():
                    mongodoc[key] = value
            # and add a new line
            mongodoc.save()
