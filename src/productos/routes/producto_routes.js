/*
    Se encargará de comunicar que operación se ejecutará
    en esa ruta
*/

const express = require('express');
const router = express.Router();

// Controller module
const producto_controller = require ('../controllers/producto_controller.js');


// ruta /
router.get('/', async function(req, res){
    return res.status(200).send({status: "OK"});
});

// ruta /status
router.get('/status', async function(req, res){
    return res.status(200).send({status: "OK"});
});


// Rutas para el producto

// GET todos los productos
router.get('/productos', producto_controller.productsData);

// GET un producto concreto (por su id)
router.get('/productos/:_id', producto_controller.productData);

// GET productos que contengan una palabra clave en su nombre o descripción
router.get('productos/:palabra', producto_controller.productDataWord);

// GET productos en un rango de precio
//router.get('/productos/min/:min/max/:max',      );

// GET productos que pertenezcan a una categoría
//router.get('/productos/categoria/:categoria',      );


// POST producto
router.post('/productos', producto_controller.insertProduct);

// PUT producto
router.put('/productos/:_id', producto_controller.editProduct);

// DELETE producto
router.delete('/productos/:_id',producto_controller.deleteProduct);



module.exports = router;
