### Notas de usabilidad de las opciones de **TextPatterns**:

La opción TextPatterns del fichero de configuración permite filtrar los tweets una vez que hayan sido recuperados por alguno de los comandos.
Su principal usabilidad esta asociada al comando [**listener**](./CMDlistener.md) ya que la API oficial de twitter de streaming tiene algunas limitaciones cuanto a las palabras que puede buscar.

**TextPatterns** contiene tres campos:

```
[TextPatterns]
patternstoexclude = 
patternstoinclude = 
langtoinclude = 
```
los caso de uso son:

1. Solo patternstoexclude:
	```
	[TextPatterns]
	patternstoexclude = ["un beso"]
	```
	Todos los tweets se consideran buenos excepto los que contienen "un beso"

 2. Solo patternstoinclude:
 	```
 	[TextPatterns]
	patternstoinclude = ["un beso"]
 	```
 	Todos los tweets son candidatos a seren excluidos excepto los que contienen "un beso".

 3. Definido las dos patterns:
 	```
 	[TextPatterns]
	patternstoexclude = ["beso"]
	patternstoinclude = ["un beso"]
	```
	Todos los tweets se consideran buenos. Si alguno de ellos contiene "beso" sera excluido excepto cuando contenga "un beso".

Estos casos no cubren todos los resultados posibles pero si cubren los resultados necesarios para procesar un tweet correctamente desde el punto de vista del paquete.

