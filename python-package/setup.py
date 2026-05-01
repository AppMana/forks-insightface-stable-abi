#!/usr/bin/env python
"""Build script for the insightface stable-ABI fork.

Produces:

* a ``cp311-abi3`` wheel when built on Python 3.11+ (works on Python 3.11,
  3.12, 3.13, 3.14...) — the stable-ABI path that we keep for the long
  term. Cython memoryviews require ``Py_buffer``, which only entered the
  limited API in 3.11.
* a regular ``cp310-cp310`` wheel when built on Python 3.10 — non-stable
  ABI, version-locked. This is here purely so people still on 3.10 get a
  binary instead of falling back to the sdist.

Both flavours compile against NumPy 2.x and remain runtime-compatible with
NumPy 1.x consumers thanks to NumPy 2's stable C ABI.
"""
import os
import sys

import numpy as np
from Cython.Build import cythonize
from setuptools import Extension, setup

ABI3 = sys.version_info >= (3, 11)
PY_LIMITED_API = "0x030B0000"

define_macros = [
    ("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION"),
    ("NPY_TARGET_VERSION", "NPY_2_0_API_VERSION"),
]
if ABI3:
    define_macros += [
        ("Py_LIMITED_API", PY_LIMITED_API),
        ("CYTHON_LIMITED_API", "1"),
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
        py_limited_api=ABI3,
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

setup_options = {}
if ABI3:
    setup_options["bdist_wheel"] = {"py_limited_api": "cp311"}

setup(
    ext_modules=ext_modules,
    include_dirs=[np.get_include()],
    options=setup_options,
)
