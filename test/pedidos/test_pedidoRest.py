#!/usr/bin/env python
# coding: utf-8

import unittest
import json
import sys, os.path

# Añadir la ruta de los módulos 
src_path = (os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
+ '/src/pedidos/')
sys.path.append(src_path)

from pedidos_rest import app

class TestPedidosRest (unittest.TestCase):

    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_00_obtener_pedidos_vacio(self):
        result = self.app.get('pedidos')
        self.assertEqual(result.status_code, 200)

    def test_01_insertar_pedido(self):
        pedido_test =  {"id": "PYTEST", "destinatario": "Antonio", "direccion": "c/testing", "productos": [{"id": "MI200","unidades": 4},{"id": "LAM3","unidades": 7}]}
        result = self.app.post('pedidos', json=pedido_test)
        self.assertEqual(result.status_code, 201)

    def test_02_insertar_pedido_malformado(self):
        pedido_test =  {"id": "PYTEST2", "dest": "Antonio", "dir": "c/testing", "prods": [{"id": "MI200","unids": 4},{"id": "LAM3","unids": 7}]}
        result = self.app.post('pedidos', json=pedido_test)
        self.assertEqual(result.status_code, 400)

    def test_03_insertar_pedido_existente(self):
        pedido_test =  {"id": "PYTEST", "destinatario": "Antonio", "direccion": "c/testing", "productos": [{"id": "MI200","unidades": 4},{"id": "LAM3","unidades": 7}]}
        result = self.app.post('pedidos', json=pedido_test)
        self.assertEqual(result.status_code, 400)

    def test_04_modificar_pedido(self):
        pedido_test =  {"id": "PYTEST", "destinatario": "Antonio", "direccion": "c/testing", "productos": [{"id": "MI200","unidades": 4},{"id": "LAM3","unidades": 8}]}
        result = self.app.put('pedidos/PYTEST', json=pedido_test)
        self.assertEqual(result.status_code, 200)

    def test_05_modificar_pedido_malformado(self):
        pedido_test =  {"id": "PYTEST", "dest": "Antonio", "dir": "c/testing", "prods": [{"id": "MI200","uades": 4},{"id": "LAM3","idades": 8}]}
        result = self.app.put('pedidos/PYTEST', json=pedido_test)
        self.assertEqual(result.status_code, 400)

    def test_06_modificar_pedido_inexistente(self):
        pedido_test =  {"id": "PYTEST", "destinatario": "Antonio", "direccion": "c/testing", "productos": [{"id": "MI200","unidades": 4},{"id": "LAM3","unidades": 8}]}
        result = self.app.put('pedidos/PYTEST2', json=pedido_test)
        self.assertEqual(result.status_code, 404)



    def test_09_obtener_pedidos(self):
        result = self.app.get('pedidos')
        self.assertEqual(result.status_code, 200)

    def test_10_eliminar_pedido(self):
        result = self.app.delete('pedidos/PYTEST')
        self.assertEqual(result.status_code, 200)

    def test_11_eliminar_pedido_inexistente(self):
        result = self.app.delete('pedidos/PYTEST2')
        self.assertEqual(result.status_code, 404)
