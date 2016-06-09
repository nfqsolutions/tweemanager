# -*- coding:utf-8 -*-
import pymongo
import datetime


# 1º ListOfdays:
def genListOfdays(StartDate, EndDate):
    """
    """
    onedaydelta = datetime.timedelta(1)
    StartDate = datetime.datetime(StartDate.year, StartDate.month, StartDate.day)
    EndDate = datetime.datetime(EndDate.year, EndDate.month, EndDate.day + 1)
    delta = EndDate - StartDate
    for i in xrange(delta.days):
        yield {'Start': StartDate, 'End': StartDate + onedaydelta}
        StartDate = StartDate + onedaydelta


# 2º ListOfWeeks:
def genListOfWeeks(StartDate, EndDate):
    """
    """
    onedaydelta = datetime.timedelta(1)
    oneweekdelta = datetime.timedelta(7)
    StartDate = datetime.datetime(StartDate.year, StartDate.month, StartDate.day)
    while StartDate.weekday() != 0:
        StartDate = StartDate - onedaydelta
    EndDate = datetime.datetime(EndDate.year, EndDate.month, EndDate.day) + onedaydelta
    deltadays = EndDate - StartDate
    deltaweeks = deltadays.days / 7
    for i in xrange(deltaweeks + 1):
        yield {'Start': StartDate, 'End': StartDate + oneweekdelta}
        StartDate = StartDate + oneweekdelta

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


# Agg Function:
def aggResults(StartDate, EndDate):
    """
    """
    pipeline = [
        {"$match": {"created_at": {"$gte": StartDate}, "created_at": {"$lt": EndDate}}},
        {"$group": {"_id": "", "count": {"$sum": 1}}},
    ]
    for result in coll.aggregate(pipeline):
        result = result
    return result
#
client = pymongo.MongoClient()
db = client.tweets
coll = db.Tweets
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
for values in genListOfdays(StartDate, EndDate):
    print(values,aggResults(values['Start'], values['End']))

# 2º ListOfWeeks:
for values in genListOfWeeks(StartDate, EndDate):
    print(values,aggResults(values['Start'], values['End']))

# 3º ListOfMonth:
for values in genListOfMonth(StartDate, EndDate):
    print(values,aggResults(values['Start'], values['End']))
