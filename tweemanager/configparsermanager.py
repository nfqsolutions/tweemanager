#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from ConfigParser import ConfigParser
except:
    from configparser import ConfigParser

# Do this more pythonic:
CFGINFO = None


class ConfigParserManager(ConfigParser):

    """ ConfigParserManager
    A simple extension from ConfigParser.
    """

    TwitterAPIcredentials = "TwitterAPIcredentials"
    ListenerSpecs = "ListenerSpecs"
    SearchSpecs = "SearchSpecs"
    MongoDBSpecs = "MongoDBSpecs"
    GOTSpecs = "GOTSpecs"

    def __init__(self, cpath):
        """
        """
        ConfigParser.__init__(self)
        self.configpath = cpath
        try:
            self.read(self.configpath)
        except:
            pass

    def templateinit(self):
        """
        """
        self.add_section(self.TwitterAPIcredentials)
        self.set(self.TwitterAPIcredentials, "consumer_key", "")
        self.set(self.TwitterAPIcredentials, "consumer_secret", "")
        self.set(self.TwitterAPIcredentials, "access_key", "")
        self.set(self.TwitterAPIcredentials, "access_secret", "")
        self.add_section(self.ListenerSpecs)
        self.set(self.ListenerSpecs, "usersarray", "")
        self.set(self.ListenerSpecs, "trackarray", "")
        self.set(self.ListenerSpecs, "patternstoexclude", "")
        self.set(self.ListenerSpecs, "patternstoinclude", "")
        self.add_section(self.SearchSpecs)
        self.set(self.SearchSpecs, "searchquery", "")
        self.set(self.SearchSpecs, "maxtweets", "")
        self.add_section(self.GOTSpecs)
        self.set(self.GOTSpecs, "username", "")
        self.set(self.GOTSpecs, "since", "")
        self.set(self.GOTSpecs, "until", "")
        self.set(self.GOTSpecs, "querysearch", "")
        self.set(self.GOTSpecs, "maxtweets", "")
        self.add_section(self.MongoDBSpecs)
        self.set(self.MongoDBSpecs, "repocollname", "")
        self.set(self.MongoDBSpecs, "name", "")
        self.set(self.MongoDBSpecs, "username", "")
        self.set(self.MongoDBSpecs, "password", "")
        self.set(self.MongoDBSpecs, "host", "")

    def getTwitterAPIcredentials(self, key):
        """
        """
        result = self.get(self.TwitterAPIcredentials, key)
        if result == '':
            return None
        else:
            return result

    def getListenerSpecs(self, key):
        """
        """
        result = self.get(self.ListenerSpecs, key)
        if result == '':
            return None
        return result

    def getSearchSpecs(self, key):
        """
        """
        result = self.get(self.SearchSpecs, key)
        if result == '':
            return None
        else:
            return result

    def getGOTSpecs(self, key):
        """
        """
        result = None
        try:
            result = self.get(self.GOTSpecs, key)
            if not result:
                raise
        except:
            return None
        finally:
            return result

    def getMongoDBSpecs(self, key):
        """
        """
        try:
            result = self.get(self.MongoDBSpecs, key)
            if result == '':
                raise
        except:
            result = None
        return result
