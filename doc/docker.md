# Docker

**Índice**:

- [Dockerfile](#dockerfile)
- [Docker Hub](#docker-hub)
- [Uso](#uso)
- [Referencias](#referencias)

## Dockerfile

Este es el Dockerfile utilizado para el microservicio de productos:  

```dockerfile
# Seleccionar imagen padre a partir de la cual se creará
# esta imagen. node:alpine es la más liviana (~5MB).
# (https://hub.docker.com/_/node/)
FROM node:alpine

# Indicar el mantenedor de la imagen
LABEL maintainer="toni97sk8@gmail.com"

# El puerto y la uri de la base de datos se establecerán como variables de entorno
ENV PORT ${PORT}
ENV DB_URI ${DB_URI}

# Establecer el directorio de trabajo
WORKDIR /home/nonrootuser/cc-gestionProductos

# Copiar exclusivamente los ficheros necesarios
COPY package*.json ./
COPY src/productos/controllers src/productos/controllers
COPY src/productos/models src/productos/models/
COPY src/productos/routes src/productos/routes
COPY app.js ./

# Instalar dependecias
# Al haber usado RUN, se instalarán al construir la imagen
RUN npm ci

# Indicar que el puerto que se ejecutará por defecto será el 8080
EXPOSE 8080

# Crear un usuario sin permisos de root
RUN adduser -D nonrootuser

# Indicar el usuario a usar al ejecutar la imagen.
USER nonrootuser

# Iniciar servicio
# Ejecutar script start indicado en el fichero package.json
CMD npm start
```

Puede consultar la [prueba de eleccion de la imagen base](eleccionImagenDocker.md) para ver las pruebas realizadas para escoger la imagen base.

Se puede observar el uso de las siguientes reglas:

- **FROM:** Indica cual será la imagen base sobre la que se construirá el dockerfile.
- **LABEL:** Añade metadatos a la imagen.
- **ENV:** Crea variables de entorno.
- **WORKDIR:** Establece el directorio de trabajo.
- **COPY:** Copia ficheros.
- **RUN:** Ejecuta comandos en tiempo de construcción.
- **EXPOSE:** Indica a modo informativo el puerto en el que escucha el contenedor.
- **USER:** Indica el usuario que se usará al ejecutar la imagen.
- **CMD:** Comando que ejecutará el contenedor por defecto al ejecutarse.  

## Docker Hub

Para subir la imagen a [docker hub](https://hub.docker.com/) hay que realizar los siguientes pasos:

- Iniciar sesión.
- Crear un repositorio y enlazarlo a un repositorio de GitHub.  

![crear-repositorio](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/docker/crear-repositorio.png)  

- Automatizar la construcción de la imagen.

![construccion-automática](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/docker/automated-build.png)  

## Uso

### Construir la imagen en local

Desde el directorio en el que se encuentra el dockerfile hacer:

```bash
docker build -t node-productos .
```

### Construir la imagen con docker hub

```bash
docker pull tonimr/cc-gestion-productos:latest
```

### Ejecutar la imagen

- Para ejecutar la imagen con el puerto por defecto:

```bash
docker run -e DB_URL=<uri_a_bd> -t <tag_imagen>
```

- Para ejecutar la imagen con otro puerto:  

```bash
docker run -e PORT=<puerto_deseado> -e DB_URL=<uri_a_bd> -t <tag_imagen>
```

- Para mapear el puerto de docker a otro en el host:

```bash
docker run -e PORT=<puerto_en_docker> -e DB_URL=<uri_a_bd> -p <puerto_host>:<puerto_en_docker> -t <tag_imagen>
```

- En caso de que se quiera utilizar una BD en local utilizar:

```bash
docker run -e DB_URI=<uri_a_bd> -e PORT=<puerto_deseado> --network="host" -t <tag_imagen>
```

**--network="host"** hace que los servicios que se ejecuten en el contenedor docker se ejecuten en la red del host. Lo ideal sería que solo redirigiera el puerto necesario para el servicio de la BD establecida en el host pero no lo conseguía. Esto lo cambiaré más adelante.  

La DB_URI debería ser, por ejemplo: "mongodb://localhost:27017/productos"

## Referencias

[Dockerfile reference](https://docs.docker.com/engine/reference/builder/)  

[Host networking](https://docs.docker.com/network/host/)
