import numpy
from Cython.Build import cythonize
from setuptools import Extension, setup

setup(
    name="fast_overlap",
    use_scm_version={"write_to": "fast_overlap/_version.py"},
    ext_modules=cythonize(
        [
            Extension(
                "fast_overlap._engine",
                ["fast_overlap/fast_overlap.pyx"],
                include_dirs=[numpy.get_include()],
                extra_compile_args=["-fopenmp", "-O3"],
                extra_link_args=["-fopenmp"],
            )
        ],
        language_level="3",
    ),
)
