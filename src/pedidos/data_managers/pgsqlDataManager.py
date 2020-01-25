#!/usr/bin/env python
# coding: utf-8

import psycopg2

import logging
#import logstash
import json
import sys, os.path

# Añadir la ruta de los módulos 
src_path = (os.path.abspath(os.path.join(os.path.dirname(__file__), './..')))
sys.path.append(src_path)
from pedido import Pedido

logger = logging.getLogger('python-logger')
logger.setLevel(logging.INFO)
#logger.addHandler(logstash.LogstashHandler(host, 5959, version=1)
#logger.addHandler(logstash.TCPLogstashHandler(host, 5959, version=1)

class PgsqlDataMager:

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
                                        id VARCHAR(255) PRIMARY KEY,
                                        destinatario VARCHAR(255) NOT NULL,
                                        direccion VARCHAR(255) NOT NULL,
                                        estado VARCHAR(255) NOT NULL
                                    );
                                    """)

                    logger.info("Se ha creado la tabla pedidos correctamente")
                except (Exception, psycopg2.Error) as error :
                    logger.error("Error al crear la tabla pedidos: " + str(error))
                    #print ("Error creating the PostgreSQL Database: ", error)


            # Comprobar si existe la tabla productos_pedido
            self.cursor.execute("SELECT table_name FROM information_schema.columns WHERE table_name='productos_pedido';")

            # Obtener la respuesta de la consulta
            if self.cursor.fetchone() == None:
                try:
                    # Crear la tabla productos_pedido en la base de datos db_name
                    self.cursor.execute("""
                                    CREATE TABLE productos_pedido (
                                        id VARCHAR(255) NOT NULL,
                                        id_pedido VARCHAR(255) REFERENCES pedidos(id),
                                        unidades INT NOT NULL,
                                        PRIMARY KEY (id, id_pedido)
                                    )
                                    """)

                    logger.info("Se ha creado la tabla productos_pedido correctamente")
                except (Exception, psycopg2.Error) as error :
                    logger.error("Error al crear la tabla productos_pedido: " + str(error))
                    #print ("Error creating the PostgreSQL Database: ", error)

        except (Exception, psycopg2.Error) as error :
            #print ("Error while connecting to PostgreSQL", error)
            logger.error("Error al conectarse a PostgreSQL: " + str(error))


    # Obtener todos los pedidos
    def getPedidos(self):
        try:
            # Obtener todos los id
            self.cursor.execute ("SELECT id FROM pedidos")

            #Obtener resultados
            tmp = self.cursor.fetchall()

            pedidos = []
            for i in range(0, len(tmp)):
                # i es el indice de cada fila
                for j in range (0, len(tmp[i])):
                    # j es el indice de cada valor de la fila
                    id_pedido = tmp[i][j]
                    pedidos.append(self.getPedido(id_pedido))

            return pedidos

        except (Exception, psycopg2.Error) as error :
            raise ValueError ("Error: Error al obtener todos los pedidos: " + str(error))
            logger.error("Error al obtener todos los pedidos: " + str(error))


    # Obtener un pedido
    def getPedido(self, id_pedido):
        try:
            # Valores consulta
            valores = {
                "id_pedido": id_pedido
            }

            # Consulta
            query = """SELECT id_pedido, destinatario, direccion, estado, productos_pedido.id, unidades 
                       FROM pedidos
                       LEFT OUTER JOIN productos_pedido ON pedidos.id = productos_pedido.id_pedido
                       WHERE productos_pedido.id_pedido =  %(id_pedido)s
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
                        
                pedido = Pedido(pedido_dict["id_pedido"], pedido_dict["destinatario"], pedido_dict["direccion"], pedido_dict["productos"], pedido_dict["estado"])
            
            return(pedido)
            
        except (Exception, psycopg2.Error) as error :
            raise ValueError ("Error: Error al obtener el pedido con id " + id_pedido + ": " + str(error))
            logger.error("Error al obtener pedido: " + str(error))


    # Obtener productos de un pedido
    def getProductosPedido (self, id_pedido):
        try:
            # Realizar consulta
            self.cursor.execute ("SELECT id, unidades FROM productos_pedido WHERE id_pedido = %(id_pedido)s;", {"id_pedido": id_pedido})

            # Obtener resultados
            tmp = self.cursor.fetchall()

            productos = []
            if len(tmp) != 0:
                # Crear diccionario con los valores devueltos
                producto_dict = {}
                # Recorrer valores respuesta
                for i in range(0, len(tmp)):
                    # i es el indice de cada fila
                    for j in range (0, len(tmp[i])):
                        # j es el indice de cada valor de la fila
                        producto_dict[self.cursor.description[j][0]] = tmp[i][j]
                    productos.append(producto_dict)
                    producto_dict = {}

            return productos
        except (Exception, psycopg2.Error) as error :
            raise ValueError ("Error: Error al obtener los productos del pedido con id " + id_pedido + ": " + str(error))
            logger.error("Error al obtener los productos del pedido con id: " + id_pedido + ": " + str(error))
            

    # Insertar un pedido
    def insertarPedido(self, pedido):
        msg = ""
        try:
            # Valores consulta
            valores = json.loads(pedido.toJSON())

            # Consulta 
            query = """
                        INSERT INTO pedidos (id, destinatario, direccion, estado) VALUES (%(id)s, %(destinatario)s, %(direccion)s, %(estado)s);
                    """
            for p in valores["productos"]:
                query = query + "INSERT INTO productos_pedido (id, id_pedido, unidades) VALUES ('" + p["id"] + "', %(id)s," + str(p["unidades"]) + "); "
                
            # Ejecutar consulta 
            self.cursor.execute(query, valores)
        except (Exception, psycopg2.Error) as error:
            raise ValueError ("Error: Error al insertar productos pedido: " + str(error))
            logger.error("Error al insertar pedido: " + str(error))


    # Insertar productos a un pedido
    def insertarProductosPedido(self, id_pedido, productos):
        try:
            # Valores consulta
            valores = {
                "id_pedido": id_pedido,
                "productos": productos 
            }

            # Consulta 
            query = ""
            for p in valores["productos"]:
                query = query + "INSERT INTO productos_pedido (id, id_pedido, unidades) VALUES ('" + p["id"] + "', %(id_pedido)s," + str(p["unidades"]) + "); "
                
            # Ejecutar consulta 
            self.cursor.execute(query, valores)

        except (Exception, psycopg2.Error) as error:
            logger.error("Error al insertar productos pedido: " + str(error))


    # Modificar un pedido
    def modificarPedido(self, id_pedido, pedido):
        try:
            # Valores consulta
            valores = json.loads(pedido.toJSON())
            valores['id_pedido'] = id_pedido

            # Consulta 
            query = """
                        UPDATE pedidos 
                        SET destinatario = %(destinatario)s,
                            direccion = %(direccion)s,
                            estado = %(estado)s
                        WHERE
                            id = %(id_pedido)s;
                    """

            # Ejecutar consulta 
            self.cursor.execute(query, valores)

            # Modificar productos del pedido
            self.modificarProductosPedido(id_pedido, pedido.getProductos())

        except (Exception, psycopg2.Error) as error :
            logger.error("Error al modificar pedido: " + str(error))


    # Modificar los productos de un pedido
    def modificarProductosPedido(self, id_pedido, productos):
        try:
            self.eliminarProductosPedido(id_pedido)
            self.insertarProductosPedido(id_pedido, productos)

        except (Exception, psycopg2.Error) as error :
            logger.error("Error al modificar productos del pedido: " + str(error))

    
    # Eliminar pedido
    def eliminarPedido(self, id_pedido):
        try:
            self.eliminarProductosPedido(id_pedido)

            valores = {
                "id_pedido": id_pedido
            }

            # Consulta 
            query = """DELETE FROM pedidos
                    WHERE id = %(id_pedido)s"""
                
            # Ejecutar consulta 
            self.cursor.execute(query, valores)

        except (Exception, psycopg2.Error) as error:
            raise ValueError ("Error: Error al borrar el pedido con id " + id_pedido + ": " + str(error))
            logger.error("Error al eliminar pedido: " + str(error))


    # Eliminar productos de un pedido
    def eliminarProductosPedido(self, id_pedido):
        try:
            # Valores consulta
            valores = {
                "id_pedido": id_pedido
            }

            # Consulta 
            query = """DELETE FROM productos_pedido
                    WHERE id_pedido = %(id_pedido)s"""
                
            # Ejecutar consulta 
            self.cursor.execute(query, valores)

        except (Exception, psycopg2.Error) as error :
            raise ValueError ("Error: Error al borrar los productos del pedido con id " + id_pedido + ": " + str(error))
            logger.error("Error al borrar productos del pedido: " + str(error))


    # Cerrar conexión
    def close(self):
        if(self.connection):
            self.cursor.close()
            self.connection.close()
            logger.info("Conexión con PostgreSQL cerrada")
