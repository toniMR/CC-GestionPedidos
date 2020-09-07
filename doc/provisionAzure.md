# Vagrant en Azure

## Requisitos

1. Instalar CLI de Azure

Para instalar el CLI de Azure hay que seguir los pasos de la [Documentación oficial](https://docs.microsoft.com/es-es/cli/azure/install-azure-cli-apt?view=azure-cli-latest)

2. Instalar plugin de Azure para Vagrant. [Vagrant-Azure](https://www.rubydoc.info/gems/vagrant-azure/1.3.0)

```bash
    vagrant plugin install vagrant-azure
```

3. Generar AAD (Azure Active Directory) para poder acceder a nuestros recursos en Azure:

[Creación de una entidad de servicio de Azure con la CLI de Azure](https://docs.microsoft.com/es-es/cli/azure/create-an-azure-service-principal-azure-cli?view=azure-cli-latest)

```bash
    az ad sp create-for-rbac
```

4. Exportar variables de entorno con los datos obtenidos en el comando anterior

```bash
export AZURE_TENANT_ID=<tenant>
export AZURE_CLIENT_ID=<appId>
export AZURE_CLIENT_SECRET=<password>
export AZURE_SUBSCRIPTION_ID=<id>
```

5. Añadir dummy box de vagrant azure

```bash
    vagrant box add azure https://github.com/azure/vagrant-azure/raw/v2.0/dummy.box --provider azure
```

[Vagrant Azure Provider](https://github.com/Azure/vagrant-azure)

## Vagrantafile

Para configurar el Vagrantfile necesitamos saber varias cosas:

1. Región en la que desplegaremos la máquina

```bash
az account list-locations -o table
```

2. Tipos de máquinas que se pueden desplegar en una región

```bash
az vm list-skus --location francesouth --output table
```

3. Imágenes disponibles para usar en nuestra máquina:

```bash
az vm image list --output table --all
```

```vagrantfile
# Este fichero sirve para crear en azure la máquina virtual que alojará ambos
# microservicios:

# Especificar el uso de la versión 1.1+ hasta 2.0.x de vagrant
Vagrant.configure("2") do |config|
  
  # Configurar la box
  config.vm.box = "azure"

  # Configurar ruta a la clave privada para conectar remotamente
  # al vagrant box
  config.ssh.private_key_path = '~/.ssh/id_rsa'

  # Establece la configuración de la máquina para un proveedor específico
  # Crea una variable, en mi caso llamada azure para realizar la configuración
  config.vm.provider :azure do |azure|

    # Parámetros para los datos de la suscripción de Azure
    # Establece variables de entorno para poder asignarles el valor
    azure.tenant_id = ENV['AZURE_TENANT_ID']
    azure.client_id = ENV['AZURE_CLIENT_ID']
    azure.client_secret = ENV['AZURE_CLIENT_SECRET']
    azure.subscription_id = ENV['AZURE_SUBSCRIPTION_ID']

    # Nombre de la máquina virtual
    azure.vm_name = "ccmastergestionpedidos"

    # Nombre de usuario del administrador de la Máquina Virtual
    azure.admin_username = "toniMR"

    # Puerto por el que nos conectaremos a la máquina
    azure.tcp_endpoints = [8000,8080]

    # Región en la que se creará la máquina
    # France central
    azure.location = 'francecentral'

    # Especificar os recursos que le proporcionaremos a la máquina
    # Standard_F4s:
    # vCPU: 4
    # Memoria: 8 GiB
    # He escogido esta porque el maximo de cores que me permiten en la
    # suscripción es 4. Standard_F4s
    azure.vm_size = "Standard_F4s"

    # Especificar la imagen a montar en la máquina
    azure.vm_image_urn = 'Canonical:UbuntuServer:18.04-LTS:latest'

    # Especificar grupo de recursos
    azure.resource_group_name = 'CCGestionPedidos'
  end


  config.vm.define "gp_azure" do |gestionpedidos|
    # Establecer configuración de provisionamiento
    config.vm.provision :ansible do |ansible|
      # Indica la ruta en la que encuentra el archivo playbook.yml
      ansible.playbook = "./playbook-azure.yml"
    end
  end
end
```

## Ansible

Tras la creación de nuestra máquina la provisionamos con Ansible.

```yml
# Este playbook será llamado automáticamente desde el Vagrantfile para crear
# la máquina en local y el Vagrantfile para crearla en Azure
---
- hosts: all
  remote_user: toniMR
  # Permitir escalada de privilegios
  become: yes

  # Indicar a pip que instale el módulo de docker
  vars:
    pip_install_packages:
      - name: docker

  # Roles utilizados
  roles:
    # Instalar docker con un rol descargado desde Ansible galaxy
    - geerlingguy.pip
    - geerlingguy.docker

  # Establecer tareas:
  tasks:
    # Actualizar sistema
    - name: Apt | Update
      apt:
        update_cache: 'yes'

    # Descargar la imagen desde Docker Hub del microservicio Productos:
    - name: docker pull productos image
      docker_image:
        name: tonimr/cc-gestion-productos:productos
        source: pull 

    # Descargar la imagen desde Docker Hub del microservicio Pedidos:
    - name: docker pull pedidos image
      docker_image:
        name: tonimr/cc-gestion-productos:pedidos
        source: pull

    # Copiar los ficheros .env de cada microservicio para establecer
    # las variables de entorno necesarias.
    - name: copy .env
      copy:
        src: ../.env_productos
        dest: /etc/.env

    # Ejecutar el contenedor de productos:
    - name: docker run productos container
      docker_container:
        name: productos
        image: tonimr/cc-gestion-productos:productos
        auto_remove: yes
        detach: yes
        # Publicar el puerto 8080 para poder acceder desde el anfitrion
        # al contenedor desde ese puerto
        published_ports: 8080:8080
        # Indicar la ruta del archivo .env de los productos:
        env_file: /etc/.env

    # Ejecutar el contenedor de pedidos:
    - name: Docker | Run pedidos container
      docker_container:
        name: pedidos
        image: tonimr/cc-gestion-productos:pedidos
        auto_remove: yes
        detach: yes
        # Publicar el puerto 8000 para poder acceder desde el anfitrion
        # al contenedor desde ese puerto
        published_ports: 8000:8000
        # Indicar la ruta del archivo .env de los productos:
        env_file: /etc/.env
```

## Microservicio Productos

![azure-productos](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/azure/azure-productos.png)

### Rendimiento Productos

Microservicio de Productos en Azure:

![terminal-productos-azure](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/azure/terminal-productos-azure.png)
![bzm-productos-azure](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/azure/bzm-productos-azure.png)

## Microservicio Pedidos

![azure-pedidos](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/azure/azure-pedidos.png)

### Rendimiento Pedidos

Microservicio de Pedidos en Azure:

![terminal-pedidos-azure](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/azure/terminal-pedidos-azure.png)
![bzm-pedidos-azure](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/azure/bzm-pedidos-azure.png)

Como se puede observar, el rendimiento en Azure es muy bajo con alrededor de 135 peticiones por segundo y 65ms de tiempo de respuesta medio para ambos
 microservicios. Esto es debido a la latencia que hay por la ubicación del servidor.

## Referencias

[Instalar CLI Azure](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-apt?view=azure-cli-latest)  
[Ver Imagenes](https://docs.microsoft.com/en-us/azure/virtual-machines/linux/cli-ps-findimage)  
[Tipos de máquinas](https://docs.microsoft.com/es-es/azure/azure-resource-manager/templates/error-sku-not-available)  
