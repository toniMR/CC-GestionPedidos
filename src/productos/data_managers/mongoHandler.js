/*
    Esta clase se encargará de manejar las operaciones
    con la Base de Datos utilizando MongoDB.
*/

const mongoose = require('mongoose')
const Producto = require('../models/producto_model')


class MongoHandler{

    constructor(){};

    
    // Iniciar conexión con la base de datos
    connect(DB_URI){
        mongoose.connect(DB_URI, {useNewUrlParser: true, useUnifiedTopology: true, useFindAndModify: false})
            .then(()=> console.log('Conectado a la BD'))
            .catch(erro => console.log('No se pudo conectar a la BD'))
    }


    // Obtener todos los productos
    getProducts(){
        return Producto.find();
    }


    // Obtener el producto identificado por su _id
    getProduct(product_id){
        return Producto.findById(product_id);
    };


    // Obtener productos en un rango de precio
    getProductsPriceRange (price_min, price_max){
        return Producto.find({precio: { $gt: price_min, $lt: price_max }});
    };


    // Obtener productos pertenecientes a ciertas categorias
    getProductsWithCategories (categories) {
        return Producto.find({categorias: { $all: categories}});
    }


    // Obtener productos que contengan un texto
    getProductsWithText (text) {
        return Producto.find({$text: { $search: text.toString() }});
    }


    // Insertar producto
    insertProduct (product_dict){
        const new_product = new Producto({
            _id: product_dict._id,
            nombre: product_dict.nombre,
            descripcion: product_dict.descripcion,
            categorias: product_dict.categorias,
            precio: product_dict.precio,
            stock: product_dict.stock
        })
        return new_product.save();
    };


    // Editar producto
    editProduct (product, product_dict){
        return product.updateOne({
                                    "nombre": product_dict.nombre,
                                    "descripcion": product_dict.descripcion,
                                    "categorias": product_dict.categorias,
                                    "precio": product_dict.precio,
                                    "stock": product_dict.stock
                                });
    }


    // Eliminar producto identificado por su _id
    deleteProduct (product_id){
        return Producto.findByIdAndDelete(product_id)
    };
}


module.exports = MongoHandler;
