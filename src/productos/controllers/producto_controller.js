
const Producto = require('../models/producto_model')


// Obtener todos los productos
exports.productsData = async function(req, res){
    try{
        const products = await Producto.find()

        res.status(200).send(products)
    }catch(error){
        return res.status(404).json({'mensaje':'Error:' + error});
    }
};


// Obtener el producto identificado por su _id
exports.productData = async function(req, res) {
    try{
        const product = await Producto.findById(req.params._id)

        if (product){
            return res.status(200).send(product);
        }
        else{
            return res.status(404).json({'mensaje':'No existe un producto con ese id'});
        }
    }catch(error){
        return res.status(404).json({'mensaje':'Error:' + error});
    }
};


// Obtener productos en un rango de precio
exports.productsPriceRange = async function(req, res) {
    try{
        // Parsear parametros a enteros
        const precio_min = parseInt(req.params.precio_min, 10);
        const precio_max = parseInt(req.params.precio_max, 10);

        // Comprobar que son enteros
        if (!isNaN(precio_min) && !isNaN(precio_max)){
            // Obtener array de productos en ese rango de precio
            const products = await Producto.find({precio: { $gt: precio_min, $lt: precio_max }})
            // Ha encontrado productos
            if (products.length > 0){
                return res.status(200).send(products);
            }
            else{
                return res.status(404).json({'mensaje':'No hay productos en ese rango de precio'});
            }
        // No son enteros
        }else{
            throw ("Debe especificar numeros enteros");
        }
    // Hubo algún error
    }catch(error){
        return res.status(400).json({'mensaje':'Error: ' + error});
    }
};


// Obtener productos pertenecientes a ciertas categorias
exports.productsCategories = async function(req, res) {
    try{
        // Obtener categorias
        var categorias_split = (req.params.categorias).split(",");
        var categorias = []
        for (var i=0; i<categorias_split.length; i++){
            categorias.push(categorias_split[i].toLowerCase());
        }
        // Obtener array de productos que estén en esas categorias
        const products = await Producto.find({categorias: { $all: categorias}});
        // Ha encontrado productos
        if (products.length > 0){
            return res.status(200).send(products);
        }
        else{
            return res.status(404).json({'mensaje':'No hay productos que pertenezcan a todas esas categorias'});
        }
    }catch(error){
        return res.status(400).json({'mensaje':'Error: ' + error});
    }
}


// Obtener productos que contengan un texto
exports.productsText = async function(req, res) {
    try{
        // Obtener palabras
        const texto = (req.params.texto).split(",");
        // Obtener array de productos que contengan esas palabras
        const products = await Producto.find({$text: { $search: texto.toString() }});
        // Ha encontrado productos
        if (products.length > 0){
            return res.status(200).send(products);
        }
        else{
            return res.status(404).json({'mensaje':'No hay productos que contengan esas palabras'});
        }
    }catch(error){
        return res.status(400).json({'mensaje':'Error: ' + error});
    }
}


// Insertar producto
exports.insertProduct = async function(req, res){
    try{
        // Buscar si existe un producto con ese _id
        const product = await Producto.findById(req.body._id)

        // Si existe
        if (product){
            return res.status(400).json({'mensaje':'Ya existe un producto con ese id'});
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
    }catch(error){
        return res.status(404).json({'mensaje':'Error: ' + error});
    }
    
};

// Editar producto
exports.editProduct = async function(req, res){
    try{
        const product = await Producto.findById(req.params._id);

        // Si existe el producto, se actualiza
        if(product){
            const result = await product.updateOne({
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
            return res.status(404).json({'mensaje':'No existe un producto con ese id'});
        }
    }catch(error){
        return res.status(404).json({'mensaje':'Error: ' + error});
    }
}


// Eliminar producto identificado por su _id
exports.deleteProduct = async function(req, res){
    try{
        const product = await Producto.findByIdAndDelete(req.params._id)

        // Si existe el producto se elimina
        if (product){
            return res.status(200).json({'mensaje':'Producto borrado'});
        }
        else{
            return res.status(404).json({'mensaje':'No existe un producto con ese id'});
        }
    }catch(error){
        return res.status(404).json({'mensaje':'Error: ' + error});
    }
};
