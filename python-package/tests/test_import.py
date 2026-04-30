"""Smoke tests: every public submodule must import cleanly under NumPy 2."""
import importlib

import numpy as np
import pytest


@pytest.mark.parametrize(
    "module",
    [
        "insightface",
        "insightface.app",
        "insightface.app.common",
        "insightface.app.face_analysis",
        "insightface.data",
        "insightface.data.image",
        "insightface.model_zoo",
        "insightface.model_zoo.arcface_onnx",
        "insightface.model_zoo.attribute",
        "insightface.model_zoo.landmark",
        "insightface.model_zoo.model_zoo",
        "insightface.model_zoo.retinaface",
        "insightface.model_zoo.scrfd",
        "insightface.utils",
        "insightface.utils.face_align",
        "insightface.utils.transform",
        "insightface.thirdparty.face3d.mesh.cython.mesh_core_cython",
    ],
)
def test_import(module: str) -> None:
    importlib.import_module(module)


def test_numpy_is_2x() -> None:
    """The fork is built and tested against NumPy 2.x."""
    assert int(np.__version__.split(".")[0]) >= 2, f"Need NumPy 2.x, got {np.__version__}"


def test_version() -> None:
    import insightface

    assert insightface.__version__
