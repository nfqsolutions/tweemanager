# -*- coding: utf-8 -*-

from bson import json_util as json
import codecs
import datetime
import sys

# Introduces por linea de comandos "python dict_to_json.py file > file1.json"
# Pensado para tweets en diccionario de un archivo a un JSON

with open(sys.argv[1], 'r') as fichero:
    while 1:
        output = codecs.getwriter('utf8')(sys.stdout)
        linea = fichero.readline()
        try:
            linea = eval(linea)
            valor_json = json.dumps(linea, default=json.default, ensure_ascii=False)

            output.write(valor_json)
            output.write("\n")
        except Exception as e:
            if 'invalid' in str(e): # caso Status(), mal parseado
                pass
            else:
                raise
                break
