#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This Script is a template to show how to populate mongo information using a Classifier.

import pymongo
import random
# one could use the mongoengine but for this case we will use pymongo instead.


def classifyTweets(mongouri="mongodb://127.0.0.1:27017/", dbname='tweets', collname='Tweets'):
    """
    """
    # start a connection:
    client = pymongo.MongoClient(mongouri)
    db = client[dbname]
    coll = db[collname]
    # This script will perform a dummy classification on mongo tweets.

    def getDummyValoration():
        """
        """
        # It will randomly generate information like this:
        # {valuation:{manual:positive,
        #              classifier1:{prob:0.7
        #                           value:positive}}}
        # or
        # {valuation:{classifier1:{prob:0.7
        #                           value:positive}}}
        #
        manual = random.uniform(0, 1)
        classifier1 = random.uniform(0, 1)

        if manual > 0.7:
            valuation = {'valuation': {'manual': 'positive' if classifier1 > 0.5 else 'negative',
                                        'classifier1': {'prob': classifier1,
                                                       'value': 'positive' if classifier1 > 0.5 else 'negative'}}}
        else:
            valuation = {'valuation': {'classifier1': {'prob': classifier1,
                                                       'value': 'positive' if classifier1 > 0.5 else 'negative'}}}

        return valuation

    for tweet in coll.find():
        coll.update({'_id': tweet['_id']}, {'$set': getDummyValoration()})


if __name__ == '__main__':
    classifyTweets()
