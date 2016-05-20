# -*- coding: utf-8 -*-

# Python 2->3 compat
try:
    import urllib2 as urllib
except:
    import urllib
    import urllib.parse
    import urllib.request
import re
import datetime
import simplejson as json
from .. import models
from pyquery import PyQuery
import chardet


class TweetManager:

    def __init__(self):
        pass

    @staticmethod
    def getTweets(tweetCriteria):
        refreshCursor = ''

        results = []

        while True:
            json = TweetManager.getJsonReponse(tweetCriteria, refreshCursor)
            if len(json['items_html'].strip()) == 0:
                break

            refreshCursor = json['min_position']
            tweets = PyQuery(json['items_html'])('div.js-stream-tweet')

            if len(tweets) == 0:
                break

            for tweetHTML in tweets:
                # print(tweetHTML)
                tweetPQ = PyQuery(tweetHTML)
                #print(str(tweetPQ))
                tweet = models.Tweet()

                usernameTweet = tweetPQ("span.username.js-action-profile-name b").text()

                urls = tweetPQ("p.js-tweet-text a.twitter-timeline-link").attr("data-expanded-url")
                # print("toma" + tweetPQ("p.js-tweet-text").text())
                txt = tweetPQ("p.js-tweet-text").text().replace('# ', '#')\
                                                       .replace('@ ', '@')\
                                                       .replace('http:// ', 'http://')\
                                                       .replace('https:// ', 'https://')\
                                                       .replace('http://www. ', 'http://www.')\
                                                       .replace('https://www. ', 'https://www.')
                #urls = tweetPQ("p.js-tweet-text a").attr("data-expanded-url")
                try:
                    txt = re.sub(urls[0:3]+'.*?'+urls[-5:],urls,txt, flags=re.DOTALL)
                except:
                    pass
                re.sub(r"\s+", " ", re.sub(r"[^\x00-\x7F]", "", tweetPQ("p.js-tweet-text").text()))
                retweets = int(tweetPQ("span.ProfileTweet-action--retweet span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""))
                favorites = int(tweetPQ("span.ProfileTweet-action--favorite span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""))
                dateSec = int(tweetPQ("small.time span.js-short-timestamp").attr("data-time"))
                id = tweetPQ.attr("data-tweet-id")
                permalink = tweetPQ.attr("data-permalink-path")

                geoText = ''
                geoSpan = tweetPQ('span.Tweet-geo')
                if len(geoSpan) > 0:
                    geoText = geoSpan.attr('title')

                tweet[u'id'] = id
                tweet[u'permalink'] = 'https://twitter.com' + permalink
                tweet[u'username'] = usernameTweet
                tweet[u'text'] = txt
                tweet[u'date'] = datetime.datetime.fromtimestamp(dateSec)
                tweet[u'retweets'] = retweets
                tweet[u'favorites'] = favorites
                tweet[u'mentions'] = " ".join(re.compile('(@\\w*)').findall(tweet[u'text']))
                tweet[u'hashtags'] = " ".join(re.compile('(#\\w*)').findall(tweet[u'text']))
                tweet[u'geoText'] = geoText

                results.append(tweet)

                if tweetCriteria.maxTweets > 0 and len(results) >= tweetCriteria.maxTweets:
                    return results

        return results

    @staticmethod
    def getJsonReponse(tweetCriteria, refreshCursor):
        url = "https://twitter.com/i/search/timeline?f=realtime&q=%s&src=typd&max_position=%s"

        urlGetData = ''
        if hasattr(tweetCriteria, 'username'):
            urlGetData += ' from:' + tweetCriteria.username

        if hasattr(tweetCriteria, 'since'):
            urlGetData += ' since:' + tweetCriteria.since

        if hasattr(tweetCriteria, 'until'):
            urlGetData += ' until:' + tweetCriteria.until

        if hasattr(tweetCriteria, 'querySearch'):
            urlGetData += ' ' + tweetCriteria.querySearch

        headers = {'User-Agent': ''}
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

        # Python 2->3 compat
        try:
            url = url % (urllib.quote(urlGetData), refreshCursor)
        except:
            url = url % (urllib.parse.quote(urlGetData), refreshCursor)

        # Python 2->3 compat
        try:
            req = urllib.Request(url, headers=headers)
        except:
            req = urllib.request.Request(url, headers=headers)

        # Python 2->3 compat
        try:
            response = urllib.urlopen(req)
        except:
            response = urllib.request.urlopen(req)

        jsonResponse = response.read()

        encoding = chardet.detect(jsonResponse)

        dataJson = json.loads(jsonResponse)

        return dataJson
