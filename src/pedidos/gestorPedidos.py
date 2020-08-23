#!/usr/bin/env python
# coding: utf-8

from pedido import Pedido
from pedido_schema import PedidoSchema
import json


class GestorPedidos:

    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.pedido_schema = PedidoSchema()


    # Devolver todos los pedidos
    def getPedidos(self):
        return self.data_manager.getPedidos()


    # Devolver el pedido con el identificador "_id"
    def getPedido(self, id_pedido):
        return self.data_manager.getPedido(id_pedido)


    # Devolver los pedidos con un estado determinado
    def getPedidosEstado(self, estado):
        return self.data_manager.getPedidosEstado(estado)
        

    # Añadir un pedido nuevo
    def insertarPedido(self, p_json):
        if self.pedido_schema.is_valid(p_json):
            nuevo_pedido = Pedido(p_json["id"], p_json["destinatario"], p_json["direccion"], p_json["productos"])
            # Buscar si existe un pedido con ese identificador
            _id = nuevo_pedido.getID()
            existe = self.data_manager.getPedido(_id)
            if existe:
                # Ya existe un pedido con ese identificador
                raise ValueError ("Error: Ya existe un pedido con el id: " + _id)
            else:
                # No existe un pedido con ese identificador
                self.data_manager.insertarPedido(nuevo_pedido)
        else:
            raise ValueError ("Error: El json enviado está mal formado")


    # Modificar un pedido
    def modificarPedido(self, id_pedido, p_json):
        if self.pedido_schema.is_valid(p_json):
            nuevos_datos_pedido = Pedido(p_json["id"], p_json["destinatario"], p_json["direccion"], p_json["productos"])
            if nuevos_datos_pedido.getID() == id_pedido:
                # El id en la ruta y en el json enviado coinciden
                self.data_manager.modificarPedido(id_pedido, nuevos_datos_pedido)
            else:
                # El id del pedido en la ruta y en el json enviado no coinciden
                raise ValueError ("Error: El id en la ruta no coincide con el json enviado. El id no se puede modificar")
        else:
            raise ValueError ("Error: El json enviado está mal formado")


    # Borrar el pedido con el identificador "id"
    def borrarPedido(self, id_pedido):
        self.data_manager.eliminarPedido(id_pedido)


