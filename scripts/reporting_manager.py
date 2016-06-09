# -*- coding:utf-8 -*-
import pymongo
import datetime


# 1º ListOfdays:
def genListOfdays(StartDate, EndDate=datetime.datetime.now()):
    """
    """
    # onedaydelta = datetime.timedelta(days=1)
    # StartDate = datetime.datetime(StartDate.year, StartDate.month, StartDate.day)
    # EndDate = datetime.datetime(EndDate.year, EndDate.month, EndDate.day)
    # while StartDate < EndDate:
    #     yield {'Start': StartDate, 'End': StartDate + onedaydelta}
    #     StartDate += onedaydelta

    # Old Code
    onedaydelta = datetime.timedelta(days=1)
    StartDate = datetime.datetime(StartDate.year, StartDate.month, StartDate.day)
    EndDate = datetime.datetime(EndDate.year, EndDate.month, EndDate.day)
    delta = EndDate - StartDate
    for i in xrange(delta.days):
        yield {'Start': StartDate, 'End': StartDate + onedaydelta}
        StartDate += onedaydelta


# 2º ListOfWeeks:
def genListOfWeeks(StartDate, EndDate):
    """
    """
    # onedaydelta = datetime.timedelta(days=1)
    # oneweekdelta = datetime.timedelta(days=7)
    # StartDate = datetime.datetime(StartDate.year, StartDate.month, StartDate.day)
    # while StartDate.weekday() != 0:
    #     StartDate = StartDate - onedaydelta
    # EndDate = datetime.datetime(EndDate.year, EndDate.month, EndDate.day) + onedaydelta
    # while StartDate < EndDate:
    #     yield {'Start': StartDate, 'End': StartDate + oneweekdelta}
    #     StartDate += oneweekdelta

    # Old Code
    onedaydelta = datetime.timedelta(days=1)
    oneweekdelta = datetime.timedelta(days=7)
    StartDate = datetime.datetime(StartDate.year, StartDate.month, StartDate.day)
    while StartDate.weekday() != 0:
        StartDate = StartDate - onedaydelta
    EndDate = datetime.datetime(EndDate.year, EndDate.month, EndDate.day) + onedaydelta
    deltadays = EndDate - StartDate
    deltaweeks = deltadays.days / 7
    for i in xrange(deltaweeks + 1):
        yield {'Start': StartDate, 'End': StartDate + oneweekdelta}
        StartDate += oneweekdelta

# 3º ListOfMonth:
def genListOfMonth(StartDate, EndDateInp):
    """
    """
    StartDate = datetime.datetime(StartDate.year, StartDate.month, 1)
    EndDate = datetime.datetime(StartDate.year, StartDate.month, 1)
    while EndDate < EndDateInp:
        EndDate = datetime.datetime(StartDate.year, StartDate.month + 1, 1)
        yield {'Start': StartDate, 'End': EndDate}
        StartDate = EndDate


# Agg Functions:
def aggCount(StartDate, EndDate):
    """
    It returns the number of tweets between a time interval
    """
    pipeline = [
        {"$match": {"$and": [{"created_at": {"$gte": StartDate}}, {"created_at": {"$lt": EndDate}}]}},
        {"$group": {"_id": "", "count": {"$sum": 1}}},
    ]
    result = {'count':0}
    for result in coll.aggregate(pipeline):
        result = result
    return result

def aggPositivos(StartDate, EndDate):
    """
    It returns the number of positive tweets classified by an algoritm in a time interval
    """
    pipeline = [
        {"$match": {"$and": [{"created_at": {"$gte": StartDate}}, {"created_at": {"$lt": EndDate}}]}},
        {"$group": {"_id": "", "npos": {"$sum": {"$cond":[{"$eq":["$valoration.algoritmo_7.clasificado","positivo"]},1,0]}}
        }},
    ]
    result = {'npos':0}
    for result in coll.aggregate(pipeline):
        result = result
    return result

def aggNegativos(StartDate, EndDate):
    """
    It returns the number of negative tweets classified by an algoritm in a time interval
    """
    pipeline = [
        {"$match": {"$and": [{"created_at": {"$gte": StartDate}}, {"created_at": {"$lt": EndDate}}]}},
        {"$group": {"_id": "", "nneg": {"$sum": {"$cond":[{"$eq":["$valoration.algoritmo_7.clasificado","negativo"]},1,0]}}
        }},
    ]
    result = {'nneg':0}
    for result in coll.aggregate(pipeline):
        result = result
    return result

def aggRepo(StartDate, EndDate):
    """
    It returns another features of our classifier
    """
    pipeline = [
        {"$match": {"$and": [{"created_at": {"$gte": StartDate}}, {"created_at": {"$lt": EndDate}}]}},
        {"$group": {"_id": "", "count": {"$sum": "$valoration.algoritmo_7.dis_pos"}
        }},
        ]
    result = {'count':0}
    for result in coll.aggregate(pipeline):
        result = result
    return result

if __name__ == '__main__':
    #
    client = pymongo.MongoClient('mongodb://127.0.0.1', 27017)
    db = client.tweets
    coll = db.TweetsRepo
    #

    # 1º get first date
    for tweet in coll.find().sort('created_at', 1).limit(1):
        StartDate = tweet['created_at']
    print(StartDate)
    # 2º get last date
    for tweet in coll.find().sort('created_at', -1).limit(1):
        EndDate = tweet['created_at']
    print(EndDate)
    # 3º get all data:

    # Perform aggregations on the time table:
    # 1º ListOfdays:
    print("Por días")
    for values in genListOfdays(StartDate, EndDate):
        print("Tweets")

        print(values['Start'].strftime("%Y-%m-%d"),
            values['End'].strftime("%Y-%m-%d"),
            aggCount(values['Start'], values['End'])['count'])
        print("Positivos")
        print(values['Start'].strftime("%Y-%m-%d"),
            values['End'].strftime("%Y-%m-%d"),
            aggPositivos(values['Start'], values['End'])['npos'])
        print("Negativos")
        print(values['Start'].strftime("%Y-%m-%d"),
            values['End'].strftime("%Y-%m-%d"),
            aggNegativos(values['Start'], values['End'])['nneg'])
        print("Métrica")
        print(values['Start'].strftime("%Y-%m-%d"),
            values['End'].strftime("%Y-%m-%d"),
            aggRepo(values['Start'], values['End'])['count'])
        print("")

    # 2º ListOfWeeks:
    print("Por semanas")
    for values in genListOfWeeks(StartDate, EndDate):
        print("Tweets")
        print(values['Start'].strftime("%Y-%m-%d"),
            values['End'].strftime("%Y-%m-%d"),
            aggCount(values['Start'], values['End'])['count'])
        print("Positivos")
        print(values['Start'].strftime("%Y-%m-%d"),
            values['End'].strftime("%Y-%m-%d"),
            aggPositivos(values['Start'], values['End'])['npos'])
        print("Negativos")
        print(values['Start'].strftime("%Y-%m-%d"),
            values['End'].strftime("%Y-%m-%d"),
            aggNegativos(values['Start'], values['End'])['nneg'])
        print("Métrica")
        print(values['Start'].strftime("%Y-%m-%d"),
            values['End'].strftime("%Y-%m-%d"),
            aggRepo(values['Start'], values['End'])['count'])
        print("")

    # 3º ListOfMonth:
    print("Por meses")
    for values in genListOfMonth(StartDate, EndDate):
        print("Tweets")
        print(values['Start'].strftime("%Y-%m-%d"),
            values['End'].strftime("%Y-%m-%d"),
            aggCount(values['Start'], values['End'])['count'])
        print("Positivos")
        print(values['Start'].strftime("%Y-%m-%d"),
            values['End'].strftime("%Y-%m-%d"),
            aggPositivos(values['Start'], values['End'])['npos'])
        print("Negativos")
        print(values['Start'].strftime("%Y-%m-%d"),
            values['End'].strftime("%Y-%m-%d"),
            aggNegativos(values['Start'], values['End'])['nneg'])
        print("Métrica")
        print(values['Start'].strftime("%Y-%m-%d"),
            values['End'].strftime("%Y-%m-%d"),
            aggRepo(values['Start'], values['End'])['count'])
        print("")