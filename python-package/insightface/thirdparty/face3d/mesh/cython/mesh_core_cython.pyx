# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
"""Cython wrapper around the C++ mesh core.

Uses typed memoryviews (PEP 3118 buffer protocol) so the generated C
compiles cleanly under Py_LIMITED_API / abi3, and works against any
NumPy 1.23+ / 2.x release without regenerating.
"""
from libcpp.string cimport string


cdef extern from "mesh_core.h":
    void _rasterize_triangles_core(
        float* vertices, int* triangles,
        float* depth_buffer, int* triangle_buffer, float* barycentric_weight,
        int nver, int ntri,
        int h, int w)

    void _render_colors_core(
        float* image, float* vertices, int* triangles,
        float* colors,
        float* depth_buffer,
        int nver, int ntri,
        int h, int w, int c)

    void _render_texture_core(
        float* image, float* vertices, int* triangles,
        float* texture, float* tex_coords, int* tex_triangles,
        float* depth_buffer,
        int nver, int tex_nver, int ntri,
        int h, int w, int c,
        int tex_h, int tex_w, int tex_c,
        int mapping_type)

    void _get_normal_core(
        float* normal, float* tri_normal, int* triangles,
        int ntri)

    void _write_obj_with_colors_texture(string filename, string mtl_name,
        float* vertices, int* triangles, float* colors, float* uv_coords,
        int nver, int ntri, int ntexver)


def get_normal_core(float[:, ::1] normal not None,
                    float[:, ::1] tri_normal not None,
                    int[:, ::1] triangles not None,
                    int ntri):
    _get_normal_core(&normal[0, 0], &tri_normal[0, 0], &triangles[0, 0], ntri)


def rasterize_triangles_core(float[:, ::1] vertices not None,
                             int[:, ::1] triangles not None,
                             float[:, ::1] depth_buffer not None,
                             int[:, ::1] triangle_buffer not None,
                             float[:, ::1] barycentric_weight not None,
                             int nver, int ntri,
                             int h, int w):
    _rasterize_triangles_core(
        &vertices[0, 0], &triangles[0, 0],
        &depth_buffer[0, 0], &triangle_buffer[0, 0], &barycentric_weight[0, 0],
        nver, ntri, h, w)


def render_colors_core(float[:, :, ::1] image not None,
                       float[:, ::1] vertices not None,
                       int[:, ::1] triangles not None,
                       float[:, ::1] colors not None,
                       float[:, ::1] depth_buffer not None,
                       int nver, int ntri,
                       int h, int w, int c):
    _render_colors_core(
        &image[0, 0, 0], &vertices[0, 0], &triangles[0, 0],
        &colors[0, 0],
        &depth_buffer[0, 0],
        nver, ntri, h, w, c)


def render_texture_core(float[:, :, ::1] image not None,
                        float[:, ::1] vertices not None,
                        int[:, ::1] triangles not None,
                        float[:, :, ::1] texture not None,
                        float[:, ::1] tex_coords not None,
                        int[:, ::1] tex_triangles not None,
                        float[:, ::1] depth_buffer not None,
                        int nver, int tex_nver, int ntri,
                        int h, int w, int c,
                        int tex_h, int tex_w, int tex_c,
                        int mapping_type):
    _render_texture_core(
        &image[0, 0, 0], &vertices[0, 0], &triangles[0, 0],
        &texture[0, 0, 0], &tex_coords[0, 0], &tex_triangles[0, 0],
        &depth_buffer[0, 0],
        nver, tex_nver, ntri,
        h, w, c,
        tex_h, tex_w, tex_c,
        mapping_type)


def write_obj_with_colors_texture_core(string filename, string mtl_name,
                                       float[:, ::1] vertices not None,
                                       int[:, ::1] triangles not None,
                                       float[:, ::1] colors not None,
                                       float[:, ::1] uv_coords not None,
                                       int nver, int ntri, int ntexver):
    _write_obj_with_colors_texture(
        filename, mtl_name,
        &vertices[0, 0], &triangles[0, 0], &colors[0, 0], &uv_coords[0, 0],
        nver, ntri, ntexver)
