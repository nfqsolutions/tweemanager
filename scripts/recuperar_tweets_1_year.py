# -*- coding:utf-8 -*-

from tweemanager.tools import MongoTweetProcessor
from tweemanager.getoldtweets import setTweetCriteria, getoldtweetsGenerator
# from tweemanager.tweetdocument import TweetDocument
import datetime as dt
import mongoengine

mongoengine.connect(host="mongodb://192.168.80.221:27017/tweets")

fecha_actual = dt.datetime.now()
year = dt.timedelta(days=365) # Como criterio, tomamos A/365
a_year_ago = fecha_actual - year
deltat = dt.timedelta(days=1)
query = [u'cabk', u'caixabank']
# Necesitamos transformar el array a string para getoldtweets
cont = 1
for element in query:
    if cont == 1:
        query_to_search = element
    else:
        query_to_search += ' AND ' + element

patternstoexclude = [u'caixa cataluña', u'caixa galicia']

while fecha_actual > a_year_ago - deltat:
    tweetCriteria = setTweetCriteria(
        since=fecha_actual - deltat,
        until=fecha_actual,
        querySearch=query_to_search,
        maxTweets=100)

    for tweet in getoldtweetsGenerator(tweetCriteria):
        TweetProcessor = MongoTweetProcessor
        TweetProcessor.PATTERNSTOINCLUDE = query
        TweetProcessor.PATTERNSTOEXCLUDE = patternstoexclude

        posttweet = TweetProcessor(tweet)
        posttweet.sendtooutput()
        logging.info('getoldtweets command Done')

    fecha_actual = fecha_actual - deltat