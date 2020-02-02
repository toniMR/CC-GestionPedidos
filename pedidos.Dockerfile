FROM bitnami/minideb:latest

# Indicar el mantenedor de la imagen
LABEL maintainer="toni97sk8@gmail.com"

# El usuario, contraseña, host, puerto y nombre de la base de datos para acceder a la base de datos datos se establecerán como variables de entorno
ENV DB_HOST ${DB_HOST}
ENV DB_PORT ${DB_PORT}
ENV DB_USERNAME ${DB_USERNAME}
ENV DB_PASSWORD ${DB_PASSWORD}
ENV DB_NAME $DB_NAME
ENV GUNI_HOST $GUNI_HOST
ENV GUNI_PORT ${GUNI_PORT}


# Instalar dependencias
RUN apt update && apt upgrade && apt-get install -y gnupg2 \
    # Instalar python3
    && install_packages python3 python3-pip python3-dev \
    && echo "deb  http://deb.debian.org/debian  stretch main"  >> /etc/apt/sources.list \
    && echo "deb-src  http://deb.debian.org/debian  stretch main" >> /etc/apt/sources.list \
    && apt  update \
    # Instalar postgresql
    && apt install wget -y \
    && apt install postgresql -y \
    # Instalar dependencias de psycopg2
    && apt install libpq-dev -y \
    && apt install gcc -y \
    # Crear un usuario sin permisos de root
    && useradd -m nonrootuser

# Establecer el directorio de trabajo
WORKDIR /home/nonrootuser/cc-gestionProductos

# Copiar archivos
COPY setup.py ./
COPY src/pedidos/pedido.py src/pedidos/
COPY src/pedidos/gestorPedidos.py src/pedidos/
COPY src/pedidos/pedido_schema.py src/pedidos/
COPY src/pedidos/data_managers/* src/pedidos/data_managers/
COPY src/pedidos/pedidos_rest.py ./src/pedidos/

# Instalar dependencias
# Hay que instalar setuptools  y wheel porque no está instalado por defecto
# y es necesario para usar setup.py
RUN pip3 install --upgrade wheel \
    && pip3 install --upgrade setuptools \
    && pip3 install . 

# Usar el usuario postgres creado por defecto al instalar postgresql
USER postgres

# Al ejecutar la imagen se iniciará el servicio de postgres, se creará un rol de 
# postgres llamado <USERNAME> con contraseña <PASSWORD>  y se inciará la aplicación con
# start definido en setup.py, en el que inicia la aplicación con gunicorn.
CMD /etc/init.d/postgresql start \
    && psql --command "CREATE USER ${DB_USERNAME} WITH PASSWORD '${DB_PASSWORD}';" \
    && createdb -O ${DB_USERNAME} ${DB_NAME} \
    # No puedo utilizar python3 setup.py start porque me da error
    # python3 setup.py start -w 8 --host=${GUNI_HOST} -p {GUNI_PORT}
    && cd src/pedidos \
    && gunicorn -w ${WORKERS} -b ${GUNI_HOST}:${GUNI_PORT} pedidos_rest:app
