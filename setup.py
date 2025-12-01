from setuptools import setup, Extension
from Cython.Build import cythonize
import os

# Rutas a los archivos fuente
src_dir = os.path.join(os.path.dirname(__file__), 'src')
cython_dir = os.path.join(os.path.dirname(__file__), 'cython')

# Definir la extensión
extensions = [
    Extension(
        name="grafo_wrapper",
        sources=[
            os.path.join(cython_dir, "grafo_wrapper.pyx"),
            os.path.join(src_dir, "GrafoDisperso.cpp"),
        ],
        include_dirs=[src_dir],
        language="c++",
        extra_compile_args=["/std:c++11"] if os.name == 'nt' else ["-std=c++11"],
    )
]

setup(
    name="NeuroNet",
    version="1.0",
    description="Sistema híbrido de análisis de grafos masivos con C++ y Python",
    ext_modules=cythonize(
        extensions,
        compiler_directives={'language_level': "3"}
    ),
    zip_safe=False,
)
