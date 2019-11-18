/*
    Esta clase será la encargada de modelar y gestionar
    los productos.
*/

class Producto{
    constructor(id, nombre, descripcion, categorias, precio, stock){
        this.id = id;
        this.nombre = nombre;
        this.descripcion = descripcion;
        this.categorias = categorias;
        this.precio = precio;
        this.stock = stock;
    }

    setNombre(nombre){
        this.nombre = nombre;
    }

    setDescripcion(descripcion){
        this.descripcion = descripcion;
    }

    setCategorias(categorias){
        this.categorias = categorias;
    }

    setPrecio(precio){
        this.precio = precio;
    }

    setStock(stock){
        this.stock = stock;
    }

    getNombre(){
        return this.nombre;
    }

    getDescripcion(){
        return this.descripcion;
    }

    getCategorias(){
        return this.categorias;
    }

    getPrecio(){
        return this.precio;
    }

    getStock(){
        return this.stock;
    }

    toString(){
        var categoriasString = "";
        this.categorias.forEach(function(value){
            categoriasString += value + ", ";
        });
        var str = "ID: " + this.id + "\n" +
        "Nombre: " + this.nombre + "\n" +
        "Descripción: " + this.descripcion + "\n" +
        "Categorías: " +  categoriasString+ "\n" +
        "Precio: " + this.precio + " €\n" +
        "Stock: " + this.stock + "\n";

        return str;
    }
}

module.exports = Producto;
