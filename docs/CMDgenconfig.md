### Notas de usabilidad del comando **genconfig**:


Comando **genconfig**:

```bash
python tweemanager genconfig
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
patternstoexclude = 
patternstoinclude = 

[SearchSpecs]
searchquery = 
maxtweets = 

[GOTSpecs]
username = 
since = 
until = 
querysearch = 
maxtweets = 

[MongoDBSpecs]
repocollname = 
name = 
username = 
password = 
host = 
```

Solamente tienes que usar/rellenar los campos que necesite cada comando.