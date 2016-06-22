# -*- coding:utf-8 -*-
import pymongo
import datetime
import json
from bson.code import Code

# IP host should be changed to your MongoDB server
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client.tweets
coll = db.Tweets
name_collection = coll.name

# List of alert words - a list of warning words
alert_words = ["perro", "gato", "cajero", "moneda"]

mapper = Code("""
    function() {  
    var summary = this.text_clean;
    var alert_words = """
                  + str(alert_words) +
                    """
    if (summary) { 
        summary = summary.toLowerCase().split(" "); 
        for (var i = 0; i < summary.length; i++) {
            if ( alert_words.indexOf(summary[i]) != -1){
                if (summary[i])  {
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

# It prints the results
result = coll.map_reduce(mapper, reducer, "word_count")
for doc in result.find():
    print(doc)