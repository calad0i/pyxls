# API Overview

pyxls exposes four main modules. All primary classes and functions are re-exported from the top-level `xls` package for convenience.

## `xls.c_api`: Core Types and Functions

The `c_api` module provides the core abstractions that mirror the XLS C API:

- `Package`: a container for IR functions and types. Created via `Package.create()` or `Package.parse_ir()`.
- `Function` / `FunctionBase`: an XLS function. Supports interpretation (`interpret`), JIT compilation (`to_jit`), and SMT encoding (`to_z3_smtlib`).
- `FunctionJit`: a JIT-compiled function. Call `run(args)` for fast repeated execution.
- `FunctionType`: describes a function's parameter and return types.
- `Type`: represents an XLS type (`bits[N]`, tuple, array, token). Query with `get_kind()`, `get_flat_bit_count()`.
- `Value`: a concrete XLS value. Construct with `Value.make_ubits()`, `Value.make_sbits()`, `Value.make_tuple()`, etc.
- `Bits`: raw bit-vector data. Supports arithmetic operators (`+`, `-`, `&`, `|`, `^`, `<<`, `>>`) and conversion to/from Python integers and bytes.
- `BitsRope`: for concatenate `Bits` values.
- `ScheduleAndCodegenResult`: the output of `Package.schedule_and_codegen()`, providing `get_verilog_text()`.

Likely useful functions:

| Function                           | Description                                           |
| ---------------------------------- | ----------------------------------------------------- |
| `convert_dslx_to_ir(...)`          | Compile DSLX source to XLS IR text                    |
| `optimize_ir(ir, top)`             | Run IR optimisation passes                            |
| `mangle_dslx_name(module, fn)`     | Produce the mangled IR name for a DSLX function       |
| `parse_ir_package(ir, filename)`   | Parse IR text into a `Package`                        |
| `parse_typed_value(input)`         | Parse a typed value from its string representation    |
| `jit_fn_predict(jit, inputs, ...)` | Run a JIT function with numpy inputs, loop inside C++ |

## `xls.ir_builder`: Functional IR Builder API

The `ir_builder` module lets you build XLS IR functions in Python without writing textual IR:

- `FunctionBuilder`: entry point for building a new function. Call `FunctionBuilder.create(name, package)` then `add_parameter()` to add typed inputs, and finally `build_with_return_value(bval)` to finalise.
- `BuilderBase`: holds all the arithmetic, logical, bitwise, and structural operations. Obtain via `fb.as_builder_base()`. Operations include:
  - Arithmetic: `add_add`, `add_sub`, `add_umul`, `add_smul`, `add_udiv`, `add_sdiv`, …
  - Bitwise/logical: `add_and`, `add_or`, `add_xor`, `add_not`, `add_negate`, …
  - Comparisons: `add_ult`, `add_slt`, `add_eq`, `add_ne`, …
  - Reductions: `add_and_reduce`, `add_or_reduce`, `add_xor_reduce`
  - Bit manipulation: `add_bit_slice`, `add_sign_extend`, `add_zero_extend`, `add_concat`, …
  - Collections: `add_tuple`, `add_tuple_index`, `add_array`, `add_array_index`, …
  - Multiplexing: `add_select`, `add_one_hot`, `add_one_hot_select`, `add_priority_select`
- `BValue`: a reference to a node in the IR graph (symbolic value).

## `xls.dslx`: DSLX Language Support

The `dslx` module exposes the DSLX parser and typechecker. DSLX is XLS's statically typed, hardware-oriented functional language.

Key entry point:

```python
from xls.dslx import parse_and_typecheck, ImportData

import_data = ImportData.create(dslx_stdlib_path='', additional_search_paths=[])
result = parse_and_typecheck(dslx_text, 'module.x', 'module_name', import_data)
```

The returned `TypecheckedModule` exposes the parsed AST and type information. The module also provides types for introspecting DSLX programs: `DslxModule`, `DslxFunction`, `StructDef`, `EnumDef`, `TypeInfo`, `ParametricEnv`, `InterpValue`, and more.

## `xls.vast`: Verilog AST

The `vast` module provides a structured API for constructing Verilog and SystemVerilog files:

- `VerilogFile`: top-level file object. Create with `VerilogFile.create(FileType.SYSTEM_VERILOG)` or `FileType.VERILOG`. Call `emit()` to produce Verilog text.
- `VerilogModule`: a Verilog module. Add via `vf.add_module(name)`. Then use `add_input()`, `add_output()`, `add_logic()`, `add_wire()`, `add_reg()` to declare ports and signals.
- `LogicRef`: a reference to a declared signal. Use `as_expression()` in expressions.
- `Expression`: a Verilog expression node. Call `emit()` for the text form.
- `DataType`: a Verilog data type (scalar or bit-vector).

The `VerilogFile` object also provides factory methods for all expression and statement types: `make_literal()`, `make_unary()`, `make_binary()`, `make_scalar_type()`, `make_bit_vector_type()`, etc.
