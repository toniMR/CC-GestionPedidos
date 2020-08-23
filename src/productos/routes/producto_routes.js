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

// GET productos en un rango de precio
router.get('/productos/precio/min/:precio_min/max/:precio_max', producto_controller.productsPriceRange);

// GET productos pertenecientes a varias categorias
router.get('/productos/categorias/:categorias', producto_controller.productsCategories);

// POST producto
router.post('/productos', producto_controller.insertProduct);

// PUT producto
router.put('/productos/:_id', producto_controller.editProduct);

// DELETE producto
router.delete('/productos/:_id',producto_controller.deleteProduct);


module.exports = router;
