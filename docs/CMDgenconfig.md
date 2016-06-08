### Notas de usabilidad del comando **genconfig**:


Comando **genconfig**:

```bash
tweemanager genconfig
```

Este comando genera un fichero template de configuración:
```
[TwitterAPIcredentials]
consumer_key =
consumer_secret =
access_key =
access_secret =

[ListenerSpecs]
usersarray =
trackarray =

[SearchSpecs]
searchquery =
maxtweets =

[GOTSpecs]
username =
since =
until =
querysearch =
maxtweets =

[TextPatterns]
patternstoexclude =
patternstoinclude =
langtoinclude =

[MongoDBSpecs]
repocollname =
name =
username =
password =
host =

[ElasticSpecs]
host =
index =
username =
password =
```

Solamente tienes que usar/rellenar los campos que necesite cada comando.
Los tipos de datos son json o sea strings con \"\" int y floats normal y listas con \[\].
