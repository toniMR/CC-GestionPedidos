const mongoose = require('mongoose');
const Schema = mongoose.Schema;

let pedidoSchema = new Schema({
    nombre: {type: String, required: true},
    descripcion: {type: String, required: true},
    categoria: {type: String, required: true},
    precio: {type: Number, multipleOf: 0.01},
    stock: {type: Number, min: 0, required: true}
})