# -*- coding: utf-8 -*-
import sys

resultshandler = None

from tweetdocument import TweetDocument
from bson import json_util
import simplejson as json
import codecs

def avg(items):
    return float(sum(items)) / len(items)

class outputhandler(object):
    """
    This Handler perform the processing needed from obtained tweet.
    """

    def __init__(self,outputtype=None):
        """
        """
        if outputtype is None:
            if (sys.version_info) > (3,5):
                self.output = sys.stdout
            else:
                self.output = codecs.getwriter('utf8')(sys.stdout)
            self.tipo = "stdout"
        if outputtype == "mongodb":
            self.tipo = "mongodb"
            self.output = TweetDocument
        elif isinstance(outputtype,str):
            self.tipo = "file"
            #self.output = open(outputtype,'a')
            self.output = codecs.open(outputtype, "a", encoding='utf8')

    def putresult(self,result):
        """
        """
        # validate and complement information:
        # 
        
        # add location:

        try:
            if result.get('geo',None):
                if result['geo']['type'] == 'Point':
                    result['location'] = {'lat':result['geo']['type'][0],'lon':result['geo']['type'][1]}
            elif result.get("place",None):
                if result.get('place',{}).get('bounding_box',{}).get('type',None) == 'Polygon':
                    # calculate polygon centroid.
                    transposed = zip(*result['place']['bounding_box']['coordinates'][0])
                    # sums = map(sum, transposed)
                    averages = map(avg, transposed)
                    result['location'] = {'lat':averages[1],'lon':averages[0]}
                else:
                    if result.get('place',{}).get('full_name',None):
                        print("has full name")
                        print(result['place']['full_name'])
                        from geopy.geocoders import Nominatim
                        geolocator = Nominatim()
                        loc = geolocator.geocode(result['place']['full_name'])
                        if loc:
                            result['location'] =  {"lat" : loc.latitude,"lon" : loc.longitude}
        except:
            pass
        # add clean text for unique count and training:
        try:
            text_clean = result['text']
            result['text_clean'] = " ".join(filter(lambda x:(x[0]!=u'#' and x[0]!=u'@' and x[0:4]!=u'http'), text_clean.split()))
        except:
            pass
        # Adding other kind of info: the tweet permalink
        try:
            if not result.get('permalink',None):
                result['permalink'] = u'https://twitter.com/'+result['user']['screen_name']+u'/status/'+unicode(result['id'])
        except:
            pass
        if self.tipo == "file":
            self.output.write(json.dumps(result, default=json_util.default, ensure_ascii=False, encoding='utf8'))
            # and add a new line
            self.output.write("\n")
        #elif isinstance(self.output,type(TweetDocument)):
        elif self.tipo == "mongodb":
            # if not a file it is assumed that is a mongodocument
            mongodoc = self.output(id=result['id'])
            if (sys.version_info) > (3,5):
                for key,value in result.items():
                                        mongodoc[key] = value
            else:
                for key,value in result.iteritems():
                    mongodoc[key] = value
            # and add a new line
            mongodoc.save()
        elif self.tipo == "stdout":
            self.output.write(json.dumps(result, default=json_util.default, ensure_ascii=False, encoding='utf8'))
            # and add a new line
            self.output.write("\n")
            
            
            

