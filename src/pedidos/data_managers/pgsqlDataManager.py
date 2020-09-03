#!/usr/bin/env python
# coding: utf-8

import psycopg2
import sys, os.path

# Añadir la ruta de los módulos 
src_path = (os.path.abspath(os.path.join(os.path.dirname(__file__), './..')))
sys.path.append(src_path)
from pedido import Pedido


class PgsqlDataManager:

    def __init__(self, user, password, host, port, db_name):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name
        self.connection = None
        self.cursor = None


    def connect (self):
        try:
            # Conectarse a la base de datos
            self.connection = psycopg2.connect(user = self.user,
                                        password = self.password,
                                        host = self.host,
                                        port = self.port,
                                        dbname = self.db_name)

            # Establecer autocommit a True para no tener que realizar commit tras cada consulta   
            self.connection.autocommit = True

            self.cursor = self.connection.cursor()


            # Comprobar si existe la tabla pedidos
            self.cursor.execute("SELECT table_name FROM information_schema.columns WHERE table_name='pedidos';")

            # Obtener la respuesta de la consulta
            if self.cursor.fetchone() == None:
                try:
                    # Crear la tabla pedidos en la base de datos bd_name
                    self.cursor.execute("""CREATE TABLE pedidos (
                                        pedido_id VARCHAR(255) PRIMARY KEY,
                                        destinatario VARCHAR(255) NOT NULL,
                                        direccion VARCHAR(255) NOT NULL,
                                        estado VARCHAR(255) NOT NULL
                                    );
                                    """)
                except (Exception, psycopg2.Error) as error :
                    raise ValueError ("Error al crear la tabla pedidos:  " + str(error))


            # Comprobar si existe la tabla productos_pedido
            self.cursor.execute("SELECT table_name FROM information_schema.columns WHERE table_name='productos_pedido';")

            # Obtener la respuesta de la consulta
            if self.cursor.fetchone() == None:
                try:
                    # Crear la tabla productos_pedido en la base de datos db_name
                    self.cursor.execute("""
                                    CREATE TABLE productos_pedido (
                                        producto_id VARCHAR(255) NOT NULL,
                                        pedido_id VARCHAR(255) REFERENCES pedidos(pedido_id),
                                        unidades INT NOT NULL,
                                        PRIMARY KEY (producto_id, pedido_id)
                                    )
                                    """)
                except (Exception, psycopg2.Error) as error :
                    raise ValueError ("Error al crear la tabla productos_pedido: " + str(error))

        except (Exception, psycopg2.Error) as error :
            raise ValueError ("Error al conectarse a PostgreSQL: " + str(error))


    # Obtener todos los pedidos
    def getPedidos(self):
        try:
            # Obtener todos los id
            self.cursor.execute ("SELECT pedido_id FROM pedidos")

            #Obtener resultados
            tmp = self.cursor.fetchall()

            pedidos = []
            for i in range(0, len(tmp)):
                # i es el indice de cada fila
                for j in range (0, len(tmp[i])):
                    # j es el indice de cada valor de la fila
                    pedido_id = tmp[i][j]
                    pedidos.append(self.getPedido(pedido_id))

            return pedidos

        except (Exception, psycopg2.Error) as error :
            raise ValueError ("Error: Error al obtener todos los pedidos: " + str(error))


    # Obtener un pedido
    def getPedido(self, pedido_id):
        try:
            # Valores consulta
            valores = {
                "pedido_id": pedido_id
            }

            # Consulta
            query = """SELECT pedidos.pedido_id, destinatario, direccion, estado, productos_pedido.producto_id, unidades 
                       FROM pedidos
                       LEFT OUTER JOIN productos_pedido ON pedidos.pedido_id = productos_pedido.pedido_id
                       WHERE productos_pedido.pedido_id =  %(pedido_id)s
                       ;"""

            # Realizar consulta
            self.cursor.execute (query, valores)

            # Obtener resultados
            tmp = self.cursor.fetchall()

            pedido = None
            if len(tmp) != 0:
                # Crear diccionario con los valores devueltos
                pedido_dict = {}
                pedido_dict["productos"] = []
                producto_dict = {}
                # Recorrer valores respuesta
                for i in range(0, len(tmp)):
                    # i es el indice de cada fila
                    for j in range (0, len(tmp[i])):
                        # j es el indice de cada valor de la fila
                        if i==0 and j < 4:
                            pedido_dict[self.cursor.description[j][0]] = tmp[i][j]
                        elif j > 3:
                            producto_dict[self.cursor.description[j][0]] = tmp[i][j]
                    pedido_dict["productos"].append(producto_dict)
                    producto_dict = {}
                        
                pedido = Pedido(pedido_dict["pedido_id"], pedido_dict["destinatario"], pedido_dict["direccion"], pedido_dict["productos"], pedido_dict["estado"])
            
            return(pedido)
            
        except (Exception, psycopg2.Error) as error :
            raise ValueError ("Error: Error al obtener el pedido con id " + pedido_id + ": " + str(error))

    
    # Obtener todos los pedidos que tengan un estado concreto
    def getPedidosEstado (self, estado):
        try:
            # Obtener todos los id
            self.cursor.execute ("SELECT pedido_id FROM pedidos WHERE estado = %(estado)s;", {"estado": estado})

            #Obtener resultados
            tmp = self.cursor.fetchall()

            pedidos = []
            for i in range(0, len(tmp)):
                # i es el indice de cada fila
                for j in range (0, len(tmp[i])):
                    # j es el indice de cada valor de la fila
                    pedido_id = tmp[i][j]
                    pedidos.append(self.getPedido(pedido_id))

            return pedidos
        except (Exception, psycopg2.Error) as error :
            raise ValueError ("Error: Error al obtener los productos con estado " + estado + ": " + str(error))

            
    # Insertar un pedido
    def insertarPedido(self, pedido):
        msg = ""
        try:
            # Valores consulta
            valores = pedido.toJSON()
            # Consulta 
            query = """
                        INSERT INTO pedidos (pedido_id, destinatario, direccion, estado) VALUES (%(pedido_id)s, %(destinatario)s, %(direccion)s, %(estado)s);
                    """
            for p in valores["productos"]:
                query = query + "INSERT INTO productos_pedido (producto_id, pedido_id, unidades) VALUES ('" + p["producto_id"] + "', %(pedido_id)s," + str(p["unidades"]) + "); "
                
            # Ejecutar consulta 
            self.cursor.execute(query, valores)
        except (Exception, psycopg2.Error) as error:
            raise ValueError ("Error: Error al insertar pedido: " + str(error))


    # Insertar productos a un pedido
    def insertarProductosPedido(self, pedido_id, productos):
        try:
            # Valores consulta
            valores = {
                "pedido_id": pedido_id,
                "productos": productos 
            }

            # Consulta 
            query = ""
            for p in valores["productos"]:
                query = query + "INSERT INTO productos_pedido (producto_id, pedido_id, unidades) VALUES ('" + p["producto_id"] + "', %(pedido_id)s," + str(p["unidades"]) + "); "
                
            # Ejecutar consulta 
            self.cursor.execute(query, valores)

        except (Exception, psycopg2.Error) as error:
            raise ValueError ("Error: Error al insertar productos pedido: " + str(error))


    # Modificar un pedido
    def modificarPedido(self, pedido_id, pedido):
        try:
            # Valores consulta
            valores = pedido.toJSON()
            valores['pedido_id'] = pedido_id

            # Consulta 
            query = """
                        UPDATE pedidos 
                        SET destinatario = %(destinatario)s,
                            direccion = %(direccion)s,
                            estado = %(estado)s
                        WHERE
                            pedido_id = %(pedido_id)s;
                    """

            # Ejecutar consulta 
            self.cursor.execute(query, valores)

            # Modificar productos del pedido
            self.modificarProductosPedido(pedido_id, pedido.getProductos())

        except (Exception, psycopg2.Error) as error :
            raise ValueError ("Error al modificar pedido: " + str(error))


    # Modificar los productos de un pedido
    def modificarProductosPedido(self, pedido_id, productos):
        try:
            self.eliminarProductosPedido(pedido_id)
            self.insertarProductosPedido(pedido_id, productos)

        except (Exception, psycopg2.Error) as error :
            raise ValueError ("Error al modificar productos del pedido: " + str(error))

    
    # Eliminar pedido
    def eliminarPedido(self, pedido_id):
        try:
            self.eliminarProductosPedido(pedido_id)

            valores = {
                "pedido_id": pedido_id
            }

            # Consulta 
            query = """DELETE FROM pedidos
                    WHERE pedido_id = %(pedido_id)s"""
                
            # Ejecutar consulta 
            self.cursor.execute(query, valores)

        except (Exception, psycopg2.Error) as error:
            raise ValueError ("Error: Error al borrar el pedido con id " + pedido_id + ": " + str(error))


    # Eliminar productos de un pedido
    def eliminarProductosPedido(self, pedido_id):
        try:
            # Valores consulta
            valores = {
                "pedido_id": pedido_id
            }

            # Consulta 
            query = """DELETE FROM productos_pedido
                    WHERE pedido_id = %(pedido_id)s"""
                
            # Ejecutar consulta 
            self.cursor.execute(query, valores)

        except (Exception, psycopg2.Error) as error :
            raise ValueError ("Error: Error al borrar los productos del pedido con id " + pedido_id + ": " + str(error))


    # Cerrar conexión
    def close(self):
        if(self.connection):
            self.cursor.close()
            self.connection.close()
