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

4. Buscar una palabra o frase en un campo de los tweets:
	```javascript
	db.Tweets.find({"text":{"$regex":"que tal", "$options":"i"}}
	```
*$options* permite opciones de búsqueda *regex* como *i* (que significa *sensitive case*).

5. Conteo de los hashtags ordenado por ocurrencias:
	```javascript
	db.Tweets.aggregate([
		{$unwind:"$entities.hashtags"},
		{$group: {_id: "$entities.hashtags.text", total: {$sum: 1} }},
		{$sort:{total:-1}}])
	```

6. Contar el número de idiomas distintos ordenados por hashtag:

	6.1 Programático:

		Nlanguages = db.Tweets.distinct("lang");
		for (i=0; i< Nlanguages.length; i++) {
		    print(Nlanguages[i], db.Tweets.find({"lang": Nlanguages[i] }).count() );
		}

	6.2 Aggregación:		

		db.Tweets.aggregate({$group: {_id: "$lang", total: {$sum: 1} }})
		

7. Contar palabras con stop words (Map-Reduce):

	```javascript
	var map = function() {  
	    var summary = this.text_clean;
	    var stopwords = ["atmention", "url", "de","la","que","el","en","y","a","los","del","se","las","por","un","para","con","no","una","su","al","lo","como","mas","pero","sus","le","ya","o","este","si","porque","esta","entre","cuando","muy","sin","sobre","tambien","me","hasta","hay","donde","quien","desde","todo","nos","durante","todos","uno","les","ni","contra","otros","ese","eso","ante","ellos","e","esto","mi","antes","algunos","que","unos","yo","otro","otras","otra","el","tanto","esa","estos","mucho","quienes","nada","muchos","cual","poco","ella","estar","estas","algunas","algo","nosotros","mi","mis","tu","te","ti","tu","tus","ellas","nosotras","vosostros","vosostras","os","mio","mia","mios","mias","tuyo","tuya","tuyos","tuyas","suyo","suya","suyos","suyas","nuestro","nuestra","nuestros","nuestras","vuestro","vuestra","vuestros","vuestras","esos","esas","estoy","estas","esta","estamos","estais","estan","este","estes","estemos","esteis","esten","estare","estaras","estara","estaremos","estareis","estaran","estaria","estarias","estariamos","estariais","estarian","estaba","estabas","estabamos","estabais","estaban","estuve","estuviste","estuvo","estuvimos","estuvisteis","estuvieron","estuviera","estuvieras","estuvieramos","estuvierais","estuvieran","estuviese","estuvieses","estuviesemos","estuvieseis","estuviesen","estando","estado","estada","estados","estadas","estad","he","has","ha","hemos","habeis","han","haya","hayas","hayamos","hayais","hayan","habre","habras","habra","habremos","habreis","habran","habria","habrias","habriamos","habriais","habrian","habia","habias","habiamos","habiais","habian","hube","hubiste","hubo","hubimos","hubisteis","hubieron","hubiera","hubieras","hubieramos","hubierais","hubieran","hubiese","hubieses","hubiesemos","hubieseis","hubiesen","habiendo","habido","habida","habidos","habidas","soy","eres","es","somos","sois","son","sea","seas","seamos","seais","sean","sere","seras","sera","seremos","sereis","seran","seria","serias","seriamos","seriais","serian","era","eras","eramos","erais","eran","fui","fuiste","fue","fuimos","fuisteis","fueron","fuera","fueras","fueramos","fuerais","fueran","fuese","fueses","fuesemos","fueseis","fuesen","sintiendo","sentido","sentida","sentidos","sentidas","siente","sentid","tengo","tienes","tiene","tenemos","teneis","tienen","tenga","tengas","tengamos","tengais","tengan","tendre","tendras","tendra","tendremos","tendreis","tendran","tendria","tendrias","tendriamos","tendriais","tendrian","tenia","tenias","teniamos","teniais","tenian","tuve","tuviste","tuvo","tuvimos","tuvisteis","tuvieron","tuviera","tuvieras","tuvieramos","tuvierais","tuvieran","tuviese","tuvieses","tuviesemos","tuvieseis","tuviesen","teniendo","tenido","tenida","tenidos","tenidas","tened"]
	    if (summary) { 
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
	};

	var reduce = function( key, values ) {    
	    var count = 0;    
	    values.forEach(function(v) {            
	        count +=v;    
	    });
	    return count;
	}

	// full thing
	db.Tweets.mapReduce(map, reduce, { out: "word_count" })
	```


8. Contar bigramas con stop-bigramas (Map-Reduce):

	```javascript
	var map = function() {  
    var summary = this.text_clean;
    var stopwords = ["atmention", "url", "de","la","que","el","en","y","a","los","del","se","las","por","un","para","con","no","una","su","al","lo","como","mas","pero","sus","le","ya","o","este","si","porque","esta","entre","cuando","muy","sin","sobre","tambien","me","hasta","hay","donde","quien","desde","todo","nos","durante","todos","uno","les","ni","contra","otros","ese","eso","ante","ellos","e","esto","mi","antes","algunos","que","unos","yo","otro","otras","otra","el","tanto","esa","estos","mucho","quienes","nada","muchos","cual","poco","ella","estar","estas","algunas","algo","nosotros","mi","mis","tu","te","ti","tu","tus","ellas","nosotras","vosostros","vosostras","os","mio","mia","mios","mias","tuyo","tuya","tuyos","tuyas","suyo","suya","suyos","suyas","nuestro","nuestra","nuestros","nuestras","vuestro","vuestra","vuestros","vuestras","esos","esas","estoy","estas","esta","estamos","estais","estan","este","estes","estemos","esteis","esten","estare","estaras","estara","estaremos","estareis","estaran","estaria","estarias","estariamos","estariais","estarian","estaba","estabas","estabamos","estabais","estaban","estuve","estuviste","estuvo","estuvimos","estuvisteis","estuvieron","estuviera","estuvieras","estuvieramos","estuvierais","estuvieran","estuviese","estuvieses","estuviesemos","estuvieseis","estuviesen","estando","estado","estada","estados","estadas","estad","he","has","ha","hemos","habeis","han","haya","hayas","hayamos","hayais","hayan","habre","habras","habra","habremos","habreis","habran","habria","habrias","habriamos","habriais","habrian","habia","habias","habiamos","habiais","habian","hube","hubiste","hubo","hubimos","hubisteis","hubieron","hubiera","hubieras","hubieramos","hubierais","hubieran","hubiese","hubieses","hubiesemos","hubieseis","hubiesen","habiendo","habido","habida","habidos","habidas","soy","eres","es","somos","sois","son","sea","seas","seamos","seais","sean","sere","seras","sera","seremos","sereis","seran","seria","serias","seriamos","seriais","serian","era","eras","eramos","erais","eran","fui","fuiste","fue","fuimos","fuisteis","fueron","fuera","fueras","fueramos","fuerais","fueran","fuese","fueses","fuesemos","fueseis","fuesen","sintiendo","sentido","sentida","sentidos","sentidas","siente","sentid","tengo","tienes","tiene","tenemos","teneis","tienen","tenga","tengas","tengamos","tengais","tengan","tendre","tendras","tendra","tendremos","tendreis","tendran","tendria","tendrias","tendriamos","tendriais","tendrian","tenia","tenias","teniamos","teniais","tenian","tuve","tuviste","tuvo","tuvimos","tuvisteis","tuvieron","tuviera","tuvieras","tuvieramos","tuvierais","tuvieran","tuviese","tuvieses","tuviesemos","tuvieseis","tuviesen","teniendo","tenido","tenida","tenidos","tenidas","tened"];
	    if (summary) { 
	        // quick lowercase to normalize per your requirements
	        summary = summary.toLowerCase().split(" "); 
	        for (var i = 0; i < summary.length - 1; i++) {
	            if ( stopwords.indexOf(summary[i]) == -1 && stopwords.indexOf(summary[i+1]) == -1){ // bigrams of stopowords are avoided                     
	                if (summary[i])  {      // make sure there's something
	                   emit(summary[i] + " " + summary[i+1], 1);
	                }
	            }
	        }
	    }
	};

	var reduce = function( key, values ) {    
	    var count = 0;    
	    values.forEach(function(v) {            
	        count +=v;    
	    });
	    return count;
	}

	// full thing
	db.Tweets.mapReduce(map, reduce, { out: "bigram_count" })
	```


