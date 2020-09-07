
# Provision Google

En esta provision en Google Cloud se desplegaraán los microservicios haciendo uso del fichero
docker-compose creado, de forma que se desplegará el microservicio de Productos y el de
Pedidos junto a un servicio Nginx como API Gateway.

## Requisitos

- [Instalar SDK de Google](https://cloud.google.com/sdk/docs/)
- [Instalar plugin de Google para Vagrant](https://www.rubydoc.info/gems/vagrant-google/0.2.3)
- [Crear una configuración en Google Cloud Platform](https://github.com/mitchellh/vagrant-google#google-cloud-platform-setup)
  - Crear un proyecto
  - Obtener una clave JSON
  - Asociar clave SSH

## Vagrant

Para la creación del Vagrantfile necesitaremos cierta información:

Podemos obtener que imágenes podemos utilizar con:

```bash
gcloud compute images list
```

```Vagrantfile
# -*- mode: ruby -*-
# vi: set ft=ruby :

# Este fichero sirve para crear con Vagrant la máquina virtual que 
# alojará ambos microservicios en Google Cloud

# Especificar el uso de la versión 1.1+ hasta 2.0.x de vagrant
Vagrant.configure("2") do |config|

  # Configurar la box
  config.vm.box = "google/gce"

  # Network
  # -----------------------------------------------------------------------
  # Google provider no permite ninguna configuración de red de alto nivel
  # creada en Vagrant. Por lo que la redirección de puertos se realizará
  # posteriormente con el SDK de Google Cloud.

  # Establece la configuración de la máquina para un proveedor específico
  # Crea una variable, en mi caso llamada google para realizar la configuración
  config.vm.provider :google do |google, override|

    # Id del proyecto en Google Cloud
    google.google_project_id = "cloudcomputing-288611"
    # Clave .json obtenida en Google Cloud
    google.google_json_key_location = "./cloudcomputing-288611-6cd514040cda.json"
    # Nombre que le daremos a la instancia
    google.name = "cc-tonimr"
    # Espeficar donde se alojara la máquina
    google.zone = "europe-west2-b"
    # Tipo de máquina
    google.machine_type = "n1-standard-4"
    google.image_project_id = "ubuntu-os-cloud"
    google.image = "ubuntu-2004-focal-v20200902"
    # Establecer nombre de usuario y ubicacion de la clave
    # con la que accederemos a la máquina.
    override.ssh.username = "antonio"
    override.ssh.private_key_path = "~/.ssh/id_rsa"
  end


  config.vm.define "gp_google" do |gestionpedidos|
    # Establecer configuración de provisionamiento
    config.vm.provision :ansible do |ansible|
      # ansible.verbose = 'vvv'
      # Indica la ruta en la que encuentra el archivo playbook.yml
      ansible.playbook = "./playbook-google.yml"
    end
  end
end
```

## Ansible

Tras la creación de nuestra máquina la provisionamos con Ansible.

```yml
---
  - hosts: all
    remote_user: toniMR
    # Permitir escalada de privilegios
    become: yes

    pre_tasks:
      # Actualizar sistema
      - name: Apt update
        apt:
          update_cache: 'yes'

  
    # Indicar a pip que instale el módulo de docker
    vars:
      pip_install_packages:
        - docker
        - docker-compose


    # Roles utilizados
    roles:
      # Instalar docker con un rol descargado desde Ansible galaxy
      - geerlingguy.docker
      - geerlingguy.pip


    # Especificamos las tareas del playbook:
    tasks:
  
      - name: Copiar fichero .env
        copy:
          src: ../../.env
          dest: ./.env

      - name: Copiar carpeta api_gateway
        copy:
          src: ../../api_gateway
          dest: ./
  
      - name: Copiar fichero docker-compose.yml
        copy:
          src: ../../docker-compose.yml
          dest: ./docker-compose.yml
  
  
      # Levantar todos los contenedores con docker-compose:
      - name: Levantar contenedores
        docker_compose:
          project_src: ./
```

### Roles

Para la instalación de docker utilizaremos roles de ansible galaxy. En mi caso he utilizado los
siguietes:

- [geerlingguy.docker](https://galaxy.ansible.com/geerlingguy/docker)
- [geerlingguy.pip](https://galaxy.ansible.com/geerlingguy/pip)


### Uso

1. Descargar roles necesarios desde Ansible Galaxy

Desde el directorio /provision/google:

```bash
    ansible-galaxy install -p roles geerlingguy.docker
    ansible-galaxy install -p roles geerlingguy.pip
```

2. Realizar provisionamiento

```bash
    vagrant up
```

Con esta instrucción se encargará de crear la máquina virtual y de realizar el provisionamiento haciendo uso de los roles
para levantar los servicios con Docker. 

3. Crear reglas del firewall.  [Documentación](https://cloud.google.com/vpc/docs/using-firewalls)

Permitir que se pueda acceder desde el puerto 80. Esto se debe hacer desde el SDK de Google, ya que el proveedor de Google
para Vagrant no permite realizar configuraciones de red de alto nivel desde Vagrant.

```bash
gcloud compute firewall-rules create allow-microservices-access \
     --network default \
     --direction ingress \
     --action allow \
     --source-ranges 0.0.0.0/0 \
     --rules tcp:80
```

4. Ver estado de la máquina [Documentacion](https://cloud.google.com/sdk/gcloud/reference/compute/addresses/list?hl=es)

Una vez creada la máquina podremos ver su estado y su ip con el siguiente comando del SDK:

```bash
gcloud compute instances list
```

## Microservicio Productos

![google-productos](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/google/google-pedidos-req.png)  

### Rendimiento Productos

![terminal-productos-google](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/google/terminal-productos-google.png)  
![bzm-productos-google](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/google/bzm-productos-google.png)  

## Microservicio Pedidos

![google-pedidos](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/google/google-productos-req.png)  

### Rendimiento Pedidos

![terminal-pedidos-google](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/google/terminal-pedidos-google.png)  
![bzm-pedidos-google](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/google/bzm-pedidos-google.png)  

Como se puede observar, en ambos microservicios se obtiene un rendimiento muy bajo. Esto se debe a la latencia por la ubicación del servidor.
