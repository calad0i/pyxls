"""Tests for xls.raw.c_api bindings."""

import pytest

import xls.raw as raw

SAMPLE_IR = """\
package test_pkg

top fn add(x: bits[32], y: bits[32]) -> bits[32] {
  ret add.3: bits[32] = add(x, y, id=3)
}
"""

MULTI_FN_IR = """\
package multi_pkg

fn double(x: bits[32]) -> bits[32] {
  ret add.2: bits[32] = add(x, x, id=2)
}

top fn add(x: bits[32], y: bits[32]) -> bits[32] {
  ret add.3: bits[32] = add(x, y, id=3)
}
"""


# ============================================================
# Package operations
# ============================================================


def test_parse_ir_package(sample_ir):
    pkg = raw.c_api.xls_parse_ir_package(sample_ir)
    assert pkg is not None
    assert isinstance(pkg, raw.Package)


def test_parse_ir_package_with_filename(sample_ir):
    pkg = raw.c_api.xls_parse_ir_package(sample_ir, 'test.ir')
    assert pkg is not None


def test_package_to_string(package):
    s = raw.c_api.xls_package_to_string(package)
    assert isinstance(s, str)
    assert 'add' in s
    assert 'bits[32]' in s


def test_package_get_function(package):
    fn = raw.c_api.xls_package_get_function(package, 'add')
    assert fn is not None
    assert isinstance(fn, raw.Function)


def test_package_get_function_missing(package):
    with pytest.raises(Exception):
        raw.c_api.xls_package_get_function(package, 'nonexistent')


def test_package_get_functions_single():
    pkg = raw.c_api.xls_parse_ir_package(SAMPLE_IR)
    fns = raw.c_api.xls_package_get_functions(pkg)
    assert isinstance(fns, list)
    assert len(fns) == 1
    assert isinstance(fns[0], raw.Function)


def test_package_get_functions_multi():
    pkg = raw.c_api.xls_parse_ir_package(MULTI_FN_IR)
    fns = raw.c_api.xls_package_get_functions(pkg)
    assert len(fns) == 2
    names = {raw.c_api.xls_function_get_name(f) for f in fns}
    assert 'add' in names
    assert 'double' in names


def test_package_verify(package):
    # Should not raise
    raw.c_api.xls_verify_package(package)


def test_package_get_type_for_value(package):
    v = raw.c_api.xls_value_make_ubits(32, 42)
    t = raw.c_api.xls_package_get_type_for_value(package, v)
    assert t is not None
    assert isinstance(t, raw.Type)


# ============================================================
# Function operations
# ============================================================


def test_function_get_name(function):
    name = raw.c_api.xls_function_get_name(function)
    assert name == 'add'


def test_function_get_param_name(function):
    x_name = raw.c_api.xls_function_get_param_name(function, 0)
    y_name = raw.c_api.xls_function_get_param_name(function, 1)
    assert x_name == 'x'
    assert y_name == 'y'


def test_function_get_type(function):
    ft = raw.c_api.xls_function_get_type(function)
    assert ft is not None
    assert isinstance(ft, raw.FunctionType)


def test_function_type_param_count(function):
    ft = raw.c_api.xls_function_get_type(function)
    count = raw.c_api.xls_function_type_get_param_count(ft)
    assert count == 2


def test_function_type_param_type(function):
    ft = raw.c_api.xls_function_get_type(function)
    param0 = raw.c_api.xls_function_type_get_param_type(ft, 0)
    assert isinstance(param0, raw.Type)
    assert raw.c_api.xls_type_to_string(param0) == 'bits[32]'


def test_function_type_return_type(function):
    ft = raw.c_api.xls_function_get_type(function)
    ret_type = raw.c_api.xls_function_type_get_return_type(ft)
    assert isinstance(ret_type, raw.Type)
    assert raw.c_api.xls_type_to_string(ret_type) == 'bits[32]'


def test_function_type_to_string(function):
    ft = raw.c_api.xls_function_get_type(function)
    s = raw.c_api.xls_function_type_to_string(ft)
    assert isinstance(s, str)
    assert 'bits[32]' in s


def test_function_to_string(function):
    s = raw.c_api.xls_function_to_string(function)
    assert isinstance(s, str)
    assert 'add' in s


# ============================================================
# Type operations
# ============================================================


def test_type_get_kind(function):
    ft = raw.c_api.xls_function_get_type(function)
    ret_type = raw.c_api.xls_function_type_get_return_type(ft)
    kind = raw.c_api.xls_type_get_kind(ret_type)
    assert kind == raw.c_api.ValueKind.BITS


def test_type_to_string(function):
    ft = raw.c_api.xls_function_get_type(function)
    ret_type = raw.c_api.xls_function_type_get_return_type(ft)
    s = raw.c_api.xls_type_to_string(ret_type)
    assert s == 'bits[32]'


def test_type_get_flat_bit_count(function):
    ft = raw.c_api.xls_function_get_type(function)
    ret_type = raw.c_api.xls_function_type_get_return_type(ft)
    count = raw.c_api.xls_type_get_flat_bit_count(ret_type)
    assert count == 32


def test_type_get_leaf_count(function):
    ft = raw.c_api.xls_function_get_type(function)
    ret_type = raw.c_api.xls_function_type_get_return_type(ft)
    count = raw.c_api.xls_type_get_leaf_count(ret_type)
    assert count == 1


# ============================================================
# Value operations
# ============================================================


def test_value_make_ubits():
    v = raw.c_api.xls_value_make_ubits(32, 42)
    assert v is not None
    assert isinstance(v, raw.Value)


def test_value_make_ubits_zero():
    v = raw.c_api.xls_value_make_ubits(8, 0)
    s = raw.c_api.xls_value_to_string(v)
    assert '0' in s


def test_value_make_sbits():
    v = raw.c_api.xls_value_make_sbits(32, -1)
    assert v is not None
    assert isinstance(v, raw.Value)


def test_value_make_sbits_negative():
    v = raw.c_api.xls_value_make_sbits(8, -42)
    s = raw.c_api.xls_value_to_string(v)
    assert s is not None


def test_value_make_token():
    v = raw.c_api.xls_value_make_token()
    assert v is not None
    kind = raw.c_api.xls_value_get_kind(v)
    assert kind == raw.c_api.ValueKind.TOKEN


def test_value_make_true():
    v = raw.c_api.xls_value_make_true()
    assert v is not None
    s = raw.c_api.xls_value_to_string(v)
    assert '1' in s


def test_value_make_false():
    v = raw.c_api.xls_value_make_false()
    assert v is not None
    s = raw.c_api.xls_value_to_string(v)
    assert '0' in s


def test_value_make_array():
    e0 = raw.c_api.xls_value_make_ubits(8, 10)
    e1 = raw.c_api.xls_value_make_ubits(8, 20)
    e2 = raw.c_api.xls_value_make_ubits(8, 30)
    arr = raw.c_api.xls_value_make_array([e0, e1, e2])
    assert arr is not None
    kind = raw.c_api.xls_value_get_kind(arr)
    assert kind == raw.c_api.ValueKind.ARRAY


def test_value_make_tuple():
    e0 = raw.c_api.xls_value_make_ubits(8, 1)
    e1 = raw.c_api.xls_value_make_ubits(16, 2)
    tup = raw.c_api.xls_value_make_tuple([e0, e1])
    assert tup is not None
    kind = raw.c_api.xls_value_get_kind(tup)
    assert kind == raw.c_api.ValueKind.TUPLE


def test_value_to_string():
    v = raw.c_api.xls_value_make_ubits(32, 42)
    s = raw.c_api.xls_value_to_string(v)
    assert isinstance(s, str)
    assert '42' in s


def test_value_eq_same():
    a = raw.c_api.xls_value_make_ubits(32, 7)
    b = raw.c_api.xls_value_make_ubits(32, 7)
    assert raw.c_api.xls_value_eq(a, b)


def test_value_eq_different():
    a = raw.c_api.xls_value_make_ubits(32, 7)
    b = raw.c_api.xls_value_make_ubits(32, 8)
    assert not raw.c_api.xls_value_eq(a, b)


def test_value_get_kind_bits():
    v = raw.c_api.xls_value_make_ubits(32, 1)
    kind = raw.c_api.xls_value_get_kind(v)
    assert kind == raw.c_api.ValueKind.BITS


def test_value_get_kind_array():
    e = raw.c_api.xls_value_make_ubits(8, 0)
    arr = raw.c_api.xls_value_make_array([e])
    kind = raw.c_api.xls_value_get_kind(arr)
    assert kind == raw.c_api.ValueKind.ARRAY


def test_value_get_kind_tuple():
    e = raw.c_api.xls_value_make_ubits(8, 0)
    tup = raw.c_api.xls_value_make_tuple([e])
    kind = raw.c_api.xls_value_get_kind(tup)
    assert kind == raw.c_api.ValueKind.TUPLE


def test_value_clone():
    v = raw.c_api.xls_value_make_ubits(32, 99)
    cloned = raw.c_api.xls_value_clone(v)
    assert raw.c_api.xls_value_eq(v, cloned)


def test_value_get_element_array():
    e0 = raw.c_api.xls_value_make_ubits(8, 10)
    e1 = raw.c_api.xls_value_make_ubits(8, 20)
    arr = raw.c_api.xls_value_make_array([e0, e1])
    elem = raw.c_api.xls_value_get_element(arr, 0)
    assert raw.c_api.xls_value_eq(elem, e0)
    elem1 = raw.c_api.xls_value_get_element(arr, 1)
    assert raw.c_api.xls_value_eq(elem1, e1)


def test_value_get_element_tuple():
    e0 = raw.c_api.xls_value_make_ubits(8, 5)
    e1 = raw.c_api.xls_value_make_ubits(16, 6)
    tup = raw.c_api.xls_value_make_tuple([e0, e1])
    elem = raw.c_api.xls_value_get_element(tup, 0)
    assert raw.c_api.xls_value_eq(elem, e0)


def test_value_get_element_count_array():
    elems = [raw.c_api.xls_value_make_ubits(8, i) for i in range(5)]
    arr = raw.c_api.xls_value_make_array(elems)
    count = raw.c_api.xls_value_get_element_count(arr)
    assert count == 5


def test_parse_typed_value():
    v = raw.c_api.xls_parse_typed_value('bits[32]:42')
    assert v is not None
    s = raw.c_api.xls_value_to_string(v)
    assert '42' in s


def test_parse_typed_value_array():
    v = raw.c_api.xls_parse_typed_value('[bits[8]:1, bits[8]:2, bits[8]:3]')
    assert v is not None
    kind = raw.c_api.xls_value_get_kind(v)
    assert kind == raw.c_api.ValueKind.ARRAY


def test_value_get_bits():
    v = raw.c_api.xls_value_make_ubits(32, 42)
    bits = raw.c_api.xls_value_get_bits(v)
    assert bits is not None
    assert isinstance(bits, raw.Bits)


def test_value_from_bits():
    bits = raw.c_api.xls_bits_make_ubits(32, 77)
    v = raw.c_api.xls_value_from_bits(bits)
    assert v is not None
    s = raw.c_api.xls_value_to_string(v)
    assert '77' in s


def test_value_flatten_to_bits():
    v = raw.c_api.xls_value_make_ubits(32, 100)
    bits = raw.c_api.xls_value_flatten_to_bits(v)
    assert bits is not None
    n = raw.c_api.xls_bits_to_uint64(bits)
    assert n == 100


def test_value_to_string_format_preference():
    v = raw.c_api.xls_value_make_ubits(8, 255)
    s_hex = raw.c_api.xls_value_to_string_format_preference(v, raw.c_api.FormatPreference.HEX)
    assert 'ff' in s_hex.lower() or 'FF' in s_hex


def test_format_preference_from_string():
    pref = raw.c_api.xls_format_preference_from_string('hex')
    assert pref == raw.c_api.FormatPreference.HEX


def test_format_preference_binary():
    pref = raw.c_api.xls_format_preference_from_string('binary')
    assert pref == raw.c_api.FormatPreference.BINARY


# ============================================================
# Bits operations
# ============================================================


def test_bits_make_ubits():
    bits = raw.c_api.xls_bits_make_ubits(32, 42)
    assert bits is not None
    assert isinstance(bits, raw.Bits)


def test_bits_make_sbits():
    bits = raw.c_api.xls_bits_make_sbits(32, -1)
    assert bits is not None


def test_bits_get_bit_count():
    bits = raw.c_api.xls_bits_make_ubits(16, 0)
    count = raw.c_api.xls_bits_get_bit_count(bits)
    assert count == 16


def test_bits_to_uint64():
    bits = raw.c_api.xls_bits_make_ubits(32, 12345)
    val = raw.c_api.xls_bits_to_uint64(bits)
    assert val == 12345


def test_bits_to_int64():
    bits = raw.c_api.xls_bits_make_sbits(32, -99)
    val = raw.c_api.xls_bits_to_int64(bits)
    assert val == -99


def test_bits_to_bytes():
    bits = raw.c_api.xls_bits_make_ubits(8, 0xAB)
    data = raw.c_api.xls_bits_to_bytes(bits)
    assert isinstance(data, bytes)
    assert len(data) == 1
    assert data[0] == 0xAB


def test_bits_to_string():
    bits = raw.c_api.xls_bits_make_ubits(8, 42)
    s = raw.c_api.xls_bits_to_string(bits, raw.c_api.FormatPreference.UNSIGNED_DECIMAL)
    assert '42' in s


def test_bits_to_debug_string():
    bits = raw.c_api.xls_bits_make_ubits(8, 5)
    s = raw.c_api.xls_bits_to_debug_string(bits)
    assert isinstance(s, str)


def test_bits_get_bit():
    # bits[8]:1 => bit 0 is 1, rest 0
    bits = raw.c_api.xls_bits_make_ubits(8, 1)
    assert raw.c_api.xls_bits_get_bit(bits, 0) is True
    assert raw.c_api.xls_bits_get_bit(bits, 1) is False


def test_bits_make_bits_from_bytes():
    data = bytes([0x42])
    bits = raw.c_api.xls_bits_make_bits_from_bytes(8, data)
    val = raw.c_api.xls_bits_to_uint64(bits)
    assert val == 0x42


def test_bits_eq_same():
    a = raw.c_api.xls_bits_make_ubits(32, 100)
    b = raw.c_api.xls_bits_make_ubits(32, 100)
    assert raw.c_api.xls_bits_eq(a, b)


def test_bits_eq_different():
    a = raw.c_api.xls_bits_make_ubits(32, 100)
    b = raw.c_api.xls_bits_make_ubits(32, 101)
    assert not raw.c_api.xls_bits_eq(a, b)


def test_bits_ne():
    a = raw.c_api.xls_bits_make_ubits(32, 1)
    b = raw.c_api.xls_bits_make_ubits(32, 2)
    assert raw.c_api.xls_bits_ne(a, b)


def test_bits_ult():
    a = raw.c_api.xls_bits_make_ubits(32, 5)
    b = raw.c_api.xls_bits_make_ubits(32, 10)
    assert raw.c_api.xls_bits_ult(a, b)
    assert not raw.c_api.xls_bits_ult(b, a)


def test_bits_ule():
    a = raw.c_api.xls_bits_make_ubits(32, 5)
    b = raw.c_api.xls_bits_make_ubits(32, 5)
    assert raw.c_api.xls_bits_ule(a, b)


def test_bits_ugt():
    a = raw.c_api.xls_bits_make_ubits(32, 10)
    b = raw.c_api.xls_bits_make_ubits(32, 5)
    assert raw.c_api.xls_bits_ugt(a, b)


def test_bits_uge():
    a = raw.c_api.xls_bits_make_ubits(32, 5)
    b = raw.c_api.xls_bits_make_ubits(32, 5)
    assert raw.c_api.xls_bits_uge(a, b)


def test_bits_slt():
    a = raw.c_api.xls_bits_make_sbits(32, -5)
    b = raw.c_api.xls_bits_make_sbits(32, 5)
    assert raw.c_api.xls_bits_slt(a, b)


def test_bits_sle():
    a = raw.c_api.xls_bits_make_sbits(32, -5)
    b = raw.c_api.xls_bits_make_sbits(32, -5)
    assert raw.c_api.xls_bits_sle(a, b)


def test_bits_sgt():
    a = raw.c_api.xls_bits_make_sbits(32, 5)
    b = raw.c_api.xls_bits_make_sbits(32, -5)
    assert raw.c_api.xls_bits_sgt(a, b)


def test_bits_sge():
    a = raw.c_api.xls_bits_make_sbits(32, 3)
    b = raw.c_api.xls_bits_make_sbits(32, 3)
    assert raw.c_api.xls_bits_sge(a, b)


def test_bits_add():
    a = raw.c_api.xls_bits_make_ubits(32, 10)
    b = raw.c_api.xls_bits_make_ubits(32, 5)
    result = raw.c_api.xls_bits_add(a, b)
    assert raw.c_api.xls_bits_to_uint64(result) == 15


def test_bits_sub():
    a = raw.c_api.xls_bits_make_ubits(32, 10)
    b = raw.c_api.xls_bits_make_ubits(32, 3)
    result = raw.c_api.xls_bits_sub(a, b)
    assert raw.c_api.xls_bits_to_uint64(result) == 7


def test_bits_and():
    a = raw.c_api.xls_bits_make_ubits(8, 0b11001100)
    b = raw.c_api.xls_bits_make_ubits(8, 0b10101010)
    result = raw.c_api.xls_bits_and(a, b)
    assert raw.c_api.xls_bits_to_uint64(result) == 0b10001000


def test_bits_or():
    a = raw.c_api.xls_bits_make_ubits(8, 0b11001100)
    b = raw.c_api.xls_bits_make_ubits(8, 0b10101010)
    result = raw.c_api.xls_bits_or(a, b)
    assert raw.c_api.xls_bits_to_uint64(result) == 0b11101110


def test_bits_xor():
    a = raw.c_api.xls_bits_make_ubits(8, 0b11001100)
    b = raw.c_api.xls_bits_make_ubits(8, 0b10101010)
    result = raw.c_api.xls_bits_xor(a, b)
    assert raw.c_api.xls_bits_to_uint64(result) == 0b01100110


def test_bits_negate():
    a = raw.c_api.xls_bits_make_ubits(8, 1)
    result = raw.c_api.xls_bits_negate(a)
    # 2's complement negation: -1 = 0xFF for 8-bit
    assert raw.c_api.xls_bits_to_uint64(result) == 0xFF


def test_bits_not():
    a = raw.c_api.xls_bits_make_ubits(8, 0b00001111)
    result = raw.c_api.xls_bits_not(a)
    assert raw.c_api.xls_bits_to_uint64(result) == 0b11110000


def test_bits_umul():
    a = raw.c_api.xls_bits_make_ubits(8, 3)
    b = raw.c_api.xls_bits_make_ubits(8, 4)
    result = raw.c_api.xls_bits_umul(a, b)
    assert raw.c_api.xls_bits_to_uint64(result) == 12


def test_bits_shift_left_logical():
    a = raw.c_api.xls_bits_make_ubits(8, 1)
    result = raw.c_api.xls_bits_shift_left_logical(a, 3)
    assert raw.c_api.xls_bits_to_uint64(result) == 8


def test_bits_shift_right_logical():
    a = raw.c_api.xls_bits_make_ubits(8, 8)
    result = raw.c_api.xls_bits_shift_right_logical(a, 3)
    assert raw.c_api.xls_bits_to_uint64(result) == 1


def test_bits_shift_right_arithmetic():
    a = raw.c_api.xls_bits_make_sbits(8, -8)
    result = raw.c_api.xls_bits_shift_right_arithmetic(a, 1)
    # Arithmetic shift right of -8 by 1 = -4
    val = raw.c_api.xls_bits_to_int64(result)
    assert val == -4


def test_bits_width_slice():
    # Take bits [4:8) from 0b11110000
    a = raw.c_api.xls_bits_make_ubits(8, 0b11110000)
    result = raw.c_api.xls_bits_width_slice(a, 4, 4)
    assert raw.c_api.xls_bits_get_bit_count(result) == 4
    assert raw.c_api.xls_bits_to_uint64(result) == 0b1111


# ============================================================
# Interpret & JIT
# ============================================================


def test_interpret_function(function):
    a = raw.c_api.xls_value_make_ubits(32, 3)
    b = raw.c_api.xls_value_make_ubits(32, 4)
    result = raw.c_api.xls_interpret_function(function, [a, b])
    s = raw.c_api.xls_value_to_string(result)
    assert '7' in s


def test_interpret_function_zero(function):
    a = raw.c_api.xls_value_make_ubits(32, 0)
    b = raw.c_api.xls_value_make_ubits(32, 0)
    result = raw.c_api.xls_interpret_function(function, [a, b])
    bits = raw.c_api.xls_value_get_bits(result)
    assert raw.c_api.xls_bits_to_uint64(bits) == 0


def test_make_function_jit(function):
    jit = raw.c_api.xls_make_function_jit(function)
    assert jit is not None
    assert isinstance(jit, raw.FunctionJit)


def test_function_jit_run(jit):
    a = raw.c_api.xls_value_make_ubits(32, 3)
    b = raw.c_api.xls_value_make_ubits(32, 4)
    result = raw.c_api.xls_function_jit_run(jit, [a, b])
    s = raw.c_api.xls_value_to_string(result)
    assert '7' in s


def test_function_jit_run_overflow(jit):
    # 2^32 - 1 + 1 = 0 due to overflow
    max_val = raw.c_api.xls_value_make_ubits(32, 0xFFFFFFFF)
    one = raw.c_api.xls_value_make_ubits(32, 1)
    result = raw.c_api.xls_function_jit_run(jit, [max_val, one])
    bits = raw.c_api.xls_value_get_bits(result)
    assert raw.c_api.xls_bits_to_uint64(bits) == 0


def test_jit_matches_interpret(function):
    jit = raw.c_api.xls_make_function_jit(function)
    for x, y in [(0, 0), (1, 1), (100, 200), (0xFFFF, 1)]:
        a = raw.c_api.xls_value_make_ubits(32, x)
        b = raw.c_api.xls_value_make_ubits(32, y)
        r_interp = raw.c_api.xls_interpret_function(function, [a, b])
        r_jit = raw.c_api.xls_function_jit_run(jit, [a, b])
        assert raw.c_api.xls_value_eq(r_interp, r_jit)


# ============================================================
# Optimize IR
# ============================================================


def test_optimize_ir(sample_ir):
    optimized = raw.c_api.xls_optimize_ir(sample_ir, 'add')
    assert isinstance(optimized, str)
    assert 'add' in optimized


def test_optimize_ir_returns_valid(sample_ir):
    optimized = raw.c_api.xls_optimize_ir(sample_ir, 'add')
    pkg = raw.c_api.xls_parse_ir_package(optimized)
    assert pkg is not None


# ============================================================
# BitsRope
# ============================================================


def test_bits_rope_create():
    rope = raw.c_api.xls_create_bits_rope(8)
    assert rope is not None
    assert isinstance(rope, raw.BitsRope)


def test_bits_rope_append_and_get():
    rope = raw.c_api.xls_create_bits_rope(8)
    bits = raw.c_api.xls_bits_make_ubits(8, 0xAB)
    raw.c_api.xls_bits_rope_append_bits(rope, bits)
    result = raw.c_api.xls_bits_rope_get_bits(rope)
    assert isinstance(result, raw.Bits)
    assert raw.c_api.xls_bits_to_uint64(result) == 0xAB


def test_bits_rope_append_multiple():
    # Build 16-bit value from two 8-bit parts
    rope = raw.c_api.xls_create_bits_rope(16)
    lo = raw.c_api.xls_bits_make_ubits(8, 0xCD)
    hi = raw.c_api.xls_bits_make_ubits(8, 0xAB)
    raw.c_api.xls_bits_rope_append_bits(rope, lo)
    raw.c_api.xls_bits_rope_append_bits(rope, hi)
    result = raw.c_api.xls_bits_rope_get_bits(rope)
    val = raw.c_api.xls_bits_to_uint64(result)
    assert val == 0xABCD


# ============================================================
# DSLX name mangling
# ============================================================


def test_mangle_dslx_name():
    mangled = raw.c_api.xls_mangle_dslx_name('my_module', 'my_fn')
    assert isinstance(mangled, str)
    assert 'my_module' in mangled or 'my_fn' in mangled


# ============================================================
# Package top functions
# ============================================================


def test_package_get_top(package):
    top = raw.c_api.xls_package_get_top(package)
    assert top is not None


def test_package_set_top_by_name():
    pkg = raw.c_api.xls_parse_ir_package(MULTI_FN_IR)
    # Should not raise
    raw.c_api.xls_package_set_top_by_name(pkg, 'double')
