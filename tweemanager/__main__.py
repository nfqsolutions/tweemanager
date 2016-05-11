#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hugo M. Marrão Rodrigues, Carlos Perales Gonz
# @Date:   2016-03-02 20:20:57
# @Last Modified by:   cperales
# @Last Modified time: 2016-03-02 23:53:54
# system imports
import sys
# packages and modules imports
from docopt import docopt
import configparsermanager

__doc__ = """tweemanager.
NFQ Solutions: this package is at beta stage.

Usage:
  tweemanager (listener|searchtweets|getoldtweets|genconfig) [options]
  tweemanager pairmongoelastic
  tweemanager tweeprocessor [options]
  tweemanager importToMongo [<jsonfile>]
  tweemanager dumpFromMongo [<jsonfile>]

Commands:
  listener       Raise the tweepy listener.
  searchtweets   Access tweets using search API (less than 10 days).
  getoldtweets   Access old tweeters (unofficial API).
  tweeprocessor  Start a server that process tweets.

  genconfig      Generate the tweem.cfg

  importToMongo     import a json file to mongodb.
  dumpFromMongo     dump data from mongo to a json file.
  dumpFromMongo     dump data from mongo to a json file.

Options:
  -h --help                             Show this screen.
  --version                             Show version.
  -c <cfgfile> --cfgfile <cfgfile>      Set a config file to be used.
  -o <fout> --output <fout>             Set the output file.
                                        If not set it will use stdout.
  -y --yes                              Lets you generate the configfile
                                        automagicly.
  -w <nworkers> --workers <nworkers>    Workers to use (only makes sense with
                                        tweeprocessor command).

Comments:
  Check INSTALL.md and USAGE.md to get you started.

"""


# Command-line spinner:
def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor

# Parse command line arguments
arguments = docopt(__doc__, version='tweemanager beta')

# If no configuration file is given one will use the default one:
# tweem.cfg that is expected to be located at execution path.
if not arguments.get('--cfgfile'):
    arguments['--cfgfile'] = "tweem.cfg"

import configparsermanager

# if genconfig command is the selected one, it will generate a dummy configfile
# using the name handled by arguments['--cfgfile'].
if arguments.get('genconfig'):
    # launch a warning and a press any key to continue:
    if not arguments.get('--yes'):
        if input("This operation delete contents from" +
                 arguments['--cfgfile'] +
                 "Really want to continue?[y/n] ").lower()[0] == "n":
            print("Configuration file not generated. Exiting ...")
            sys.exit(0)
    with open(arguments['--cfgfile'], 'w') as configfile:
        configparsermanager.CFGINFO = configparsermanager.ConfigParserManager(configfile)
        configparsermanager.CFGINFO.templateinit()
        configparsermanager.CFGINFO.write(configfile)
    print("Configuration template file generated: " + arguments['--cfgfile'])
    print("Check USAGE.md to get you started!")
    sys.exit(0)

# read configuration file:
configparsermanager.CFGINFO = configparsermanager.ConfigParserManager(arguments['--cfgfile'])

from tweepystreamlistener import nfqTwitterAuth

configparsermanager.CFGINFO.api = nfqTwitterAuth(configparsermanager.CFGINFO).get_api()

# Preparing Output file. if non is given stdout will be the one to be used.
# Selection is done on outputhandler init method.
import utilities
utilities.resultshandler = utilities.outputhandler(arguments['--output'])


# if mongodb is set start the connection for mongoengine.
if (arguments['--output'] == "mongodb"):
    import mongoengine
    mongoengine.connect(
        host=configparsermanager.CFGINFO.getMongoDBSpecs('host')
    )
    # tweetdocument.TweetsRepoCollName = CFGINFO.getMongoDBSpecs('repocollname')

# listener command
if arguments.get('listener'):
    from tweepystreamlistener import letslisten
    letslisten(configparsermanager.CFGINFO.api, eval(configparsermanager.CFGINFO.getListenerSpecs("trackarray")))
    sys.exit(0)

# searchtweets command
if arguments.get('searchtweets'):
    from tweepystreamlistener import letssearch
    try:
        maxtweets = int(configparsermanager.CFGINFO.getSearchSpecs("maxtweets"))
    except:
        maxtweets = 10
    letssearch(configparsermanager.CFGINFO.api, configparsermanager.CFGINFO.getSearchSpecs("searchquery"), maxtweets)
    sys.exit(0)

# getoldtweets command
if arguments.get('getoldtweets'):
    # need a serve for ever:
    from gotsearch import gotsearch
    # get query search:
    try:
        maxtweets = int(configparsermanager.CFGINFO.getSearchSpecs("maxtweets"))
    except:
        maxtweets = 10
    gotsearch(querySearch=configparsermanager.CFGINFO.getSearchSpecs(
        "searchquery"), maxTweets=maxtweets)
    sys.exit(0)

# importToMongo command
if arguments.get('importToMongo'):
    print('Reading, processing and importing json documents to mongo')
    # mongoengine connection:
    # This command doesn't need the output flag so
    # a connection is set either way.
    import mongoengine
    mongoengine.connect(
        host=configparsermanager.CFGINFO.getMongoDBSpecs('host')
    )
    # tweetdocument.TweetsRepoCollName = CFGINFO.getMongoDBSpecs('repocollname')
    # Assume that each document is in one line:
    # if no file is given it will load from stdin
    utilities.resultshandler = utilities.outputhandler('mongodb')
    if (arguments['<jsonfile>']):
        print("Using file reader process data.")
        print("Note: File must be a json per line and not a json array.")
        inputprocess = open(arguments['<jsonfile>'], 'r')
    else:
        inputprocess = sys.stdin
        print("Using stdin to process json data.")
        print("Note: for really large jsons, use pipes. ej: \'< or |\' .")
    spinner = spinning_cursor()
    # from utilities import importToMongo
    while 1:
        try:
            line = inputprocess.readline()
            if not line:
                break
            utilities.importToMongo(line)
            try:
                sys.stdout.write(next(spinner))
                sys.stdout.flush()
                sys.stdout.write('\b')
            except:
                raise
        except ValueError:
            print("Error in json:" + line)
        except:
            raise
            break
    sys.exit(0)

#
if arguments.get('dumptweets'):
    print("dumptweets")
    print("TO BE DONE: it should be implemented.")
    print("possibly using mongo export directly.")
    sys.exit(0)
