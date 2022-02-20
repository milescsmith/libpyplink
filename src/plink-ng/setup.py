#!/usr/bin/env python3

import numpy as np
from Cython.Build import cythonize
from setuptools import setup
from setuptools.extension import Extension

ext_modules = [
    Extension(
        "pgenlib",
        sources=[
            "pgenlib.pyx",
            "src/plink-ng/c/pgenlib_ffi_support.cc",
            "src/plink-ng/c/include/pgenlib_misc.cc",
            "src/plink-ng/c/include/pgenlib_read.cc",
            "src/plink-ng/c/include/pgenlib_write.cc",
            "src/plink-ng/c/include/plink2_base.cc",
            "src/plink-ng/c/include/plink2_bits.cc",
        ],
        language="c++",
        # do not compile as c++11, since cython doesn't yet support
        # overload of uint32_t operator
        # extra_compile_args = ["-std=c++11", "-Wno-unused-function"],
        # extra_link_args = ["-std=c++11"],
        extra_compile_args=[
            "-std=c++98",
            "-Wno-unused-function",
            "-Wno-macro-redefined",
        ],
        extra_link_args=["-std=c++98"],
        include_dirs=[np.get_include()],
    )
]

setup(
    name="Pgenlib",
    version="0.8",
    description="Wrapper for pgenlib's basic reader and writer.",
    ext_modules=cythonize(ext_modules),
)
