### Notas de usabilidad del comando **searchtweets**:

Para usar este comando hay que tener definida una aplicación en twitter y crear las claves necesarias para acceder a la API oficial:
```
[TwitterAPIcredentials]
consumer_key = un_consumer_key
consumer_secret = un_consumer_secret
access_key = un_access_key
access_secret = un_access_secret
```
> Nota: Para obtener estas claves tienes que tener una cuenta en [twitter](https://twitter.com/), entrar en la cuenta y ir a la [página de aplicaciones de twitter](https://apps.twitter.com/) crear una nueva aplicación (que genera las *consumer keys* ) y generar las Access Tokens. Esa es la información necesaria para poder usar la API.


añade la *query* de búsqueda y el numero máximo de tweets:
```
[SearchSpecs]
searchquery = barackobama
maxtweets = 100
```
y lanza el comando:
```
```

para construir tu query tiene en cuenta la [documentación oficial de Twitter](https://dev.twitter.com/rest/public/search).

para guardar los datos en mongodb:
```
```