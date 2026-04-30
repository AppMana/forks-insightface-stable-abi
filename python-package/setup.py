#!/usr/bin/env python
"""Build script for the insightface stable-ABI fork.

Produces a single ``cp39-abi3`` wheel per platform that works on Python 3.9+
and NumPy 2.x (and remains forward-compatible with NumPy 1.x consumers thanks
to NumPy 2's stable ABI).
"""
import os

import numpy as np
from Cython.Build import cythonize
from setuptools import Extension, setup

PY_LIMITED_API = "0x030B0000"

define_macros = [
    ("Py_LIMITED_API", PY_LIMITED_API),
    ("CYTHON_LIMITED_API", "1"),
    ("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION"),
    ("NPY_TARGET_VERSION", "NPY_2_0_API_VERSION"),
]

if os.name == "nt":
    extra_compile_args = ["/O2", "/std:c++17"]
else:
    extra_compile_args = ["-O3", "-std=c++17"]

extensions = [
    Extension(
        "insightface.thirdparty.face3d.mesh.cython.mesh_core_cython",
        sources=[
            "insightface/thirdparty/face3d/mesh/cython/mesh_core_cython.pyx",
            "insightface/thirdparty/face3d/mesh/cython/mesh_core.cpp",
        ],
        language="c++",
        define_macros=define_macros,
        extra_compile_args=extra_compile_args,
        py_limited_api=True,
    ),
]

ext_modules = cythonize(
    extensions,
    compiler_directives={
        "language_level": "3",
        "boundscheck": False,
        "wraparound": False,
        "binding": False,
    },
)

setup(
    ext_modules=ext_modules,
    include_dirs=[np.get_include()],
    options={"bdist_wheel": {"py_limited_api": "cp311"}},
)
