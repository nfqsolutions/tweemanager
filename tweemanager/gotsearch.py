# -*- coding: utf-8 -*-

import getoldtweets

import utilities

def gotsearch(username = None,
              since = None,
              until = None,
              querySearch = None,
              maxTweets = None):
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
        result[u'created_at'] = rawtweet[u'date']
        result[u'text'] = rawtweet[u'text']
        result[u'date'] = rawtweet[u'text']
        result[u'user'] = {u'screen_name':rawtweet[u'username']}
        result[u'favorite_count'] = rawtweet[u'favorites']
        result[u'retweet_count'] = rawtweet[u'retweets']
      
        result[u'entities'] = {"user_mentions":[],
                             "hashtags":[]}
        for hashtag in rawtweet[u'hashtags'].split(','):
            if hashtag != "":
                result[u'entities'][u'hashtags'].append({u'text':hashtag.replace('#','')})
        for mention in rawtweet[u'mentions'].split(','):
            if mention != "":
                result[u'entities'][u'user_mentions'].append({u'text':mention.replace('#','')})

    utilities.resultshandler.putresult(result)
