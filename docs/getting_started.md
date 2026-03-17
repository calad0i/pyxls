# Getting Started

## Parsing and Executing XLS IR

The most direct way to use pyxls is to parse an existing XLS IR string into a `Package` and execute functions within it.

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

x = Value.make_ubits(32, 3)
y = Value.make_ubits(32, 4)
result = fn.interpret([x, y])
print(result.to_string())  # bits[32]:7
```

For repeated calls, JIT-compile the function first:

```python
jit = fn.to_jit()
result = jit.run([x, y]) # Value<bits[32]:7>
```

If the function takes **one** array argument and returns an array, you can use `jit_fn_predict` to call it directly with NumPy arrays:

```python
from xls.c_api import jit_fn_predict
import numpy as np

IR = """
package my_pkg

top fn sub(model_inp: bits[32][2] id=1) -> bits[32][1] {
  literal.2: bits[1] = literal(value=0, id=2)
  literal.5: bits[1] = literal(value=1, id=5)
  array_index.3: bits[32] = array_index(model_inp, indices=[literal.2], assumed_in_bounds=true, id=3)
  array_index.6: bits[32] = array_index(model_inp, indices=[literal.5], assumed_in_bounds=true, id=6)
  sub.7: bits[32] = sub(array_index.3, array_index.6, id=7)
  ret array.8: bits[32][1] = array(sub.7, id=8)
}
"""

pkg = Package.parse_ir(IR)
fn = pkg.get_function('sub')
jit = fn.to_jit()

inputs = np.array([[3, 4], [10, 20]], dtype=np.int64)
results = jit_fn_predict(jit, inputs, in_bit_count=32, in_word_count=2, out_word_count=1)
print(results)  # [[-1], [-10]]
```

## Building IR Programmatically

Use `FunctionBuilder` and `BuilderBase` to construct IR functions without writing textual IR.

```python
from xls import Package, FunctionBuilder, Value

pkg = Package.create('my_pkg')
fb = FunctionBuilder.create('add', pkg)
bb = fb.as_builder_base()

t32 = pkg.get_bits_type(32)
x = fb.add_parameter('x', t32)
y = fb.add_parameter('y', t32)
s = bb.add_add(x, y)
fn = fb.build_with_return_value(s)

a = Value.make_ubits(32, 10)
b = Value.make_ubits(32, 5)
print(fn.interpret([a, b]).to_string())  # bits[32]:15
```

## Converting DSLX to IR

DSLX is XLS's domain-specific language for describing hardware. Use `convert_dslx_to_ir` to convert DSLX source to XLS IR, then work with it as a normal `Package`.

```python
from xls import Package, Value, convert_dslx_to_ir, mangle_dslx_name

DSLX = """
fn add(x: u32, y: u32) -> u32 {
  x + y
}
"""

ir = convert_dslx_to_ir(DSLX, 'my_module.x', 'my_module', dslx_stdlib_path='')
mangled = mangle_dslx_name('my_module', 'add')

pkg = Package.parse_ir(ir)
fn = pkg.get_function(mangled)

x = Value.make_ubits(32, 7)
y = Value.make_ubits(32, 8)
print(fn.interpret([x, y]).to_string())  # bits[32]:15
```

## Generating Verilog

```{warning}
VAST module may contain buggy binders and is not recommended for general use. Use
```

```python

from xls.c_api import xls_schedule_and_codegen_package, xls_schedule_and_codegen_result_get_verilog_text

codegen_result = xls_schedule_and_codegen_package(pkg, '', 'generator: GENERATOR_KIND_COMBINATIONAL')
verilog = xls_schedule_and_codegen_result_get_verilog_text(codegen_result)
print(verilog)
```

The above shall generate

```verilog
module add(
  input wire [31:0] x,
  input wire [31:0] y,
  output wire [31:0] out
);
  wire [31:0] add_8;
  assign add_8 = x + y;
  assign out = add_8;
endmodule
```

Alternatively, use can use the `Package`'s `schedule_and_codegen` method to specify scheduling options and codegen flags:

```python
from xls.c_api import xls_schedule_and_codegen_result_get_verilog_text

result = pkg.schedule_and_codegen(
    scheduling_options='delay_model: "asap7", pipeline_stages: 2',
    codegen_flags='generator: GENERATOR_KIND_PIPELINE'
)

verilog = xls_schedule_and_codegen_result_get_verilog_text(result)
print(verilog)
```
module add(
  input wire clk,
  input wire [31:0] x,
  input wire [31:0] y,
  output wire [31:0] out
);
  // ===== Pipe stage 0:

  // Registers for pipe stage 0:
  reg [31:0] p0_x;
  reg [31:0] p0_y;
  always @ (posedge clk) begin
    p0_x <= x;
    p0_y <= y;
  end

  // ===== Pipe stage 1:
  wire [31:0] p1_add_12_comb;
  assign p1_add_12_comb = p0_x + p0_y;
  assign out = p1_add_12_comb;
endmodule
```

By default, neither inputs nor outputs are registered. The exact flags for the scheduling and codegen options can be found in the XLS source's protobuf definitions.
