
# Seleccionar imagen padre a partir de la cual se creará
# esta imagen. node:alpine es la más liviana (~5MB).
# (https://hub.docker.com/_/node/)
FROM node:alpine

# Indicar el mantenedor de la imagen
LABEL maintainer="toni97sk8@gmail.com"

# El puerto y la uri de la base de datos se establecerán como variables de entorno
ENV PORT ${PORT}
ENV DB_URL ${DB_URL}

# Establecer el directorio de trabajo
WORKDIR /home/nonrootuser/cc-gestionProductos

# Crear un usuario sin permisos de root
RUN adduser -D nonrootuser \
    # Instalar mongoDB
    && echo 'http://dl-cdn.alpinelinux.org/alpine/v3.6/main' >> /etc/apk/repositories \
    && echo 'http://dl-cdn.alpinelinux.org/alpine/v3.6/community' >> /etc/apk/repositories \
    && apk add mongodb \
    # Instalar directorio para la bd de mongo para nonrootuser
    && mkdir -p /home/nonrootuser/mongodb/database /home/nonrootuser/mongodb/log \
    && chown -R nonrootuser:nonrootuser /home/nonrootuser/mongodb 
    
# Copiar exclusivamente los ficheros necesarios
COPY package*.json ./
COPY src/productos/controllers src/productos/controllers
COPY src/productos/models src/productos/models/
COPY src/productos/routes src/productos/routes
COPY src/productos/productos-rest.js src/productos/

# Instalar dependecias
# Al haber usado RUN, se instalarán al construir la imagen
RUN npm ci

# El puerto que se ejecutará por defecto será el 8080
# para especificar otro puerto se tendrá que indicar al
# lanzar la imagen con:
# docker run -t -i -e PORT=<puerto_deseado> -e DB_URL=<uri_a_bd> <ImageID>
EXPOSE 8080

# Indicar el usuario a usar al ejecutar la imagen.
USER nonrootuser

# Iniciar servicio
# Ejecutar script start indicado en el package.json 
CMD mongod --fork --logpath ~/mongodb/log/mongodb.log --dbpath ~/mongodb/database \
    & npm start


# NOTAS: 
#       1) 
#         Hay que indicar la uri en la que está establecida
#         la BD de MongoDB.
#           docker run -t -i -e DB_URL=<uri_a_bd> <ImageID>
#
#       2)
#         Cambiar el puerto que usará docker:
#           docker run -t -e PORT=<puerto_deseado> -e DB_URL=<uri_a_bd> <ImageID>
# 
#       3)
#         Para mapear el puerto de docker al host se hace con:
#           docker run -t -i -e PORT=<puerto_en_docker> -e DB_URL=<uri_a_bd> -p <puerto_host>:<puerto_en_docker> <ImageID>