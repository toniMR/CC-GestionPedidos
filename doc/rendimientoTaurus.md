# Rendimiento con Taurus

Para medir las prestaciones de los microservicios se ha utilizado [Taurus](https://gettaurus.org/). Taurus
 es una herramienta de código abierto que nos permite estudiar el rendimiento de nuestras aplicaciones
de forma muy sencilla.

## Configuración del fichero .yml

Para realizar los test de rendimiento solo hay que crear un fichero .yml con las preferencias que
deseamos para realizar el test y las rutas sobre las que se harán las peticiones.

He creado el fichero **performance_request.yml**, en el que para cada microservicio he realizado 2 peticiones
GET a 2 rutas diferentes.

```yml
# Medir prestaciones de los microservicios con Taurus:
    execution:
        - concurrency: 10              # Habrá 10 usuarios concurrentes
          ramp-up: 15s                 # Se alcanzarán los 10 usuarios en 15s
          hold-for: 60s                # Los usuarios mantendrán la conexión por 1m
          scenario: pedidos-rest-test  # Nombre del test a ejecutar
    
    # Definir escenario
    scenarios:
        pedidos-rest-test:

            # Deshabilitar cache
            store-cache: false
            # Definir peticiones
            requests:
            - url: http://localhost:8000/pedidos
              method: GET

            - url: http://localhost:8000/pedidos/TAURUS
              method: GET 

        productos-rest-test:

          # Deshabilitar cache
          store-cache: false
          # Definir peticiones
          requests:
          - url: http://localhost:8080/productos
            method: GET

          - url: http://localhost:8080/productos/PR902205
            method: GET
```

Como se puede observar he establecido que sean 10 usuarios concurrentes, que mantendrán la conexión durante
1 minuto y se alcanzará los 10 usuarios concurrentes a los 15 segundos.  

Para el microservicio de pedidos se realiza una petición GET sobre los pedidos y otra petición GET sobre
un pedido concreto.

Para el microservicio de producto se realiza una petición GET sobre los productos y otra petición GET sobre
un producto concreto.

## Resultados

Se ha realizado las siguientes pruebas:

- [Microservicio de Productos con 2 workers y BD remota](#microservicio-de-productos-con-2-workers-y-bd-remota)
- [Microservicio de Productos con 2 workers](#microservicio-de-productos-con-2-workers)
- [Microservicio de Productos con 8 workers y BD remota](#microservicio-de-productos-con-8-workers-y-bd-remota)
- [Microservicio de Productos con 8 workers](#microservicio-de-productos-con-8-workers)
- [Microservicio de Pedidos con 2 workers](#microservicio-de-pedidos-con-2-workers)
- [Microservicio de Pedidos con 8 workers](#microservicio-de-pedidos-con-8-workers)

### Microservicio de Productos con 2 workers y BD remota

![terminal-productos-2workers-bdremota](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/taurus/terminal-productos-2workers-bdremota.png)
![bzm-productos-2workers-bdremota](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/taurus/bzm-productos-2workers-bdremota.png)

Como se puede observar se obtiene una media de 95.91 peticiones por segundo y el tiempo de respuesta medio es de 71ms.

### Microservicio de Productos con 2 workers

![terminal-productos-2workers](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/taurus/terminal-productos-2workers.png)
![bzm-productos-2workers](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/taurus/bzm-productos-2workers.png)

Como se puede observar se obtiene una media de 2496 peticiones por segundo y el tiempo de respuesta medio es de 3ms.

### Microservicio de Productos con 8 workers y BD remota

![terminal-productos-8workers-bdremota](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/taurus/terminal-productos-8workers-bdremota.png)
![bzm-productos-8workers-bdremota](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/taurus/bzm-productos-8workers-bdremota.png)

Como se puede observar se obtiene una media de 94.75 peticiones por segundo y el tiempo de respuesta medio es de 95ms.

### Microservicio de Productos con 8 workers

![terminal-productos-8workers](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/taurus/terminal-productos-8workers.png)
![bzm-productos-8workers](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/taurus/bzm-productos-8workers.png)

Como se puede observar se obtiene una media de 3667.65 peticiones por segundo y el tiempo de respuesta medio es de 2ms. Ha
 habido un incremento importante en cuanto a las peticiones por segundo.

### Microservicio de Pedidos con 2 workers

![terminal-pedidos-2workers](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/taurus/terminal-pedidos-2workers.png)
![bzm-pedidos-2workers](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/taurus/bzm-pedidos-2workers.png)

Como se puede observar se obtiene una media de 1354.97 peticiones por segundo y el tiempo de respuesta medio es de 6ms.

### Microservicio de Pedidos con 8 workers

![terminal-pedidos-8workers](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/taurus/terminal-pedidos-8workers.png)
![bzm-pedidos-8workers](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/taurus/bzm-pedidos-8workers.png)

Como se puede observar se obtiene una media de 2498.37 peticiones por segundo y el tiempo de respuesta medio es de 3ms. Ha
 habido un incremento de 1100 peticiones por segundo y el tiempo de respuesta medio se ha reducido a la mitad.

### Resultados generales

Ambos microservicios han superado las 1000 peticiones por segundo con 10 usuarios concurrentes.

- **Microservicio de productos:** 3667.65 peticiones/s y el tiempo de respuesta medio de 2ms con 8 workers.
- **Microservicio de pedidos:** 2498.37 peticiones/s y el tiempo de respuesta medio de 3ms con 8 workers.

Se ha observado que el uso de la Base de Datos remota en Mongo Atlas es un factor muy limitante, pues no ha podido pasar
 de las 100 peticiones por segundo tanto con 2 workers como con 8, mientras que en local y con 2 workers ya se obtiene 2400 peticiones por segundo para
 el microservicio de productos.
