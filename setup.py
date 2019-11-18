#!/usr/bin/env python
# coding: utf-8

from setuptools import setup
from distutils.command.clean import clean
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

setup(
    
    # Nombre del proyecto
    name='CC-GestionPedidos', # Required

    # Versión del proyecto
    version='2.1',            # Required

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

    # Limpiar proyecto
    # Se limpia ejecutando con: 
    #                ---->    python3 setup.py clean
    cmdclass={'clean': Cleaner},


    # Instalar dependencias
    # Se instalan ejecutando:
    #                ---->    pip3 install .
    install_requires=[
        'Flask',
    ],    
 )


