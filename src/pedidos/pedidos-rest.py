#!/usr/bin/env python
# coding: utf-8

from flask import Flask, jsonify, request
import json
import sys, os.path
from os import environ
from gestorPedidos import GestorPedidos
from data_managers.pgsqlDataManager import PgsqlDataMager

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
data_manager =PgsqlDataMager(username, password, host, port, bd_name)
data_manager.connect()

gestorPedidos = GestorPedidos(data_manager)


# Devuelve los pedidos existentes
@app.route('/pedidos', methods = ['GET', 'POST'])
def getPedidos():
    response = ""

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
