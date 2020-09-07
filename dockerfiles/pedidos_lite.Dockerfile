FROM python:3.6-alpine


# Indicar el mantenedor de la imagen
LABEL maintainer="toni97sk8@gmail.com"

# Establecer variables de entorno para acceder a la Base de datos
ENV DB_HOST ${DB_HOST}
ENV DB_PORT ${DB_PORT}
ENV DB_USERNAME ${DB_USERNAME}
ENV DB_PASSWORD ${DB_PASSWORD}
ENV DB_NAME ${DB_NAME}
ENV GUNI_HOST ${GUNI_HOST}
ENV GUNI_PORT ${GUNI_PORT}

# Actualizar y añadir ususario nonrootuser
RUN apk update \
    && adduser -D nonrootuser \
    # Instalar dependencias de psycopg2
    && apk add gcc musl-dev python3-dev postgresql-dev

# Establecer el directorio de trabajo
WORKDIR /home/nonrootuser/cc-gestionProductos

# Copiar archivos
COPY setup.py ./
COPY src/pedidos src/pedidos

# Instalar dependencias
# Hay que instalar setuptools  y wheel porque no está instalado por defecto
# y es necesario para usar setup.py
RUN pip3 install --upgrade wheel \
    && pip3 install --upgrade setuptools \
    && pip3 install . 

# Usar el usuario postgres creado por defecto al instalar postgresql
USER nonrootuser

# Iniciar microservicio
CMD cd src \
    && gunicorn -w ${WORKERS} -b ${GUNI_HOST}:${GUNI_PORT} 'pedidos:create_app()'

