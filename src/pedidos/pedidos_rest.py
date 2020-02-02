#!/usr/bin/env python
# coding: utf-8

from flask import Flask, jsonify, request
import json
import sys, os.path
from os import environ
from gestorPedidos import GestorPedidos
from data_managers.pgsqlDataManager import PgsqlDataManager

app = Flask(__name__)

# Establecer valores por defecto
username = "username"
if "DB_USERNAME" in environ and environ['DB_USERNAME'] != "":
    username = environ['DB_USERNAME']   

password = "password"
if "DB_PASSWORD" in environ and environ['DB_PASSWORD'] != "":
    password = environ['DB_PASSWORD']

host = "127.0.0.1"
if "DB_HOST" in environ and environ['DB_HOST'] != "":
    host = environ['DB_HOST']

port = "5432"
if "DB_PORT" in environ != "" and environ['DB_PORT'] != "":
    port = environ['DB_PORT']

bd_name = "ms_pedidos"
if "DB_NAME" in environ and environ['DB_NAME'] != "":
    bd_name = environ['DB_NAME']

# Seleccionar el data_manager
data_manager = PgsqlDataManager(username, password, host, port, bd_name)
data_manager.connect()

gestorPedidos = GestorPedidos(data_manager)


# Devuelve los pedidos existentes
@app.route('/pedidos', methods = ['GET', 'POST'])
def getPedidos():
    response = ""

    # Devuelve los pedidos existentes
    if request.method == 'GET':
        try:
            pedidos = gestorPedidos.getPedidos()
            pedidos_json = []
            if len(pedidos) > 0:
                for p in pedidos:
                    pedidos_json.append(json.loads(p.toJSON()))

                response = {"pedidos": pedidos_json}
                return response, 200
            else:
                response = {"mensaje": "No existen pedidos"}
                return response, 200
        except ValueError as error:
            response = {"mensage": str(error)}
            return response, 400

    # Insertar un pedido nuevo
    elif request.method == 'POST':
        try:
            pedido_json = request.get_json()
            gestorPedidos.insertarPedido(pedido_json)
            response = {"mensaje": "Pedido insertado con éxito"}
            return response, 201
        except ValueError as error:
            response = {"mensage": str(error)}
            return response, 400

    return response


# Devuelve un pedido identificado por su id
@app.route('/pedidos/<id_pedido>', methods = ['GET', 'PUT', 'DELETE'])
def getPedido(id_pedido):
    response = ""

    # Obtener un pedido
    if request.method == 'GET':
        try:
            pedido = gestorPedidos.getPedido(id_pedido)
            if(pedido):
                response = {"pedido": json.loads(data_manager.getPedido(id_pedido).toJSON())}
                return response, 200
            else:
                response = {"mensaje": "No existe el pedido con id: " + id_pedido}
                return response, 404
        except ValueError as error:
            response = {"mensage": str(error)}
            return response, 400

    # Modificar un pedido
    if request.method == 'PUT':
        try:
            existe = gestorPedidos.getPedido(id_pedido)
            if existe:
                pedido_json = request.get_json()
                gestorPedidos.modificarPedido(id_pedido, pedido_json)
                response = {"mensaje": "Pedido modificado con éxito"}
                return response, 200
            else:
                response = {"mensage": "No existe un pedido con id: " + id_pedido}
                return response, 404
        except ValueError as error:
            response = {"mensage": str(error)}
            return response, 400

    # Borrar un pedido
    elif request.method == 'DELETE':
        try:
            pedido = gestorPedidos.getPedido(id_pedido)
            if(pedido):
                gestorPedidos.borrarPedido(id_pedido)
                response = {"mensaje": "El pedido con id: " + id_pedido + " se ha borrado exitosamente."}
                return response, 200
            else:
                response = {"mensaje": "No existe el pedido con id: " + id_pedido}
                return response, 404
        except ValueError as error:
            response = {"mensage": str(error)}
            return response, 400

    return response
