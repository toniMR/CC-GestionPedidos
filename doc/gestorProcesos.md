# Gestor de Procesos

## Microservicio Gestor Productos

El gestor de procesos escogido para este microservicio implementado con Node.js y Express ha sido **pm2** por su uso tan sencillo.

### Instalación

```bash
npm install pm2 -g
```

```bash
npm install pm2 --save
```

### Uso

Listar procesos:

```bash
pm2 list
```

Ejecutar aplicación:

```bash
pm2 start app.js
```

Detener aplicación:

```bash
pm2 stop <id_proceso>
```

Reiniciar aplicación:

```bash
pm2 restart <id_proceso>
```

Ejecutar aplicación con varias instancias:

```bash
pm2 start app.js -i max
```

**max:** se encargará de desplegar todas las instancias posibles.

Para ejecutar pm2 en [Heroku](https://dashboard.heroku.com) hay que usar pm2-runtime en vez de pm2 para que funcione.  
La diferencia es que pm2-runtime ejecuta los procesos en foreground mientras que pm2 lo hace en background.

## Referencias

- [Documentación pm2](https://www.npmjs.com/package/pm2)
- [Integrar pm2 con Heroku](https://pm2.keymetrics.io/docs/integrations/heroku/)
