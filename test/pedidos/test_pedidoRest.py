#!/usr/bin/env python
# coding: utf-8

import unittest
import json
import sys, os.path

# Añadir la ruta de los módulos
src_path = (os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
+ '/src/')
sys.path.append(src_path)
import pedidos


class TestPedidosRestBase (unittest.TestCase):
    __test__ = False

    def setUp(self):
        self.flask_app = pedidos.create_app()       
        self.app = self.flask_app.test_client()


    def test_00_obtener_pedidos_vacio(self):
        result = self.app.get('pedidos')
        self.assertEqual(result.status_code, 404)


    def test_01_insertar_pedido(self):
        pedido_test =  {"pedido_id": "PYTEST", "destinatario": "Antonio", "direccion": "c/testing", "productos": [{"producto_id": "MI200","unidades": 4},{"producto_id": "LAM3","unidades": 7}]}
        result = self.app.post('pedidos', json=pedido_test)
        self.assertEqual(result.status_code, 201)


    def test_02_insertar_pedido_malformado(self):
        pedido_test =  {"pedido_id": "PYTEST2", "dest": "Antonio", "dir": "c/testing", "prods": [{"producto_id": "MI200","unids": 4},{"producto_id": "LAM3","unids": 7}]}
        result = self.app.post('pedidos', json=pedido_test)
        self.assertEqual(result.status_code, 400)


    def test_03_insertar_pedido_existente(self):
        pedido_test =  {"pedido_id": "PYTEST", "destinatario": "Antonio", "direccion": "c/testing", "productos": [{"producto_id": "MI200","unidades": 4},{"producto_id": "LAM3","unidades": 7}]}
        result = self.app.post('pedidos', json=pedido_test)
        self.assertEqual(result.status_code, 400)


    def test_04_modificar_pedido(self):
        pedido_test =  {"pedido_id": "PYTEST", "destinatario": "Antonio", "direccion": "c/testing", "productos": [{"producto_id": "MI200","unidades": 4},{"producto_id": "LAM3","unidades": 8}]}
        result = self.app.put('pedidos/PYTEST', json=pedido_test)
        self.assertEqual(result.status_code, 200)


    def test_05_modificar_pedido_malformado(self):
        pedido_test =  {"pedido_id": "PYTEST", "dest": "Antonio", "dir": "c/testing", "prods": [{"producto_id": "MI200","uades": 4},{"producto_id": "LAM3","idades": 8}]}
        result = self.app.put('pedidos/PYTEST', json=pedido_test)
        self.assertEqual(result.status_code, 400)


    def test_06_modificar_pedido_inexistente(self):
        pedido_test =  {"pedido_id": "PYTEST", "destinatario": "Antonio", "direccion": "c/testing", "productos": [{"producto_id": "MI200","unidades": 4},{"producto_id": "LAM3","unidades": 8}]}
        result = self.app.put('pedidos/PYTEST2', json=pedido_test)
        self.assertEqual(result.status_code, 404)


    def test_07_get_pedido(self):
        result = self.app.get('pedidos/PYTEST')
        self.assertEqual(result.status_code, 200)


    def test_08_get_pedido_inexistente(self):
        result = self.app.get('pedidos/PYTEST2')
        self.assertEqual(result.status_code, 404)


    def test_09_obtener_pedidos(self):
        result = self.app.get('pedidos')
        self.assertEqual(result.status_code, 200)


    def test_10_get_pedidos_estado(self):
        result = self.app.get('pedidos/estado/Unprocessed')
        self.assertEqual(result.status_code, 200)


    def test_11_get_ningun_pedido_estado(self):
        result = self.app.get('pedidos/estado/Entregado')
        self.assertEqual(result.status_code, 404)


    def test_12_get_estado_pedido(self):
        result = self.app.get('pedidos/PYTEST/estado')
        self.assertEqual(result.status_code, 200)


    def test_13_modificar_estado_pedido(self):
        pedido_test =  {"estado": "Processed"}
        result = self.app.put('pedidos/PYTEST/estado', json=pedido_test)
        self.assertEqual(result.status_code, 200)


    def test_14_eliminar_pedido(self):
        result = self.app.delete('pedidos/PYTEST')
        self.assertEqual(result.status_code, 200)


    def test_15_eliminar_pedido_inexistente(self):
        result = self.app.delete('pedidos/PYTEST2')
        self.assertEqual(result.status_code, 404)



class TestPedidosRest_Psycopg2DataManager (TestPedidosRestBase):
    __test__ = True

    def setUp(self):
        TestPedidosRestBase.setUp(self)
        self.flask_app.container.config.data_handler.override('psycopg2')


class TestPedidosRest_SqlalchemyDataManager (TestPedidosRestBase):
    __test__ = True

    def setUp(self):
        TestPedidosRestBase.setUp(self)
        self.flask_app.container.config.data_handler.override('sqlalchemy')

        