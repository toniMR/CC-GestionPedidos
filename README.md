# CC-GestionPedidos

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Build Status](https://travis-ci.com/toniMR/CC-GestionPedidos.svg?branch=master)](https://travis-ci.com/toniMR/CC-GestionPedidos)
[![CircleCI](https://circleci.com/gh/toniMR/CC-GestionPedidos/tree/master.svg?style=svg)](https://circleci.com/gh/toniMR/CC-GestionPedidos/tree/master)
[![codecov](https://codecov.io/gh/toniMR/CC-GestionPedidos/branch/master/graph/badge.svg)](https://codecov.io/gh/toniMR/CC-GestionPedidos)

## Descripción

El proyecto consistirá en un gestor de productos y pedidos en el que el usuario podrá ver todos los productos que hay y realizar un pedido con la lista de productos y cantidades que desea.  

Consistirá en 2 microservicios con los que se podrá añadir, consultar, modificar y eliminar tanto los productos como los pedidos.

## Arquitectura

Se utilizará una arquitectura basada en microservicios en el que existirá un microservicio para gestionar los productos y otro microservicio para gestionar los pedidos.  

La arquitectura se encuentra explicada extensamente en la [Documentación sobre la arquitectura escogida](doc/arquitectura.md)

## Entidades e historias de uso

[Documentación sobre entidades e historias de usuario](doc/entidades.md)

## Tests

[Documentación test, cobertura e integración continua](doc/tests.md)

## Herramientas de construcción

Microservicio Gestor de Productos:

buildtool: package.json

Microservicio Gestor de Pedidos:

buildtool: setup.py

[Documentación sobre las herramientas de construción](doc/herramientasConstruccion.md)

## Gestor de procesos

Para gestionar multiples instancias del microservicio Gestor de Productos utilizaré pm2.

[Documentación sobre el gestor de procesos](doc/gestorProcesos.md)

## Docker

El Dockerfile se ha creado utilizando como base una imagen Alpine, de esta
forma la imagen será más liviana.

Contenedor: https://hub.docker.com/r/tonimr/cc-gestion-productos

[Documentación docker](doc/docker.md)  

[Documentación elección de la imagen base docker](doc/eleccionImagenDocker.md)

## PaaS: Despliegue en Heroku

El Paas escogido para desplegar el microservicio Gestor de Productos ha sido Heroku, ya que es gratuito y se puede integrar con GitHub.

Despliegue: https://cc-gestor-productos.herokuapp.com/

Las rutas implementadas por ahora son:

- **/productos**  (GET y POST)
- **/productos/_id** (GET, PUT, DELETE)

[Documentación despliegue en Heroku](doc/despliegueHeroku.md)

## Inversión de dependecias

[Documentación inversión de dependencias](doc/inversionDependencias.md)

## Test de rendimiento

Prestaciones: performance_request.yml

[Documentación test de rendimiento](doc/rendimientoTaurus.md)

## Provisión

Para crear la máquina primero debe crear 2 ficheros .env en la raiz del proyecto. El fichero .env_productos, necesario
para el microservicio de productos:

```ini
DB_URI=<URI a BD de MongoDB>
```

(Si se deseea que se ejecute en la BD local del dockerfile que se está ejecutando en la máquina indicar `mongodb://localhost:27017/productos`)

El fichero .env_productos, necesario para el microservicio de pedidos:

```ini
DB_USERNAME=<username>
DB_PASSWORD=<password>
DB_NAME=<bd_name>
GUNI_HOSTS=<host_gunicorn>
GUNI_PORT=8000
```

Un ejemplo podría ser:

```ini
DB_USERNAME=usuario
DB_PASSWORD=contraseña
DB_NAME=ms_pedidos
GUNI_HOSTS=0.0.0.0
GUNI_PORT=8000
```

**Crear la máquina en local:**

Una vez se han creado estos archivos .env. Ejecutar desde **./provision/local/**:

```bash
    vagrant up
```

**Crear la máquina en Azure:**

Primero hay que exportar las siguientes variables de entorno, como se explica en [Provisionar máquinas de Azure con Vagrant](doc/azure.md):

```bash
    export AZURE_TENANT_ID=<tenant>
    export AZURE_CLIENT_ID=<appId>
    export AZURE_CLIENT_SECRET=<password>
    export AZURE_SUBSCRIPTION_ID=<id>
```

Después, desde la ruta **./provision/azure/**:

```bash
    vagrant up
```

Entre en la sección [Provisionamiento de Máquinas Virtuales](doc/provisionamiento.md) para ver más documentación sobre como
se ha realizado el provisionamiento de máquinas virtuales.
