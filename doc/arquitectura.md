
# Arquitectura

![Diagrama arquitectura](img/diagrama-arquitectura.png)  

Se utilizará una arquitectura basada en microservicios en el que existirá un microservicio para gestionar los productos y otro microservicio para gestionar los pedidos.  

Los usuarios mandarán las peticiones a una **API Gateway** que será la encargada de ser el punto de entrada de las peticiones y redireccionarlas al microservicio correspondiente. Esta API Gateway será configurada con [Nginx](https://www.nginx.com/), ya que será fácil de configurar el redireccionamiento al microservicio correspondiente.

El **Microservicio 1** se encargará de gestionar los pedidos, de forma que se pueda crear un nuevo pedido, consultar los pedidos, borrarlos o modificarlos. Este microservicio será implementado en [Python](https://www.python.org/), ya que dispone de una gran cantidad de módulos disponibles y una comunidad muy grande que le da soporte. Como framework utilizaré [Flask](https://www.palletsprojects.com/p/flask/) por la sencillez y rapidez de implementación. Para almacenar la información usaré [PostgreSQL](https://www.postgresql.org/), que es una base de datos relacional y open-source.  

El **Microservicio 2** se encargará de gestionar los productos, de forma que se pueda crear un nuevo producto, consultarlos, modificarlos o borrarlos. Este microservicio será implementado en [Node.js](https://nodejs.org/es/), ya que tiene un gran rendimiento y tiene un gestor de paquetes, NPM (Node Package Manager) con la que se puede acceder a muchas librerías open-source. Como framework utilizaré [Express](https://expressjs.com/es/) ya que es uno de los frameworks más utilizados junto a Node.js. Para almacenar la información usaré [MongoDB](https://www.mongodb.com/es), que es una base de datos open-source orientada a documentos.

El microservicio 1 se comunicará con el microservicio 2 a través de su API REST. Por ejemplo, al realizar un pedido, se necesita saber si existen los productos que se indicaron y si hay stock suficiente, y el microservicio 2 le responderá con el resultado. De la misma forma, al realizar un pedido, el microservicio 1 le comunicará al microservicio 2 que tiene que reducir el stock de esos productos.

Habrá un **sistema de logs**  en el que se registrará todas las peticiones que se hagan. Para ello se centralizarán usando [Logstash](https://www.elastic.co/es/products/logstash), que es una de las herramientas open-source que más se está usando. Para enviar los logs utilizaré [python-logstash](https://pypi.org/project/python-logstash/) en Python y [node-logstash](https://www.npmjs.com/package/node-logstash) en Node.js, para enviar los logs generados en la API Gateway se realizará la configuración en Nginx.

También habrá un **sistema de configuración** en el que se almacenará los parámetros comunes de configuración. Para ello utilizaré [etcd](https://etcd.io/) por la facilidad de uso.
