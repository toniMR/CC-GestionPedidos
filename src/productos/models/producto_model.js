const mongoose = require('mongoose');

const productoSchema = new mongoose.Schema({
    _id: {type: String, required: true},
    nombre: {type: String, required: true},
    descripcion: {type: String, required: true},
    categorias: [{type: String, required: true}],
    precio: {type: Number, multipleOf: 0.01},
    stock: {type: Number, min: 0, required: true}
})

const Producto = mongoose.model('Producto', productoSchema);

module.exports = Producto;