# Installation

## From PyPI

When binary wheels are available:

```bash
pip install pyxls
```

## From Source

Building from source requires:

- Python ≥ 3.10
- A C++20-capable compiler (GCC ≥ 11 or Clang ≥ 14)
- [Meson](https://mesonbuild.com/) ≥ 1.0 and [Ninja](https://ninja-build.org/)

```bash
git clone https://github.com/calad0i/pyxls.git
cd pyxls
pip install .
```

The build system (`meson-python`) compiles the C++ nanobind extension and links it against the prebuilt `libxls.so` bundled in the repository. No separate XLS build is required.

## Runtime Requirements

- Python ≥ 3.10
- NumPy ≥ 2

## Optional: DSLX Standard Library

Some DSLX functionality requires pointing to the XLS standard library path via the `dslx_stdlib_path` argument. The standard library is not bundled; refer to the [XLS project](https://google.github.io/xls/) for how to obtain it.
