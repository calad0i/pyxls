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

pyxls exposes the `libxls.so`'s C API to python, mostly in 1:1 fashion, and some pythonic wrappers for some of them.

`libxls.so` provides the following APIs that are exposed in `pyxls`:

- **IR Operations**: build, view, optimize, and tweak XLS IR
- **DSLX Operations**: parse and typecheck DSLX code
- **Simulation**: execute XLS functions or DSLX code with interpretation or JIT
- **Verilog AST**: construct and emit Verilog/SystemVerilog files via an AST API (binding could be buggy for now)
- **Code Emission**: schedule and codegen XLS IR to produce Verilog output

Index
=====

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   install.md
   getting_started.md
   api_overview.md

.. toctree::
   :maxdepth: 3
   :caption: API Reference

   autodoc/xls

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
