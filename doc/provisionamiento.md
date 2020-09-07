# Provisionamiento de Máquinas Virtuales

Se creará una máquina en local, otra en Azure y otra en Google Cloud. 

## Vagrant

He utilizado Vagrant para la creación de las máquinas virtuales. En total he creado
tres vagrantfiles:

- Máquina virtual en local.
- Máquina virtual en Azure.
- Máquina virtual en Google Cloud.

Para la máquina virtual en local he escogido como imagen 'ubuntu/bionic64' porque
con las de Ubuntu Server, aunque en un principio me funcionaba, luego obtenía errores.

Las imágenes se pueden buscar desde aquí: [Buscador de imágenes vagrant](https://app.vagrantup.com/boxes/search).
Probé con las siguientes entre otras:

- [Ubuntu/trusty64](https://app.vagrantup.com/ubuntu/boxes/trusty64)
- [jeffevesque/trusty64](https://app.vagrantup.com/jeff1evesque/boxes/trusty64)
- [aspyatkin/ubuntu-18.04-server](https://app.vagrantup.com/jeff1evesque/boxes/trusty64)

A la máquina local le he dado 4 cpus y 4 GB de RAM mientras que a la máquina de Azure
le he dado 4cpus y 8 gb de ram. La suscripción gratuita solo me permitía tener hasta 4 cores.


## Ansible

Para el provisionamiento he utilizado Ansible. Para el provisionamiento en local y en Google Cloud
he usado el mismo playbook, ya que añadí un fichero docker-compose para desplegar los microservicios
más rápido. Además también añadí un API Gateway con Nginx. La razón por la que no añadí este
cambio al provisionamiento en Azure fue porque ya agoté el saldo de la cuenta gratuita.

Por lo que el playbook en el provisionamiento en Azure se encarga de:

- Actualizar el sistema.
- Instalar pip a través de un rol Ansible Galaxy.
- Instalar docker a través de un rol Ansible Galaxy.
- Instalar el módulo de python "docker".
- Descargar las imágenes docker.
- Copiar el fichero .env
- Ejecutar las imágenes.

El playbook utilizado para Google Cloud y la máquina local;

- Actualizar el sistema.
- Instalar pip a través de un rol Ansible Galaxy.
- Instalar docker a través de un rol Ansible Galaxy.
- Instalar el módulo de python "docker".
- Instalar el módulo de python "docker-compose".
- Copiar el fichero docker-compose.yml.
- Copiar el fichero .env
- Copiar el fichero nginx.conf.
- Levantar los microservicios con docker-compose.

## Variables de entorno

En la raíz del repositorio hay que crear un fichero .env con las siguientes variables

```
DB_USERNAME=<username>
DB_PASSWORD=<password>
DB_NAME=<nombre_bd>
DB_HOST=<ip_host_postgre>
DB_PORT=<port_host_postgre>
GUNI_PORT=8000
WORKERS=<NUM_WORKERS>
POSTGRES_USER=<username>
POSTGRES_PASSWORD=<password>
POSTGRES_DB=<nombre_bd>
DB_URI=<adress_mongo>
```


Un ejemplo, podría ser el siguiente:

```
DB_USERNAME=username
DB_PASSWORD=password
DB_NAME=ms_pedidos
DB_HOST=postgres (postgres: nombre contenedor)
DB_PORT=5432
GUNI_PORT=8000
WORKERS=8
POSTGRES_USER=username
POSTGRES_PASSWORD=password
POSTGRES_DB=ms_pedidos
DB_URI=mongodb://mongo:27017/productos (mongo: nombre contenedor)
```


## Creación de las máquinas

Para crear las máquinas y realizar el provisionamiento solamente hay qu posicionarse en una de las carpetas
que hay en el directorio provision y ejecutar:

```bash
    vagrant up
```

## Provisionamientos

Aquí puede ver información más detallada sobre cada uno de los provisionamientos:

- [Azure](/doc/provisionAzure.md)
- [Google Cloud](/doc/provisionGoogle.md)
- [Local](/doc/provisionLocal.md)

## Referencias

https://www.vagrantup.com/docs/vagrantfile/version.html  
https://www.vagrantup.com/docs/vagrantfile/machine_settings.html  
https://www.vagrantup.com/docs/vagrantfile/ssh_settings.html  
https://www.vagrantup.com/docs/providers/configuration.html  
https://blog.deiser.com/es/primeros-pasos-con-ansible  
https://www.adictosaltrabajo.com/2015/09/04/creacion-de-entornos-de-integracion-con-ansible-y-vagrant/  
