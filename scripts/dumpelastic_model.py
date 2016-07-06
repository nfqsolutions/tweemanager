# -*- coding: utf-8 -*-
## This script downloads tweets from our Elasticsearch database.
# It hasn't been included in 'tweemanager' package in github because of the 

def dumpelastic(archivo,index, host='127.0.0.1'):
    """
    archivo: output, fichero donde guarda la operación
    index: índice del que descarga los tweets
    idioma: guarda en español o en todos los idiomas
    """
    # check the number of dumps and do the 
    # dump in a 500 records iteration.
    # des_json(archivo,index,idioma):

    from bson import json_util as json
    from elasticsearch import Elasticsearch
    import io

    es = Elasticsearch([{'host': host}])
    outputFile = io.open(archivo, "w+", encoding='utf8')

    res = es.search(index=index, size=500, doc_type="tweet_for_elastic", body={"query": {"match_all": {}}}, scroll='10m')
    
    print('Empezando búsqueda...')
    
    tweets = res['hits']['hits']
    contador = 1

    for hit in tweets:
        try:
            hit["_source"]['text'] = hit["_source"]['text'].replace("\n"," ")
        except:
            pass

        outputFile.write('%s\n' % (json.dumps(hit,ensure_ascii=False)))

        contador +=1
        
          

    while (len(tweets)>0):

        sid = res['_scroll_id']
        res = es.scroll(scroll_id = sid, scroll = '10m')
        tweets = res['hits']['hits']

        for hit in tweets:
            try:
                hit["_source"]['text'] = hit["_source"]['text'].replace("\n"," ")
            except:
                pass
            
            outputFile.write('%s\n' % (json.dumps(hit,ensure_ascii=False)))

            contador +=1


    outputFile.close()
    print('Descarga finalizada!')
    print('Se han encontrado ',contador,' tweets')

if __name__ == '__main__':
    import datetime as dt
    index =  'as_you_want'
    host = '127.0.0.1'
    archivo = index +'__' + dt.datetime.now().strftime("%Y_%m_%d") + '.json'
    dumpelastic(archivo, index, host)