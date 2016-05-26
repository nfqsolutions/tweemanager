# -*- coding_utf-8 -*-
# Código para volver a descargar tweets que están mal parseados (pero poseemos su ID)
# Sería conveniente tener dos claves API, porque es normal que durante el proceso ocurra el error "rate limit"
# De ahí la necesidad de tantos try/except

import tweepy
import codecs
import json

try:
    # Claves1
except:
    pass

try:
    # Claves2
except:
    pass

infile = codecs.open('twitter.json', 'r', encoding='utf-8')
outfile = codecs.open('tweets_completos.json', 'w', encoding='utf-8')
errores = codecs.open('id_tweets_no_recuperados.txt', 'w', encoding='utf-8')

recuperados = 0
perdidos = 0
contador = 0
for line in infile:
    line_as_dict = json.loads(line.rstrip())
    id_tweet = line_as_dict['_id']
    try:
        tweet_completo = api1.get_status(id_tweet)
        print(tweet_completo.text)
        tweet = tweet_completo._json
        tweet[u'created_at'] = tweet_completo.created_at
        outfile.write('%s\n' % (tweet))
        recuperados += 1
    except:
        try:
            tweet_completo = api2.get_status(id_tweet)
            print(tweet_completo.text)
            tweet = tweet_completo._json
            tweet[u'created_at'] = tweet_completo.created_at
            outfile.write('%s\n' % (tweet))
            recuperados += 1
        except Exception as e:
            perdidos += 1
            print("Tweet perdido",e)
            errores.write('%s\n' % (id_tweet))
    contador += 1
    print(contador)
    
print("Tweets recuperados =",recuperados)
print("Tweets no recuperados =", perdidos)

outfile.close()
errores.close()


# A ejecutar otra vez el proceso, porque no se han descargado al realizar una llamada reiterada a la API (rate limit)

i = 0
archivos_infile = ['id_tweets_no_recuperados.txt',
                   'id_tweets_no_recuperados1.txt']

for archivo_infile in archivos_infile:
    i += 1 
    recuperados = 0
    perdidos = 0
    contador = 0

    infile = codecs.open(archivo_infile, 'r', encoding='utf-8')
    outfile = codecs.open('tweets_completos' + str(i) + '.json', 'w', encoding='utf-8')
    errores = codecs.open('id_tweets_no_recuperados' + str(i) + '.txt', 'w', encoding='utf-8')

    for line in infile:
        id_tweet = line
        try:
            tweet_completo = api1.get_status(id_tweet)
            print(tweet_completo.text)
            outfile.write('%s\n' % (tweet_completo._json))
            recuperados += 1
        except:
            try:
                tweet_completo = api2.get_status(id_tweet)
                print(tweet_completo.text)
                outfile.write('%s\n' % (tweet_completo._json))
                recuperados += 1
            except Exception as e:
                perdidos += 1
                print("Tweet perdido",e)
                errores.write('%s\n' % (id_tweet))
                    
        contador += 1
        print(contador)
        
    print("Tweets recuperados =",recuperados)
    print("Tweets no recuperados =", perdidos)

    outfile.close()
    errores.close()
