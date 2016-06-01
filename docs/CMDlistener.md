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

La api de streaming de twitter tiene alguna limitación. Por ejemplo no se puede buscar **"un beso"** como palabra.
El stream devolverá cosas como:
"No hay nada que un buen beso no pueda curar."
que puede o no ser apropriado para nuestro escuchador.

Para poder filtrar datos de este tipo podemos usar la sección de TextPatterns del fichero de configuración.

Cuando definido estos campos permiten introducir patrones de busqueda extra sobre el text del tweet, garantizando que solamente estamos guardanto tweets con secuencias de palabras correctas.

En el ejemplo anterior para garantizar que solamente tweets con **"un beso"** son registrados tenemos que añadir la siguiente configuración:

```
[TextPatterns]
patternstoexclude = ["un beso"]
```