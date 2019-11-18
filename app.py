#!/usr/bin/env python
# coding: utf-8

from flask import Flask, jsonify
import sys, os.path

# Añadir la ruta de los módulos 
src_path = (os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
+ '/src/pedidos/')
sys.path.append(src_path)

from gestorPedidos import GestorPedidos

app = Flask(__name__)

gestorPedidos = GestorPedidos("data/pedidos/test_pedidos.json")


# Devuelve los pedidos existentes
@app.route('/pedidos', methods = ['GET'])
def getPedidos():
    return jsonify(gestorPedidos.getPedidos())

# To Do
# ...
# ...
# ..


if __name__ == "__main__":
    # App will run on port 5000
	app.run(host='0.0.0.0', debug=False)