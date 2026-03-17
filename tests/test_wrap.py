"""Tests for the Python wrapper layer (xls.c_api, xls.ir_builder, etc.)."""

import xls
from xls import c_api, ir_builder, raw, vast
from xls._wrap import (
    _RAW_TO_WRAPPED,
    _WRAPPED_TO_RAW,
    auto_wrap,
    maybe_unwrap,
    maybe_wrap,
)

SAMPLE_IR = """\
package test_pkg

top fn add(x: bits[32], y: bits[32]) -> bits[32] {
  ret add.3: bits[32] = add(x, y, id=3)
}
"""


# ============================================================
# _wrap.py — registry and wrap/unwrap primitives
# ============================================================


def test_raw_to_wrapped_registry():
    assert raw.Package in _RAW_TO_WRAPPED
    assert raw.Function in _RAW_TO_WRAPPED
    assert raw.Value in _RAW_TO_WRAPPED
    assert raw.Bits in _RAW_TO_WRAPPED
    assert raw.Type in _RAW_TO_WRAPPED
    assert raw.FunctionJit in _RAW_TO_WRAPPED
    assert raw.FunctionType in _RAW_TO_WRAPPED
    assert raw.BValue in _RAW_TO_WRAPPED
    assert raw.BuilderBase in _RAW_TO_WRAPPED
    assert raw.FunctionBuilder in _RAW_TO_WRAPPED


def test_wrapped_to_raw_registry():
    assert c_api.Package in _WRAPPED_TO_RAW
    assert c_api.Function in _WRAPPED_TO_RAW
    assert c_api.Value in _WRAPPED_TO_RAW
    assert c_api.Bits in _WRAPPED_TO_RAW


def test_wrap_value_package():
    raw_pkg = raw.c_api.xls_parse_ir_package(SAMPLE_IR, '')
    wrapped = maybe_wrap(raw_pkg)
    assert isinstance(wrapped, c_api.Package)
    assert wrapped._raw is raw_pkg


def test_wrap_value_unknown_type():
    # A plain string should pass through unchanged
    s = 'hello'
    assert maybe_wrap(s) is s


def test_wrap_value_none():
    assert maybe_wrap(None) is None


def test_unwrap_value_wrapped():
    raw_pkg = raw.c_api.xls_parse_ir_package(SAMPLE_IR, '')
    wrapped = maybe_wrap(raw_pkg)
    assert maybe_unwrap(wrapped) is raw_pkg


def test_unwrap_value_plain():
    assert maybe_unwrap(42) == 42
    assert maybe_unwrap('abc') == 'abc'


def test_auto_wrap_unwraps_inputs():
    raw_pkg = raw.c_api.xls_parse_ir_package(SAMPLE_IR, '')
    wrapped_pkg = maybe_wrap(raw_pkg)

    calls = []

    def spy_fn(pkg):
        calls.append(pkg)
        return raw.c_api.xls_package_to_string(pkg)

    wrapped_fn = auto_wrap(spy_fn)
    result = wrapped_fn(wrapped_pkg)
    # Input was unwrapped before calling
    assert calls[0] is raw_pkg
    # String result passes through
    assert isinstance(result, str)
    assert 'add' in result


def test_auto_wrap_wraps_raw_output():
    raw_pkg = raw.c_api.xls_parse_ir_package(SAMPLE_IR, '')

    @auto_wrap
    def get_fn(pkg):
        return raw.c_api.xls_package_get_function(pkg, 'add')

    result = get_fn(raw_pkg)
    assert isinstance(result, c_api.Function)
    assert result._raw is not None


def test_auto_wrap_list_input():
    # auto_wrap should unwrap list elements
    raw_v1 = raw.c_api.xls_value_make_ubits(32, 3)
    raw_v2 = raw.c_api.xls_value_make_ubits(32, 4)
    w1 = maybe_wrap(raw_v1)
    w2 = maybe_wrap(raw_v2)

    raw_pkg = raw.c_api.xls_parse_ir_package(SAMPLE_IR, '')
    raw_fn = raw.c_api.xls_package_get_function(raw_pkg, 'add')

    @auto_wrap
    def run_fn(fn, args):
        return raw.c_api.xls_interpret_function(fn, args)

    result = run_fn(raw_fn, [w1, w2])
    assert isinstance(result, c_api.Value)


# ============================================================
# c_api.py — Package wrapper
# ============================================================


def test_package_parse_ir_classmethod():
    pkg = c_api.Package.parse_ir(SAMPLE_IR)
    assert isinstance(pkg, c_api.Package)
    assert isinstance(pkg._raw, raw.Package)


def test_package_create():
    pkg = c_api.Package.create('my_test_pkg')
    assert isinstance(pkg, c_api.Package)


def test_package_to_string():
    pkg = c_api.Package.parse_ir(SAMPLE_IR)
    s = pkg.to_string()
    assert isinstance(s, str)
    assert 'add' in s


def test_package_get_function():
    pkg = c_api.Package.parse_ir(SAMPLE_IR)
    fn = pkg.get_function('add')
    assert isinstance(fn, c_api.Function)


def test_package_get_top():
    pkg = c_api.Package.parse_ir(SAMPLE_IR)
    top = pkg.get_top()
    assert top is not None
    # get_top returns a FunctionBase (the registered wrapper for raw.FunctionBase)
    assert isinstance(top, c_api.FunctionBase)


def test_package_set_top():
    pkg = c_api.Package.parse_ir(SAMPLE_IR)
    ok = pkg.set_top('add')
    assert ok is True or ok is None  # may return bool or None


def test_package_verify():
    pkg = c_api.Package.parse_ir(SAMPLE_IR)
    result = pkg.verify()
    # Returns True or raises; either is acceptable
    assert result is True or result is None


def test_package_get_type_for_value():
    pkg = c_api.Package.parse_ir(SAMPLE_IR)
    v = c_api.Value.make_ubits(32, 42)
    t = pkg.get_type_for_value(v)
    assert isinstance(t, c_api.Type)
    assert t.to_string() == 'bits[32]'


def test_package_schedule_and_codegen():
    pkg = c_api.Package.parse_ir(SAMPLE_IR)
    # Use combinational generator (no pipeline, no delay model needed)
    result = pkg.schedule_and_codegen(
        scheduling_options='',
        codegen_flags='generator: GENERATOR_KIND_COMBINATIONAL',
    )
    assert isinstance(result, c_api.ScheduleAndCodegenResult)
    verilog = result.get_verilog_text()
    assert isinstance(verilog, str)
    assert len(verilog) > 0
    assert 'module add' in verilog


# ============================================================
# c_api.py — Function wrapper
# ============================================================


def test_function_get_name():
    pkg = c_api.Package.parse_ir(SAMPLE_IR)
    fn = pkg.get_function('add')
    assert fn.get_name() == 'add'


def test_function_get_type():
    pkg = c_api.Package.parse_ir(SAMPLE_IR)
    fn = pkg.get_function('add')
    ft = fn.get_type()
    assert isinstance(ft, c_api.FunctionType)


def test_function_get_param_count():
    pkg = c_api.Package.parse_ir(SAMPLE_IR)
    fn = pkg.get_function('add')
    assert fn.get_param_count() == 2


def test_function_get_param_name():
    pkg = c_api.Package.parse_ir(SAMPLE_IR)
    fn = pkg.get_function('add')
    assert fn.get_param_name(0) == 'x'
    assert fn.get_param_name(1) == 'y'


def test_function_to_string():
    pkg = c_api.Package.parse_ir(SAMPLE_IR)
    fn = pkg.get_function('add')
    s = fn.to_string()
    assert isinstance(s, str)
    assert 'add' in s


def test_function_interpret():
    pkg = c_api.Package.parse_ir(SAMPLE_IR)
    fn = pkg.get_function('add')
    a = c_api.Value.make_ubits(32, 10)
    b = c_api.Value.make_ubits(32, 5)
    result = fn.interpret([a, b])
    assert isinstance(result, c_api.Value)
    bits = result.get_bits()
    assert bits.to_uint64() == 15


def test_function_to_jit():
    pkg = c_api.Package.parse_ir(SAMPLE_IR)
    fn = pkg.get_function('add')
    jit = fn.to_jit()
    assert isinstance(jit, c_api.FunctionJit)


def test_function_jit_run():
    pkg = c_api.Package.parse_ir(SAMPLE_IR)
    fn = pkg.get_function('add')
    jit = fn.to_jit()
    a = c_api.Value.make_ubits(32, 7)
    b = c_api.Value.make_ubits(32, 3)
    result = jit.run([a, b])
    assert isinstance(result, c_api.Value)
    bits = result.get_bits()
    assert bits.to_uint64() == 10


# ============================================================
# c_api.py — Value wrapper
# ============================================================


def test_value_make_ubits():
    v = c_api.Value.make_ubits(32, 42)
    assert isinstance(v, c_api.Value)
    assert isinstance(v._raw, raw.Value)


def test_value_make_sbits():
    v = c_api.Value.make_sbits(32, -1)
    assert isinstance(v, c_api.Value)


def test_value_make_token():
    v = c_api.Value.make_token()
    assert isinstance(v, c_api.Value)


def test_value_make_true():
    v = c_api.Value.make_true()
    assert isinstance(v, c_api.Value)
    s = v.to_string()
    assert '1' in s


def test_value_make_false():
    v = c_api.Value.make_false()
    assert isinstance(v, c_api.Value)


def test_value_parse():
    v = c_api.Value.parse('bits[32]:42')
    assert isinstance(v, c_api.Value)
    bits = v.get_bits()
    assert bits.to_uint64() == 42


def test_value_clone():
    v = c_api.Value.make_ubits(32, 99)
    cloned = v.clone()
    assert isinstance(cloned, c_api.Value)
    assert v == cloned


def test_value_eq():
    a = c_api.Value.make_ubits(32, 7)
    b = c_api.Value.make_ubits(32, 7)
    c = c_api.Value.make_ubits(32, 8)
    assert a == b
    assert not (a == c)


def test_value_get_kind():
    v = c_api.Value.make_ubits(32, 1)
    kind = v.get_kind()
    assert kind == raw.c_api.ValueKind.BITS


def test_value_get_bits():
    v = c_api.Value.make_ubits(32, 123)
    bits = v.get_bits()
    assert isinstance(bits, c_api.Bits)
    assert bits.to_uint64() == 123


def test_value_flatten_to_bits():
    v = c_api.Value.make_ubits(32, 55)
    bits = v.flatten_to_bits()
    assert isinstance(bits, c_api.Bits)
    assert bits.to_uint64() == 55


def test_value_repr():
    v = c_api.Value.make_ubits(32, 42)
    r = repr(v)
    assert '42' in r


# ============================================================
# c_api.py — Bits wrapper
# ============================================================


def test_bits_make_ubits():
    b = c_api.Bits.make_ubits(32, 100)
    assert isinstance(b, c_api.Bits)


def test_bits_make_sbits():
    b = c_api.Bits.make_sbits(32, -50)
    assert isinstance(b, c_api.Bits)
    assert b.to_int64() == -50


def test_bits_get_bit_count():
    b = c_api.Bits.make_ubits(16, 0)
    assert b.get_bit_count() == 16


def test_bits_to_uint64():
    b = c_api.Bits.make_ubits(32, 12345)
    assert b.to_uint64() == 12345


def test_bits_to_int64():
    b = c_api.Bits.make_sbits(32, -99)
    assert b.to_int64() == -99


def test_bits_to_bytes():
    b = c_api.Bits.make_ubits(8, 0xAB)
    data = b.to_bytes()
    assert isinstance(data, bytes)
    assert data[0] == 0xAB


def test_bits_arithmetic():
    a = c_api.Bits.make_ubits(32, 10)
    b = c_api.Bits.make_ubits(32, 5)
    assert (a + b).to_uint64() == 15
    assert (a - b).to_uint64() == 5
    assert (a & b).to_uint64() == 0
    assert (a | b).to_uint64() == 15
    assert (a ^ b).to_uint64() == 15


def test_bits_comparison():
    a = c_api.Bits.make_ubits(32, 5)
    b = c_api.Bits.make_ubits(32, 10)
    assert a < b
    assert a <= b
    assert b > a
    assert b >= a
    assert a == a
    assert a != b


def test_bits_shift():
    a = c_api.Bits.make_ubits(8, 1)
    assert (a << 3).to_uint64() == 8
    assert (a << 3 >> 3).to_uint64() == 1


def test_bits_invert():
    a = c_api.Bits.make_ubits(8, 0b00001111)
    result = ~a
    assert result.to_uint64() == 0b11110000


def test_bits_negate():
    a = c_api.Bits.make_ubits(8, 1)
    result = -a
    assert result.to_uint64() == 0xFF  # 2's complement


# ============================================================
# c_api.py — Type wrapper
# ============================================================


def test_type_to_string():
    pkg = c_api.Package.parse_ir(SAMPLE_IR)
    fn = pkg.get_function('add')
    ft = fn.get_type()
    ret = ft.get_return_type()
    assert isinstance(ret, c_api.Type)
    assert ret.to_string() == 'bits[32]'


def test_type_get_flat_bit_count():
    pkg = c_api.Package.parse_ir(SAMPLE_IR)
    fn = pkg.get_function('add')
    ft = fn.get_type()
    ret = ft.get_return_type()
    assert ret.get_flat_bit_count() == 32


# ============================================================
# c_api.py — FunctionType wrapper
# ============================================================


def test_function_type_param_count():
    pkg = c_api.Package.parse_ir(SAMPLE_IR)
    fn = pkg.get_function('add')
    ft = fn.get_type()
    assert ft.get_param_count() == 2


def test_function_type_param_type():
    pkg = c_api.Package.parse_ir(SAMPLE_IR)
    fn = pkg.get_function('add')
    ft = fn.get_type()
    p0 = ft.get_param_type(0)
    assert isinstance(p0, c_api.Type)
    assert p0.to_string() == 'bits[32]'


def test_function_type_return_type():
    pkg = c_api.Package.parse_ir(SAMPLE_IR)
    fn = pkg.get_function('add')
    ft = fn.get_type()
    ret = ft.get_return_type()
    assert isinstance(ret, c_api.Type)
    assert ret.to_string() == 'bits[32]'


# ============================================================
# c_api.py — module-level convenience functions
# ============================================================


def test_parse_ir_package_fn():
    pkg = c_api.parse_ir_package(SAMPLE_IR)
    assert isinstance(pkg, c_api.Package)


def test_parse_typed_value_fn():
    v = c_api.parse_typed_value('bits[32]:77')
    assert isinstance(v, c_api.Value)
    assert v.get_bits().to_uint64() == 77


def test_optimize_ir_fn():
    result = c_api.optimize_ir(SAMPLE_IR, 'add')
    assert isinstance(result, str)
    assert 'add' in result


def test_mangle_dslx_name_fn():
    mangled = c_api.mangle_dslx_name('my_mod', 'my_fn')
    assert isinstance(mangled, str)
    assert len(mangled) > 0


# ============================================================
# ir_builder.py — FunctionBuilder wrapper
# ============================================================


def test_function_builder_create():
    pkg = c_api.Package.create('test')
    fb = ir_builder.FunctionBuilder.create('my_add', pkg)
    assert isinstance(fb, ir_builder.FunctionBuilder)


def test_function_builder_full_flow():
    pkg = c_api.Package.create('test_wrap')
    t32 = pkg.get_bits_type(32)
    fb = ir_builder.FunctionBuilder.create('addme', pkg)
    bb = fb.as_builder_base()
    assert isinstance(bb, ir_builder.BuilderBase)
    x = fb.add_parameter('x', t32)
    y = fb.add_parameter('y', t32)
    assert isinstance(x, ir_builder.BValue)
    s = bb.add_add(x, y)
    assert isinstance(s, ir_builder.BValue)
    fn = fb.build_with_return_value(s)
    assert isinstance(fn, c_api.Function)
    # Run via JIT
    jit = fn.to_jit()
    a = c_api.Value.make_ubits(32, 6)
    b = c_api.Value.make_ubits(32, 4)
    result = jit.run([a, b])
    assert result.get_bits().to_uint64() == 10


def test_builder_base_add_sub():
    pkg = c_api.Package.create('test_sub')
    t32 = pkg.get_bits_type(32)
    fb = ir_builder.FunctionBuilder.create('sub_fn', pkg)
    bb = fb.as_builder_base()
    x = fb.add_parameter('x', t32)
    y = fb.add_parameter('y', t32)
    diff = bb.add_sub(x, y)
    fn = fb.build_with_return_value(diff)
    jit = fn.to_jit()
    a = c_api.Value.make_ubits(32, 10)
    b = c_api.Value.make_ubits(32, 3)
    result = jit.run([a, b])
    assert result.get_bits().to_uint64() == 7


def test_builder_base_add_literal():
    pkg = c_api.Package.create('test_lit')
    fb = ir_builder.FunctionBuilder.create('lit_fn', pkg)
    bb = fb.as_builder_base()
    val = c_api.Value.make_ubits(32, 42)
    lit = bb.add_literal(val)
    assert isinstance(lit, ir_builder.BValue)
    fn = fb.build_with_return_value(lit)
    jit = fn.to_jit()
    result = jit.run([])
    assert result.get_bits().to_uint64() == 42


def test_builder_base_get_last_value():
    pkg = c_api.Package.create('test_last')
    t8 = pkg.get_bits_type(8)
    fb = ir_builder.FunctionBuilder.create('last_fn', pkg)
    bb = fb.as_builder_base()
    x = fb.add_parameter('x', t8)
    y = fb.add_parameter('y', t8)
    bb.add_add(x, y)
    last = bb.get_last_value()
    assert isinstance(last, ir_builder.BValue)


# ============================================================
# vast.py — VerilogFile wrapper
# ============================================================


def test_verilog_file_create():
    vf = vast.VerilogFile.create()
    assert isinstance(vf, vast.VerilogFile)


def test_verilog_file_add_module():
    vf = vast.VerilogFile.create()
    mod = vf.add_module('my_module')
    assert isinstance(mod, vast.VerilogModule)


def test_verilog_module_add_input_output():
    vf = vast.VerilogFile.create()
    mod = vf.add_module('test_mod')
    dt = vf.make_scalar_type()
    assert isinstance(dt, vast.DataType)
    in_ref = mod.add_input('in_a', dt)
    out_ref = mod.add_output('out_b', dt)
    assert isinstance(in_ref, vast.LogicRef)
    assert isinstance(out_ref, vast.LogicRef)
    assert in_ref.get_name() == 'in_a'
    assert out_ref.get_name() == 'out_b'


def test_verilog_file_emit():
    vf = vast.VerilogFile.create()
    mod = vf.add_module('simple')
    dt = vf.make_scalar_type()
    mod.add_input('clk', dt)
    text = vf.emit()
    assert isinstance(text, str)
    assert 'simple' in text
    assert 'clk' in text


def test_verilog_module_add_wire():
    vf = vast.VerilogFile.create()
    mod = vf.add_module('wire_mod')
    dt = vf.make_bit_vector_type(8)
    wire = mod.add_wire('w', dt)
    assert isinstance(wire, vast.LogicRef)
    assert wire.get_name() == 'w'


def test_verilog_expression_emit():
    vf = vast.VerilogFile.create()
    lit = vf.make_plain_literal(42)
    # make_plain_literal returns a VastLiteral (subtype of Expression in Verilog hierarchy)
    assert isinstance(lit, vast.Expression) or isinstance(lit, vast.VastLiteral)
    # Access emit via as_expression if it's a VastLiteral
    if isinstance(lit, vast.VastLiteral):
        expr = lit.as_expression()
        text = expr.emit()
    else:
        text = lit.emit()
    assert '42' in text


def test_logic_ref_as_expression():
    vf = vast.VerilogFile.create()
    mod = vf.add_module('expr_mod')
    dt = vf.make_scalar_type()
    ref = mod.add_input('sig', dt)
    expr = ref.as_expression()
    assert isinstance(expr, vast.Expression)
    text = expr.emit()
    assert 'sig' in text


# ============================================================
# __init__.py — top-level imports
# ============================================================


def test_init_imports():
    assert hasattr(xls, 'raw')
    assert hasattr(xls, 'Package')
    assert hasattr(xls, 'Function')
    assert hasattr(xls, 'FunctionJit')
    assert hasattr(xls, 'Value')
    assert hasattr(xls, 'Bits')
    assert hasattr(xls, 'Type')
    assert hasattr(xls, 'FunctionBuilder')
    assert hasattr(xls, 'BuilderBase')
    assert hasattr(xls, 'BValue')
    assert hasattr(xls, 'convert_dslx_to_ir')
    assert hasattr(xls, 'optimize_ir')
    assert hasattr(xls, 'mangle_dslx_name')
    assert hasattr(xls, 'parse_ir_package')
    assert hasattr(xls, 'parse_typed_value')


def test_init_package_class_is_wrapper():
    assert xls.Package is c_api.Package


def test_init_end_to_end():
    pkg = xls.parse_ir_package(SAMPLE_IR)
    assert isinstance(pkg, xls.Package)
    fn = pkg.get_function('add')
    assert isinstance(fn, xls.Function)
    jit = fn.to_jit()
    a = xls.Value.make_ubits(32, 20)
    b = xls.Value.make_ubits(32, 22)
    result = jit.run([a, b])
    assert isinstance(result, xls.Value)
    assert result.get_bits().to_uint64() == 42
