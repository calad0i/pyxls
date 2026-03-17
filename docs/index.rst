======================================
pyxls — Python bindings for XLS
======================================

.. image:: https://img.shields.io/badge/repo-github-blue
   :target: https://github.com/calad0i/pyxls
   :alt: GitHub

.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://www.apache.org/licenses/LICENSE-2.0
   :alt: Apache 2.0

`pyxls` is a python Python bindings for the `XLS <https://google.github.io/xls/>`_ (eXtensible Logic Synthesis) compiler infrastructure. XLS is a high-level synthesis toolkit for generating RTL (Register Transfer Level) hardware descriptions from high-level specifications.

.. note::
   ``pyxls`` is a third-party project interfacing with the XLS C API. It is not affiliated, endorsed, or maintained by the XLS team at Google.

.. warning::
   ``pyxls`` is in early development. The API is not stable and may change without deprecation.

.. warning::
   The ``libxls.so`` library bundled with pyxls is built from official XLS releases. However, since the c APIs are not considered stable in XLS, replacing the bundled library with a custom build may lead to undefined behavior. Currently, pyxls release is done manually, which will likely not keep up with the pace of XLS development. CI builds are planned but no estimated timeline yet. The current version is built against XLS commit [`202e8d5ce`](https://github.com/google/xls/releases/tag/v0.0.0-9549-g202e8d5ce).



pyxls exposes the `libxls.so`'s C API to python, mostly in 1:1 fashion, and some pythonic wrappers for some of them.

`libxls.so` provides the following APIs that are exposed in `pyxls`:

- **IR Operations**: build, view, optimize, and tweak XLS IR
- **DSLX Operations**: parse and typecheck DSLX code
- **Simulation**: execute XLS functions or DSLX code with interpretation or JIT
- **Verilog AST**: construct and emit Verilog/SystemVerilog files via an AST API

  - binding could be buggy for now, use with caution

- **Code Emission**: schedule and codegen XLS IR to produce Verilog output

Index
=====

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   install.md
   getting_started.md
   api_overview.md

.. .. toctree::
..    :maxdepth: 3
..    :caption: API Reference

..    autodoc/xls

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
