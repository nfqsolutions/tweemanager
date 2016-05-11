# Queries más frecuentes para el esquema inducido por los tweets

1. Número de tweets en base de datos:
	```javascript
	db.Tweets.count()
	```

2. Número de tweets que no están en español:
	```javascript
	db.Tweets.find({"lang": {"$eq": "es"}}).count()
	```

3. Número de tweets entre dos fechas:
	```javascript
	db.Tweets.find({"created_at":{$gt: new ISODate('2016-04-25'), $lt: new ISODate('2016-04-25 12:19:08.000Z')}})
	```

4. Conteo de los hashtags ordenado por ocurrencias:
	```javascript
	db.Tweets.aggregate([
		{$unwind:"$entities.hashtags"},
		{$group: {_id: "$entities.hashtags.text", total: {$sum: 1} }},
		{$sort:{total:-1}}])
	```

5. Contar el número de idiomas distintos ordenados por hashtag:

	5.1 Programático:

		```javascript
		Nlanguages = db.Tweets.distinct("lang");
		for (i=0; i< Nlanguages.length; i++) {
		    print(Nlanguages[i], db.Tweets.find({"lang": Nlanguages[i] }).count() );
		}
		```

	5.2 Aggregación:		
	
		```javascript
		db.Tweets.aggregate({$group: {_id: "$lang", total: {$sum: 1} }})
		```

6. Contar palabras con stopwords:
