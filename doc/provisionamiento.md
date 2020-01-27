# Provisionamiento de Máquinas Virtuales

Se creará una máquina en local y otra en Azure. Ambas contendrán las 2 imagenes docker creadas. La imagen docker
de los pedidos y la imagen docker de los productos.

## Vagrant

He utilizado Vagrant para la creación de las máquinas virtuales. En total he creado
dos vagrantfiles:

- Máquina virtual en local.
- Máquina virtual en Azure.

Para la máquina virtual en local he escogido como imagen 'ubuntu/bionic64' porque
con las de Ubuntu Server, aunque en un principio me funcionaba, luego obtenía errores.

Las imágenes se pueden buscar desde aquí: [Buscador de imágenes vagrant](https://app.vagrantup.com/boxes/search).
Probé con las siguientes entre otras:

- [Ubuntu/trusty64](https://app.vagrantup.com/ubuntu/boxes/trusty64)
- [jeffevesque/trusty64](https://app.vagrantup.com/jeff1evesque/boxes/trusty64)
- [aspyatkin/ubuntu-18.04-server](https://app.vagrantup.com/jeff1evesque/boxes/trusty64)

A la máquina local le he dado 3 cpus y 4 GB de RAM mientras que a la máquina de Azure
le he dado 4cpus y 8 gb de ram. La suscripción gratuita solo me permitía tener hasta 4 cores.

En [Provisionar máquinas de Azure con Vagrant](./azure.md) documento como he realizado el Vagrantfile para Azure.

## Ansible

Para el provisionamiento he utilizado Ansible.

Tanto para la máquina virtual en local como en Azure he utilizado el mismo fichero, playbook.yml.

Este se encargará de:

- Instalar docker a través de un rol Ansible Galaxy.
- Instalar el módulo de python "docker".
- Descargar las imágenes docker.
- Copiar los ficheros .env_pedidos y .env_productos
- Ejecutar las imágenes.

Para instalar docker he descargado el rol desde [Galaxy Ansible](https://galaxy.ansible.com/search?deprecated=false&keywords=docker&order_by=-relevance&page=1) y he escogido el que más descargas tenía, que era
el de gerlingguy.

## Rendimiento

### Máquina virtual local

Microservicio de Productos en local:

![Rendimiento-productos-vb-local](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/virtualbox-local-productos.png)

Microservicio de Pedidos en local:

![Rendimiento-pedidos-vb-local](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/virtualbox-local-pedidos.png)

### Máquina virtual en Azure

Microservicio de Productos en local:

![Rendimiento-productos-vb-Azure](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/virtualbox-azure-productos.png)

Microservicio de Pedidos en local:

![Rendimiento-pedidos-vb-Azure](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/virtualbox-azure-pedidos.png)

## Referencias

[Documentación](https://www.vagrantup.com/docs/vagrantfile/version.html)  
[Documentación](https://www.vagrantup.com/docs/vagrantfile/machine_settings.html)  
[Documentación](https://www.vagrantup.com/docs/vagrantfile/ssh_settings.html)  
[Documentación](https://www.vagrantup.com/docs/providers/configuration.html)  