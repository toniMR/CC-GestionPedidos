from dependency_injector import containers, providers
import logging
from gestorPedidos import GestorPedidos
from data_managers.pgsqlDataManager import PgsqlDataManager


class Container(containers.DeclarativeContainer):

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
    gestor_pedidos = providers.Factory(GestorPedidos, pgsql_data_manager, logger)


    