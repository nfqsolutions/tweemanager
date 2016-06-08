# -*- coding: utf-8 -*-

import os
import sys
import docopt
import logging
import traceback
import mongoengine
from .getoldtweets import setTweetCriteria, getoldtweetsGenerator
from .searchlistenerAPI import listenertweets, searchtweets
from .tools import StdoutTweetProcessor, FileTweetProcessor, MongoTweetProcessor
from bson import json_util as json
from .settings import cfgmanager
from .version import __version__
#
TweetProcessor = None


def tweemanager():
    """ tweemanager:
    NFQ Solutions: this package is at beta-rc stage.

    Usage:
        tweemanager (listener|searchtweets|getoldtweets)
                    [--c <cfgfile> | --cfgjsonstr <cfgjsonstr>]
                    [options]
        tweemanager genconfig [options]
        tweemanager reporting [options]
        tweemanager --version

    Options:
        --logfile <logfile>                 log file name:
        --loglevel <loglevel>               loglevel and command line verbosity:
                                                CRITICAL
                                                ERROR
                                                WARNING
                                                INFO
                                                DEBUG
                                                NOTSET
        -c <cfgfile> --cfgfile <cfgfile>    Set a config file to be used.
        --cfgjsonstr <cfgjsonstr>           Set a config json string to be used.
        -o <fout> --output <fout>           Set the output file/database.
                                            If not set it will use stdout.

    Complements:
        --resetall                          Option for reporting. Will reset all reports
                                            and generate new ones.
        -h --help                           Show this screen.
        --version                           Show version.

    """
    #
    # Arguments Handling and Validation
    #
    args = docopt.docopt(tweemanager.__doc__,version=__version__)
    #
    # Arguments Handling Done
    #
    # #########################################################################
    #
    # Config Handling
    #
    config = cfgmanager()
    if args['--cfgfile'] and args['--cfgjsonstr']:
        print(Exception("ERROR: you cannot provide two configuration options\n" +
                        "       use only one option (--cfgjsonstr | --cfgfile)"))
        sys.exit(0)
    if args['--cfgjsonstr']:
        # given a jsonstring:
        print('config via json string')
        config.readfromjsonstr(args['--cfgjsonstr'])
    elif args['--cfgfile']:
        # given a cfgfile:
        cfgfile, cfgfile_extension = os.path.splitext(args['--cfgfile'])
        if cfgfile_extension.lower() == '.json':
            print('.json')
            config.readfromjsonfile(args['--cfgfile'])
        elif cfgfile_extension.lower() == '.ini' or cfgfile_extension.lower() == '.cfg':
            print('.ini/.cfg')
            config.readfromfile(args['--cfgfile'])
        else:
            print(Exception("ERROR: unkown file extension for given file '{0}{1}'".format(cfgfile, cfgfile_extension)))
            sys.exit(0)
    else:
        # if no configuration is given it will use tweem.cfg that will be created
        # at runtime directory.
        try:
            # check if file exists isn
            args['--cfgfile'] = "tweem.json"
            config.readfromjsonfile(args['--cfgfile'])
        except:

            args['--cfgfile'] = "tweem.cfg"
            config.readfromfile(args['--cfgfile'])
    cfgmanager.setconfigassettings(config._sections)
    #
    # Config Handling
    #
    # #########################################################################
    #
    # command genconfig
    #
    if args['genconfig']:
        print('genconfig command activated')
        print('Done')
        return
    #
    # command genconfig Done
    #
    # #########################################################################
    #
    # logging basic config
    #
    loglevels = {
        "CRITICAL": logging.CRITICAL,
        "ERROR": logging.ERROR,
        "WARNING": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
        "NOTSET": logging.NOTSET
    }
    # Build default using config file:
    if (sys.version_info) >= (3, 4):
        cfgit = cfgmanager.LogSpecs.items()
    else:
        cfgit = cfgmanager.LogSpecs.iteritems()
    for key, value in cfgit:
        if key == 'loglevel':
            if not value or value is None:
                cfgmanager.LogSpecs['loglevel'] = 'INFO'
        if key == 'logfile':
            if not value or value is None:
                cfgmanager.LogSpecs['logfile'] = None
    # overwritting if command line options:
    if args['--loglevel']:
        cfgmanager.LogSpecs['loglevel'] = args['--loglevel']
    if args['--logfile']:
        cfgmanager.LogSpecs['logfile'] = args['--logfile']
    # start the logger:
    logging.basicConfig(
        level=loglevels[cfgmanager.LogSpecs['loglevel']],
        format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
        filename=cfgmanager.LogSpecs['logfile']
    )
    logging.info("logging configuration done")
    logging.debug("using configuration {}".format(dict(cfgmanager.LogSpecs)))
    #
    # logging basic config Done
    #
    # #########################################################################
    #
    # TweetHandler
    #
    # Setting output
    if args['--output']:
        if args['--output'] == 'mongodb':
            logging.info('Setting output to {}'.format(args['--output']))
            mongoengine.connect(host=cfgmanager.MongoDBSpecs['host'])
            TweetProcessor = MongoTweetProcessor
        else:
            logging.info('Setting default output to {}'.format(args['--output']))
            FileTweetProcessor.OUTPUT_FILE = args['--output']
            TweetProcessor = FileTweetProcessor
    else:
        logging.info('Setting default output to stdout')
        TweetProcessor = StdoutTweetProcessor
    # Setting output done
    # Setting TextPatterns
    logging.info("Setting TextPatterns")
    logging.debug("using TextPatterns {}".format(dict(cfgmanager.TextPatterns)))
    TweetProcessor.PATTERNSTOEXCLUDE = cfgmanager.TextPatterns['patternstoexclude']
    TweetProcessor.PATTERNSTOINCLUDE = cfgmanager.TextPatterns['patternstoinclude']
    TweetProcessor.LANGTOINCLUDE = cfgmanager.TextPatterns['langtoinclude']
    logging.info("Setting TextPatterns Done")
    # Setting TextPatterns Done
    # #########################################################################
    #
    # command listener
    #
    if args['listener']:
        try:
            logging.info('listener command activated')
            listenertweets(TweetProcessor, cfgmanager.ListenerSpecs['trackarray'])
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            formatted_traceback = traceback.format_exception(exc_type, exc_value, exc_traceback)
            for traceback_line in formatted_traceback:
                logging.critical(traceback_line)
            logging.critical('Error in searchtweets command')
        return
    # #########################################################################
    #
    # command searchtweets
    #
    if args['searchtweets']:
        try:
            logging.info('searchtweets command selected')
            searchtweets(TweetProcessor, cfgmanager.SearchSpecs['searchquery'], maxtweets=cfgmanager.SearchSpecs['maxtweets'])
            logging.info('searchtweets command Done')
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            formatted_traceback = traceback.format_exception(exc_type, exc_value, exc_traceback)
            for traceback_line in formatted_traceback:
                logging.critical(traceback_line)
            logging.critical('Error in searchtweets command')
        finally:
            return
    #
    # command searchtweets Done
    #
    # #########################################################################
    #
    # command getoldtweets
    #
    if args['getoldtweets']:
        try:
            logging.info('getoldtweets command selected')
            tweetCriteria = setTweetCriteria(
                username=cfgmanager.GOTSpecs['username'],
                since=cfgmanager.GOTSpecs['since'],
                until=cfgmanager.GOTSpecs['until'],
                querySearch=cfgmanager.GOTSpecs['querysearch'],
                maxTweets=cfgmanager.GOTSpecs['maxtweets'])

            for tweet in getoldtweetsGenerator(tweetCriteria):
                posttweet = TweetProcessor(tweet)
                posttweet.sendtooutput()
            logging.info('getoldtweets command Done')
        except:
            logging.critical('Error in getoldtweets command')
        finally:
            return
    #
    # command getoldtweets Done
    #
    # #########################################################################
    #
    # command reporting
    #
    if args['reporting']:
        logging.info('reporting command selected')
        logging.debug('Not implemented')
        return
    #
    # command reporting Done
    #
    # #########################################################################
    #
    # command importToMongo
    #
    if args['importToMongo']:
        logging.info('importToMongo command selected')
        return
    #
    # command importToMongo Done
    #
    # #########################################################################
    #
    # command dumpFromMongo
    #
    if args['dumpCorpusFromMongo']:
        logging.info('importToMongo command selected')
        logging.debug('Not implemented')
        return
    #
    # command dumpFromMongo Done
    #
    # #########################################################################
    #
    # command importToElastic
    #
    if args['importToElastic']:
        logging.info('importToMongo command selected')
        logging.debug('Not implemented')
        return
    #
    # command importToElastic Done
    #
    # #########################################################################
    #
    # command mongo2elastic
    #
    if args['mongo2elastic']:
        logging.info('mongo2elastic command selected')
        logging.debug('Not implemented')
        return
    #
    # command mongo2elastic Done
    #
    # #########################################################################


if __name__ == '__main__':
    sys.exit(tweemanager())
