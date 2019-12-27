# Herramientas de construcción

## package.json

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

## setup.py

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