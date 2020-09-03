#!/usr/bin/env python
# coding: utf-8

from dependency_injector import containers, providers
import logging
from .gestorPedidos import GestorPedidos
from .data_managers.pgsqlDataManager import PgsqlDataManager


from flask import Flask
from dependency_injector.ext import flask

class Container(containers.DeclarativeContainer):

    app = flask.Application(Flask, __name__)

    # Configuración
    config = providers.Configuration('config')

    # Dependencias
    logger = providers.Singleton(logging.Logger, name='logger')
    pgsql_data_manager = providers.Singleton(PgsqlDataManager,
                                            user=config.username,
                                            password=config.password,
                                            host=config.host,
                                            port=config.port,
                                            db_name=config.db_name)


    # Servicios
    gestor_pedidos = providers.Selector(
        config.data_handler,
        psycopg2 = providers.Factory(GestorPedidos, pgsql_data_manager, logger),
    )


    