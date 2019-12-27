# Tests

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

## Integración continua

### Travis CI

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

### Circle CI

Para el microservicio de productos, realizado en Python, utilizaré [**Circle CI**](https://circleci.com/)

Para usar Circle CI hay que realizar los siguientes pasos:

1) Registrarse en Circle CI.com con la cuenta de GitHub.
2) Aceptar autorización de Circle CI.
3) Seleccionar el repositorio.
4) Crear un fichero .circleci/config.yml en la raiz del proyecto.

El fichero config.yml lo he creado siguiendo la  [documentación  de Circle CI](https://circleci.com/docs/2.0/project-walkthrough/). Para configurar circle ci para testear varias versiones he seguido un [ejemplo de configuración para testear varias versiones](https://github.com/excitedleigh/virtualfish/blob/aa3d6271bcb86ad27b6d24f96b5bd386d176f588/.circleci/config.yml). Las dependencias las instalaré con pip3 install . y los test los ejecutaré con python3 setup.py test como he mencionado al explicar el fichero setup.py.