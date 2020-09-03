#!/usr/bin/env python
# coding: utf-8

from flask import Blueprint, request, current_app

api = Blueprint('pedidos', __name__, url_prefix='/')


# Consultas genéricas con pedidos
@api.route('/pedidos', methods = ['GET', 'POST'])
def pedidos():
    gestorPedidos = current_app.container.gestor_pedidos()
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
@api.route('/pedidos/<pedido_id>', methods = ['GET', 'PUT', 'DELETE'])
def pedido(pedido_id):
    gestorPedidos = current_app.container.gestor_pedidos()
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
@api.route('/pedidos/estado/<estado>', methods = ['GET'])
def pedidosEstado(estado):
    gestorPedidos = current_app.container.gestor_pedidos()
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
@api.route('/pedidos/<pedido_id>/estado', methods = ['GET', 'PUT'])
def estadoPedido(pedido_id):
    gestorPedidos = current_app.container.gestor_pedidos()
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

            