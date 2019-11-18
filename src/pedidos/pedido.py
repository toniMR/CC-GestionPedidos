#!/usr/bin/env python
# coding: utf-8

import json

class Pedido:
    def __init__(self, _id, destinatario, direccion, productos):
        self._id = _id
        self.destinatario = destinatario
        self.direccion = direccion
        self.productos = productos
        self.estado = "No procesado"

    def getID(self):
        return self._id

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
            "_id": self._id,
            "destinatario": self.destinatario,
            "direccion": self.direccion,
            "estado": self.estado,
            "productos": self.productos
        }
        return json.dumps(p)

    def toString(self):
        productos_str = ""
        for p in self.productos:
            for k in p:
                productos_str = productos_str + k + ": " + str(p[k]) + " unidades, "

        msg = "ID: " + self._id + "\nDestinatario: " + self.destinatario + "\nDirección: " + self.direccion + "\nEstado: " + self.estado + "\nProductos: " + productos_str
        return msg
                
