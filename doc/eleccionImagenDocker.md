# Elección de la imagen Docker

Para elegir que base utilizaré para mi Dockerfile he realizado un pequeño test con [Apache Benchmark](https://httpd.apache.org/docs/2.4/programs/ab.html). Las pruebas que he realizado son 1000 peticiones con 1 usuario concurrente y 1000 peticiones con 8 usuarios concurrentes. Estos test los he realizado con la BD en [Mongo Atlas](https://www.mongodb.com/cloud/atlas) y en local para comparar los resultados.

**Índice:**

- [Dockerfiles utilizados](#dockerfiles-utilizados)
- [Tests realizados](#tests-realizados)
- [Resultado](#resultado)

## Dockerfiles utilizados

### CentOS

```dockerfile
# Seleccionar imagen padre a partir de la cual se creará
# esta imagen.
FROM centos:centos7

# Indicar el mantenedor de la imagen
LABEL maintainer="toni97sk8@gmail.com"

# Actualizar
RUN yum -y upgrade

# Instalar node
RUN curl -sL https://rpm.nodesource.com/setup_8.x | bash -
RUN yum install nodejs -y

# El puerto y la uri de la base de datos se establecerán como variables de entorno
ENV PORT ${PORT}
ENV DB_URI ${DB_URI}

# Crear un usuario sin permisos de root
RUN useradd -m nonrootuser

# Indicar el usuario a usar al ejecutar la imagen.
USER nonrootuser

# Crear directorio cc-gestionProductos
RUN mkdir /home/nonrootuser/cc-gestionProductos

# Establecer el directorio de trabajo
WORKDIR /home/nonrootuser/cc-gestionProductos

# Copiar exclusivamente los ficheros necesarios
COPY package*.json ./
COPY src/productos/controllers src/productos/controllers
COPY src/productos/models src/productos/models/
COPY src/productos/routes src/productos/routes
COPY app.js ./

# Instalar dependencias
RUN npm ci

# El puerto que se ejecutará por defecto será el 8080
EXPOSE 8080

# Iniciar servicio
# Ejecutar script start indicado en el package.json 
CMD ["npm", "start"]
```

### Alpine

```dockerfile
# Seleccionar imagen padre a partir de la cual se creará
# esta imagen.
FROM node:alpine

# Indicar el mantenedor de la imagen
LABEL maintainer="toni97sk8@gmail.com"

# El puerto y la uri de la base de datos se establecerán como variables de entorno
ENV PORT ${PORT}
ENV DB_URI ${DB_URI}

# Actualizar
RUN apk update

# Establecer el directorio de trabajo
WORKDIR /home/nonrootuser/cc-gestionProductos

# Copiar exclusivamente los ficheros necesarios
COPY package*.json ./
COPY src/productos/controllers src/productos/controllers
COPY src/productos/models src/productos/models/
COPY src/productos/routes src/productos/routes
COPY app.js ./

# Instalar dependecias
RUN npm ci

# El puerto que se ejecutará por defecto será el 8080
EXPOSE 8080

# Crear un usuario sin permisos de root
RUN adduser -D nonrootuser

# Indicar el usuario a usar al ejecutar la imagen.
USER nonrootuser

# Iniciar servicio
# Ejecutar script start indicado en el package.json
CMD npm start
```

![alpine-1-atlas](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/docker/docker-images.png)

Se puede observar que la imagen construida con Alpine es mucho mas liviana.

## Tests realizados

Tests que he realizado:

- [Alpine con 1 usuarios concurrentes y BD en Mongo Atlas](#alpine-con-1-usuarios-concurrentes-y-bd-en-mongo-atlas)
- [Alpine con 8 usuarios concurrentes y BD en Mongo Atlas](#alpine-con-8-usuarios-concurrentes-y-bd-en-mongo-atlas)
- [Alpine con 1 usuarios concurrentes y BD en local](#alpine-con-1-usuarios-concurrentes-y-BD-en-local)
- [Alpine con 8 usuarios concurrentes y BD en local](#alpine-con-8-usuarios-concurrentes-y-BD-en-local)
- [CentOS con 1 usuarios concurrentes y BD en Mongo Atlas](#centos-con-1-usuarios-concurrentes-y-bd-en-mongo-atlas)
- [CentOS con 8 usuarios concurrentes y BD en Mongo Atlas](#centos-con-8-usuarios-concurrentes-y-bd-en-mongo-atlas)
- [CentOS con 1 usuarios concurrentes y BD en local](#centos-con-1-usuarios-concurrentes-y-bd-en-local)
- [CentOS con 8 usuarios concurrentes y BD en local](#centos-con-8-usuarios-concurrentes-y-bd-en-local)

### Alpine con 1 usuarios concurrentes y BD en Mongo Atlas

![alpine-1-atlas](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/ab/salidas/alpine-1-atlas.png)

![grafica-alpine-1-atlas](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/ab/graficas/res-alpine-1-atlas.png)

[Lista tests](#tests-realizados)

### Alpine con 8 usuarios concurrentes y BD en Mongo Atlas

![alpine-8-atlas](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/ab/salidas/alpine-8-atlas.png)

![grafica-alpine-8-atlas](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/ab/graficas/res-alpine-8-atlas.png)

[Lista tests](#tests-realizados)

### Alpine con 1 usuarios concurrentes y BD en local

![alpine-1-local](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/ab/salidas/alpine-1-loc.png)

![grafica-alpine-1-local](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/ab/graficas/res-alpine-1-loc.png)

[Lista tests](#tests-realizados)

### Alpine con 8 usuarios concurrentes y BD en local

![alpine-8-local](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/ab/salidas/alpine-8-loc.png)

![grafica-alpine-8-local](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/ab/graficas/res-alpine-8-loc.png)

[Lista tests](#tests-realizados)

### CentOS con 1 usuarios concurrentes y BD en Mongo Atlas

![centos-1-atlas](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/ab/salidas/centos-1-atlas.png)

![grafica-centos-1-atlas](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/ab/graficas/res-centos-1-atlas.png)

[Lista tests](#tests-realizados)

### CentOS con 8 usuarios concurrentes y BD en Mongo Atlas

![centos-8-atlas](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/ab/salidas/centos-8-atlas.png)

![grafica-centos-8-atlas](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/ab/graficas/res-centos-8-atlas.png)

[Lista tests](#tests-realizados)

### CentOS con 1 usuarios concurrentes y BD en local

![centos-1-local](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/ab/salidas/centos-1-loc.png)

![grafica-centos-1-local](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/ab/graficas/res-centos-1-loc.png)

[Lista tests](#tests-realizados)

### CentOS con 8 usuarios concurrentes y BD en local

![centos-8-local](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/ab/salidas/centos-8-loc.png)

![grafica-centos-8-local](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/ab/graficas/res-centos-8-loc.png)

[Lista tests](#tests-realizados)

## Resultado

Se puede observar que hay una gran diferencia entre usar la BD en local frente a usarla en Mongo Atlas.

Como se puede observar en las imágenes anteriores para 8 usuarios concurrentes, 1000 peticiones y la BD en local:

- **Alpine**: 2066.95 peticiones por segundo
- **CentOS**: 1830.09 peticiones por segundo

Cada vez que se ejecuta los tests varían esos resultados, pero siempre obtienen unos resultados parecidos entre CentOS y Alpine.

Por lo que al tener un rendimiento muy parecido y ser Alpine una imagen más liviana usaré esa.
