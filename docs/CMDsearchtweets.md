### Notas de usabilidad del comando **searchtweets**:

Para usar el comando **searchtweets** hay que definir una aplicación en twitter y crear las claves necesarias para acceder a la API oficial:
```
[TwitterAPIcredentials]
consumer_key = un_consumer_key
consumer_secret = un_consumer_secret
access_key = un_access_key
access_secret = un_access_secret
```
> Nota: Para obtener estas claves hay que tener una cuenta en [twitter](https://twitter.com/), hacer login y ir a la [página de aplicaciones de twitter](https://apps.twitter.com/), crear una nueva aplicación (que genera las *consumer keys* ) y generar las Access Tokens para esa aplicación.

añade la *query* de búsqueda y el numero máximo de tweets a tu fichero de configuración:
```
[SearchSpecs]
searchquery = barackobama
maxtweets = 100
```
y lanza el comando:
```
python tweemanager searchtweets -c tweemUsoRapido.cfg
```
usa la opción -o o el redireccionador ">" para guardar la busqueda en un fichero.

para construir tu query tiene en cuenta la [documentación oficial de Twitter](https://dev.twitter.com/rest/public/search).

para guardar los datos en mongodb:
```
python tweemanager searchtweets -c tweemUsoRapido.cfg -o mongodb
```
o guárdalos en un fichero y usa el comando importToMongo.