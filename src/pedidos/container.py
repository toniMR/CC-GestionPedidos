#!/usr/bin/env python
# coding: utf-8

from dependency_injector import containers, providers
import logging
from .gestorPedidos import GestorPedidos
from .data_managers.postgres.psycopg2.psycopg2DataManager import Psycopg2DataManager
from .data_managers.postgres.sqlalchemy.sqlAlchemyORMDataManager import SqlAlchemyORMDataManager
from flask import Flask
from dependency_injector.ext import flask

class Container(containers.DeclarativeContainer):

    app = flask.Application(Flask, __name__)

    # Configuración
    config = providers.Configuration('config')

    # Dependencias
    logger = providers.Singleton(logging.Logger, name='logger')
    psycopg2_data_manager = providers.Singleton(Psycopg2DataManager,
                                            user=config.username,
                                            password=config.password,
                                            host=config.host,
                                            port=config.port,
                                            db_name=config.db_name)

    sqlalchemy_orm_data_manager = providers.Singleton(SqlAlchemyORMDataManager,
                                            user=config.username,
                                            password=config.password,
                                            host=config.host,
                                            port=config.port,
                                            db_name=config.db_name)

    # Servicios
    gestor_pedidos = providers.Selector(
        config.data_handler,
        psycopg2 = providers.Factory(GestorPedidos, psycopg2_data_manager, logger),
        sqlalchemy = providers.Factory(GestorPedidos, sqlalchemy_orm_data_manager, logger),
    )

