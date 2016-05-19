# -*- coding: utf-8 -*-

import getoldtweets

import utilities

import logging


def gotsearch(username=None,
              since=None,
              until=None,
              querySearch=None,
              maxTweets=None):
    """Get Old Tweets

    function to get data from Twitter search Page.
    """
    tweetCriteria = getoldtweets.manager.TweetCriteria()
    if username:
        tweetCriteria.username = username
    if since:
        tweetCriteria.since = since
    if until:
        tweetCriteria.until = until
    if querySearch:
        tweetCriteria.querySearch = querySearch
    if maxTweets:
        tweetCriteria.maxTweets = maxTweets

    for rawtweet in getoldtweets.manager.TweetManager.getTweets(tweetCriteria):
        # Mapping result from result
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

        logging.info("Got Tweet with id %s" % result[u'id'])
        utilities.resultshandler.putresult(result)
