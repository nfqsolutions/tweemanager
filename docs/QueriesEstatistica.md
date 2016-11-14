# Queries más frecuentes de estadistica y información relevante del repositorio:

1. Número de tweets valorados manualmente:
	```javascript
	db.Tweets.count({"valuation.manual":{"$exists":true}})
	```

2. Número de positivos, negativos y no valorados manualmente:
	```javascript
	db.Tweets.group(
	   {
	     key: { 'valuation.manual': 1 },
	     reduce: function( curr, result ) {
	                 result.total += 1;
	             },
	     initial: { total : 0 }
	   }
	)
	```

3. Número de positivos y negativos del clasificador:
	```javascript
	db.Tweets.group(
	   {
	     key: { 'valuation.classifier1.value': 1 },
	     reduce: function( curr, result ) {
	                 result.total += 1;
	             },
	     initial: { total : 0 }
	   }
	)
	```

4. Número de tweets por dispositivos/app del tweet:
	```javascript
	db.Tweets.group(
	   {
	     key: { 'source': 1 },
	     reduce: function( curr, result ) {
	                 result.total += 1;
	             },
	     initial: { total : 0 }
	   }
	)
	```

	Para este caso es conviniente ordenar. Para hacer este tipo de operaciones hay que recorrer al pipeline de agregacion.

	```javascript
	db.Tweets.aggregate([
	{ $project : { "source": 1, _id: 0 } },
	{ $group : { _id: "$source", total: {$sum: 1}} },
	{ $sort: {total: -1}}
	])
	```

	Al estilo histograma podemos realizar la siguiente operación: Contar los positivos y negativos por tipo de tweet:

	```javascript
	db.Tweets.aggregate([
	{ $project : { "source": 1, "valuation": 1, _id: 0 } },
	{ $group : { _id: "$source", 
                     "total_Good": {"$sum": {"$cond":[{"$eq":["$valuation.classifier1.value","positive"]},1,0]}},
                     "total_Bad": {"$sum": {"$cond":[{"$eq":["$valuation.classifier1.value","negative"]},1,0]}},
                     "total": {"$sum": 1}
                   }
        },
	{ $sort: {"total": -1}}
	])
	```

	El problema de este ultimo es que requiere conocer los valores que queremos agregar en segundo nivel. Para poder realizar la misma operacion sin conocer los valores podemos realizar un duplo group:

	```javascript
	db.Tweets.aggregate([
	{ $project : { "source": 1, "valuation": 1, _id: 0 } },
	{ $group : { _id: {source: "$source",
	                   valuation : "$valuation.classifier1.value"},
                     total:{"$sum":1}}
        },
    { $project : { source: "$_id.source", valuation: "$_id.valuation",total: "$total", _id: 0 } },
    { $sort: {"total": -1}}
	])
	```

5. Número de tweets positivos y negativos por idioma:
	
	```javascript
	db.Tweets.aggregate([
	{ $project : { "lang": 1, "valuation": 1, _id: 0 } },
	{ $group : { _id: {source: "$lang",
	                   valuation : "$valuation.classifier1.value"},
                     total:{"$sum":1}}
        },
    { $project : { source: "$_id.source", valuation: "$_id.valuation",total: "$total", _id: 0 } },
    { $sort: {"total": -1}}
	])
	```

	En el punto anterior vimos como realizar esta operación.

6. Número de tweets positivos y negativos por semana:

	```javascript
	db.Tweets.aggregate([
	{ '$project' : { "source": 1, "valuation": 1, '_id': 0, 'week': { '$week': "$created_at" } } },
	{ '$group' : { '_id': "$week", 
	                 "total_positivos": {"$sum": {"$cond":[{"$eq":["$valuation.algoritmo_1.clasificado","positivo"]},1,0]}},
	                 "total_negativos": {"$sum": {"$cond":[{"$eq":["$valuation.algoritmo_1.clasificado","negativo"]},1,0]}},
	                 "total": {"$sum": 1},
	               }
	    },
	{ '$project' : { "semana": "$_id", "positivos": "$total_positivos", "negativos":"$total_negativos", "total":"$total","por_valorar":{'$subtract':["$total",{'$add':["$total_positivos", "$total_negativos"]}]} } },
	{ '$sort': {"semana": 1}}
	])
	```

	Permite realizar un reporting semanal de nuestra base de datos