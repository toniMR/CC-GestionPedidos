#!/usr/bin/env python
# coding: utf-8

import json

class Pedido:
    def __init__(self, pedido_id, destinatario, direccion, productos, estado="Unprocessed"):
        self.pedido_id = pedido_id
        self.destinatario = destinatario
        self.direccion = direccion
        self.productos = productos
        self.estado = estado

    def getID(self):
        return self.pedido_id

    def getDestinatario(self):
        return self.destinatario

    def getDireccion(self):
        return self.direccion

    def getProductos(self):
        return self.productos

    def getEstado(self):
        return self.estado

    def setDestinatario(self, destinatario):
        self.destinatario = destinatario

    def setDireccion(self, direccion):
        self.direccion = direccion

    def setProductos(self, productos):
        self.productos = productos

    def setEstado(self, estado):
        self.estado = estado

    def toJSON(self):
        p = {
            "pedido_id": self.pedido_id,
            "destinatario": self.destinatario,
            "direccion": self.direccion,
            "estado": self.estado,
            "productos": self.productos
        }
        return json.loads(json.dumps(p))

    def toString(self):
        productos_str = ""
        for p in self.productos:
            productos_str = productos_str + "producto_id: " + p["producto_id"] + " unidades: " + str(p["unidades"]) + ", "

        msg = "ID: " + self.pedido_id + "\nDestinatario: " + self.destinatario + "\nDirección: " + self.direccion + "\nEstado: " + self.estado + "\nProductos: " + productos_str
        return msg
        
            