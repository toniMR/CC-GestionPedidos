#!/usr/bin/env python
# coding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import *
import sys
import os
from .models import Pedidos, Cesta

# Añadir la ruta de los módulos 
src_path = (os.path.abspath(os.path.join(os.path.dirname(__file__), './../../../')))
sys.path.append(src_path)
from pedido import Pedido


class SqlAlchemyORMDataManager:

    def __init__(self, user, password, host, port, db_name):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name
        self.connection = None
        self.session = None


    def connect (self):
        try:
            self.connection = create_engine(f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}')
            Pedidos.__table__.create(bind=self.connection, checkfirst=True)
            Cesta.__table__.create(bind=self.connection, checkfirst=True)
            Session = sessionmaker(bind=self.connection)
            self.session = Session()
        except (Exception) as error :
            raise ValueError ("Error al conectarse a PostgreSQL: " + str(error))

    
    # Obtener todos los pedidos
    def getPedidos(self):
        pedidos = []
        pedidos_data = self.session.query(Pedidos).all()
        if pedidos_data:
            for p in pedidos_data:
                pedidos.append(p.toPedido())
        return pedidos

    
    # Obtener un pedido
    def getPedido(self, id_pedido):
        pedido = None
        p = self.session.query(Pedidos).get(id_pedido)
        if p:
            pedido = p.toPedido()
        return pedido


    # Obtener todos los pedidos que tengan un estado concreto
    def getPedidosEstado (self, estado):
        pedidos = []
        pedidos_data = self.session.query(Pedidos).filter(Pedidos.estado==estado).all()
        for p in pedidos_data:
            pedidos.append(p.toPedido())
        return pedidos


    # Insertar un pedido
    def insertarPedido(self, p):
        pedido_dict = {
                        'pedido_id': p.getID(),
                        'destinatario': p.getDestinatario(),
                        'direccion': p.getDireccion(),
                        'estado': p.getEstado()
        }

        pedido = Pedidos(**pedido_dict)

        # Establecer productos de la cesta
        for p in p.getProductos():
            producto = Cesta(producto_id=p['producto_id'], unidades=p['unidades'])
            pedido.productos.append(producto)

        # Realizar cambios en la BD
        self.session.add(pedido)
        self.session.commit()


    # Modificar un pedido
    def modificarPedido(self, id_pedido, p):

        pedido = self.session.query(Pedidos).get(id_pedido)
        pedido_dict = {
                        'pedido_id': p.getID(),
                        'destinatario': p.getDestinatario(),
                        'direccion': p.getDireccion(),
                        'estado': p.getEstado()
        }

        pedido = Pedidos(**pedido_dict)

        # Establecer productos de la cesta
        for p in p.getProductos():
            producto = Cesta(producto_id=p['producto_id'], unidades=p['unidades'])
            pedido.productos.append(producto)

        # Realizar cambios en la BD
        self.session.commit()



    # Eliminar pedido
    def eliminarPedido(self, id_pedido):
        p = self.session.query(Pedidos).get(id_pedido)
        self.session.delete(p)
        self.session.commit()

