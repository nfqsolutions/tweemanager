from datetime import datetime
from elasticsearch_dsl import DocType, String, Date, Integer, Mapping, GeoPoint
from elasticsearch_dsl.connections import connections


class TweetForElastic(DocType):
    """
    Main data is tweet time geo and id that could be getter from geopy
    This data will generate a tweet_for_elastic type.
    """

    # Defining the index content:
    location = GeoPoint()
    tweettime = Date()
    # It is useful to save url as a non-tokenized string
    url = String(analyzer='snowball', fields={'raw': String(index='not_analyzed')})
    # An analyzer of type snowball that uses the standard tokenizer, with standard filter, lowercase filter, stop filter, and snowball filter.

    # index will be parsed from name tweet_for_elastic
    class Meta:
        index = 'twitter_collector'

    def save(self, ** kwargs):
        return super(TweetForElastic, self).save(** kwargs)


def startTweetForElastic(configdata):
    """
    """
    # Define a default Elasticsearch client
    connections.create_connection(hosts=[configdata.get("Elasticsearch","ES_URL")+":"+configdata.get("Elasticsearch","ES_PORT")])

    # create the mappings in elasticsearch
    TweetForElastic.init()
