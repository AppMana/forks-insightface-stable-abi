"""Exercise the abi3 Cython extension via the buffer protocol."""
import numpy as np
import pytest

from insightface.thirdparty.face3d.mesh.cython import mesh_core_cython


def _unit_triangle() -> tuple[np.ndarray, np.ndarray]:
    vertices = np.array(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
        dtype=np.float32,
    )
    triangles = np.array([[0, 1, 2]], dtype=np.int32)
    return vertices, triangles


def test_extension_is_abi3() -> None:
    """The compiled module must ship as a stable-ABI .abi3.{so,pyd}."""
    name = mesh_core_cython.__file__
    assert ".abi3." in name, f"expected stable-ABI suffix, got {name}"


def test_get_normal_core_runs() -> None:
    vertices, triangles = _unit_triangle()
    normal = np.zeros_like(vertices)
    tri_normal = np.zeros((triangles.shape[0], 3), dtype=np.float32)
    mesh_core_cython.get_normal_core(normal, tri_normal, triangles, triangles.shape[0])


def test_rasterize_runs() -> None:
    vertices, triangles = _unit_triangle()
    h, w = 8, 8
    depth_buffer = np.full((h, w), -1e9, dtype=np.float32)
    triangle_buffer = np.full((h, w), -1, dtype=np.int32)
    barycentric_weight = np.zeros((h * w, 3), dtype=np.float32)
    mesh_core_cython.rasterize_triangles_core(
        vertices, triangles,
        depth_buffer, triangle_buffer, barycentric_weight,
        vertices.shape[0], triangles.shape[0],
        h, w,
    )


def test_render_colors_runs() -> None:
    vertices, triangles = _unit_triangle()
    h, w, c = 8, 8, 3
    image = np.zeros((h, w, c), dtype=np.float32)
    colors = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.float32)
    depth_buffer = np.full((h, w), -1e9, dtype=np.float32)
    mesh_core_cython.render_colors_core(
        image, vertices, triangles, colors, depth_buffer,
        vertices.shape[0], triangles.shape[0], h, w, c,
    )


def test_rejects_non_contiguous() -> None:
    """Memoryview args require C-contiguous input — non-contiguous must raise."""
    vertices, triangles = _unit_triangle()
    big = np.zeros((vertices.shape[0] * 2, 3), dtype=np.float32)
    non_contig = big[::2]
    assert not non_contig.flags["C_CONTIGUOUS"]
    tri_normal = np.zeros((triangles.shape[0], 3), dtype=np.float32)
    with pytest.raises((ValueError, TypeError, BufferError)):
        mesh_core_cython.get_normal_core(non_contig, tri_normal, triangles, triangles.shape[0])
