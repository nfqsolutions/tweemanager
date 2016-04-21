# -*- coding: utf-8 -*-

from ConfigParser import ConfigParser

class ConfigParserManager(ConfigParser):
	""" ConfigParserManager
	A simple extension from ConfigParser.
	"""

	TwitterAPIcredentials = "TwitterAPIcredentials"
	ListenerSpecs = "ListenerSpecs"
	SearchSpecs = "SearchSpecs"
	MongoDBSpecs = "MongoDBSpecs"

	def __init__(self,cpath):
		"""
		"""
		ConfigParser.__init__(self)
		self.configpath = cpath
		self.read(self.configpath)

	def templateinit(self):
		"""
		"""
		
		self.add_section(self.TwitterAPIcredentials)
		self.set(self.TwitterAPIcredentials,"consumer_key",)
		self.set(self.TwitterAPIcredentials,"consumer_secret",)
		self.set(self.TwitterAPIcredentials,"access_key",)
		self.set(self.TwitterAPIcredentials,"access_secret",)
		self.add_section(self.ListenerSpecs)
		self.set(self.ListenerSpecs,"usersarray",)
		self.set(self.ListenerSpecs,"trackarray",)
		self.set(self.ListenerSpecs,"patternstoexclude",)
		self.set(self.ListenerSpecs,"patternstoinclude",)
		self.add_section(self.SearchSpecs)
		self.set(self.SearchSpecs,"searchquery",)
		self.set(self.SearchSpecs,"maxtweets",)
		self.add_section(self.mongodb)
		self.set(self.MongoDBSpecs,"name",)
		self.set(self.MongoDBSpecs,"username",)
		self.set(self.MongoDBSpecs,"password",)
		self.set(self.MongoDBSpecs,"host",)

	def getTwitterAPIcredentials(self,key):
		"""
		"""
		return self.get(self.TwitterAPIcredentials,key)

	def getListenerSpecs(self,key):
		"""
		"""
		return self.get(self.ListenerSpecs,key)

	def getSearchSpecs(self,key):
		"""
		"""
		return self.get(self.SearchSpecs,key)

	def getMongoDBSpecs(self,key):
		"""
		"""
		
		try:
			result = self.get(self.MongoDBSpecs,key)
		except:
			result = None
		return result