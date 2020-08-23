from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("ma_crossover.pyx")
)
