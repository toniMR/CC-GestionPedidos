# CC-GestionPedidos

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Descripción

El proyecto consistirá en un gestor de productos y pedidos en el que el usuario podrá ver todos los productos que hay y realizar un pedido con la lista de productos y cantidades que desea.  

Consistirá en 2 microservicios con los que se podrá añadir, consultar, modificar y eliminar tanto los productos como los pedidos.

## Arquitectura

[Documentación sobre la arquitectura escogida](doc/arquitectura.md)

## Entidades e historias de uso

En el proyecto se va a trabajar con 2 entidades principales: Productos y Pedidos.

### Productos

Son los productos que podrán solicitar los usuarios. Cada producto contendrá:

- Código de producto.
- Nombre.
- Descripción.
- Precio.
- Stock.
- Categorías.

#### Historias de usuario asociadas a los Productos

[Issue 16: Consultar productos existentes](https://github.com/toniMR/CC-GestionPedidos/issues/16)  
[Issue 17: Consultar productos existentes que cumplan ciertas condiciones](https://github.com/toniMR/CC-GestionPedidos/issues/17)  
[Issue 18:  Añadir un nuevo producto](https://github.com/toniMR/CC-GestionPedidos/issues/18)  
[Issue 19: Modificar un producto](https://github.com/toniMR/CC-GestionPedidos/issues/19)  
[Issue 20: Eliminar un producto](https://github.com/toniMR/CC-GestionPedidos/issues/20)  

### Pedidos

Son los pedidos que realizarán  los usuarios. Cada pedido contendrá:

- Código de pedido.
- Nombre del destinatario.
- Dirección de envío.
- Lista de #Producto y unidades solicitadas.
- Estado del pedido (No procesado, Procesado, Entregando, Entregado)

#### Historias de usuario asociadas a los Pedidos

[Issue 21: Realizar un pedido](https://github.com/toniMR/CC-GestionPedidos/issues/21)  
[Issue 22: Modificar un pedido](https://github.com/toniMR/CC-GestionPedidos/issues/22)  
[Issue 23: Eliminar un pedido](https://github.com/toniMR/CC-GestionPedidos/issues/23)  
[Issue 24: Consultar un pedido](https://github.com/toniMR/CC-GestionPedidos/issues/24)  
[Issue 25: Consultar todos los pedidos](https://github.com/toniMR/CC-GestionPedidos/issues/25)  
[Issue 26: Consultar los pedidos con un estado determinado](https://github.com/toniMR/CC-GestionPedidos/issues/26)  
[Issue 27: Modificar el estado de un pedido](https://github.com/toniMR/CC-GestionPedidos/issues/27)  
