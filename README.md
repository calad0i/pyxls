# pyxls

[![Documentation](https://img.shields.io/github/actions/workflow/status/calad0i/pyxls/sphinx-build.yml?label=doc)](https://calad0i.github.io/pyxls/)
[![PyPI](https://img.shields.io/pypi/v/xls-python)](https://pypi.org/project/xls-python/)
[![LGPLv3](https://img.shields.io/badge/License-Apache%202.0-orange)](https://www.apache.org/licenses/LICENSE-2.0)

Python bindings for the [XLS](https://google.github.io/xls/) (eXtensible Logic Synthesis) compiler infrastructure.

> [!NOTE]
> `pyxls` is a third-party project interfacing with the XLS C API. It is not affiliated, endorsed, or maintained by the XLS team at Google.


> [!WARNING]
> pyxls is in early development. The API is not stable and may change without deprecation.


> [!WARNING]
> The `libxls.so` library bundled with pyxls is built from official XLS releases. However, since the c APIs are not considered stable in XLS, replacing the bundled library with a custom build may lead to undefined behavior. Currently, pyxls release is done manually, which will likely not keep up with the pace of XLS development. CI builds are planned but no estimated timeline yet. The current version is built against XLS commit [`202e8d5ce`](https://github.com/google/xls/releases/tag/v0.0.0-9549-g202e8d5ce).

## Installation

```bash
pip install xls-python
```

Or from source (requires a C++20 compiler, Meson, and Ninja):

```bash
pip install .
```

## Quick Start

```python
from xls import Package, Value

IR = """
package my_pkg

top fn add(x: bits[32], y: bits[32]) -> bits[32] {
  ret add.3: bits[32] = add(x, y, id=3)
}
"""

pkg = Package.parse_ir(IR)
fn = pkg.get_function('add')
result = fn.interpret([Value.make_ubits(32, 3), Value.make_ubits(32, 4)])
print(result.to_string())  # bits[32]:7
```

## Documentation

See [https://calad0i.github.io/pyxls/](https://calad0i.github.io/pyxls/) for full documentation.

## License

Apache 2.0
