const express = require ('express')
const mongoose = require('mongoose')
const productoRouter = require('./src/productos/routes/producto_routes.js');

const app = express();

// Variables de entorno para configurar el puerto y la URI a 
const PORT = process.env.PORT || 8080
const DB_URI = process.env.DB_URI

// Escuchar en el puerto PORT
const server = app.listen(PORT, ()=> console.log('Escuchando puerto: ' + PORT));

// Configurar 
app.use(express.json());
app.use(express.urlencoded({extended:true}));
app.use(productoRouter);

// Iniciar conexión con la base de datos
mongoose.connect(DB_URI, {useNewUrlParser: true, useUnifiedTopology: true, useFindAndModify: false})
    .then(()=> console.log('Conectado a la BD'))
    .catch(erro => console.log('No se pudo conectar a la BD'))


/*
    Exporto la aplicación y la variable server. La 
    variable server la utilizaré en test_api.js para 
    poder cerrar la conexión de la aplicación
*/
module.exports = {
                    app: app,
                    server: server
                };
