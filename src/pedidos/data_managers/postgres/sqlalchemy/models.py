from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import sys
import os
# Añadir la ruta de los módulos 
src_path = (os.path.abspath(os.path.join(os.path.dirname(__file__), './../../../')))
sys.path.append(src_path)
from pedido import Pedido

Base = declarative_base()


class Pedidos(Base):
    __tablename__ = "pedidos"
    pedido_id = Column(String, primary_key=True)
    destinatario = Column(String)
    direccion = Column(String)
    estado = Column(String)

    # Establecer relación 0 a muchos con la tabla Cesta
    productos = relationship('Cesta', backref = 'pedidos', lazy=True, cascade="all, delete-orphan")
    
    def toPedido(self):
        pedido_dict = self.__dict__
        productos = []
        for producto in self.productos:
            productos.append({'producto_id': producto.__dict__['producto_id'], 'unidades': producto.__dict__['unidades']})
        return Pedido(pedido_dict["pedido_id"], pedido_dict["destinatario"], pedido_dict["direccion"], productos, pedido_dict["estado"])


class Cesta(Base):
    __tablename__= "cesta"
    __table_args__ = (
        PrimaryKeyConstraint('pedido_id', 'producto_id', 'unidades'),
    )
    pedido_id = Column(String, ForeignKey('pedidos.pedido_id'))
    producto_id = Column(String)
    unidades = Column(Integer)
    
