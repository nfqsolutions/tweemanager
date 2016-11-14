# -*- coding:utf-8 -*-

import valoratweets
import mongoengine
from tweemanager.tweetdocument import TweetDocument
import pprint
import re
import datetime as dt
from bson import json_util as json


mongoengine.connect(host="mongodb://192.168.80.221:27017/tweets")

cosas = TweetDocument._get_collection().aggregate(
    [
{ '$project' : { "source": 1, "valuation": 1, '_id': 0, 'week': { '$week': "$created_at" } } },
{ '$group' : { '_id': "$week", 
                 "total_positivos": {"$sum": {"$cond":[{"$eq":["$valuation.algoritmo_1.clasificado","positivo"]},1,0]}},
                 "total_negativos": {"$sum": {"$cond":[{"$eq":["$valuation.algoritmo_1.clasificado","negativo"]},1,0]}},
                 "total": {"$sum": 1},
               }
    },
{ '$project' : { "semana": "$_id", "positivos": "$total_positivos", "negativos":"$total_negativos", "total":"$total","por_valorar":{'$subtract':["$total",{'$add':["$total_positivos", "$total_negativos"]}]} } },
{ '$sort': {"semana": 1}}
]
    )

outfile = open('semanas.csv', 'w')
outfile.write('semana\ttotal\tpositivos\tnegativos\tsin_valorar\n')

for valor in cosas:
        print(json.dumps(valor))
        semana = valor['semana']
        positivos = valor['positivos']
        negativos = valor['negativos']
        sin_valorar = valor['por_valorar']
        total = valor['total']
        outfile.write('%s\t%s\t%s\t%s\t%s\n' % (semana,
                                         total,
                                         positivos,
                                         negativos,
                                         sin_valorar))

outfile.close()
