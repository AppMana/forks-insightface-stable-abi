"""End-to-end FaceAnalysis test, gated on a real model being available.

The wheel CI runs this only when ``INSIGHTFACE_E2E=1`` so the wheel build
itself stays offline.
"""
import os

import numpy as np
import pytest


@pytest.mark.skipif(
    os.environ.get("INSIGHTFACE_E2E") != "1",
    reason="set INSIGHTFACE_E2E=1 to run the model-download end-to-end test",
)
def test_buffalo_l_round_trip() -> None:
    pytest.importorskip("onnxruntime")
    from insightface.app import FaceAnalysis
    from insightface.data import get_image as ins_get_image

    app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
    app.prepare(ctx_id=-1, det_size=(320, 320))
    img = ins_get_image("t1")
    faces = app.get(img)
    assert len(faces) > 0
    f = faces[0]
    assert f.bbox.shape == (4,)
    assert f.kps.shape == (5, 2)
    assert f.embedding.shape == (512,)
    assert isinstance(f.gender, (int, np.integer))
    assert isinstance(f.age, (int, np.integer))
