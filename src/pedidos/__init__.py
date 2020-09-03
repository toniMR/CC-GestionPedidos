#!/usr/bin/env python
# coding: utf-8

from os import environ
from .container import Container


"""Create and return Flask application."""
def create_app():

    # Establecer valores para la conexión a la BD.
    username = "username"
    if "DB_USERNAME" in environ and environ['DB_USERNAME'] != "":
        username = environ['DB_USERNAME']   

    password = "password"
    if "DB_PASSWORD" in environ and environ['DB_PASSWORD'] != "":
        password = environ['DB_PASSWORD']

    host = "127.0.0.1"
    if "DB_HOST" in environ and environ['DB_HOST'] != "":
        host = environ['DB_HOST']

    port = "5432"
    if "DB_PORT" in environ != "" and environ['DB_PORT'] != "":
        port = environ['DB_PORT']

    db_name = "ms_pedidos"
    if "DB_NAME" in environ and environ['DB_NAME'] != "":
        db_name = environ['DB_NAME']

    
    container = Container(config={
                                'data_handler': 'psycopg2',
                                'username': username,
                                'password': password,
                                'host': host,
                                'port': port,
                                'db_name': db_name
                            })
    app = container.app()
    app.container = container

    from pedidos import routes
    app.register_blueprint(routes.api)
    
    
    return app
    