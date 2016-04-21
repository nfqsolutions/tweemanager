# -*- coding: utf-8 -*-
import sys

resultshandler = None

from tweetdocument import TweetDocument
from bson import json_util
import simplejson as json
import codecs

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
        print(type(self.output))
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
            
            
            

