
# Despliegue en Heroku

Para desplegar el microservicio en Heroku, tras iniciar sesión en Heroku debemos crear una aplicación:  

![crear-aplicacion-heroku](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/heroku/create_app.png)

Una vez creada la aplicación se conecta al repositorio de GitHub:  

![conectar-repositorio-heroku](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/heroku/conexión.png)

Se esccoge el buildpack del lenguaje usado en la implementación del microservicio. En mi caso en Heroku voy a desplegar el microservicio de productos implementado en Node.js.  

![buildpack-heroku](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/heroku/buildpack.png)  
Establecer las variables de entorno necesarias. En mi caso he establecido la variable PORT y DB_URI para establecer la dirección de la BD.

![heroku-variables-entorno](https://github.com/toniMR/CC-GestionPedidos/blob/master/doc/img/heroku/env_vars.png)

Después será necesario crear un archivo **heroku.yml**:  

```yaml
# Indicar que se utilizará el Dockerfile
build:
    docker:
      web: Dockerfile
# Se ejecutará la orden CMD indicada en el Dockerfile
```

De esta forma se le indicará a Heroku que lo que tiene que desplegar es un Dockerfile.  

## Referencias

[Documentación Heroku](https://devcenter.heroku.com/articles/getting-started-with-nodejs)

[Documentación Heroku 2](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml)
