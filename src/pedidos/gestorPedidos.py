#!/usr/bin/env python
# coding: utf-8

from pedido import Pedido
import json


class GestorPedidos:

    def __init__(self, example_data_path):
        with open(example_data_path) as file:
            # Obtener datos desde un fichero de ejemplo .json
            self.pedidos = json.load(file)

    # Devolver todos los pedidos
    def getPedidos(self):
        return self.pedidos


    # Devolver el pedido con el identificador "_id"
    def getPedido(self, _id):
        pedido = None
        # Buscar el pedido con el identificador "i_d"
        for p in self.pedidos:
            if p['_id'] == _id:
                pedido = p
        return pedido

    '''
    # Añadir un pedido nuevo
    # (Posteriormente el identificador no lo tendrá que indicar el usuario)
    #
    def insertarPedido(self, nuevo_pedido):
        # Buscar si existe un pedido con ese identificador
        existe = False
        _id = nuevo_pedido.getID()
        for p in self.pedidos:
            if p['_id'] == _id:
                existe = True
        if existe:
            # Ya existe un pedido con ese identificador
            return False
        else:
            # No existe un pedido con ese identificador
            self.pedidos.append(json.loads(nuevo_pedido.toJSON()))
            with open('data/pedidos/test_pedidos.json', 'w') as f:
                json.dump(self.pedidos, f, indent=4, sort_keys=True)
                f.close()
            return True


    # Borrar el pedido con el identificador "id"
    # Devuelve True si hubo exito, False si no lo hubo
    def borrarPedido(self, _id):
        borrado = False
        for p in self.pedidos:
            if p['_id'] == _id:
                self.pedidos.remove(p)
                borrado = True
                with open('data/pedidos/test_pedidos.json', 'w') as f:
                    json.dump(self.pedidos, f, indent=4, sort_keys=True)
                    f.close()
        return borrado
    '''