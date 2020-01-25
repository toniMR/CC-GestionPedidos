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
from gestorPedidos import GestorPedidos

gestorPedidos = GestorPedidos("data/pedidos/test_pedidos.json")

class TestGestorPedidos(unittest.TestCase):
    '''
    # Comprobar que se inicializa correctamente
    def test_incializacion(self):
        self.assertIsInstance(gestorPedidos, GestorPedidos, "Se ha inicializado correctamente")

    # Comprobar que devuelve todos los pedidos
    def test_getPedidos(self):
        with open("data/pedidos/test_pedidos.json") as file:
            # Obtener datos desde un fichero de ejemplo .json
            pedidos = json.load(file)
        self.assertEqual(gestorPedidos.getPedidos(), pedidos, "Pedidos devueltos correctamente")

    # Comprobar que devuelve un pedido identificado por su _id
    def test_getPedido(self):
        pedido = Pedido ("123123123", "Antonio Martos", "c/ ejemplo", [{"MI120": 1},{"LAM1": 2}])
        pedidoJSON = json.loads(pedido.toJSON())
        self.assertEqual(gestorPedidos.getPedido("123123123"), pedidoJSON, "Pedido identificado devuelto correctamente")

    # Comprobar que inserta 
    def test_insertarPedido(self):
        nuevo_pedido = Pedido("333444555", "Test", "c/ testing, Nº4", [{"ITEM1": 3, "ITEM2": 2}])
        self.assertEqual(gestorPedidos.insertarPedido(nuevo_pedido), True, "Pedido insertado correctamente")
    
    # Comprobar que borra correctamente
    def test_borrarPedido(self):
        self.assertEqual(gestorPedidos.borrarPedido("333444555"), True, "El pedido se ha borrado correctamente")
    '''