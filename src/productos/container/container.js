/*
    En este fichero se establecerán las dependencias
    que serán necesarias.
*/

var inversify = require("inversify");
require("reflect-metadata");
const MongoHandler = require('../data_managers/mongoHandler.js');


// Declare as injectable and its dependencies
inversify.decorate(inversify.injectable(), MongoHandler);
inversify.decorate(inversify.inject('DBHandler'), MongoHandler);

// Declare bindings
var container = new inversify.Container();
container.bind('DBHandler').to(MongoHandler);


module.exports = container;
