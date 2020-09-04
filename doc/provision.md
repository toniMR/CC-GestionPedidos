# Provisión

Para crear la máquina primero debe crear 2 ficheros .env en la raiz del proyecto. El fichero .env_productos, necesario
para el microservicio de productos:

```ini
DB_URI=<URI a BD de MongoDB>
```

(Si se deseea que se ejecute en la BD local del dockerfile que se está ejecutando en la máquina indicar `mongodb://localhost:27017/productos`)

El fichero .env_productos, necesario para el microservicio de pedidos:

```ini
DB_USERNAME=<username>
DB_PASSWORD=<password>
DB_NAME=<bd_name>
GUNI_HOSTS=<host_gunicorn>
GUNI_PORT=<port_gunicorn>
WORKERS=<n_workers>
```

Un ejemplo podría ser:

```ini
DB_USERNAME=usuario
DB_PASSWORD=contraseña
DB_NAME=ms_pedidos
GUNI_HOSTS=0.0.0.0
GUNI_PORT=8000
WORKERS=2
```

**Crear la máquina en local:**

Una vez se han creado estos archivos .env. Ejecutar desde **./provision/local/**:

```bash
    vagrant up
```

**Crear la máquina en Azure:**

Primero hay que exportar las siguientes variables de entorno, como se explica en [Provisionar máquinas de Azure con Vagrant](/doc/azure.md):

```bash
    export AZURE_TENANT_ID=<tenant>
    export AZURE_CLIENT_ID=<appId>
    export AZURE_CLIENT_SECRET=<password>
    export AZURE_SUBSCRIPTION_ID=<id>
```

Después, desde la ruta **./provision/azure/**:

```bash
    vagrant up
```

Entre en la sección [Provisionamiento de Máquinas Virtuales](/doc/provisionamiento.md) para ver más documentación sobre como
se ha realizado el provisionamiento de máquinas virtuales.
