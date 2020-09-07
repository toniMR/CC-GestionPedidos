FROM node:8.17-alpine

# Establecer variables de entorno para acceder a la Base de datos
ENV DB_URI ${DB_URI}

# Actualizar y añadir ususario nonrootuser
RUN apk update \
    && adduser -D nonrootuser

# Establecer el directorio de trabajo
WORKDIR /home/nonrootuser/cc-gestionProductos

# Copiar archivos
COPY package*.json ./
COPY src/productos src/productos

# Instalar dependencias
RUN npm ci

# Usar el usuario nonrootuser creado
USER nonrootuser

# Iniciar aplicación
CMD npm start