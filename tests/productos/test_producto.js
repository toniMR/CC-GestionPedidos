/*
    Esta clase será la encargada de testear la clase Producto
*/

var Producto = require('../../src/productos/classes/producto')

var assert = require('assert');

// Test para la creación de un producto
describe('Producto', function(){

    var producto = new Producto("LAM2", "Lampara AM 2", "Lampara amarilla de 2 bombillas", ["muebles", "iluminacion", "hogar"], 27, 30)

    // Testear la inclusión del módulo producto
    describe('Test tipo', function(){
        it('Debe ser del tipo Producto', function(){
            assert.equal(producto instanceof Producto, true,  "Tipo correcto");
        });
    });

    // Testear la creación correcta de un producto
    describe("Test creación correcta", function(){
        it('Debe devolver el nombre', function(){
            assert.equal(producto.getNombre(), "Lampara AM 2", "Nombre devuelto correctamente");
        });

        it('Debe devolver la descripción', function(){
            assert.equal(producto.getDescripcion(), "Lampara amarilla de 2 bombillas", "Descripción devuelta correctamente");
        });

        it('Debe devolver las categorías', function(){
            assert.deepEqual(producto.getCategorias(), ["muebles", "iluminacion", "hogar"], "Categorías devueltas correctamente");
        });

        it('Debe devolver el precio', function(){
            assert.equal(producto.getPrecio(), 27, "Precio devuelto correctamente");
        });

        it('Debe devolver el stock', function(){
            assert.equal(producto.getStock(), 30, "Stock devuelto correctamente");
        });
    });


    // Testear los modificadores
    describe("Modificación correcta", function(){

        it('Debe modificar el nombre', function(){
            var producto2 = new Producto("LAM2", "Lampara AM 2", "Lampara amarilla de 2 bombillas", ["muebles", "iluminacion", "hogar"], 27, 30)
            producto2.setNombre("Foco")
            assert.equal(producto2.getNombre(), "Foco", "Nombre modificado correctamente");
        });

        it('Debe modificar la descripción', function(){
            var producto2 = new Producto("LAM2", "Lampara AM 2", "Lampara amarilla de 2 bombillas", ["muebles", "iluminacion", "hogar"], 27, 30)
            producto2.setDescripcion("Foco grande negro")
            assert.equal(producto2.getDescripcion(), "Foco grande negro", "Descripcion modificada correctamente");
        });

        it('Debe modificar las categorias', function(){
            var producto2 = new Producto("LAM2", "Lampara AM 2", "Lampara amarilla de 2 bombillas", ["muebles", "iluminacion", "hogar"], 27, 30)
            producto2.setCategorias(["iluminacion"])
            assert.deepEqual(producto2.getCategorias(), ["iluminacion"], "Categorías modificadas correctamente");
        });

        it('Debe modificar el precio', function(){
            var producto2 = new Producto("LAM2", "Lampara AM 2", "Lampara amarilla de 2 bombillas", ["muebles", "iluminacion", "hogar"], 14, 30)
            producto2.setPrecio(19)
            assert.equal(producto2.getPrecio(), 19, "Precio modificado correctamente");
        });

        it('Debe modificar el stock', function(){
            var producto2 = new Producto("LAM2", "Lampara AM 2", "Lampara amarilla de 2 bombillas", ["muebles", "iluminacion", "hogar"], 14, 30)
            producto2.setStock(29)
            assert.equal(producto2.getStock(), 29, "Stock modificado correctamente");
        });
    });
    

    // Testear el método toString()
    describe("Test método toString()", function(){
        it('Debe mostrar toda la información del producto', function(){
            var str = "ID: " + "LAM2\n" +
                        "Nombre: " + "Lampara AM 2\n" +
                        "Descripción: " + "Lampara amarilla de 2 bombillas\n" +
                        "Categorías: " + "muebles, iluminacion, hogar, \n" +
                        "Precio: " + "27 €\n" +
                        "Stock: " + "30\n"
            assert.equal(producto.toString(), str, "String formado correctamente");
        });
    });
});
