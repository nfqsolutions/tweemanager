### Notas de usabilidad del comando **listener**:

Para usar este comando hay que tener definida una aplicación en twitter y crear las claves necesarias para acceder a la API oficial:
```
[TwitterAPIcredentials]
consumer_key = un_consumer_key
consumer_secret = un_consumer_secret
access_key = un_access_key
access_secret = un_access_secret
```
> Nota: Para obtener estas claves tienes que tener una cuenta en [twitter](https://twitter.com/), entrar en la cuenta y ir a la [página de aplicaciones de twitter](https://apps.twitter.com/) crear una nueva aplicación (que genera las *consumer keys* ) y generar las Access Tokens. Esa es la información necesaria para poder usar la API.

añade las *track words* que quieres **escuchar**:
```
[ListenerSpecs]
trackarray = ["palabras","cosas"]
```

y lanza el comando:
```
python tweemanager listener -c tweemUsoRapido.cfg
```

Al construir el trackarray hay que tener en cuenta la información del la [api para streaming](https://dev.twitter.com/streaming/overview/request-parameters#track). Tiene algunas limitaciones y por veces hay que escribir algunas **patterns** filtrar los tweets obtenidos de esta forma.

Para guardar los datos en mongodb:
```
python tweemanager listener -c tweemUsoRapido.cfg -o mongodb
```
o guárdalos en un fichero y usa el comando importToMongo.