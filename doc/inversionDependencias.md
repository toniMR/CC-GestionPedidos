# Inversión de dependencias

La inversión de dependencias es un principio que nos ayuda a desacoplar las dependencias en nuestro proyecto, de forma que este se vuelve más flexible, claro y fácil de testear. Es por ello que he realizado la inversión de dependencias en ambos microservicios.

## Microservicio de Pedidos

Para realizar la inversión de dependencias en el microservicio de pedidos he hecho uso del framework [python-dependency-injector](https://github.com/ets-labs/python-dependency-injector).  

Con esta herramienta hemos creado un Contenedor en el fichero [container.py](/src/pedidos/container.py) que será el encargado de establecer las dependencias del proyecto. Cuando se crea la aplicación Flask en [__init__.py](/src/pedidos/__init__.py), se llama al contenedor [container.py](/src/pedidos/container.py) y se establecen las variables de configuración. De esta forma se puede establecer que depencias son las que se van a utilizar. Estas dependencias serán pasadas en el constructor de [GestorPedidos](/src/pedidos/gestorPedidos.py). En mi caso, tengo dos manejadores de bases de datos en [data_managers](/src/pedidos/data_managers), que son [Psycopg2DataManager](/src/pedidos/data_managers/postgres/psycopg2/) y [SqlAlchemyDataManager](/src/pedidos/data_managers/postgres/sqlalchemy/), que hacen uso de herramientas diferentes para tratar con [PostgreSQL](https://www.postgresql.org/).  

Por ejemplo, en mi caso, en el contenedor he establecido un Selector, de forma que depende de la configuración establecida se escoja un manejador de datos u otro. Si quisiera cambiar del manejador de Base de Datos [Psycopg2DataManager](/src/pedidos/data_managers/postgres/psycopg2/) al [SqlAlchemyDataManager](/src/pedidos/data_managers/postgres/sqlalchemy/) solo tendría que cambiar la configuración del contenedor al crear la aplicación Flask en el fichero [__init__.py](/src/pedidos/__init__.py#L34) y establecer el deseado.  

El único requisito para que esto funcione es que todos los manejadores de bases de datos deben tener los mismos métodos.  

Además simplifica el trabajo a la hora de realizar tests, ya que con tan solo sobreescribir la configuración del contenedor ya estaríamos usando otras dependencias. [Ejemplo](/test/pedidos/test_pedidoRest.py#L124)  

A la hora de establecer las dependencias en el Container hago uso de [Singleton provider](http://python-dependency-injector.ets-labs.org/providers/singleton.html) para que siempre se devuelva la misma instancia de la dependencia. Si s hiciera con [Factory provider](http://python-dependency-injector.ets-labs.org/providers/factory.html) se crearía una nueva instancia cada vez que se llamara a la dependencia. En mi caso, al usar Factory provider, el rendimiento disminuyó de alrededor de las 2300 peticiones por segundo a alrededor de 300.

## Microservicio de Productos

Para realizar la inversión de dependencias en el microservicio de productos he hecho uso de [InversifyJS](https://github.com/inversify/InversifyJS)

Con esta herramienta he creado un Contenedor en el fichero [container.js](/src/productos/container/container.js) en el que establezco las dependencias que se podrán inyectar, de esta forma cuando un modulo requiere la dependencia la puede solicitar del contenedor, Como se hace por ejemplo en [controller.js](/src/productos/controllers/producto_controller.js).  

En este caso si quisiera cambiar el manejador de la base de datos por otro solo tendría que indicarlo en [container.js](/src/productos/container/container.js)

## Referencias

- [Flask-tutorial python-dependency-injector](http://python-dependency-injector.ets-labs.org/tutorials/flask.html#flask-tutorial)
- [Ejemplo InversifyJS en Javascript](https://github.com/inversify/InversifyJS/blob/master/wiki/basic_js_example.md)
