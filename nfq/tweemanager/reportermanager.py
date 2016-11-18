# -*- coding:utf-8 -*-
import pymongo
import datetime
import json
# import mongoengine
import datetime as dt
from bson.code import Code
from nfq.tweemanager.tools import textclean
# from pprint import pprint # For debugging

stopwords = ['…',
             'de',
             'url',
             'atmention', 
                'la',
                'que',
                'el',
                'en',
                'y',
                'a',
                'los',
                'del',
                'se',
                'las',
                'por',
                'un',
                'para',
                'con',
                'no',
                'una',
                'su',
                'al',
                'lo',
                'como',
                'más',
                'pero',
                'sus',
                'le',
                'ya',
                'o',
                'este',
                'sí',
                'porque',
                'esta',
                'entre',
                'cuando',
                'muy',
                'sin',
                'sobre',
                'también',
                'me',
                'hasta',
                'hay',
                'donde',
                'quien',
                'desde',
                'todo',
                'nos',
                'durante',
                'todos',
                'uno',
                'les',
                'ni',
                'contra',
                'otros',
                'ese',
                'eso',
                'ante',
                'ellos',
                'e',
                'esto',
                'mí',
                'antes',
                'algunos',
                'qué',
                'unos',
                'yo',
                'otro',
                'otras',
                'otra',
                'él',
                'tanto',
                'esa',
                'estos',
                'mucho',
                'quienes',
                'nada',
                'muchos',
                'cual',
                'poco',
                'ella',
                'estar',
                'estas',
                'algunas',
                'algo',
                'nosotros',
                'mi',
                'mis',
                'tú',
                'te',
                'ti',
                'tu',
                'tus',
                'ellas',
                'nosotras',
                'vosostros',
                'vosostras',
                'os',
                'mío',
                'mía',
                'míos',
                'mías',
                'tuyo',
                'tuya',
                'tuyos',
                'tuyas',
                'suyo',
                'suya',
                'suyos',
                'suyas',
                'nuestro',
                'nuestra',
                'nuestros',
                'nuestras',
                'vuestro',
                'vuestra',
                'vuestros',
                'vuestras',
                'esos',
                'esas',
                'estoy',
                'estás',
                'está',
                'estamos',
                'estáis',
                'están',
                'esté',
                'estés',
                'estemos',
                'estéis',
                'estén',
                'estaré',
                'estarás',
                'estará',
                'estaremos',
                'estaréis',
                'estarán',
                'estaría',
                'estarías',
                'estaríamos',
                'estaríais',
                'estarían',
                'estaba',
                'estabas',
                'estábamos',
                'estabais',
                'estaban',
                'estuve',
                'estuviste',
                'estuvo',
                'estuvimos',
                'estuvisteis',
                'estuvieron',
                'estuviera',
                'estuvieras',
                'estuviéramos',
                'estuvierais',
                'estuvieran',
                'estuviese',
                'estuvieses',
                'estuviésemos',
                'estuvieseis',
                'estuviesen',
                'estando',
                'estado',
                'estada',
                'estados',
                'estadas',
                'estad',
                'he',
                'has',
                'ha',
                'hemos',
                'habéis',
                'han',
                'haya',
                'hayas',
                'hayamos',
                'hayáis',
                'hayan',
                'habré',
                'habrás',
                'habrá',
                'habremos',
                'habréis',
                'habrán',
                'habría',
                'habrías',
                'habríamos',
                'habríais',
                'habrían',
                'había',
                'habías',
                'habíamos',
                'habíais',
                'habían',
                'hube',
                'hubiste',
                'hubo',
                'hubimos',
                'hubisteis',
                'hubieron',
                'hubiera',
                'hubieras',
                'hubiéramos',
                'hubierais',
                'hubieran',
                'hubiese',
                'hubieses',
                'hubiésemos',
                'hubieseis',
                'hubiesen',
                'habiendo',
                'habido',
                'habida',
                'habidos',
                'habidas',
                'soy',
                'eres',
                'es',
                'somos',
                'sois',
                'son',
                'sea',
                'seas',
                'seamos',
                'seáis',
                'sean',
                'seré',
                'serás',
                'será',
                'seremos',
                'seréis',
                'serán',
                'sería',
                'serías',
                'seríamos',
                'seríais',
                'serían',
                'era',
                'eras',
                'éramos',
                'erais',
                'eran',
                'fui',
                'fuiste',
                'fue',
                'fuimos',
                'fuisteis',
                'fueron',
                'fuera',
                'fueras',
                'fuéramos',
                'fuerais',
                'fueran',
                'fuese',
                'fueses',
                'fuésemos',
                'fueseis',
                'fuesen',
                'sintiendo',
                'sentido',
                'sentida',
                'sentidos',
                'sentidas',
                'siente',
                'sentid',
                'tengo',
                'tienes',
                'tiene',
                'tenemos',
                'tenéis',
                'tienen',
                'tenga',
                'tengas',
                'tengamos',
                'tengáis',
                'tengan',
                'tendré',
                'tendrás',
                'tendrá',
                'tendremos',
                'tendréis',
                'tendrán',
                'tendría',
                'tendrías',
                'tendríamos',
                'tendríais',
                'tendrían',
                'tenía',
                'tenías',
                'teníamos',
                'teníais',
                'tenían',
                'tuve',
                'tuviste',
                'tuvo',
                'tuvimos',
                'tuvisteis',
                'tuvieron',
                'tuviera',
                'tuvieras',
                'tuviéramos',
                'tuvierais',
                'tuvieran',
                'tuviese',
                'tuvieses',
                'tuviésemos',
                'tuvieseis',
                'tuviesen',
                'teniendo',
                'tenido',
                'tenida',
                'tenidos',
                'tenidas',
                'tened']


# 1º ListOfdays:
def gen_list_of_days(StartDate, EndDate=datetime.datetime.now()):
    """
    """
    onedaydelta = datetime.timedelta(days=1)
    StartDate = datetime.datetime(StartDate.year, StartDate.month, StartDate.day)
    EndDate = datetime.datetime(EndDate.year, EndDate.month, EndDate.day)
    delta = EndDate - StartDate
    for i in range(delta.days):
        yield {'start': StartDate, 'end': StartDate + onedaydelta}
        StartDate += onedaydelta

# 2º ListOfWeeks:
def gen_list_of_weeks(StartDate, EndDate):
    """
    """
    try:
        if type(StartDate) is not dt.date:
            StartDate = dt.datetime.strptime(StartDate, '%Y-%m-%d')
        if type(EndDate) is not dt.date:
            EndDate = dt.datetime.strptime(EndDate, '%Y-%m-%d')
    except:
        pass

    onedaydelta = datetime.timedelta(days=1)
    oneweekdelta = datetime.timedelta(days=7)
    StartDate = datetime.datetime(StartDate.year, StartDate.month, StartDate.day)
    while StartDate.weekday() != 0:
        StartDate = StartDate - onedaydelta
    EndDate = datetime.datetime(EndDate.year, EndDate.month, EndDate.day) + onedaydelta
    deltadays = EndDate - StartDate
    deltaweeks = deltadays.days / 7
    for i in range(int(deltaweeks) + 1):
        yield {'start': StartDate, 'end': StartDate + oneweekdelta}
        StartDate += oneweekdelta

# 3º ListOfMonth:
def gen_list_of_months(StartDate,EndDateInp):
    """
    """
    StartDate = datetime.datetime(StartDate.year, StartDate.month, 1)
    EndDate = datetime.datetime(StartDate.year, StartDate.month, 1)

    def add_month(Date):
        """
        """
        year = int(Date.year + (Date.month / 12))
        month  = ((Date.month) % 12) + 1
        monthplusone = datetime.datetime(year , month  , Date.day)
        return monthplusone

    while EndDate < EndDateInp:
        EndDate = add_month(StartDate)
        yield {'start': StartDate, 'end': EndDate}
        StartDate = EndDate

# Agg Functions:
def agg_count(StartDate, EndDate, coll, fromgot, classifier):
    """
    It returns the number of tweets between a time interval
    """
    # Classifier and values should be change to use your owns
    if fromgot: # retweeted tweets are considered
        pipeline = [
            {"$match": {"$and": [{"created_at": {"$gte": StartDate}}, {"created_at": {"$lt": EndDate}}]}},
            {"$group": {"_id": "",
            "count": {"$sum": 1},
            "npos": {"$sum": {"$cond":[{"$eq":["$valuation." + classifier + ".value","positive"]},{"$cond":[{"$eq":["$retweet_count",0]},1,"$retweet_count"]},0]}},
            "nneg": {"$sum": {"$cond":[{"$eq":["$valuation." + classifier + ".value","negative"]},{"$cond":[{"$eq":["$retweet_count",0]},1,"$retweet_count"]},0]}},
            "met": {"$sum": {"$multiply": ["$valuation." + classifier + ".metric", {"$cond":[{"$eq":["$retweet_count",0]},1,"$retweet_count"]}]}}
            }},
        ]

        result = {'count':0, 'npos':0, 'nneg':0, 'met':0}
        for result in coll.aggregate(pipeline):
            result = result
        return result

    else: # Only tweets in database are counted
        pipeline = [
            {"$match": {"$and": [{"created_at": {"$gte": StartDate}}, {"created_at": {"$lt": EndDate}}]}},
            {"$group": {"_id": "",
            "count": {"$sum": 1},
            "npos": {"$sum": {"$cond":[{"$eq":["$valuation." + classifier + ".value","positive"]},1,0]}},
            "nneg": {"$sum": {"$cond":[{"$eq":["$valuation." + classifier + ".value","negative"]},1,0]}},
            "met": {"$sum": "$valuation." + classifier + ".metric"}
            }},
        ]

        result = {'count':0, 'npos':0, 'nneg':0, 'met':0}
        for result in coll.aggregate(pipeline):
            result = result
        return result

def alert_words(StartDate, EndDate, coll, alert_words, db):
    """
    List of alert words - a list of warning words
    alert_words = cfgmanager.TextPatterns['alert_words']
    """
    aux_list = []
    aux_dict = {}
    for word in alert_words:
        aux_list.append(str(textclean(word)))
        try:
            aux_dict.update({str(textclean(word)): word})
        except:
            aux_dict = {str(textclean(word)): word}


    mapper = Code("""
        function() {  
        var summary = this.text_clean;
        var fecha = this.created_at;
        var Start = """ + StartDate + """;
        var StartDate = ISODate(Start);
        var End   = """ + EndDate   + """;
        var EndDate = ISODate(End);
        var alert_words = """
                        + str(aux_list) +
                          """
        if (summary) { 
            summary = summary.toLowerCase().split(" "); 
            for (var i = 0; i < summary.length; i++) {
                if ( alert_words.indexOf(summary[i]) != -1){
                    if (fecha >= StartDate && fecha < EndDate)  {
                       emit(summary[i], 1);
                    }
                }
            }
        }
    }
    """)

    reducer = Code("""
        function( key, values ) {    
        var count = 0;    
        values.forEach(function(v) {            
            count +=v;    
        });
        return count;
    }
    """)

    result = coll.map_reduce(mapper, reducer, 'alert_words')
    dic_of_results = {}
    for doc in result.find():
        # TO DO:
        # Instead of this, save with text cleaned as label
        key = aux_dict[doc[u'_id']]
        try:
            dic_of_results.update({key: doc[u'value']})
        except:
            dic_of_results = {key: doc[u'value']}


    # Include alert words with 0 mentions
    for word in alert_words:
        if word not in dic_of_results.keys():
            dic_of_results.update({word: 0})

    db.drop_collection('alert_words')
    return dic_of_results

def word_count(StartDate, EndDate, coll, stopwords, db, max_words=30):
    """
    This function returns a dictionary with the most tweeted
    words.

    :param StartDate: Start date to search.
    :param EndDate: End date to search.
    :param coll: Mongo collection.
    :param stopwords: Stopwords applied.
    :param db: Mongo database.
    :param max_words: Maximum number of words
                      selected.
    """
    mapper = Code("""
        function() {  
        var summary = this.text_clean;
        var lang = this.lang;
        var stopwords = """ + str(stopwords) + """

        if (summary) { 
            if (lang == "es") {
                // quick lowercase to normalize per your requirements
                summary = summary.toLowerCase().split(" "); 
                for (var i = 0; i < summary.length; i++) {
                    if ( stopwords.indexOf(summary[i]) == -1){ // stopwords are avoided                     
                        if (summary[i])  {      // make sure there's something
                           emit(summary[i], 1);
                        }
                    }
                }
            }
        }
    }
    """)

    reducer = Code("""
        function( key, values ) {    
        var count = 0;    
        values.forEach(function(v) {            
            count +=v;    
        });
        return count;
    }
    """)

    result = coll.map_reduce(mapper, reducer, 'word_count')
    dic_of_results = {}
    count = 0
    # Words that just are found one time are not searched
    for doc in result.find({"value":{"$gt":1}}).sort('value', pymongo.DESCENDING):
        key = doc[u'_id']
        try:
            dic_of_results.update({key: doc[u'value']})
        except:
            dic_of_results = {key: doc[u'value']}
        count += 1
        if count >= max_words:
            break

    db.drop_collection('word_count')
    return dic_of_results

def source_count(StartDate, EndDate, coll, db, max_sources=30):
    """
    TODO: this operation can be done in pipeline (agregation)
    instead of map reduce (as it is implemented).

    This function returns a dictionary with the sources which
    the people tweet the most.

    :param StartDate: Start date to search.
    :param EndDate: End date to search.
    :param coll: Mongo collection.
    :param db: Mongo database.
    :param max_sources: Maximum number of sources
                        selected.
    """
    mapper = Code("""
        function() {
        var source = this.source;
        var lang = this.lang;
        if (source) {// make sure there's something
            emit(source, 1);
        }
    }
    """)

    reducer = Code("""
        function( key, values ) {    
        var count = 0;    
        values.forEach(function(v) {            
            count +=v;    
        });
        return count;
    }
    """)

    result = coll.map_reduce(mapper, reducer, 'source_count')
    dic_of_results = {}
    count = 0
    # Words that just are found one time are not searched
    for doc in result.find({"value":{"$gt":1}}).sort('value', pymongo.DESCENDING):
        key = str(doc[u'_id']).replace(".", "_")
        try:
            dic_of_results.update({key: {'source':doc[u'_id'], 'value':doc[u'value']}})
        except:
            dic_of_results = {key: {'source':doc[u'_id'], 'value':doc[u'value']}}
        count += 1
        if count >= max_sources:
            break

    db.drop_collection('source_count')
    return dic_of_results

def web_count(StartDate, EndDate, coll, db, max_sources=30):
    """
    TODO: this operation can be done in pipeline (agregation)
    instead of map reduce (as it is implemented).

    This function returns a dictionary with the sources which
    the people tweet the most.

    :param StartDate: Start date to search.
    :param EndDate: End date to search.
    :param coll: Mongo collection.
    :param db: Mongo database.
    :param max_sources: Maximum number of sources
                        selected.
    """
    mapper = Code("""
        function() {
            var entities = this.entities;
            if (entities) {
                var urls = entities.urls;
                if (urls) {
                    for (var i = 0; i < urls.length; i++)
                    var url = urls[i].expanded_url
                    if (url) {
                    emit(url, 1);
                    }
                }
            }
        }
    """)

    reducer = Code("""
        function( key, values ) {    
        var count = 0;    
        values.forEach(function(v) {            
            count +=v;    
        });
        return count;
    }
    """)

    result = coll.map_reduce(mapper, reducer, 'web_count')

    dic_of_results = {}
    count = 0
    # Words that just are found one time are not searched
    for doc in result.find({"value":{"$gt":1}}).sort('value', pymongo.DESCENDING):
        key = str(doc[u'_id']).replace(".", "_")
        try:
            dic_of_results.update({key: {'url':doc[u'_id'], 'value':doc[u'value']}})
        except:
            dic_of_results = {key: {'url':doc[u'_id'], 'value':doc[u'value']}}
        count += 1
        if count >= max_sources:
            break

    db.drop_collection('source_count')
    return dic_of_results

# Reports to MongoDB or to a JSON file
def generate_reports(host,
                      name_collection='TweetsRepo',
                      alertwords=None,
                      StartDate=None,
                      EndDate=None,
                      output='mongodb',
                      output_name='Reports',
                      fromgot=True,
                      classifier='algorithm_1',
                      max_elements=20):

    def _generate_reports(values, db, coll, fromgot, classifier, alertwords, max_elements):
        """
        To reduce code, repetitive code is grouped in functions.
        """
        linea = {}
        valor = agg_count(values['start'], values['end'], coll, fromgot, classifier)
        linea['start'] = values['start']
        linea['end'] = values['end']
        linea['tweets'] = valor['count']
        linea['positives'] = valor['npos']
        linea['negatives'] = valor['nneg']
        linea['metrica'] = valor['met']
        linea['report'] = {'type':'monthly', 'from':name_collection}
        key = values['start'].strftime("%Y%m%d") + values['end'].strftime("%Y%m%d")
        if alertwords:
            linea['alert_words'] = alert_words(values['start'].strftime("%Y%m%d"),
                                              values['end'].strftime("%Y%m%d"),
                                              coll, alertwords, db)
        if stopwords:
            linea['word_count'] = word_count(values['start'].strftime("%Y%m%d"),
                                              values['end'].strftime("%Y%m%d"), 
                                              coll, stopwords, db, max_elements)
        linea['source_count'] = source_count(values['start'].strftime("%Y%m%d"),
                                              values['end'].strftime("%Y%m%d"), 
                                              coll, db, max_elements)
        linea['web_count'] = web_count(values['start'].strftime("%Y%m%d"),
                                              values['end'].strftime("%Y%m%d"), 
                                              coll, db, max_elements)
        return linea, key

    # Make connection
    client = pymongo.MongoClient(host=host)
    db = client.get_default_database()
    coll = db[name_collection]

    # 1º get first date
    if StartDate == None:
        for tweet in coll.find().sort('created_at', 1).limit(1):
            StartDate = tweet['created_at']
    print(StartDate)

    # 2º get last date
    if EndDate == None:
        for tweet in coll.find().sort('created_at', -1).limit(1):
            EndDate = tweet['created_at']
    print(EndDate)
    
    if output=='json':
        if '.json' not in output_name:
            output_name = output_name + '.json'

        outfile = open(output_name, 'w')
        # 1º ListOfDays:
        print("Writing report by days...")
        for values in gen_list_of_days(StartDate, EndDate):
            linea, key = _generate_reports(values, db, coll, fromgot, classifier, alertwords, max_elements)
            linea = json.dumps(linea)
            outfile.write(linea)
            outfile.write("\n")

        # 2º ListOfWeeks:
        print("Writing report by weeks...")
        for values in gen_list_of_weeks(StartDate, EndDate):
            linea, key = _generate_reports(values, db, coll, fromgot, classifier, alertwords, max_elements)
            linea = json.dumps(linea)
            outfile.write(linea)
            outfile.write("\n")

        # 3º ListOfMonth:
        print("Writing report by monts...")
        for values in gen_list_of_months(StartDate, EndDate):
            linea, key = _generate_reports(values, db, coll, fromgot, classifier, alertwords, max_elements)
            linea = json.dumps(linea)
            outfile.write(linea)
            outfile.write("\n")
        outfile.close()

    elif output == 'mongodb':
        collreporting = db[output_name]

        print("Uploading report by days...")
        # 1º ListOfDays:
        for values in gen_list_of_days(StartDate, EndDate):
            linea, key = _generate_reports(values, db, coll, fromgot, classifier, alertwords, max_elements)
            collreporting.update({"_id":key}, linea, upsert = True)

        print("Uploading report by weeks...")
        # 2º ListOfWeeks:
        for values in gen_list_of_weeks(StartDate, EndDate):
            linea, key = _generate_reports(values, db, coll, fromgot, classifier, alertwords, max_elements)
            collreporting.update({"_id":key}, linea, upsert = True)

        print("Uploading report by months...")
        # 3º ListOfMonth:
        for values in gen_list_of_months(StartDate, EndDate):
            linea, key = _generate_reports(values, db, coll, fromgot, classifier, alertwords, max_elements)
            collreporting.update({"_id":key}, linea, upsert = True)
    
    else: #stdout
        print("Report by days...")
        # 1º ListOfDays:
        for values in gen_list_of_days(StartDate, EndDate):
            linea, key = _generate_reports(values, db, coll, fromgot, classifier, alertwords, max_elements)
            print(linea)

        print("Report by weeks...")
        # 2º ListOfWeeks:
        for values in gen_list_of_weeks(StartDate, EndDate):
            linea, key = _generate_reports(values, db, coll, fromgot, classifier, alertwords, max_elements)
            print(linea)

        print("Report by months...")
        # 3º ListOfMonth:
        for values in gen_list_of_months(StartDate, EndDate):
            linea, key = _generate_reports(values, db, coll, fromgot, classifier, alertwords, max_elements)
            print(linea)
