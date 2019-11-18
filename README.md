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

Para realizar los tests he utilizado las siguientes herramientas:  

Para el microservicio de productos, desarrollado en **Node.js**, utilizaré **Mocha** como marco de tests.

Para el microservicio de pedidos, desarrollado en **Python**, utilizaré **Pytest** como marco de tests y **unnitest** como biblioteca de aserciones.

## Cobertura

Para realizar la cobertura para el código escrito en Python utilizaré **pytest-cov**, que permite generar reportes de cobertura con tan solo indicar la ruta de los archivos.

```bash
    pytest --cov=./src/pedidos/
```

Para realizar la cobertura para el código escrito en Node.js utilizaré **nyc**, ya que es muy sencilla de utilizar. En un principio iba a utilizar instanbul, pero en la [documentación](https://www.npmjs.com/package/istanbul) indican que ya no se está desarrollando más y recomiendan nyc.

```bash
    nyc mocha --recursive
```

La plataforma en la que subiré los reportes de cobertura será [**Codecov**](https://codecov.io/).

[Documentación pytest-cov](https://pypi.org/project/pytest-cov/)  

[Uso de nyc](https://github.com/istanbuljs/nyc)  

[Uso de nyc (2)](https://istanbul.js.org/docs/tutorials/mocha/)  

[GitHub Codecov](https://github.com/codecov/example-python#can-i-upload-my-coverage-files)  

## Herramientas de construcción

### package.json

buildtool: package.json

Para el microservicio de productos, realizado en Node.js, usaré **package.json**. En este fichero se indicará el nombre del proyecto, el autor, la licencia, scripts y las dependencias necesarias para el entorno de producción y para el de desarrollo y testing.

Para realizar los tests hay que ejecutar el script test indicado en el fichero:

```bash
    npm test
```

Esto ejecutará la orden siguiente:

```bash
    nyc --reporter=lcov mocha --recursive && codecov
```

nyc realizará la cobertura del código testeado con mocha --recursive, --reporter=lcov es necesario para generar el reporte que se subirá a codecov. Tras realizar el reporte se subirá a codecov con la orden codecov.

Para instalar las dependencias hay que ejecutar:

```bash
    npm install
```

También se puede ejecutar:

```bash
    npm ci
```

La diferencia es que npm ci se suele utilizar en entornos de automatización como plataformas de integración continua. Realiza instalaciones de dependecias de forma más limpia y rápida. Para usarlo es necesario haber instalado previamente las dependencias con npm install para generar el fichero **package-lock.json**.

[Uso de nyc](https://github.com/istanbuljs/nyc)

[Uso de nyc (2)](https://istanbul.js.org/docs/tutorials/mocha/)  

[Documentación npm ci](https://docs.npmjs.com/cli/ci.html)  

[Información npm ci](https://medium.com/better-programming/npm-ci-vs-npm-install-which-should-you-use-in-your-node-js-projects-51e07cb71e26)

### setup.py

buildtool: setup.py

Para el microservicio de gestión de pedidos he utilizado como herramienta de construcción **setup.py**, ya que este fichero se utiliza para empaquetar el proyecto con Distutils, que es la herramienta estándar para distribuir módulos de Python. En mi caso lo he configurado con **setuptools**, ya que facilita la configuración y está basado en disutils.

En este fichero se indica el nombre del proyecto, el autor, versión y dependencias para el entorno de producción y para el de desarrollo y testing.

Las herramientas necesarias para el entorno de producción se indican en **install_requires** y las que son necesarias para realizar los test se indican en **tests_require**. De esta forma si el proyecto se va a usar en un entorno de producción solo se instalarán las dependencias necesarias para ello y las de testing solo se instalarán en el momento que se vayan a ejecutar los test.

Para realizar los tests con pytest y generar la cobertura con pytest-cov he tenido que indicar estas dependencias en test_require. En **setup_requires** he tenido que indicar la dependencia **pytest-runner** para poder ejecutar pytest desde setup.py. También he tenido que crear un archivo llamado setup.cfg en el que indico un alias para test, que será pytest, **addopts** para indicar los argumentos que se pasarán a pytest y **python_files** para indicar los archivos de tests.

Para limpiar el proyecto he creado una clase que será la encargada de ejecutar los comandos necesarios. Para hacerlo así he indicado en cmdclass el nombre clean y le he asociado la clase Cleaner.

Ejecutar los tests:

```bash
    python3 setup.py test
```

Instalar dependencias del proyecto:

```bash
    pip3 install .
```

Limpiar el proyecto:

```bash
    python3 setup.py clean
```

[Configurar pytest en setup.py](https://pytest.readthedocs.io/en/2.8.7/goodpractices.html)

[Building and Distributing Packages with Setuptools](https://setuptools.readthedocs.io/en/latest/setuptools.html)

### Integración continua

#### Travis CI

Utilizaré dos sistema de integración continua. Cada microservicio se realizará en un sistema diferente para agilizar el proceso de testing.

Para el microservicio de productos, realizado en Node.js, utilizaré [**Travis CI**](https://travis-ci.com/)  

Para usar Travis CI hay que realizar los siguientes pasos:

1) Registrarse en Travis-ci.com con la cuenta de GitHub.
2) Aceptar autorización de Travis CI. Será rediccionado a Github.
3) Seleccionar los repositorios en los que quieras usar Travis CI.
4) Crear un fichero .travis.yml en la raiz del proyecto.

En el fichero **.travis.yml** se indicará que se utilizará el lenguage Node.js y las versiones a testear. Previamente he testeado cuál es la versión mínima compatible y he obtenido que es la 8.16.2. Las dependencias las instalaré con npm ci y los test se ejecutarán con npm test, como he mecionado al explicar el fichero package.json.

[Documentación Travis CI](https://docs.travis-ci.com/user/languages/javascript-with-nodejs/)  

[Configurar Travis CI para usar npm ci](https://docs.npmjs.com/cli/ci.html)

#### Circle CI

Para el microservicio de productos, realizado en Python, utilizaré [**Circle CI**](https://circleci.com/)

Para usar Circle CI hay que realizar los siguientes pasos:

1) Registrarse en Circle CI.com con la cuenta de GitHub.
2) Aceptar autorización de Circle CI.
3) Seleccionar el repositorio.
4) Crear un fichero .circleci/config.yml en la raiz del proyecto.

El fichero config.yml lo he creado siguiendo la  [documentación  de Circle CI](https://circleci.com/docs/2.0/project-walkthrough/). Para configurar circle ci para testear varias versiones he seguido un [ejemplo de configuración para testear varias versiones](https://github.com/excitedleigh/virtualfish/blob/aa3d6271bcb86ad27b6d24f96b5bd386d176f588/.circleci/config.yml). Las dependencias las instalaré con pip3 install . y los test los ejecutaré con python3 setup.py test como he mencionado al explicar el fichero setup.py.
