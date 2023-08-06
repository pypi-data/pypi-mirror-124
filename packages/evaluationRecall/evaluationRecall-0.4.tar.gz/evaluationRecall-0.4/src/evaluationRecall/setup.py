from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy

extensions = [
    Extension(
        "neighbors_utils_cython", ["neighbors_cython.pyx"], include_dirs=[numpy.get_include()]
    ),
]

setup(ext_modules=cythonize(extensions),)
