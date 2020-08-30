const express = require('express')
const productoRouter = require('./routes/producto_routes.js');
const container = require ('./container/container.js')


// Variables de entorno para configurar el puerto y la URI a la BD
const PORT = process.env.PORT || 8080
const DB_URI = process.env.DB_URI


// Inversión de dependencias
// ---------------------------------------------------------------
// Establecer dependencias
const db_handler = container.get('DBHandler')
// ---------------------------------------------------------------


// Configurar aplicación
const app = express();

// Escuchar en el puerto PORT
const server = app.listen(PORT, ()=> console.log('Escuchando puerto: ' + PORT));

app.use(express.json());
app.use(express.urlencoded({extended:true}));
app.use(productoRouter);


// Iniciar conexión con la base de datos
db_handler.connect(DB_URI);

/*
    Exporto la aplicación y la variable server. La 
    variable server la utilizaré en test_api.js para 
    poder cerrar la conexión de la aplicación
*/
module.exports = {
                    app: app,
                    server: server
                };
