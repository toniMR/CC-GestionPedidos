
const Producto = require('../../src/productos/classes/producto');
const app = require('../../src/productos/productos-rest');
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

        var producto = new Producto("LAM2", "Lampara AM 2", "Lampara amarilla de 2 bombillas", ["muebles", "iluminacion", "hogar"], 27, 30);
        
        it('Debe insertar el producto correctamente', function(done){
            supertest(app.app)
                .post('/productos')
                .send(producto)
                .expect(201, done)
        });

        it('Debe responder que ya existe un producto con ese id', function(done){
            supertest(app.app)
                .post('/productos')
                .send(producto)
                .expect(400)
                .end(function(err, res){
                    if(err){done(err)}
                    else{
                        chai.expect(res.body.mensaje).to.eql("Ya existe un producto con ese id");
                        done();
                    }
                })
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

    
    // Testear la obtención de productos en un rango de precio
    describe('Test obtener productos en rango de precio', function(){

        it('Debe obtener los productos en el rango de precio', function(done){
            supertest(app.app)
                .get('/productos/precio/min/10/max/30')
                .expect(200)
                .end(function(err, res){
                    if(err){done(err)}
                    else{
                        chai.expect(res.body[0]._id).to.eql("LAM2");
                        chai.expect(res.body[0].nombre).to.eql("Lampara AM 2");
                        chai.expect(res.body[0].descripcion).to.eql("Lampara amarilla de 2 bombillas");
                        chai.expect(res.body[0].categorias).to.eql(["muebles", "iluminacion", "hogar"]);
                        chai.expect(res.body[0].precio).to.eql(27);
                        chai.expect(res.body[0].stock).to.eql(30);
                        done();
                    }
                })
        });

        it('Debe mostrar que no existen productos para ese rango de precio', function(done){
            supertest(app.app)
                .get('/productos/precio/min/1000/max/3000')
                .expect(404)
                .end(function(err, res){
                    if(err){done(err)}
                    else{
                        chai.expect(res.body.mensaje).to.eql("No hay productos en ese rango de precio");
                        done();
                    }
                })
        });

        it('Debe indicar que los parametros deben ser enteros', function(done){
            supertest(app.app)
                .get('/productos/precio/min/ad10dad/max/asd30s')
                .expect(400)
                .end(function(err, res){
                    if(err){done(err)}
                    else{
                        chai.expect(res.body.mensaje).to.eql("Error: Debe especificar numeros enteros");
                        done();
                    }
                })
        });

    });


    describe('Test obtener productos en categorias', function(){

        it('Debe obtener los productos con esas categorias', function(done){
            supertest(app.app)
                .get('/productos/categorias/Muebles,Iluminacion,Hogar')
                .expect(200)
                .end(function(err, res){
                    if(err){done(err)}
                    else{
                        chai.expect(res.body[0]._id).to.eql("LAM2");
                        chai.expect(res.body[0].nombre).to.eql("Lampara AM 2");
                        chai.expect(res.body[0].descripcion).to.eql("Lampara amarilla de 2 bombillas");
                        chai.expect(res.body[0].categorias).to.eql(["muebles", "iluminacion", "hogar"]);
                        chai.expect(res.body[0].precio).to.eql(27);
                        chai.expect(res.body[0].stock).to.eql(30);
                        done();
                    }
                })
        });

        it('Debe obtener los productos que incluyan esas categorias', function(done){
            supertest(app.app)
                .get('/productos/categorias/Muebles,Iluminacion')
                .expect(200)
                .end(function(err, res){
                    if(err){done(err)}
                    else{
                        chai.expect(res.body[0]._id).to.eql("LAM2");
                        chai.expect(res.body[0].nombre).to.eql("Lampara AM 2");
                        chai.expect(res.body[0].descripcion).to.eql("Lampara amarilla de 2 bombillas");
                        chai.expect(res.body[0].categorias).to.eql(["muebles", "iluminacion", "hogar"]);
                        chai.expect(res.body[0].precio).to.eql(27);
                        chai.expect(res.body[0].stock).to.eql(30);
                        done();
                    }
                })
        });

        it('No debe encontrar ningun producto con esas categorias', function(done){
            supertest(app.app)
                .get('/productos/categorias/Muebles,Iluminacion,Hogar,Piscina')
                .expect(404)
                .end(function(err, res){
                    if(err){done(err)}
                    else{
                        chai.expect(res.body.mensaje).to.eql("No hay productos que pertenezcan a todas esas categorias");
                        done();
                    }
                })
        });

    });


    describe('Test obtener productos que incluya el texto', function(){

        it('Debe obtener los productos que contengan ese texto', function(done){
            supertest(app.app)
                .get('/productos/texto/lampara,amarilla')
                .expect(200)
                .end(function(err, res){
                    if(err){done(err)}
                    else{
                        chai.expect(res.body[0]._id).to.eql("LAM2");
                        chai.expect(res.body[0].nombre).to.eql("Lampara AM 2");
                        chai.expect(res.body[0].descripcion).to.eql("Lampara amarilla de 2 bombillas");
                        chai.expect(res.body[0].categorias).to.eql(["muebles", "iluminacion", "hogar"]);
                        chai.expect(res.body[0].precio).to.eql(27);
                        chai.expect(res.body[0].stock).to.eql(30);
                        done();
                    }
                })
        });

        it('Debe obtener los productos que contengan alguna de las palabras del texto', function(done){
            supertest(app.app)
                .get('/productos/texto/armario,sillon,lampara,amarilla')
                .expect(200)
                .end(function(err, res){
                    if(err){done(err)}
                    else{
                        chai.expect(res.body[0]._id).to.eql("LAM2");
                        chai.expect(res.body[0].nombre).to.eql("Lampara AM 2");
                        chai.expect(res.body[0].descripcion).to.eql("Lampara amarilla de 2 bombillas");
                        chai.expect(res.body[0].categorias).to.eql(["muebles", "iluminacion", "hogar"]);
                        chai.expect(res.body[0].precio).to.eql(27);
                        chai.expect(res.body[0].stock).to.eql(30);
                        done();
                    }
                })
        });

        it('No debe encontrar ningun producto que contenga ese texto', function(done){
            supertest(app.app)
                .get('/productos/texto/armario,silla')
                .expect(404)
                .end(function(err, res){
                    if(err){done(err)}
                    else{
                        chai.expect(res.body.mensaje).to.eql("No hay productos que contengan esas palabras");
                        done();
                    }
                })
        });

    });


    // Testear la modificación de un producto
    describe('Test modificar un producto', function(){

        var producto = new Producto("LAM2", "Lampara AM 2", "Lampara amarilla de 2 bombillas", ["muebles", "iluminacion", "hogar"], 27, 30);
        producto.setNombre("Lámpara");

        it('Debe modificar el producto correctamente', function(done){
            supertest(app.app)
                .put('/productos/LAM2')
                .send(producto)
                .expect(200)
                .end(function(err, res){
                    if(err){done(err)}
                    else{
                        chai.expect(res.body.nModified).to.eql(1);
                        done();
                    }
                })
        });

        it('Debe responder que no existe producto con ese id', function(done){
            supertest(app.app)
                .put('/productos/ASDFG')
                .send(producto)
                .expect(404)
                .end(function(err, res){
                    if(err){done(err)}
                    else{
                        chai.expect(res.body.mensaje).to.eql("No existe un producto con ese id");
                        done();
                    }
                })
        });

    });


    // Testear la eliminación de un producto
    describe('Test eliminar un producto', function(){
        
        it('Debe eliminar el producto correctamente', function(done){
            supertest(app.app)
                .delete('/productos/LAM2')
                .expect(200)
                .end(function(err, res){
                    if(err){done(err)}
                    else{
                        chai.expect(res.body.mensaje).to.eql("Producto borrado");
                        done();
                    }
                })
        });

        it('Debe responder que no existe producto con ese id', function(done){
            supertest(app.app)
                .delete('/productos/ASDFG')
                .expect(404)
                .end(function(err, res){
                    if(err){done(err)}
                    else{
                        chai.expect(res.body.mensaje).to.eql("No existe un producto con ese id");
                        done();
                    }
                })
        });

    });


});
