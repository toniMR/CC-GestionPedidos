#!/usr/bin/env python
# coding: utf-8

from flask import Flask, request
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
            if len(pedidos) > 0:
                response = {"pedidos": pedidos}
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
            gestorPedidos.insertarPedido(request.get_json())
            response = {"mensaje": "Pedido insertado con éxito"}
            return response, 201
        except ValueError as error:
            response = {"mensaje": str(error)}
            return response, 400


# Consultas genéricas con un pedido determinado
@app.route('/pedidos/<pedido_id>', methods = ['GET', 'PUT', 'DELETE'])
def pedido(pedido_id):
    response = ""

    # Obtener un pedido
    if request.method == 'GET':
        try:
            pedido = gestorPedidos.getPedido(pedido_id)
            if(pedido):
                response = {"pedido": gestorPedidos.getPedido(pedido_id).toJSON()}
                return response, 200
            else:
                response = {"mensaje": "No existe el pedido con id: " + pedido_id}
                return response, 404
        except ValueError as error:
            response = {"mensaje": str(error)}
            return response, 400

    # Modificar un pedido
    if request.method == 'PUT':
        try:
            existe = gestorPedidos.getPedido(pedido_id)
            if existe:
                pedido_json = request.get_json()
                gestorPedidos.modificarPedido(pedido_id, pedido_json)
                response = {"mensaje": "Pedido modificado con éxito"}
                return response, 200
            else:
                response = {"mensaje": "No existe un pedido con id: " + pedido_id}
                return response, 404
        except ValueError as error:
            response = {"mensaje": str(error)}
            return response, 400

    # Borrar un pedido
    elif request.method == 'DELETE':
        try:
            pedido = gestorPedidos.getPedido(pedido_id)
            if(pedido):
                gestorPedidos.borrarPedido(pedido_id)
                response = {"mensaje": "El pedido con id: " + pedido_id + " se ha borrado exitosamente."}
                return response, 200
            else:
                response = {"mensaje": "No existe el pedido con id: " + pedido_id}
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
                response = {"pedidos": pedidos}
                return response, 200
            else:
                response = {"mensaje": "No existe ningún pedido con estado " + estado}
                return response, 404
        except ValueError as error:
            response = {"mensaje": str(error)}
            return response, 400


# Consultas sobre el estado de un pedido determinado
@app.route('/pedidos/<pedido_id>/estado', methods = ['GET', 'PUT'])
def estadoPedido(pedido_id):
    response = ""

    # Obtener estado de un pedido determinado
    if request.method == 'GET':
        try:
            pedido = gestorPedidos.getPedido(pedido_id)
            if(pedido):
                response = {"estado": pedido.getEstado()}
                return response, 200
            else:
                response = {"mensaje": "No existe el pedido con id: " + pedido_id}
                return response, 404
        except ValueError as error:
            response = {"mensaje": str(error)}
            return response, 400

    # Obtener estado de un pedido determinado
    if request.method == 'PUT':
        try:
            pedido = gestorPedidos.getPedido(pedido_id)
            if(pedido):
                pedido.setEstado(request.get_json()['estado'])
                gestorPedidos.modificarPedido(pedido_id, pedido.toJSON())
                response = {"mensaje": "El estado del pedido con id: " + pedido_id + "ha sido modificado con éxito"}
                return response, 200
            else:
                response = {"mensaje": "No existe el pedido con id: " + pedido_id}
                return response, 404
        except ValueError as error:
            response = {"mensaje": str(error)}
            return response, 400


