# -*- coding: utf-8 -*-
import tweepy
from nfq.tweemanager.settings import cfgmanager


def searchtweets(outputclass, query, maxtweets=10):
    """
    """
    if query is None:
        raise Exception("A query must be set")
    if not isinstance(maxtweets, int):
        raise Exception("maxtweets must be a number")
    api = nfqTwitterAuth(consumer_key=cfgmanager.TwitterAPIcredentials['consumer_key'],
                         consumer_secret=cfgmanager.TwitterAPIcredentials['consumer_secret'],
                         access_key=cfgmanager.TwitterAPIcredentials['access_key'],
                         access_secret=cfgmanager.TwitterAPIcredentials['access_secret'],
                         )
    for status in tweepy.Cursor(api.get_api().search, q=query).items(maxtweets):
        data = status._json
        # Check if a retweet exists!
        if data.get(u'retweeted_status', None):
            retweetdata = data[u'retweeted_status']
            retweetdata[u'created_at'] = status.retweeted_status.created_at
            retweetpostdata = outputclass(retweetdata)
            retweetpostdata.sendtooutput()
        data[u'created_at'] = status.created_at
        tweetdata = outputclass(data)
        tweetdata.sendtooutput()


def listenertweets(outputclass, trackarray):
    """
    """
    api = nfqTwitterAuth(consumer_key=cfgmanager.TwitterAPIcredentials['consumer_key'],
                         consumer_secret=cfgmanager.TwitterAPIcredentials['consumer_secret'],
                         access_key=cfgmanager.TwitterAPIcredentials['access_key'],
                         access_secret=cfgmanager.TwitterAPIcredentials['access_secret']
                         )
    NFQlistener = nfqTwitterStreamListener()
    NFQlistener.TweetProcessor = outputclass
    thecurrentstream = tweepy.Stream(auth=api.auth, listener=NFQlistener)
    thecurrentstream.filter(track=trackarray)


class nfqTwitterAuth(object):
    """
    class to manage the twitter authorization
    """

    def __init__(self, consumer_key=None,
                 consumer_secret=None,
                 access_key=None,
                 access_secret=None
                 ):
        """
        """
        try:
            if not (consumer_key and consumer_secret and access_key and access_secret):
                raise Exception("TwitterAPIcredentials incomplete")
            # check if credentials are set:
            self.auth = tweepy.OAuthHandler(
                consumer_key,
                consumer_secret)
            self.auth.set_access_token(
                access_key,
                access_secret)
            self.api = tweepy.API(self.auth)
        except:
            raise

    def get_auth(self):
        return self.auth

    def get_api(self):
        return self.api


class nfqTwitterStreamListener(tweepy.StreamListener):
    """nfqlistener
    """
    # class attribute containing some configdata
    configdata = None
    TweetProcessor = None

    def tweetprocess(self):
        """
        """

    def on_error(self, code):
        """On error it won't stop the listener.
        """
        print("Error while listening with code:" + str(code))

    def on_status(self, status):
        """Handle recevied tweet:

        This status will put candidate in a MQ.
        """
        data = status._json
        # Avoid manual parsing datetime and use the one on the Status object.
        if data.get(u'retweeted_status', None):
            retweetdata = data[u'retweeted_status']
            retweetdata[u'created_at'] = status.retweeted_status.created_at
            retweetpostdata = self.TweetProcessor(retweetdata)
            retweetpostdata.sendtooutput()
        # check if there is a retweet_status
        data[u'created_at'] = status.created_at
        posttweet = self.TweetProcessor(data)
        posttweet.sendtooutput()
