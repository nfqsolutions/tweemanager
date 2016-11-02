1.- Clona este repositorio:

```bash
git clone https://github.com/ekergy/tweemanager.git
```

2.- Instala el paquete:

```bash
python setup.py install
```

> Nota: Opcionalmente instala un venv (o virtualenv) con tu instalación de python. Puedes usar Python 2.7, Python 3.4 o Python 3.5 (si tienes algún problema o encuentras uno [notifica el problema](https://github.com/ekergy/tweemanager/issues))


3.- Busca unos cuantos tweets:

```bash
tweemanager getoldtweets -c tweemUsoRapido.cfg -o TestUsoRapido.json
```

> Nota: Para este caso no hay que registrar una app en twitter.

consulta la página [CMDgetoldtweets.md](./CMDgetoldtweets.md) para más info del comando.

Ya tenemos unos cuantos tweets. Estos pueden ser mostrados por pantalla o guardados en una base de datos, como mongodb.

4.- Inserta los datos en mongodb:

Añade mongo a tu fichero de configuración:
```
[MongoDBSpecs]
host="mongodb://127.0.0.1/tweets"
repocollname="RepoDeTweets"
```

y ejecuta el comando de importación para importar los datos obtenidos anteriormente:
```bash
tweemanager importToMongo TestUsoRapido.json
```

> Nota: podemos realizar el paso anterior directamente para mongo usando la opción *-o mongodb*: ```tweemanager importToMongo TestUsoRapido.json -o mongodb```

En el caso de poseer un clasificador, puedes generar un informe de clasificación. Como ejemplo tonto:

```bash
 python scripts/dummyClassifier.py
```
