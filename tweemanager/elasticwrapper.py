from datetime import datetime
from elasticsearch_dsl import DocType, String, Date, Integer, Mapping, GeoPoint
from elasticsearch_dsl.connections import connections


class TweetForElastic(DocType):
    """
    main data is tweet time geo and id that could be getter from geopy
    This data will generate a tweet_for_elastic type.
    """

    # Defining the index content:

    location = GeoPoint()
    tweettime = Date()
    # type will be parsed from name tweet_for_elastic
    class Meta:
        index = 'lacaixa_collector'

    def save(self, ** kwargs):
        #self.lines = len(self.body.split())
        return super(TweetForElastic, self).save(** kwargs)


def startTweetForElastic(configdata):
    """
    """
    # Define a default Elasticsearch client
    connections.create_connection(hosts=[configdata.get("Elasticsearch","ES_URL")+":"+configdata.get("Elasticsearch","ES_PORT")])

    # create the mappings in elasticsearch
    TweetForElastic.init()
