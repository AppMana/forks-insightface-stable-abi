"""Force tests to run against the installed wheel, not the source tree.

The fork has tests/ inside the python-package/ source directory. Without this,
pytest's discovery walks up to python-package/ and Python's import machinery
loads the unbuilt source tree (which has no .abi3.so) instead of the installed
wheel under site-packages.
"""
import os
import sys
from pathlib import Path

_SOURCE_PARENT = str(Path(__file__).resolve().parent.parent)
_CWD = os.getcwd()
for _stale in (_SOURCE_PARENT, _CWD, ""):
    while _stale in sys.path:
        sys.path.remove(_stale)

if "insightface" in sys.modules:
    del sys.modules["insightface"]
