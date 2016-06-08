### Notas de usabilidad del comando **getoldtweets**:


Comando **getoldtweets**:

```bash
tweemanager getoldtweets
```

datos de entrada (fichero de configuración):


```
[GOTSpecs]
username = "barackobama"
querysearch = "barackobama"
maxtweets = 100
since = "2016-01-01"
until = "2016-05-01"
```

El comando funciona como la búsqueda avanzada que un puede realizar en la [página de twitter](https://twitter.com/search-advanced).

La información generada es similar a la da API oficial con algunas limitaciones ya que ni todos los campos están disponibles.

Puedes usar varias palabras en querysearch con OR y AND (en mayúsculas) y poner \" entre dos palabras consecutivas.
Para el username si se usan dos busca que el usuario1 haya mencionado al usuario2
Las búsquedas no son case sensitive. Ejemplo:
```
[GOTSpecs]
username = "barackobama"
querysearch = "Donald Trump"
maxtweets = 100
```
obtiene resultados distintos de
```
[GOTSpecs]
username = "barackobama"
querysearch = "Donald Trump"
maxtweets = 100
```
y también resultados distintos de:
```
[GOTSpecs]
username = "barackobama OR hillaryclinton"
querysearch = "Donald Trump"
maxtweets = 10
```