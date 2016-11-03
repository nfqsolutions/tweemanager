![Alt text](/docs/images/nfq_solutions.png?raw=true)

# *Tweemanager OpenSource Software by [NFQ](http://nfq.es/solutions/)*

## NFQ

En [NFQ](http://nfq.es/solutions/) ponemos la tecnología, la ciencia y la innovación al servicio de nuestros clientes. Contamos con múltiples soluciones propias, implantadas en entidades nacionales e internacionales que permiten cubrir el grueso de necesidades en el ámbito de la gestión, la medición y el control de riesgos.

## Tweemanager

Tweemanager es un paquete escrito en Python que recolecta y almacena información desde Twitter, al mismo tiempo que permite procesar dicha información. Esta librería es la parte *opensource* que se engloba dentro de la aplicación comercial [Qdos](http://qdosapp.com/).

## Qdos

La reputación corporativa puede convertirse en un obstáculo para el crecimiento de la empresa. La opinión que una entidad proyecta o transmite dentro de su sistema de negocio consiste en un factor de riesgo actual o futuro para los beneficios, fondos propios o liquidez, derivado de un daño en la reputación de la misma.

[Qdos](http://qdosapp.com/) analiza de forma automática y en tiempo real la reputación corporativa mediante un conjunto de indicadores previamente definidos que nos permite obtener una medida de riesgo.

### PyCon ES 2016

El trabajo matemático e informático desarrollado para conseguir esta aplicación fue expuesto en la conferencia de Python [PyCon ES 2016](http://2016.es.pycon.org/es/), y la presentación está disponible [aquí](https://github.com/cperales/Riesgo-Reputacional-PyConES2016).

## Como usar el código de Tweemanager:

Código preparado para Python 2.7, Python 3.4 y Python 3.5

Para instalar el código:

Paso 0:

```bash
git clone https://github.com/nfqsolutions/tweemanager.git && cd tweemanager
```

Paso 1:

```bash
virtualenv2 .env # opcional
# or
pyvenv .env # opcional
source .env/bin/activate && pip install --upgrade pip # optional
python setup.py install
```

> Si encuentras algún problema reclama [aquí](https://github.com/ekergy/tweemanager/issues).
  En Windows es posible que haya que instalar alguna dependencia precompilada (ej. lxml).
  Puedes descargar las dependencias [aquí](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml)

Paso 2:

Prueba el paquete
```bash
tweemanager -h
```
y deberás ver la ayuda del paquete.

Para un uso rápido [clica aquí](/docs/UsoRapido.md)

Puedes encontrar mas información en la carpeta [docs](/docs/)

## Licencia:

Tweemanager está distribuido bajo una licencia doble. El código fuente
es distribuido bajo licencia AGPL version 3, una copia de la licencia
(en inglés) [está incluida](LICENSE.md) con el código fuente. Si esta licencia
no se adecua a tus necesidades, puedes comprar una licencia comercial
de [NFQ Solutions](http://nfqsolutions.com).
