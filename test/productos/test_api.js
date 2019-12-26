
const Producto = require('../../src/productos/classes/producto');
const app = require('../../app');
const supertest = require('supertest');
const mongoose = require('mongoose')
const chai = require('chai');


// Test para la creación de un producto
describe('Test API', function(){

    /*
       Con after, cuando se ejecuten todos los tests se 
       borrará la base de datos usada para los tests,
       se cerrará la conexión con la BD y la aplicación.
    
       NOTA: Si no se cierra la conexión con la aplicación
       tras pasar los tests se queda ejecutándose y no 
       pasa a realizar la cobertura. Para cerrar la conexión de 
       la aplicación hay que cerrar también la conexión con la BD. 
    */
    after(function (){
        mongoose.connection.db.dropDatabase()
        mongoose.connection.close();
        app.server.close();
    })


    // Testear la inserción de un producto correcto
    describe('Test inserción de producto', function(){
        
        it('Debe insertar el producto correctamente', function(done){
            var producto = new Producto("LAM2", "Lampara AM 2", "Lampara amarilla de 2 bombillas", ["muebles", "iluminacion", "hogar"], 27, 30);

            supertest(app.app)
                .post('/productos')
                .send(producto)
                .expect(201, done)

        });
    });

    // Testear la obtención del producto insertado
    describe('Test obtener un producto', function(){
        
        it('Debe obtener el producto correctamente', function(done){

            supertest(app.app)
                .get('/productos/LAM2')
                .expect(200)
                .end(function(err, res){
                    if(err){done(err)}
                    else{
                        chai.expect(res.body._id).to.eql("LAM2");
                        chai.expect(res.body.nombre).to.eql("Lampara AM 2");
                        chai.expect(res.body.descripcion).to.eql("Lampara amarilla de 2 bombillas");
                        chai.expect(res.body.categorias).to.eql(["muebles", "iluminacion", "hogar"]);
                        chai.expect(res.body.precio).to.eql(27);
                        chai.expect(res.body.stock).to.eql(30);
                        done();
                    }
                })

        });
    });
});
