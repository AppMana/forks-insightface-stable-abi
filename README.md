# InsightFace Stable ABI Wheels

Fork of [`deepinsight/insightface`](https://github.com/deepinsight/insightface) that publishes:

* a single `cp311-abi3` wheel per platform (works on Python 3.11+),
* compiled cleanly against **NumPy 2.x** (forward-compatible with NumPy 1.x consumers),
* with the [PR #2870](https://github.com/deepinsight/insightface/pull/2870) modernization (PEP 621 metadata, regenerated Cython output) and the [PR #2849](https://github.com/deepinsight/insightface/pull/2849) albumentations-warning fix already applied.

The default branch for this fork is `abi3_stable`.

## Indexes

* `https://appmana.github.io/forks-insightface-stable-abi/cu128/`
* `https://appmana.github.io/forks-insightface-stable-abi/cu130/`

The wheels are CUDA-agnostic (insightface uses `onnxruntime`, not CUDA directly), so both indexes serve the same wheels — the `cu*` layout matches the convention used by the AppMana pip facade.

## Install With pip

```bash
pip install insightface --index-url https://appmana.github.io/forks-insightface-stable-abi/cu128
```

## Install With uv

```bash
uv pip install --system insightface --index-url https://appmana.github.io/forks-insightface-stable-abi/cu128
```

`pyproject.toml` example for `uv`:

```toml
[[tool.uv.index]]
name = "insightface"
url = "https://appmana.github.io/forks-insightface-stable-abi/cu128"
explicit = true

[tool.uv.sources]
insightface = { index = "insightface" }
```

## Build From Source

```bash
uv pip install --system "setuptools>=80" "numpy>=2.0" "cython>=3.1" wheel build
python -m build --wheel python-package
```

The wheel is written to `python-package/dist/`.

## Dev Notes

* The only C extension is `insightface.thirdparty.face3d.mesh.cython.mesh_core_cython`, rewritten to use typed memoryviews so the generated C compiles under `Py_LIMITED_API=0x030B0000`.
* `Py_buffer` only entered the Python stable ABI in 3.11 ([PEP 688](https://peps.python.org/pep-0688/)), which is why the floor is `cp311-abi3` rather than `cp39-abi3` like the sister sageattention/nunchaku forks.
* Wheel ABI compliance is verified in CI via [`abi3audit`](https://github.com/pypa/abi3audit).
* Built with `cibuildwheel` for Linux x86_64/aarch64, macOS x86_64/arm64, and Windows AMD64.
