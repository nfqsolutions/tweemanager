# -*- coding: utf-8 -*-
import sys
import codecs
from bson import json_util as json

try:
    from ConfigParser import RawConfigParser
except:
    from configparser import RawConfigParser


class cfgmanager(RawConfigParser):
    """ """

    TwitterAPIcredentials = {}
    ListenerSpecs = {}
    SearchSpecs = {}
    GOTSpecs = {}
    TextPatterns = {}
    MongoDBSpecs = {}
    ElasticSpecs = {}
    LogSpecs = {}

    def __init__(self, filename=None, jsonstr=None):
        """
        """
        if filename:
            self.filename = filename
        else:
            self.filename = 'tweem.cfg'
        RawConfigParser.__init__(self)
        self.add_section('TwitterAPIcredentials')
        self.set('TwitterAPIcredentials', 'consumer_key', '')
        self.set('TwitterAPIcredentials', 'consumer_secret', '')
        self.set('TwitterAPIcredentials', 'access_key', '')
        self.set('TwitterAPIcredentials', 'access_secret', '')
        self.add_section('ListenerSpecs')
        self.set('ListenerSpecs', 'usersarray', '')
        self.set('ListenerSpecs', 'trackarray', '')
        self.add_section('SearchSpecs')
        self.set('SearchSpecs', 'searchquery', '')
        self.set('SearchSpecs', 'maxtweets', '')
        self.add_section('GOTSpecs')
        self.set('GOTSpecs', 'username', '')
        self.set('GOTSpecs', 'since', '')
        self.set('GOTSpecs', 'until', '')
        self.set('GOTSpecs', 'querysearch', '')
        self.set('GOTSpecs', 'maxtweets', '')
        self.add_section('TextPatterns')
        self.set('TextPatterns', 'patternstoexclude', '')
        self.set('TextPatterns', 'patternstoinclude', '')
        self.set('TextPatterns', 'langtoinclude', '')
        self.add_section('MongoDBSpecs')
        self.set('MongoDBSpecs', 'repocollname', '')
        self.set('MongoDBSpecs', 'name', '')
        self.set('MongoDBSpecs', 'username', '')
        self.set('MongoDBSpecs', 'password', '')
        self.set('MongoDBSpecs', 'host', '')
        self.add_section('ElasticSpecs')
        self.set('ElasticSpecs', 'host', '')
        self.set('ElasticSpecs', 'index', '')
        self.set('ElasticSpecs', 'username', '')
        self.set('ElasticSpecs', 'password', '')
        self.add_section('LogSpecs')
        self.set('LogSpecs', 'loglevel', '')
        self.set('LogSpecs', 'logfile', '')

    def _write(self, fp):
        """ Configparser write method modified to correct process data from/to json
        Write an .ini-format representation of the configuration state.
        """
        DEFAULTSECT = "DEFAULT"
        if self._defaults:
            fp.write("[%s]\n" % DEFAULTSECT)
            for (key, value) in self._defaults.items():
                fp.write("%s = %s\n" % (key, str(value).replace('\n', '\n\t')))
            fp.write("\n")
        for section in self._sections:
            fp.write("[%s]\n" % section)
            for (key, value) in self._sections[section].items():
                if key == "__name__":
                    continue
                if value == 'null':
                    key = key + " = "
                elif (value is not None) or (self._optcre == self.OPTCRE):
                    if (sys.version_info) >= (3, 4):
                        key = " = ".join((key, str(value).replace('\n', '\n\t')))
                    elif (sys.version_info) <= (2, 7):
                        key = " = ".join((key, str(value).decode('utf-8').replace('\n', '\n\t')))
                fp.write("%s\n" % (key))
            fp.write("\n")

    def writetofile(self, filename=None):
        """
        """
        if filename:
            self.filename = filename
        for section in self.sections():
            for key, value in self.items(section):
                try:
                    self.set(section, key, json.dumps(value, default=json.default, ensure_ascii=False).encode('utf-8'))
                except ValueError:
                    self.set(section, key, None)
        self._write(codecs.open(self.filename, 'wb+', 'utf-8'))
        # get data back from written file:
        self.readfromfile(self.filename)

    def readfromfile(self, filename=None):
        """
        """
        if filename:
            self.filename = filename
        self.read(self.filename)
        # read proper data using json loads to properly parse strings:
        for section in self.sections():
            for key, value in self.items(section):
                try:
                    if (sys.version_info) >= (3, 4):
                        self.set(section, key, json.loads(value))
                    else:
                        self.set(section, key, json.loads(value.decode('utf-8')))
                except ValueError:
                    self.set(section, key, None)

    def writetojsonstr(self):
        """
        """
        # read proper data using json loads to properly parse strings:
        return json.dumps(self.__dict__['_sections'], default=json.default, ensure_ascii=False)

    def readfromjsonstr(self, jsonstr):
        """
        """
        # read proper data using json loads to properly parse strings:
        data = json.loads(jsonstr)
        for section, value in data.iteritems():
            for item, val in value.iteritems():
                self.set(section, item, val)
        #return json.dumps(self.__dict__['_sections'],default=json.default,ensure_ascii=False)

    def readfromjsonfile(self, filename=None):
        """
        """
        with codecs.open(filename, 'r', 'utf-8') as cfgfile:
            jsonstr = cfgfile.read().replace('\n', '')
        self.readfromjsonstr(jsonstr)

    @classmethod
    def setconfigassettings(cls, sections):
        """
        """
        if (sys.version_info) >= (3, 4):
            secit = sections.items()
        else:
            secit = sections.iteritems()
        for section, value in secit:
            setattr(cls, section, value)
