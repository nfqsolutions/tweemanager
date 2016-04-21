#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hugo M. Marrão Rodrigues, Carlos Perales Gonz
# @Date:   2016-03-02 20:20:57
# @Last Modified by:   cperales
# @Last Modified time: 2016-03-02 23:53:54

import sys

from docopt import docopt

from configparsermanager import ConfigParserManager
from tweepystreamlistener import letslisten,letssearch,nfqTwitterAuth
import utilities

__doc__ = """tweemanager.
NFQ Solutions: this package is at beta stage.

Usage:
  tweemanager (listener|searchtweets|getoldtweets|genconfig) [options]
  tweemanager pairmongoelastic
  tweemanager tweeprocessor [options]
  tweemanager loadtweets [<jsonfile>]
  tweemanager dumptweets [<jsonfile>]

Commands:
  listener       Raise the tweepy listener.
  searchtweets   Access tweets using search API (less than 10 days).
  getoldtweets   Access old tweeters (unofficial API).
  tweeprocessor  Start a server that process tweets.
  loadtweets     load tweets from file.
  dumptweets     dump all tweets.
  genconfig      Generate the tweem.cfg

Options:
  -h --help                             Show this screen.
  --version                             Show version.
  -c <cfgfile> --cfgfile <cfgfile>      Set a config file to be used.
  -o <fout> --output <fout>             Set the output file. If not set it will use stdout.                      
  -y --yes                              Lets you generate the configfile automagicly.
  -w <nworkers> --workers <nworkers>    Workers to use (only makes sense with 
                                        tweeprocessor command).

Comments:
  Check INSTALL.md and USAGE.md to get you started.
  
"""

# Parse command line arguments
arguments = docopt(__doc__, version='tweemanager beta')

# First things first: 
# if no configuration file is given one will use the default one:
# tweem.cfg that is expected to be located at execution path.
if not arguments.get('--cfgfile'):
    arguments['--cfgfile'] = "tweem.cfg"

# Preparing Output file. if non is given stdout will be the one to be used.
utilities.resultshandler = utilities.outputhandler(arguments['--output'])

# if genconfig command is executed it will generate a dummy configfile
if arguments.get('genconfig'):
    # launch a warning and a press any key to continue:
    if not arguments.get('--yes'):
        if raw_input("This operation delete contents from"
          +arguments['--cfgfile']
          +"Really want to continue?[y/n] ").lower()[0] == "n":
            print("Configuration file not generated. Exiting ...")
            sys.exit(0)
    with open(arguments['--cfgfile'],'w') as configfile:
        cfginfo = ConfigParserManager(configfile)
        cfginfo.templateinit()
        cfginfo.write(configfile)
    print("Configuration template file generated: "+arguments['--cfgfile'])
    print("Check USAGE.md to get you started!")
    sys.exit(0)


# read configuration file
cfginfo = ConfigParserManager(arguments['--cfgfile'])
cfginfo.api = nfqTwitterAuth(cfginfo).get_api()

#outputhandler = outputhandler(arguments['--output'])

utilities.resultshandler = utilities.outputhandler(arguments['--output'])

# if mongodb is set add the connection to the the engine.
if (arguments['--output'] == "mongodb"):
    import mongoengine
    mongoengine.connect(
        host = cfginfo.getMongoDBSpecs('host')
    )

if arguments.get('listener'):
    letslisten(cfginfo.api,eval(cfginfo.getListenerSpecs("trackarray")))
    sys.exit(0)


if arguments.get('searchtweets'):
    # TODO: maxtweets should be a input
    # if (arguments['--output'] == "mongodb"):
    #   import mongoengine
    #   mongoengine.connect(
    #     host = cfginfo.getMongoDBSpecs('host')
    #     )
    try:
        maxtweets = int(cfginfo.getSearchSpecs("maxtweets"))
    except:
        maxtweets = 10
    letssearch(cfginfo.api,cfginfo.getSearchSpecs("searchquery"),maxtweets)
    sys.exit(0)
    
#
if arguments.get('getoldtweets'):
    # need a serve for ever:
    from gotsearch import gotsearch
    #get query search:
    try:
        maxtweets = int(cfginfo.getSearchSpecs("maxtweets"))
    except:
        maxtweets = 10
    gotsearch(querySearch=cfginfo.getSearchSpecs("searchquery"),maxTweets=maxtweets)
    sys.exit(0)

#
if arguments.get('loadtweets'):
    import mongoengine
    mongoengine.connect(
        host = cfginfo.getMongoDBSpecs('host')
    )
    #
    # Assume that each document is in one line:
    # 
    print("loadtweets")
    from tweetdocument import importDocuments
    k = 0
    for line in sys.stdin:
        jsonline = line
        importDocuments(line)
        k += 1
    # while 1:
    #     try:
    #         print sys.stdin.readline()
    #         k += 1
    #     except EOFError:
    #         break

    # try:
        
    # except:
    #     sys.stdout.flush()
    #     pass
    sys.exit(0)

#
if arguments.get('dumptweets'):
    print("dumptweets")
    sys.exit(0)
