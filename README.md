![Alt text](/docs/images/nfq_solutions.png?raw=true)
# Ekergy *OpenSource* Software by [NFQ solutions S.L.](http://nfq.es/solutions/)

## Tweemanager

### Como usar el código:

Código preparado para Python 2.7 Python 3.4 y Python 3.5

Para instalar el código:

Paso 0:

```bash
git clone https://github.com/ekergy/tweemanager.git && cd tweemanager
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
  En windows es posible que haya que instalar alguna dependencia precompilada (ej. lxml).
  Puedes descargar las dependencias [aquí](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml)

Paso 2:

Prueba el paquete
```bash
tweemanager -h
```
y deberás ver la ayuda del paquete.

Para un uso rápido [clica aquí](/docs/UsoRapido.md)

Puedes encontrar mas información en la carpeta [docs](/docs/)

### Licencia:

Tweemanager está distribuido bajo una licencia doble. El código fuente
es distribuido bajo licencia AGPL version 3, una copia de la licencia
(en inglés) está incluida con el código fuente. Si esta licencia
no se adecua a tus necesidades, puedes comprar una licencia comercial
de [NFQ Solutions](http://nfqsolutions.com).
