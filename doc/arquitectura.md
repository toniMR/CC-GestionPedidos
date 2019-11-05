
# Arquitectura

![Diagrama arquitectura](img/diagrama-arquitectura.png)  

Se utilizará una arquitectura basada en microservicios en el que existirá un microservicio para gestionar los productos y otro microservicio para gestionar los pedidos.  

Los usuarios mandarán las peticiones a una **API Gateway** que será la encargada de ser el punto de entrada de las peticiones y redireccionarlas al microservicio correspondiente. Esta API Gateway será configurada con **Nginx**, ya que la API será fácil de configurar.

El **Microservicio 1** se encargará de gestionar los pedidos, de forma que se pueda crear un nuevo pedido, consultar los pedidos, borrarlos o modificarlos. Este microservicio será implementado en **Python** y como framework utilizaré **Flask** por la sencillez de implementación. Para almacenar la información usaré **PostgreSQL**, que es una base de datos relacional y open-source.  

El **Microservicio 2** se encargará de gestionar los productos, de forma que se pueda crear un nuevo producto, consultarlos, modificarlos o borrarlos. Este microservicio será implementado en **Node.js** y como framework utilizaré **Express**, ya que es uno de los frameworks más utilizados junto a Node.js. Para almacenar la información usaré **MongoDB**, que es una base de datos open-source orientada a documentos.

El microservicio 1 se comunicará con el microservicio 2 a través de su API REST. Por ejemplo, al realizar un pedido, se necesita saber si existen los productos que se indicaron y si hay stock suficiente, y el microservicio 2 le responderá con el resultado. De la misma forma, al realizar un pedido, el microservicio 1 le comunicará al microservicio 2 que tiene que reducir el stock de esos productos.

Además, habrá un **sistema de logs** en el que se registrará todas las peticiones que se hagan y un **sistema de configuración** en el que se almacenará los parámetros comunes de configuración. 