#!/usr/bin/env python
# coding: utf-8

from flask import Flask, jsonify
import sys, os.path
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
