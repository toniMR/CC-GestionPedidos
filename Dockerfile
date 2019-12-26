
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
