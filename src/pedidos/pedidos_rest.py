#!/usr/bin/env python
# coding: utf-8

from flask import Flask, jsonify, request
import json
import sys, os.path
from os import environ
from container import Container

app = Flask(__name__)


# Establecer valores para la conexión a la BD.
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

db_name = "ms_pedidos"
if "DB_NAME" in environ and environ['DB_NAME'] != "":
    db_name = environ['DB_NAME']
    

# Inyección de dependencias
# ----------------------------------------------------------
container = Container(config={
                                'username': username,
                                'password': password,
                                'host': host,
                                'port': port,
                                'db_name': db_name
                            })
gestorPedidos = container.gestor_pedidos()
gestorPedidos.connect()
# ----------------------------------------------------------


# Consultas genéricas con pedidos
@app.route('/pedidos', methods = ['GET', 'POST'])
def pedidos():
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
                return response, 404
        except ValueError as error:
            response = {"mensaje": str(error)}
            return response, 400

    # Insertar un pedido nuevo
    elif request.method == 'POST':
        try:
            pedido_json = request.get_json()
            gestorPedidos.insertarPedido(pedido_json)
            response = {"mensaje": "Pedido insertado con éxito"}
            return response, 201
        except ValueError as error:
            response = {"mensaje": str(error)}
            return response, 400


# Consultas genéricas con un pedido determinado
@app.route('/pedidos/<id_pedido>', methods = ['GET', 'PUT', 'DELETE'])
def pedido(id_pedido):
    response = ""

    # Obtener un pedido
    if request.method == 'GET':
        try:
            pedido = gestorPedidos.getPedido(id_pedido)
            if(pedido):
                response = {"pedido": json.loads(gestorPedidos.getPedido(id_pedido).toJSON())}
                return response, 200
            else:
                response = {"mensaje": "No existe el pedido con id: " + id_pedido}
                return response, 404
        except ValueError as error:
            response = {"mensaje": str(error)}
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
                response = {"mensaje": "No existe un pedido con id: " + id_pedido}
                return response, 404
        except ValueError as error:
            response = {"mensaje": str(error)}
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
            response = {"mensaje": str(error)}
            return response, 400


# Consultas con el estado los pedidos
@app.route('/pedidos/estado/<estado>', methods = ['GET'])
def pedidosEstado(estado):
    response = ""

    # Devuelve el estado del pedido indicado
    if request.method == 'GET':
        try:
            pedidos = gestorPedidos.getPedidosEstado(estado)
            if len(pedidos) > 0:
                pedidos_json = []
                for p in pedidos:
                    pedidos_json.append(json.loads(p.toJSON()))
                response = {"pedidos": pedidos_json}
                return response, 200
            else:
                response = {"mensaje": "No existe ningún pedido con estado " + estado}
                return response, 404
        except ValueError as error:
            response = {"mensaje": str(error)}
            return response, 400


# Consultas sobre el estado de un pedido determinado
@app.route('/pedidos/<id_pedido>/estado', methods = ['GET', 'PUT'])
def estadoPedido(id_pedido):
    response = ""

    # Obtener estado de un pedido determinado
    if request.method == 'GET':
        try:
            pedido = gestorPedidos.getPedido(id_pedido)
            if(pedido):
                response = {"estado": pedido.getEstado()}
                return response, 200
            else:
                response = {"mensaje": "No existe el pedido con id: " + id_pedido}
                return response, 404
        except ValueError as error:
            response = {"mensaje": str(error)}
            return response, 400

    # Obtener estado de un pedido determinado
    if request.method == 'PUT':
        try:
            pedido = gestorPedidos.getPedido(id_pedido)
            if(pedido):
                estado = request.get_json()['estado']
                pedido_json = json.loads(pedido.toJSON())
                pedido_json['estado'] = estado
                gestorPedidos.modificarPedido(id_pedido, pedido_json)
                response = {"mensaje": "El estado del pedido con id: " + id_pedido + "ha sido modificado con éxito"}
                return response, 200
            else:
                response = {"mensaje": "No existe el pedido con id: " + id_pedido}
                return response, 404
        except ValueError as error:
            response = {"mensaje": str(error)}
            return response, 400


