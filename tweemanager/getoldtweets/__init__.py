# -*- coding: utf-8 -*-

from .manager import TweetCriteria
from .manager import TweetManager
# import .models
import logging


def setTweetCriteria(username=None,
                     since=None,
                     until=None,
                     querySearch=None,
                     maxTweets=None):
    """
    Sets and validate TweetCriteria
    """
    # validating criteria
    try:
        if (username is None) and (querySearch is None):
            raise Exception("At least a username of querySearch must be provided")
    except:
        raise
    tweetCriteria = TweetCriteria()
    if username:
        tweetCriteria.username = username
    if since:
        tweetCriteria.since = since
    if until:
        tweetCriteria.until = until
    if querySearch:
        tweetCriteria.querySearch = querySearch
    if maxTweets:
        tweetCriteria.maxTweets = int(maxTweets)
    else:
        tweetCriteria.maxTweets = 10

    logging.info("TweetCriteria {}".format(tweetCriteria))

    return tweetCriteria

def getoldtweetsGenerator(SearchCriteria):
    """
    scraping tool for the results
    using tweet search Page. It is an alternative to oficial tweeter API.
    but information return results from scraping a webpage so it depends
    on how the scraping is done.
    """
    for rawtweet in TweetManager.getTweets(SearchCriteria):
        result = dict()
        
        result[u'id'] = rawtweet[u'id']
        result[u'id_str'] = rawtweet[u'id']
        result[u'created_at'] = rawtweet[u'date']
        result[u'text'] = rawtweet[u'text']
        result[u'user'] = {u'screen_name': rawtweet[u'username']}
        result[u'favorite_count'] = rawtweet[u'favorites']
        result[u'retweet_count'] = rawtweet[u'retweets']
        # process place full_name
        if rawtweet[u'geoText']:
            result[u'place'] = {u'full_name': rawtweet[u'geoText']}

        result[u'entities'] = {"user_mentions": [],
                               "hashtags": []}
        # Process hashtags
        for hashtag in rawtweet[u'hashtags'].split(' '):
            if hashtag != "":
                result[u'entities'][u'hashtags'].append(
                    {u'text': hashtag.replace('#', '')})
        # Process mentions
        for mention in rawtweet[u'mentions'].split(' '):
            if mention != "":
                result[u'entities'][u'user_mentions'].append(
                    {u'text': mention.replace('@', '')})

        # remove entities if no data is set:
        if (len(result[u'entities'][u'hashtags']) == 0) and (len(result[u'entities'][u'user_mentions']) == 0):
            result.pop(u'entities')
            
        yield result
