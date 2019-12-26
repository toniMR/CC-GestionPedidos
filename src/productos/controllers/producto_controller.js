
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


// Editar producto
exports.editProduct = async function(req, res){
    const product = await Producto.findById(req.params._id);

    // Si existe el producto, se actualiza
    if(product){
        const result = await product.updateOne({
                                                "_id": req.body._id,
                                                "nombre": req.body.nombre,
                                                "descripcion": req.body.descripcion,
                                                "categorias": req.body.categorias,
                                                "precio": req.body.precio,
                                                "stock": req.body.stock
                                            });
        return res.status(200).send(result);
    }
    // No existe un producto con ese id
    else{
        return res.status(404).send('No existe un producto con ese id');
    }
}

// Eliminar producto identificado por su _id
exports.deleteProduct = async function(req, res){
    const product = await Producto.findByIdAndDelete(req.params._id)

    // Si existe el producto se elimina
    if (product)
        return res.status(200).send('Producto borrado')
    else{
        return res.status(404).send('No existe un producto con ese id');
    }
};
