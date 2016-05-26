#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hugo M. Marrão Rodrigues, Carlos Perales Gonz
# @Date:   2016-03-02 20:20:57
# @Last Modified by:   cperales
# @Last Modified time: 2016-03-02 23:53:54
# system imports
import os
import sys
import traceback
# packages and modules imports
from docopt import docopt
import logging

__doc__ = """tweemanager.
NFQ Solutions: this package is at beta stage.

Usage:
  tweemanager (listener|searchtweets|getoldtweets|genconfig) [options]
  tweemanager pairmongoelastic
  tweemanager tweeprocessor [options]
  tweemanager importToMongo [<jsonfile>]
  tweemanager dumpFromMongo [<jsonfile>]

Commands:
  listener          Raise the tweepy listener.
  searchtweets      Access tweets using search API (less than 10 days).
  getoldtweets      Access old tweeters (unofficial API).
  tweeprocessor     Start a server that process tweets.

  genconfig         Generate the tweem.cfg

  importToMongo     import a json file to mongodb.
  dumpFromMongo     dump data from mongo to a json file.
  dumpFromMongo     dump data from mongo to a json file.

Options:
  -h --help                             Show this screen.
  --version                             Show version.
  --loglevel <loglevel>                 loglevel and command line verbosity:
                                        CRITICAL
                                        ERROR
                                        WARNING
                                        INFO
                                        DEBUG
                                        NOTSET
  -c <cfgfile> --cfgfile <cfgfile>      Set a config file to be used.
  -o <fout> --output <fout>             Set the output file/database.
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

# aux variables:
loglevels = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "NOTSET": logging.NOTSET
}

# Parse command line cmdargs
cmdargs = docopt(__doc__, version='tweemanager beta')

# Setting logging verbosity:
definedloglevel = loglevels.get(cmdargs.get('--loglevel'))
if definedloglevel:
    logging.basicConfig(
        level=loglevels[cmdargs['--loglevel']],
        format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s'
    )
else:
    logging.basicConfig(
        level=logging.INFO,
        #format="[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
        format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s'
    )


# If no configuration file is given one will use the default one:
# tweem.cfg that is expected to be located at execution path.
if not cmdargs.get('--cfgfile'):
    cmdargs['--cfgfile'] = "tweem.cfg"

import configparsermanager as cfgpm

# if genconfig command is the selected one, it will generate a dummy configfile
# using the name handled by cmdargs['--cfgfile'].
if cmdargs.get('genconfig'):
    # launch a warning and a press any key to continue:
    if not cmdargs.get('--yes'):
        try: # Python2 Python3 compat
            input = raw_input
        except NameError:
            pass
        if input("This operation delete contents from \'" +
                 cmdargs['--cfgfile'] +
                 "\', if it exists. \nReally want to continue?[y/n] ").lower()[0] == "n":
            print("Configuration file not generated. Exiting ...")
            sys.exit(0)
    with open(cmdargs['--cfgfile'], 'w') as cfgfile:
        cfgpm.CFGINFO = cfgpm.ConfigParserManager(cfgfile)
        cfgpm.CFGINFO.templateinit()
        cfgpm.CFGINFO.write(cfgfile)
    print("Configuration template file generated: " + cmdargs['--cfgfile'])
    print("Check USAGE.md to get you started!")
    sys.exit(0)

# read configuration file:
cfgpm.CFGINFO = cfgpm.ConfigParserManager(cmdargs['--cfgfile'])

# Preparing Output file. if non is given stdout will be the one to be used.
# Selection is done on outputhandler init method.
import utilities
utilities.resultshandler = utilities.outputhandler(cmdargs['--output'])


# if mongodb is set start the connection for mongoengine.
if (cmdargs['--output'] == "mongodb"):
    logging.debug("Setting a mongo connection to %s" % cfgpm.CFGINFO.getMongoDBSpecs('host'))
    import mongoengine
    mongoengine.connect(
        host=cfgpm.CFGINFO.getMongoDBSpecs('host')
    )
    logging.debug("...done")
    # tweetdocument.TweetsRepoCollName = CFGINFO.getMongoDBSpecs('repocollname')

# listener command
if cmdargs.get('listener'):
    logging.info("listener command start with pid: {}".format(os.getpid()))
    logging.debug("... listener uses oficial API")
    from tweepystreamlistener import nfqTwitterAuth
    cfgpm.CFGINFO.api = nfqTwitterAuth(cfgpm.CFGINFO).get_api()
    from tweepystreamlistener import letslisten
    letslisten(cfgpm.CFGINFO.api, eval(cfgpm.CFGINFO.getListenerSpecs("trackarray")))
    sys.exit(0)

# searchtweets command
if cmdargs.get('searchtweets'):
    logging.info("searchtweets command start with pid: {}".format(os.getpid()))
    logging.debug("... searchtweets uses oficial API")
    try:
        from tweepystreamlistener import nfqTwitterAuth
        cfgpm.CFGINFO.api = nfqTwitterAuth(cfgpm.CFGINFO).get_api()
        from tweepystreamlistener import letssearch
        try:
            maxtweets = int(cfgpm.CFGINFO.getSearchSpecs("maxtweets"))
        except:
            maxtweets = 10
        letssearch(cfgpm.CFGINFO.api, cfgpm.CFGINFO.getSearchSpecs("searchquery"), maxtweets)
        logging.info("searchtweets command done.")
        if cmdargs['--output']:
            logging.info("check {} file for results".format(cmdargs['--output']))
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        formatted_traceback = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for traceback_line in formatted_traceback:
            logging.info(traceback_line)
        logging.info("searchtweets with errors.")
    sys.exit(0)

# getoldtweets command
if cmdargs.get('getoldtweets'):
    # need a serve for ever:
    logging.info("getoldtweets command start with pid: {}".format(os.getpid()))
    try:
        from gotsearch import gotsearch
        # get query search:
        gotsearch(
            username=cfgpm.CFGINFO.getGOTSpecs("username"),
            since=cfgpm.CFGINFO.getGOTSpecs("since"),
            until=cfgpm.CFGINFO.getGOTSpecs("until"),
            querySearch=cfgpm.CFGINFO.getGOTSpecs("querysearch"),
            maxTweets=int(cfgpm.CFGINFO.getGOTSpecs("maxtweets")))
        logging.info("getoldtweets command done.")
        if cmdargs['--output']:
            logging.info("check {} file for results".format(cmdargs['--output']))
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        formatted_traceback = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for traceback_line in formatted_traceback:
            logging.info(traceback_line)
        logging.info("getoldtweets with errors.")
    sys.exit(0)

# importToMongo command
if cmdargs.get('importToMongo'):
    print('Reading, processing and importing json documents to mongo')
    # mongoengine connection:
    # This command doesn't need the output flag so
    # a connection is set either way.
    import mongoengine
    mongoengine.connect(
        host=cfgpm.CFGINFO.getMongoDBSpecs('host')
    )
    # tweetdocument.TweetsRepoCollName = CFGINFO.getMongoDBSpecs('repocollname')
    # Assume that each document is in one line:
    # if no file is given it will load from stdin
    utilities.resultshandler = utilities.outputhandler('mongodb')
    if (cmdargs['<jsonfile>']):
        print("Using file reader process data.")
        print("Note: File must be a line separated json (jsonline) and not a json array.")
        inputprocess = open(cmdargs['<jsonfile>'], 'r')
    else:
        print("Using stdin to process json data. One json per line.")
        print("Note: for really large jsons, use pipes. ej: \'< or |\' .")
        inputprocess = sys.stdin
    spinner = spinning_cursor()
    # from utilities import importToMongo
    while 1:
        try:
            line = inputprocess.readline()
            if not line:
                break
            utilities.importToMongo(line) # You can write importToMongo(line,directimport=True)
            try:
                sys.stdout.write(next(spinner))
                sys.stdout.flush()
                sys.stdout.write('\b')
            except:
                raise
        except ValueError:
            print("Error in json:" + line)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            formatted_traceback = traceback.format_exception(exc_type, exc_value, exc_traceback)
            for traceback_line in formatted_traceback:
                print(traceback_line)
        except:
            raise
            break
    sys.exit(0)

#
if cmdargs.get('dumptweets'):
    print("dumptweets")
    print("TO BE DONE: it should be implemented.")
    print("possibly using mongo export directly.")
    sys.exit(0)
