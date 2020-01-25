# Rendimiento con Taurus

Para medir las prestaciones de los microservicios se ha utilizado [Taurus](https://gettaurus.org/). Taurus
 es una herramienta de código abierto que nos permite estudiar el rendimiento de nuestras aplicaciones
de forma muy sencilla.

## Configuración del fichero .yml

Para realizar los test de rendimiento solo hay que crear un fichero .yml con las preferencias que
deseamos para realizar el test y las rutas sobre las que se harán las peticiones.

He creado el fichero **performance_request.yml**, en el que para cada microservicio he realizado el 
mismo conjunto de pruebas:

- POST (Se creará un elemento)
- PUT (Se modificará ese elemento)
- DELETE (Se eliminará ese elemento)

El fichero tiene comentarios explicativos sobre su configuración.

## Resultados

He realizado las pruebas de 2 formas:

- Sin utilizar nginx.
- Utilizando nginx para redireccionar las peticiones.

### Resultados Microservicio de Productos

![taurus-terminal-productos](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/taurus/taurus-terminal-productos.png)
![taurus-bzm-productos](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/taurus/taurus-bzm-productos.png)

Como se puede observar en la terminal, se muestra que llega hasta las 2794 peticiones por segundo, mientras que
en blazemeter muestra que tiene 2203 peticiones por segundo de media.

![taurus-terminal-productos-nginx](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/taurus/taurus-terminal-productos-nginx.png)
![taurus-bzm-productos-nginx](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/taurus/taurus-bzm-productos-nginx.png)

Como se puede observar en la terminal, se muestra que llega hasta las 2234 peticiones por segundo, mientras que
en blazemeter muestra que tiene 1950 peticiones por segundo de media.


### Resultados Microservicio de Pedidos

Como se puede observar en la terminal, se muestra que llega hasta las 2558 peticiones por segundo, mientras que
en blazemeter muestra que tiene 2270 peticiones por segundo de media.

![taurus-terminal-pedidos](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/taurus/taurus-terminal-pedidos.png)
![taurus-bzm-pedidos](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/taurus/taurus-bzm-pedidos.png)

Como se puede observar en la terminal, se muestra que llega hasta las 2239 peticiones por segundo, mientras que
en blazemeter muestra que tiene 2057 peticiones por segundo de media.

![taurus-terminal-pedidos-nginx](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/taurus/taurus-terminal-pedidos-nginx.png)
![taurus-bzm-pedidos-nginx](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/taurus/taurus-bzm-pedidos-nginx.png)

### Resultados generales

Ambos microservicios han obtenido alrededor de las 2000 peticiones por segundo con 8 usuarios concurrentes. Sin embargo,
se puede observar que el rendimiento cuando se ha utilizado Nginx para redireccionar las peticiones a los microservicios
han sido algo menores, cuando la idea era que esto mejorase las prestaciones.  
