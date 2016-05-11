# -*- coding: utf-8 -*-

from .manager import TweetCriteria
from .manager import TweetManager
# import .models

gotSearchCriteria = TweetCriteria()


def getoldtweetsGenerator(SearchCriteria):
    """
    scraping tool for the results
    using tweet search Page. It is an alternative to oficial tweeter API.
    but information return results from scraping a webpage so it depends
    on how the scraping is done.
    """
    for tweet in TweetManager.getTweets(SearchCriteria):
        result = dict()
        yield result
