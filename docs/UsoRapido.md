1. Clona este repositorio:

	```bash
	git clone https://github.com/ekergy/tweemanager.git
	```

2. Instala las dependencias minimas necesarias:

	```bash
	pip install -r requirementsUsoRapido.txt
	```

	> Nota: Opcionalmente instala un venv (o virtualenv) con tu instalación de python. Puedes usar Python 2.7 o Python 3.5 (si tienes algun problema o encuentras uno pon una issue [*s’il vous plait*](https://github.com/ekergy/tweemanager/issues))


3. Busca unos cuantos tweets (con la API oficiosa **getoldtweets**):

	```bash
	python tweemanager getoldtweets -c tweemUsoRapido.cfg -o TestUsoRapido.json
	```

	> Nota: Para este caso ni hay que registrar una app en twitter.

	consulta la página [CMDgetoldtweets.md](./CMDgetoldtweets.md) para más info del comando.

	Ya tenemos unos cuantos tweets. Podriamos procesar la información que hemos obtenido con alguno visualizador/procesador de datos.

4. Inserta los datos en mongodb:

	Añade mongo a tu fichero de configuración:
	```
	[MongoDBSpecs]
	host=mongodb://127.0.0.1/tweets
	repocollname=RepoDeTweets
	```

	y ejecuta el comando de importación para importar los datos obtenidos anteriormente:
	```bash
	python tweemanager importToMongo TestUsoRapido.json
	```

	> Nota: podemos realizar el paso anterior directamente para mongo usando la opción *-o mongodb*: ```python tweemanager importToMongo TestUsoRapido.json -o mongodb```


