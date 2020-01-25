#!/usr/bin/env python
# coding: utf-8

from setuptools import setup
from distutils.command.clean import clean
from distutils.cmd import Command
import subprocess

class Cleaner(clean):
    # Limpiar
    def run(self):
        subprocess.run(["rm", "-rf", "src/pedidos/__pycache__"])
        subprocess.run(["rm", "-rf", "tests/pedidos/__pycache__"])
        subprocess.run(["rm", "-f", ".coverage"])
        subprocess.run(["rm", "-rf", ".eggs"])
        subprocess.run(["rm", "-rf", ".pytest_cache"])
        subprocess.run(["rm", "-rf", "CC_GestionPedidos.egg-info"])

# Ejecutar pedidos-rest con gunicorn
class Start(Command):
    description = 'Ejecutar pedidos-rest con gunicorn'
    user_options = [
        # The format is (long option, short option, description).
        ('workers=', 'w', 'numero de workers'),
        ('host=', None, 'host'),
        ('port=', 'p', 'port'),
    ]

    # Inicializar opcciones
    def initialize_options(self):
        self.workers = "1"
        self.host = "127.0.0.1"
        self.port = "8000"

    # Asignar opcciones
    def finalize_options(self):
        if self.workers:
            assert self.workers.isdigit(), ('workers debe ser un número')
        if self.port:
            assert self.workers.isdigit(), ('port debe ser un número')

    def run(self):
        subprocess.run(["gunicorn", "-w", self.workers, "-b", self.host+":"+self.port, "pedidos-rest:app"])

setup(
    
    # Nombre del proyecto
    name='CC-GestionPedidos', # Required

    # Versión del proyecto
    version='4.0',            # Required

    # Página de inicio del proyecto
    url='https://github.com/toniMR/CC-GestionPedidos',   # Required

    # Descripción del proyecto
    description='Microservicio para la gestión de pedidos',

    # Autor del proyecto
    author='Antonio Martos',


    # Dependencias para realizar tests
    # Los tests se ejecutan con: 
    #                ---->    python3 setup.py test
    setup_requires=['pytest-runner'],
    tests_require=[
        'pytest',
        'pytest-cov'
    ],

    
    # Tareas personalizadas                
    cmdclass={
                # Limpiar proyecto   ---->    python3 setup.py clean
                'clean': Cleaner,
                # Iniciar aplicación ---->    python3 setup.py start (-w num_workers --host="ip_host" -p port_host)
                'start': Start
            },

    # Ejecutar

    # Instalar dependencias
    # Se instalan ejecutando:
    #                ---->    pip3 install .
    install_requires=[
        'Flask',
        'psycopg2',
        'schema',
        'gunicorn'
    ],    
 )


