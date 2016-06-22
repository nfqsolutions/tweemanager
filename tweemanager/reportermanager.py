# -*- coding:utf-8 -*-
import pymongo
import datetime
import json
import mongoengine
import datetime as dt
from bson.code import Code
from .tools import textclean

# 1º ListOfdays:
def genListOfdays(StartDate, EndDate=datetime.datetime.now()):
    """
    """
    onedaydelta = datetime.timedelta(days=1)
    StartDate = datetime.datetime(StartDate.year, StartDate.month, StartDate.day)
    EndDate = datetime.datetime(EndDate.year, EndDate.month, EndDate.day)
    delta = EndDate - StartDate
    for i in xrange(delta.days):
        yield {'start': StartDate, 'end': StartDate + onedaydelta}
        StartDate += onedaydelta

# 2º ListOfWeeks:
def genListOfWeeks(StartDate, EndDate):
    """
    """
    onedaydelta = datetime.timedelta(days=1)
    oneweekdelta = datetime.timedelta(days=7)
    StartDate = datetime.datetime(StartDate.year, StartDate.month, StartDate.day)
    while StartDate.weekday() != 0:
        StartDate = StartDate - onedaydelta
    EndDate = datetime.datetime(EndDate.year, EndDate.month, EndDate.day) + onedaydelta
    deltadays = EndDate - StartDate
    deltaweeks = deltadays.days / 7
    for i in xrange(deltaweeks + 1):
        yield {'start': StartDate, 'end': StartDate + oneweekdelta}
        StartDate += oneweekdelta

# 3º ListOfMonth:
def genListOfMonth(StartDate,EndDateInp):
    """
    """
    StartDate = datetime.datetime(StartDate.year, StartDate.month, 1)
    EndDate = datetime.datetime(StartDate.year, StartDate.month, 1)

    def addMonth(Date):
        """
        """
        #year = Date.year + (Date.month + 2) / 12
        year = Date.year + (Date.month / 12)
        month  = ((Date.month) % 12) + 1
        monthplusone = datetime.datetime(year , month  , Date.day)
        return monthplusone

    while EndDate < EndDateInp:
        EndDate = addMonth(StartDate)
        yield {'start': StartDate, 'end': EndDate}
        StartDate = EndDate

# Agg Functions:
def aggCount(StartDate, EndDate, coll):
    """
    It returns the number of tweets between a time interval
    """
    # Classifier and values should be change to use your owns
    pipeline = [
        {"$match": {"$and": [{"created_at": {"$gte": StartDate}}, {"created_at": {"$lt": EndDate}}]}},
        {"$group": {"_id": "",
        "count": {"$sum": 1},
        "npos": {"$sum": {"$cond":[{"$eq":["$valoration.classifier1.value","positive"]},1,0]}},
        "nneg": {"$sum": {"$cond":[{"$eq":["$valoration.classifier1.value","negative"]},1,0]}},
        "met": {"$sum": "$valoration.classifier1.metric"}
        }},
    ]

    result = {'count':0, 'npos':0, 'nneg':0, 'met':0}
    for result in coll.aggregate(pipeline):
        result = result
    return result

def alertWords(StartDate, EndDate, coll, alert_words):
    """
    List of alert words - a list of warning words
    alert_words = cfgmanager.TextPatterns['alertWords']
    """

    aux_list = []
    for word in alert_words:
        aux_list.append(str(textclean(word)))
    alert_words = aux_list

    mapper = Code("""
        function() {  
        var summary = this.text_clean;
        var fecha = this.created_at;
        var Start = """ + StartDate + """;
        var StartDate = ISODate(Start);
        var End   = """ + EndDate   + """;
        var EndDate = ISODate(End);
        var alert_words = """
                        + str(alert_words) +
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

    result = coll.map_reduce(mapper, reducer, "word_count")
    dic_of_results = {}
    for doc in result.find():
        try:
            dic_of_results.update({doc[u'_id']: doc[u'value']})
        except:
            dic_of_results = {doc[u'_id']: doc[u'value']}

    # Include alert words with 0 mentions
    for word in alert_words:
        if word not in dic_of_results.keys():
            dic_of_results.update({word: 0})

    return dic_of_results

# TODO: Select between reporting to MongoDB or to a JSON file
# Reports to a JSON file
def report_to_JSON(StartDate, EndDate):
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

    #cfgmanager.MongoDBSpecs['host'] 
    collreporting = db.Reporting

    outfile = open('report_days.json', 'w')
    # 1º ListOfDays:
    print("Writing report by days...")
    for values in genListOfdays(StartDate, EndDate):
        linea = {}
        valor = aggCount(values['start'], values['end'])
        linea['tweets'] = valor['count']
        linea['positives'] = valor['npos']
        linea['negatives'] = valor['nneg']
        linea['metrica'] = valor['met']
        linea = json.dumps(linea)
        outfile.write(linea)
        outfile.write("\n")
    outfile.close()

    outfile = open('report_weeks.json', 'w')
    # 2º ListOfWeeks:
    print("Writing report by weeks...")
    for values in genListOfWeeks(StartDate, EndDate):
        linea = {}
        valor = aggCount(values['start'], values['end'])
        linea['tweets'] = valor['count']
        linea['positives'] = valor['npos']
        linea['negatives'] = valor['nneg']
        linea['metrica'] = valor['met']
        linea = json.dumps(linea)
        outfile.write(linea)
        outfile.write("\n")
    outfile.close()

    outfile = open('report_months.json', 'w')
    # 3º ListOfMonth:
    print("Writing report by monts...")
    for values in genListOfMonth(StartDate, EndDate):
        linea = {}
        valor = aggCount(values['start'], values['end'])
        linea['tweets'] = valor['count']
        linea['positives'] = valor['npos']
        linea['negatives'] = valor['nneg']
        linea['metrica'] = valor['met']
        linea = json.dumps(linea)
        outfile.write(linea)
        outfile.write("\n")
    outfile.close()

# Reports to MongoDB
def generateReports(host, name_collection='TweetsRepo', alertwords=None, StartDate=None, EndDate=None, output_json=False):

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

    #cfgmanager.MongoDBSpecs['host'] 
    collreporting = db.Reporting
    
    if output_json:
        outfile = open('report_days.json', 'w')
        # 1º ListOfDays:
        print("Writing report by days...")
        for values in genListOfdays(StartDate, EndDate):
            linea = {}
            valor = aggCount(values['start'], values['end'], coll)
            # linea['date'] = values['start']
            linea['start'] = values['start'].strftime("%Y-%m-%d")
            linea['end'] = values['end'].strftime("%Y-%m-%d")
            linea['tweets'] = valor['count']
            linea['positives'] = valor['npos']
            linea['negatives'] = valor['nneg']
            linea['metrica'] = valor['met']
            linea['report'] = {'type':'daily', 'from':name_collection}
            if alertwords:
                linea['alert words'] = alertWords(values['start'].strftime("%Y%m%d"),
                                                  values['end'].strftime("%Y%m%d"), 
                                                  coll, alertwords)
            linea = json.dumps(linea)
            outfile.write(linea)
            outfile.write("\n")
        outfile.close()

        outfile = open('report_weeks.json', 'w')
        # 2º ListOfWeeks:
        print("Writing report by weeks...")
        for values in genListOfWeeks(StartDate, EndDate):
            linea = {}
            valor = aggCount(values['start'], values['end'], coll)
            linea['start'] = values['start'].strftime("%Y-%m-%d")
            linea['end'] = values['end'].strftime("%Y-%m-%d")
            linea['tweets'] = valor['count']
            linea['positives'] = valor['npos']
            linea['negatives'] = valor['nneg']
            linea['metrica'] = valor['met']
            linea['report'] = {'type':'daily', 'from':name_collection}
            if alertwords:
                linea['alert words'] = alertWords(values['start'].strftime("%Y%m%d"),
                                                  values['end'].strftime("%Y%m%d"), 
                                                  coll, alertwords)
            linea = json.dumps(linea)
            outfile.write(linea)
            outfile.write("\n")
        outfile.close()

        outfile = open('report_months.json', 'w')
        # 3º ListOfMonth:
        print("Writing report by monts...")
        for values in genListOfMonth(StartDate, EndDate):
            linea = {}
            valor = aggCount(values['start'], values['end'], coll)
            # linea['date'] = values['start']
            linea['start'] = values['start'].strftime("%Y-%m-%d")
            linea['end'] = values['end'].strftime("%Y-%m-%d")
            linea['tweets'] = valor['count']
            linea['positives'] = valor['npos']
            linea['negatives'] = valor['nneg']
            linea['metrica'] = valor['met']
            linea['report'] = {'type':'daily', 'from':name_collection}
            if alertwords:
                linea['alert words'] = alertWords(values['start'].strftime("%Y%m%d"),
                                                  values['end'].strftime("%Y%m%d"), 
                                                  coll, alertwords)
            linea = json.dumps(linea)
            outfile.write(linea)
            outfile.write("\n")
        outfile.close()

    else:
        print("Uploading report by days...")
        # 1º ListOfDays:
        for values in genListOfdays(StartDate, EndDate):
            linea = {}
            valor = aggCount(values['start'], values['end'], coll)
            linea['start'] = values['start'].strftime("%Y%m%d")
            linea['end'] = values['end'].strftime("%Y%m%d")
            linea['tweets'] = valor['count']
            linea['positives'] = valor['npos']
            linea['negatives'] = valor['nneg']
            linea['metrica'] = valor['met']
            linea['report'] = {'type':'daily', 'from':name_collection}
            key = values['start'].strftime("%Y%m%d") + values['end'].strftime("%Y%m%d")
            if alertwords:
                linea['alert words'] = alertWords(values['start'].strftime("%Y%m%d"),
                                                  values['end'].strftime("%Y%m%d"), 
                                                  coll, alertwords)
            collreporting.update({"_id":key}, linea, upsert = True)

        print("Uploading report by weeks...")
        # 2º ListOfWeeks:
        for values in genListOfWeeks(StartDate, EndDate):
            linea = {}
            valor = aggCount(values['start'], values['end'], coll)
            linea['date'] = values['start']
            linea['start'] = values['start']
            linea['end'] = values['end']
            linea['tweets'] = valor['count']
            linea['positives'] = valor['npos']
            linea['negatives'] = valor['nneg']
            linea['metrica'] = valor['met']
            linea['report'] = {'type':'weekly', 'from':name_collection}
            key = values['start'].strftime("%Y%m%d") + values['end'].strftime("%Y%m%d")
            if alertwords:
                linea['alert words'] = alertWords(values['start'].strftime("%Y%m%d"),
                                                  values['end'].strftime("%Y%m%d"),
                                                  coll, alertwords)
            collreporting.update({"_id":key}, linea, upsert = True)

        print("Uploading report by months...")
        # 3º ListOfMonth:
        for values in genListOfMonth(StartDate, EndDate):
            linea = {}
            valor = aggCount(values['start'], values['end'], coll)
            linea['date'] = values['start']
            linea['start'] = values['start']
            linea['end'] = values['end']
            linea['tweets'] = valor['count']
            linea['positives'] = valor['npos']
            linea['negatives'] = valor['nneg']
            linea['metrica'] = valor['met']
            linea['report'] = {'type':'monthly', 'from':name_collection}
            key = values['start'].strftime("%Y%m%d") + values['end'].strftime("%Y%m%d")
            if alertwords:
                linea['alert words'] = alertWords(values['start'].strftime("%Y%m%d"),
                                                  values['end'].strftime("%Y%m%d"),
                                                  coll, alertwords)
            collreporting.update({"_id":key}, linea, upsert = True)