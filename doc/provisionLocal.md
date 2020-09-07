# Provisión Local

Para crear la máquina virtual en local haremos uso de Vagrant y Ansible.

## Vagrant en local

```vagrantfile
# Este fichero sirve para crear en local la máquina virtual que alojará ambos
# microservicios:

Vagrant.configure("2") do |config|
  # Como imagen utilizaremos el box de Ubuntu 18.04 LTS:
  config.vm.box = "ubuntu/bionic64"
  # Redirigimos los puertos de la máquina anfitriona a la máquina virtual:
  config.vm.network "forwarded_port", guest: 22, host:2222
  config.vm.network "forwarded_port", guest: 80, host: 8080

  config.vm.define "gp_local" do |gestionpedidos|
    gestionpedidos.vm.provision "ansible" do |ansible|
        # ansible.verbose = 'vvv'
        ansible.playbook = "./playbook-local.yml"
    end


    # Especificamos la memoria que utilizará y el número de cores: 4GB y 4 cores lógicos
    config.vm.provider "virtualbox" do |v|
        v.memory = 4096
        v.cpus = 4
    end
  end
end
```

## Ansible

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

## Microservicio Productos

![local-productos](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/local/provision-local-productos.png)

### Rendimiento Productos

Microservicio de Productos en local:

![terminal-productos-local](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/local/provision-terminal-productos-local.png)
![bzm-productos-local](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/local/provision-bzm-productos-local.png)

## Microservicio Pedidos

![local-pedidos](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/local/provision-local-pedidos.png)

### Rendimiento Pedidos

Microservicio de Pedidos en local:

![terminal-pedidos-local](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/local/provision-terminal-pedidos-local.png)
![bzm-pedidos-local](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/provisionamiento/local/provision_bzm-pedidos-local.png)

