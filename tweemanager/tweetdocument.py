# -*- coding: utf-8 -*-
import sys
import mongoengine
import simplejson as json
from bson import json_util

class TweetDocument(mongoengine.DynamicDocument):
    """
    DynamicDocument for the mongodb insert
    """
    id = mongoengine.IntField(primary_key=True)
    created_at = mongoengine.DateTimeField()


def importDocuments(jsonline):
    """
    """
    # print jsonline
    # if not a file it is assumed that is a mongodocument
    jsontodict = json_util.loads(jsonline)
    mongodoc = TweetDocument(id=jsontodict["id"])
    if (sys.version_info) > (3,5):
        for key,value in jsontodict.items():
            mongodoc[key] = value
    else:
        for key,value in jsontodict.items():
            mongodoc[key] = value
    # and add a new line
    mongodoc.save()
