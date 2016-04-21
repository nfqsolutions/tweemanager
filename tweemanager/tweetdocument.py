# -*- coding: utf-8 -*-

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
	for key,value in jsontodict.iteritems():
		mongodoc[key] = value
	# and add a new line
	mongodoc.save()
