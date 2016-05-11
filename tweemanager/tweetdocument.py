# -*- coding: utf-8 -*-
import sys
import mongoengine
from bson import json_util
import utilities
import datetime


class TweetDocument(mongoengine.DynamicDocument):
    """
    DynamicDocument for the mongodb insert
    """
    meta = {'collection': 'Tweets'}
    id = mongoengine.LongField(primary_key=True)
    created_at = mongoengine.DateTimeField()


def importToMongo(jsonline, directimport=False):
    """
    """
    # if not a file it is assumed that is a mongodocument
    try:
        jsontodict = json_util.loads(jsonline)
        # If the json comes from elasticsearch
        jsontodict = jsontodict['_source']
        
        # Homogenize the information
        try:
            print(jsontodict['created_at'])
        except:
            jsontodict['created_at'] = jsontodict['tweettime']
            print(jsontodict['created_at'])

        # Check if created_at exists and try to parse it properly:
        if not isinstance(jsontodict['created_at'], datetime.datetime):
            # must parse date
            jsontodict['created_at'] = datetime.datetime.strptime(
                jsontodict['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        else:
            # no need to parse date
            pass
        if directimport:
            mongodoc = TweetDocument(id=int(jsontodict["id_str"]))
            if (sys.version_info) > (3, 5):
                for key, value in jsontodict.items():
                    mongodoc[key] = value
            else:
                for key, value in jsontodict.iteritems():
                    mongodoc[key] = value
            # and add a new line
            mongodoc.save()
        else:
            utilities.resultshandler.putresult(jsontodict)
    except:
        raise
