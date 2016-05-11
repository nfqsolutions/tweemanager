1. Clona este repositorio:

	```bash
	git clone https://github.com/ekergy/tweemanager.git
	```

2. Instala las dependencias minimas necesarias:

	```bash
	pip install -r requirementsUsoRapido.txt
	```

	> Nota: Opcionalmente instala un venv (o virtualenv) con tu instalación de python. Puedes usar Python 2.7 o Python 3.5 (si tienes algun problema o encuentras uno reporta en el repositorio *s’il vous plait*)


3. Busca unos cuantos tweets (con la API oficiosa **getoldtweets**):

	```bash
	python tweemanager getoldtweets -c tweemUsoRapido.cfg -o TestUsoRapido.json
	```

	> Nota: Para este caso ni hay que registrar una app en twitter.

	consulta la página [CMDgetoldtweets.md](./CMDgetoldtweets.md) para conocer el funcionamiento del comando.




