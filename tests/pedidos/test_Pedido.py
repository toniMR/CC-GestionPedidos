#!/usr/bin/env python
# coding: utf-8

import unittest
import json
import sys, os.path

# Añadir la ruta de los módulos 
src_path = (os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
+ '/src/pedidos/')
sys.path.append(src_path)

from pedido import Pedido

class TestPedido(unittest.TestCase):

    # Comprobar que se inicializa correctamente
    def test_inicializacion(self):
        pedido = Pedido ("123123123", "Antonio Martos", "c/ ejemplo", [{"MI120": 1},{"LAM1": 2}])
        self.assertIsInstance(pedido, Pedido, "Objeto inicializado correctamente")

    # Comprobar que se crea un pedido
    def test_crearPedido(self):
        pedido = Pedido ("123123123", "Antonio Martos", "c/ ejemplo", [{"MI120": 1},{"LAM1": 2}])
        self.assertEqual(pedido.getID(), "123123123", "Identificador devuelto correctamente")
        self.assertEqual(pedido.getDestinatario(), "Antonio Martos", "Destinatario devuelto correctamente")
        self.assertEqual(pedido.getDireccion(), "c/ ejemplo", "Direccion devuelta correctamente")
        self.assertEqual(pedido.getProductos(), [{"MI120": 1},{"LAM1": 2}], "Productos devueltos correctamente")
        self.assertEqual(pedido.getEstado(), "No procesado", "Estado devuelto correctamente")

    # Comprobar que se modifica el estado correctamente
    def test_modificarEstado(self):
        pedido = Pedido ("222333444", "Antonio Martos", "c/ ejemplo2", [{"MI120": 1},{"LAM1": 2}])
        pedido.setEstado("Enviando")
        self.assertEqual(pedido.getEstado(), "Enviando", "Estado cambiado correctamente")

    # Comprobar que se modifica el destinatario correctamente
    def test_modificarDestinatario(self):
        pedido = Pedido ("222333444", "Antonio Martos", "c/ ejemplo2", [{"MI120": 1},{"LAM1": 2}])
        pedido.setDestinatario("Antonio Martos 2")
        self.assertEqual(pedido.getDestinatario(), "Antonio Martos 2", "Destinatario cambiado correctamente")

    # Comprobar que se modifican los productos correctamente
    def test_modificarProductos(self):
        pedido = Pedido ("222333444", "Antonio Martos", "c/ ejemplo2", [{"MI120": 1},{"LAM1": 2}])
        pedido.setProductos([{"MI120": 1}])
        self.assertEqual(pedido.getProductos(), [{"MI120": 1}], "Estado cambiado correctamente")

    # Comprobar que se modifica la dirección correctamente
    def test_modificarDireccion(self):
        pedido = Pedido ("222333444", "Antonio Martos", "c/ ejemplo2", [{"MI120": 1},{"LAM1": 2}])
        pedido.setDireccion("c/ modificada")
        self.assertEqual(pedido.getDireccion(), "c/ modificada" , "Estado cambiado correctamente")

    # Comprobar que se forma el JSON correctamente
    def test_modificarDireccion(self):
        pedido = Pedido ("222333444", "Antonio Martos", "c/ ejemplo2", [{"MI120": 1},{"LAM1": 2}])
        dict_pedido = {"_id": "222333444", "destinatario": "Antonio Martos", "direccion": "c/ ejemplo2", "estado": "No procesado", "productos": [{"MI120": 1}, {"LAM1": 2}]}
        self.assertEqual(pedido.toJSON(), json.dumps(dict_pedido) , "Estado cambiado correctamente")

    # Comprobar el método toString()
    def test_toString(self):
        pedido = Pedido ("222333444", "Antonio Martos", "c/ ejemplo2", [{"MI120": 1},{"LAM1": 2}])
        string = "ID: 222333444\nDestinatario: Antonio Martos\nDirección: c/ ejemplo2\nEstado: No procesado\nProductos: MI120: 1 unidades, LAM1: 2 unidades, "
        self.assertEqual(pedido.toString(), string , "Estado cambiado correctamente")
