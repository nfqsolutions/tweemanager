### Notas de usabilidad del comando **genconfig**:


Comando **genconfig**:

```bash
tweemanager genconfig
```

Este comando genera un fichero template de configuración:
```
[TwitterAPIcredentials]
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

[ListenerSpecs]
usersarray = []
trackarray = []

[SearchSpecs]
searchquery = []
maxtweets = 100

[GOTSpecs]
username = ""
since = ""
until = ""
querysearch = [""]
maxtweets = 100

[TextPatterns]
patternstoexclude = []
patternstoinclude = []
langtoinclude = []
alertwords = []

[MongoDBSpecs]
repocollname = ""
name = ""
username = ""
password = ""
host = ""

[ElasticSpecs]
host = ""
index = ""
username = ""
password = ""
```

Tienes que usar/rellenar los campos que necesites en cada momento y borrar los que no.
Los tipos de datos son json o sea strings con \"\" int y floats normal y listas con \[\].
