
var productoRouter = require('./src/productos/routes/producto_routes.js');
var express = require ('express')
var app = express();

// Escuchar en el puerto 8080
app.listen(8080);

app.use(productoRouter);


module.exports = app;
