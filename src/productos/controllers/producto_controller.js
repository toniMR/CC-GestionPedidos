
var Producto = require('../models/producto_model');

exports.product_data = function(req, res) {
    res.send('NOT IMPLEMENTED: Product data');
};

exports.products_data = function(req, res) {
    res.send('NOT IMPLEMENTED: All products data');
};

exports.product_data_word = function(req, res) {
    res.send('NOT IMPLEMENTED: Product with a word');
};

// Insertar producto
exports.insertProduct = async function(req, res){

    // Buscar si existe un producto con ese _id
    const product = await Producto.findById(req.body._id)

    // Si existe
    if (product){
        return res.status(400).send('Ya existe un producto con ese id');
    }
    // Si no existe se puede insertar el producto
    else{
        const new_product = new Producto({
            _id: req.body._id,
            nombre: req.body.nombre,
            descripcion: req.body.descripcion,
            categorias: req.body.categorias,
            precio: req.body.precio,
            stock: req.body.stock
        })

        // Guardar el producto en la base de datos
        const result = await new_product.save();

        // Enviar estado 201 y enviar el producto como respuesta
        return res.status(201).send(result);
    }
};
