#!/usr/bin/env python
# coding: utf-8

from pedido import Pedido
from pedido_schema import PedidoSchema


class GestorPedidos:

    def __init__(self, data_manager, logger):
        self.pedido_schema = PedidoSchema()
        self.data_manager = data_manager
        self.logger = logger

    def connect(self):
        self.data_manager.connect()

    # Devolver todos los pedidos
    def getPedidos(self):
        self.logger.info("Obteniendo pedidos")
        pedidos_json = []
        pedidos = self.data_manager.getPedidos()
        for p in pedidos:
            pedidos_json.append(p.toJSON())
        return pedidos_json


    # Devolver el pedido con el identificador "_id"
    def getPedido(self, pedido_id):
        self.logger.info("Obteniendo pedido con id " + pedido_id)
        return self.data_manager.getPedido(pedido_id)


    # Devolver los pedidos con un estado determinado
    def getPedidosEstado(self, estado):
        self.logger.info("Obteniendo pedidos con estado " + estado)
        pedidos_json = []
        pedidos = self.data_manager.getPedidosEstado(estado)
        for p in pedidos:
            pedidos_json.append(p.toJSON())
        return pedidos_json
        

    # Añadir un pedido nuevo
    def insertarPedido(self, p_json):
        if self.pedido_schema.is_valid(p_json):
            nuevo_pedido = Pedido(p_json["pedido_id"], p_json["destinatario"], p_json["direccion"], p_json["productos"])
            # Buscar si existe un pedido con ese identificador
            _id = nuevo_pedido.getID()
            existe = self.data_manager.getPedido(_id)
            if existe:
                # Ya existe un pedido con ese identificador
                self.logger.error("Error al insertar pedido. Ya existe un pedido con el id: " + _id)
                raise ValueError ("Error: Ya existe un pedido con el id: " + _id)
            else:
                # No existe un pedido con ese identificador
                self.data_manager.insertarPedido(nuevo_pedido)
                self.logger.info("Se ha creado el pedido con  id " + _id)
        else:
            self.logger.error("Error al insertar pedido. El json enviado está mal formado")
            raise ValueError ("Error: El json enviado está mal formado")
        


    # Modificar un pedido
    def modificarPedido(self, pedido_id, p_json):
        if self.pedido_schema.is_valid(p_json):
            pedido = self.data_manager.getPedido(pedido_id)
            if pedido:
                pedido_modificado = Pedido(p_json["pedido_id"], p_json["destinatario"], p_json["direccion"], p_json["productos"])
                if pedido_modificado.getID() == pedido_id:
                    # El id en la ruta y en el json enviado coinciden
                    self.data_manager.modificarPedido(pedido_id, pedido_modificado)
                    self.logger.info("Se ha modificado el pedido con  id " + pedido_id)
                else:
                    # El id del pedido en la ruta y en el json enviado no coinciden
                    raise ValueError ("Error: El id en la ruta no coincide con el json enviado. El id no se puede modificar")
                    self.logger.error("Error al modificar el pedido con  id " + pedido_id + ". El id de un pedido no se puede modificar.")
            else:
                # No existe un pedido con ese identificador
                self.logger.error("Error al modificar pedido. No existe un pedido con el id: " + pedido_id)
                raise ValueError ("Error al modificar pedido. No existe un pedido con el id: " + pedido_id)
        else:
            self.logger.error("Error al modificar pedido. El json enviado está mal formado")
            raise ValueError ("Error: El json enviado está mal formado")


    # Borrar el pedido con el identificador "pedido_id"
    def borrarPedido(self, pedido_id):
        self.data_manager.eliminarPedido(pedido_id)
        self.logger.info("Se ha borrado el pedido con  id " + pedido_id)


