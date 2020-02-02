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

Para el provisionamiento he utilizado Ansible, he utilizado el fichero playbook-local.yml para la máquina
local y playbook-azure.yml para la máquina en Azure.

Se encargarán de:

- Actualizar el sistema.
- Instalar pip.
- Instalar docker a través de un rol Ansible Galaxy.
- Instalar el módulo de python "docker".
- Descargar las imágenes docker.
- Copiar los ficheros .env_pedidos y .env_productos
- Ejecutar las imágenes.

Lo único en que se diferencian es en la forma que instala pip y el módulo de docker con pip.

Para instalar docker he descargado el rol [docker](https://galaxy.ansible.com/geerlingguy/docker) desde [Galaxy Ansible](https://galaxy.ansible.com/search?deprecated=false&keywords=docker&order_by=-relevance&page=1) y he escogido el que más descargas tenía, que era el de gerlingguy. Para solucionar un error con pip a la hora de desplegar la máquina en Azure he utilizado el rol [pip](https://galaxy.ansible.com/geerlingguy/pip) en
playbook-azure.yml.

## Azure

### Microservicio Productos

![azure-productos](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/azure-productos.png)

### Microservicio Pedidos

![azure-pedidos](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/azure-pedidos.png)

## Rendimiento

### Máquina virtual local

Microservicio de Productos en local:

![terminal-productos-local](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/terminal-productos-local.png)
![bzm-productos-local](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/bzm-productos-local.png)

Microservicio de Pedidos en local:

![terminal-pedidos-local](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/terminal-pedidos-local.png)
![bzm-pedidos-local](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/bzm-pedidos-local.png)

### Máquina virtual en Azure

Microservicio de Productos en Azure:

![terminal-productos-azure](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/terminal-productos-azure.png)
![bzm-productos-azure](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/bzm-productos-azure.png)

Microservicio de Pedidos en Azure:

![terminal-pedidos-azure](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/terminal-pedidos-azure.png)
![bzm-pedidos-azure](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/bzm-pedidos-azure.png)

Como se puede observar, el rendimiento en Azure es muy bajo con 135 peticiones por segundo y 65ms de tiempo de respuesta medio para ambos microservicios.

## Referencias

https://www.vagrantup.com/docs/vagrantfile/version.html  
https://www.vagrantup.com/docs/vagrantfile/machine_settings.html  
https://www.vagrantup.com/docs/vagrantfile/ssh_settings.html  
https://www.vagrantup.com/docs/providers/configuration.html  
https://blog.deiser.com/es/primeros-pasos-con-ansible  
https://www.adictosaltrabajo.com/2015/09/04/creacion-de-entornos-de-integracion-con-ansible-y-vagrant/  
