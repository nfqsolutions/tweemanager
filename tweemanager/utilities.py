# -*- coding: utf-8 -*-

import sys
from tweetdocument import TweetDocument
from bson import json_util as json
import codecs
import re
import string
import unicodedata


resultshandler = None

punctuacion = set(string.punctuation + '¿¡')
repunctuacion = re.compile('[%s]' % re.escape(string.punctuation))
sourceprocessor = re.compile(r'<a.*?>(.*?)</a>', re.S | re.M)


def avg(items):
    return float(sum(items)) / len(items)


class outputhandler(object):
    """
    This Handler perform the processing needed from obtained tweet.
    """

    def __init__(self, outputtype=None):
        """
        """
        if outputtype is None:
            if (sys.version_info) > (3, 5):
                self.output = sys.stdout
            else:
                self.output = codecs.getwriter('utf8')(sys.stdout)
            self.tipo = "stdout"
        if outputtype == "mongodb":
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
                        print("has full name")
                        print(result['place']['full_name'])
                        from geopy.geocoders import Nominatim
                        geolocator = Nominatim()
                        loc = geolocator.geocode(result['place']['full_name'])
                        if loc:
                            result['location'] = {
                                "lat": loc.latitude, "lon": loc.longitude}
        except:
            pass
        # add clean text for unique count and training:
        try:
            # Proceso original pero se estaba perdiendo alguna información:
            # Quita los RT's:
            text_clean = result['text'].replace('RT ', '')
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
            text_clean = ''.join((c for c in unicodedata.normalize(
                'NFD', text_clean) if unicodedata.category(c) != 'Mn'))
            # Limpia palabras repetidas y consecutivas:
            text_clean = re.sub(r'\b(\w+)( \1\b)+', r'\1', text_clean)
            # Reemplaza espacios extra
            text_clean = re.sub('[\s]+', ' ', text_clean)
            # y añade un trimzito
            result['text_clean'] = text_clean.strip('\'"')
        except:
            raise
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
            pass
        if self.tipo == "file":
            # self.output.write(json.dumps(
            #    result, default=json_util.default,
            #    ensure_ascii=False, encoding='utf8'))
            self.output.write(json.dumps(
                result, default=json.default,
                ensure_ascii=False))
            # and add a new line
            self.output.write("\n")
        # elif isinstance(self.output,type(TweetDocument)):
        elif self.tipo == "mongodb":
            # if not a file it is assumed that is a mongodocument
            mongodoc = self.output(id=int(result['id_str']))
            result.pop('id')
            if (sys.version_info) > (3, 5):
                for key, value in result.items():
                    mongodoc[key] = value
            else:
                for key, value in result.iteritems():
                    mongodoc[key] = value
            # and add a new line
            mongodoc.save()
        elif self.tipo == "stdout":
            # self.output.write(json.dumps(
            #    result, default=json_util.default,
            #    ensure_ascii=False, encoding='utf8'))
            self.output.write(json.dumps(
                result, default=json.default,
                ensure_ascii=False))
            # and add a new line
            self.output.write("\n")
