"""Tests for xls.raw.ir_builder bindings."""

import xls.raw as raw

ib = raw.ir_builder
ca = raw.c_api


def make_add_package():
    """Helper: create a package with a simple add function."""
    pkg = ib.xls_package_create('test_pkg')
    t32 = ib.xls_package_get_bits_type(pkg, 32)
    fb = ib.xls_function_builder_create('add', pkg)
    bb = ib.xls_function_builder_as_builder_base(fb)
    x = ib.xls_function_builder_add_parameter(fb, 'x', t32)
    y = ib.xls_function_builder_add_parameter(fb, 'y', t32)
    s = ib.xls_builder_base_add_add(bb, x, y)
    fn = ib.xls_function_builder_build_with_return_value(fb, s)
    return pkg, fn


# ============================================================
# Package creation
# ============================================================


def test_package_create():
    pkg = ib.xls_package_create('my_package')
    assert pkg is not None
    assert isinstance(pkg, raw.Package)


def test_package_create_different_names():
    pkg1 = ib.xls_package_create('alpha')
    pkg2 = ib.xls_package_create('beta')
    assert pkg1 is not None
    assert pkg2 is not None


# ============================================================
# Type operations
# ============================================================


def test_get_bits_type():
    pkg = ib.xls_package_create('test')
    t = ib.xls_package_get_bits_type(pkg, 32)
    assert t is not None
    assert isinstance(t, raw.Type)
    assert ca.xls_type_to_string(t) == 'bits[32]'


def test_get_bits_type_various_widths():
    pkg = ib.xls_package_create('test')
    for width in [1, 8, 16, 32, 64]:
        t = ib.xls_package_get_bits_type(pkg, width)
        assert ca.xls_type_to_string(t) == f'bits[{width}]'


def test_get_tuple_type():
    pkg = ib.xls_package_create('test')
    t8 = ib.xls_package_get_bits_type(pkg, 8)
    t16 = ib.xls_package_get_bits_type(pkg, 16)
    tup = ib.xls_package_get_tuple_type(pkg, [t8, t16])
    assert tup is not None
    assert isinstance(tup, raw.Type)
    s = ca.xls_type_to_string(tup)
    assert 'bits[8]' in s
    assert 'bits[16]' in s


def test_get_array_type():
    pkg = ib.xls_package_create('test')
    t8 = ib.xls_package_get_bits_type(pkg, 8)
    arr = ib.xls_package_get_array_type(pkg, t8, 4)
    assert arr is not None
    s = ca.xls_type_to_string(arr)
    assert 'bits[8]' in s
    assert '4' in s


def test_get_token_type():
    pkg = ib.xls_package_create('test')
    tok = ib.xls_package_get_token_type(pkg)
    assert tok is not None
    assert isinstance(tok, raw.Type)
    s = ca.xls_type_to_string(tok)
    assert 'token' in s.lower()


# ============================================================
# FunctionBuilder
# ============================================================


def test_function_builder_create():
    pkg = ib.xls_package_create('test')
    fb = ib.xls_function_builder_create('my_fn', pkg)
    assert fb is not None
    assert isinstance(fb, raw.FunctionBuilder)


def test_function_builder_as_builder_base():
    pkg = ib.xls_package_create('test')
    fb = ib.xls_function_builder_create('fn', pkg)
    bb = ib.xls_function_builder_as_builder_base(fb)
    assert bb is not None
    assert isinstance(bb, raw.BuilderBase)


def test_add_parameter():
    pkg = ib.xls_package_create('test')
    t32 = ib.xls_package_get_bits_type(pkg, 32)
    fb = ib.xls_function_builder_create('fn', pkg)
    param = ib.xls_function_builder_add_parameter(fb, 'x', t32)
    assert param is not None
    assert isinstance(param, raw.BValue)


def test_add_multiple_parameters():
    pkg = ib.xls_package_create('test')
    t8 = ib.xls_package_get_bits_type(pkg, 8)
    t16 = ib.xls_package_get_bits_type(pkg, 16)
    fb = ib.xls_function_builder_create('fn', pkg)
    p1 = ib.xls_function_builder_add_parameter(fb, 'a', t8)
    p2 = ib.xls_function_builder_add_parameter(fb, 'b', t16)
    assert p1 is not None
    assert p2 is not None


def test_build_simple_function():
    pkg, fn = make_add_package()
    assert fn is not None
    assert isinstance(fn, raw.Function)
    assert ca.xls_function_get_name(fn) == 'add'


def test_build_with_return_value():
    pkg = ib.xls_package_create('test')
    t32 = ib.xls_package_get_bits_type(pkg, 32)
    fb = ib.xls_function_builder_create('double', pkg)
    bb = ib.xls_function_builder_as_builder_base(fb)
    x = ib.xls_function_builder_add_parameter(fb, 'x', t32)
    doubled = ib.xls_builder_base_add_add(bb, x, x)
    fn = ib.xls_function_builder_build_with_return_value(fb, doubled)
    assert fn is not None
    jit = ca.xls_make_function_jit(fn)
    val = ca.xls_value_make_ubits(32, 7)
    result = ca.xls_function_jit_run(jit, [val])
    bits = ca.xls_value_get_bits(result)
    assert ca.xls_bits_to_uint64(bits) == 14


def test_function_builder_build_auto_return():
    pkg = ib.xls_package_create('test')
    t32 = ib.xls_package_get_bits_type(pkg, 32)
    fb = ib.xls_function_builder_create('noop', pkg)
    bb = ib.xls_function_builder_as_builder_base(fb)
    x = ib.xls_function_builder_add_parameter(fb, 'x', t32)
    # add_identity as last operation
    ib.xls_builder_base_add_identity(bb, x)
    fn = ib.xls_function_builder_build(fb)
    assert fn is not None


# ============================================================
# Binary operations
# ============================================================


def _run_binary_fn(fn_name, a_val, b_val, bit_width=32):
    pkg = ib.xls_package_create('test')
    t = ib.xls_package_get_bits_type(pkg, bit_width)
    fb = ib.xls_function_builder_create('binop_func', pkg)
    bb = ib.xls_function_builder_as_builder_base(fb)
    x = ib.xls_function_builder_add_parameter(fb, 'x', t)
    y = ib.xls_function_builder_add_parameter(fb, 'y', t)
    op = getattr(ib, f'xls_builder_base_add_{fn_name}')
    result = op(bb, x, y)
    built = ib.xls_function_builder_build_with_return_value(fb, result)
    jit = ca.xls_make_function_jit(built)
    av = ca.xls_value_make_ubits(bit_width, a_val)
    bv = ca.xls_value_make_ubits(bit_width, b_val)
    out = ca.xls_function_jit_run(jit, [av, bv])
    bits = ca.xls_value_get_bits(out)
    return ca.xls_bits_to_uint64(bits)


def test_binary_op_add():
    assert _run_binary_fn('add', 10, 5) == 15


def test_binary_op_sub():
    assert _run_binary_fn('sub', 10, 5) == 5


def test_binary_op_and():
    assert _run_binary_fn('and', 0b1100, 0b1010, 8) == 0b1000


def test_binary_op_or():
    assert _run_binary_fn('or', 0b1100, 0b1010, 8) == 0b1110


def test_binary_op_xor():
    assert _run_binary_fn('xor', 0b1100, 0b1010, 8) == 0b0110


def test_binary_op_nand():
    # nand(0b1111, 0b1111) in 8-bit = NOT(0b00001111 AND 0b00001111) = NOT(0b00001111) = 0b11110000
    assert _run_binary_fn('nand', 0b1111, 0b1111, 8) == 0b11110000
    # nand(0b11111111, 0b11111111) = NOT(all-ones) = 0
    assert _run_binary_fn('nand', 0b11111111, 0b11111111, 8) == 0


def test_binary_op_nor():
    # nor(all-zeros, all-zeros) in 8-bit = NOT(0 OR 0) = all-ones = 0xFF
    assert _run_binary_fn('nor', 0b00000000, 0b00000000, 8) == 0b11111111
    # nor(1, 0) = NOT(1) = 0b11111110
    assert _run_binary_fn('nor', 0b00000001, 0b00000000, 8) == 0b11111110


def test_binary_op_shll():
    assert _run_binary_fn('shll', 1, 3, 8) == 8


def test_binary_op_shrl():
    assert _run_binary_fn('shrl', 8, 3, 8) == 1


def test_binary_op_eq():
    # eq returns 1-bit result; can't directly use _run_binary_fn easily
    pkg = ib.xls_package_create('test')
    t8 = ib.xls_package_get_bits_type(pkg, 8)
    fb = ib.xls_function_builder_create('eq_fn', pkg)
    bb = ib.xls_function_builder_as_builder_base(fb)
    x = ib.xls_function_builder_add_parameter(fb, 'x', t8)
    y = ib.xls_function_builder_add_parameter(fb, 'y', t8)
    eq = ib.xls_builder_base_add_eq(bb, x, y)
    fn = ib.xls_function_builder_build_with_return_value(fb, eq)
    jit = ca.xls_make_function_jit(fn)
    a = ca.xls_value_make_ubits(8, 5)
    b = ca.xls_value_make_ubits(8, 5)
    c = ca.xls_value_make_ubits(8, 6)
    r1 = ca.xls_function_jit_run(jit, [a, b])
    r2 = ca.xls_function_jit_run(jit, [a, c])
    assert ca.xls_bits_to_uint64(ca.xls_value_get_bits(r1)) == 1
    assert ca.xls_bits_to_uint64(ca.xls_value_get_bits(r2)) == 0


def test_binary_op_ne():
    pkg = ib.xls_package_create('test')
    t8 = ib.xls_package_get_bits_type(pkg, 8)
    fb = ib.xls_function_builder_create('ne_fn', pkg)
    bb = ib.xls_function_builder_as_builder_base(fb)
    x = ib.xls_function_builder_add_parameter(fb, 'x', t8)
    y = ib.xls_function_builder_add_parameter(fb, 'y', t8)
    ne = ib.xls_builder_base_add_ne(bb, x, y)
    fn = ib.xls_function_builder_build_with_return_value(fb, ne)
    jit = ca.xls_make_function_jit(fn)
    a = ca.xls_value_make_ubits(8, 5)
    b = ca.xls_value_make_ubits(8, 6)
    r = ca.xls_function_jit_run(jit, [a, b])
    assert ca.xls_bits_to_uint64(ca.xls_value_get_bits(r)) == 1


def test_binary_op_ult():
    pkg = ib.xls_package_create('test')
    t8 = ib.xls_package_get_bits_type(pkg, 8)
    fb = ib.xls_function_builder_create('ult_fn', pkg)
    bb = ib.xls_function_builder_as_builder_base(fb)
    x = ib.xls_function_builder_add_parameter(fb, 'x', t8)
    y = ib.xls_function_builder_add_parameter(fb, 'y', t8)
    cmp = ib.xls_builder_base_add_ult(bb, x, y)
    fn = ib.xls_function_builder_build_with_return_value(fb, cmp)
    jit = ca.xls_make_function_jit(fn)
    a = ca.xls_value_make_ubits(8, 3)
    b = ca.xls_value_make_ubits(8, 7)
    r = ca.xls_function_jit_run(jit, [a, b])
    assert ca.xls_bits_to_uint64(ca.xls_value_get_bits(r)) == 1


def test_binary_op_umul():
    pkg = ib.xls_package_create('test')
    t8 = ib.xls_package_get_bits_type(pkg, 8)
    fb = ib.xls_function_builder_create('mul_fn', pkg)
    bb = ib.xls_function_builder_as_builder_base(fb)
    x = ib.xls_function_builder_add_parameter(fb, 'x', t8)
    y = ib.xls_function_builder_add_parameter(fb, 'y', t8)
    prod = ib.xls_builder_base_add_umul(bb, x, y)
    fn = ib.xls_function_builder_build_with_return_value(fb, prod)
    jit = ca.xls_make_function_jit(fn)
    a = ca.xls_value_make_ubits(8, 3)
    b = ca.xls_value_make_ubits(8, 4)
    r = ca.xls_function_jit_run(jit, [a, b])
    assert ca.xls_bits_to_uint64(ca.xls_value_get_bits(r)) == 12


# ============================================================
# Unary operations
# ============================================================


def _run_unary_fn(fn_name, a_val, bit_width=8):
    pkg = ib.xls_package_create('test')
    t = ib.xls_package_get_bits_type(pkg, bit_width)
    fb = ib.xls_function_builder_create('unary_func', pkg)
    bb = ib.xls_function_builder_as_builder_base(fb)
    x = ib.xls_function_builder_add_parameter(fb, 'x', t)
    op = getattr(ib, f'xls_builder_base_add_{fn_name}')
    result = op(bb, x)
    built = ib.xls_function_builder_build_with_return_value(fb, result)
    jit = ca.xls_make_function_jit(built)
    av = ca.xls_value_make_ubits(bit_width, a_val)
    out = ca.xls_function_jit_run(jit, [av])
    bits = ca.xls_value_get_bits(out)
    return ca.xls_bits_to_uint64(bits)


def test_unary_not():
    # not(0b00001111) = 0b11110000 for 8-bit
    assert _run_unary_fn('not', 0b00001111) == 0b11110000


def test_unary_negate():
    # negate(1) = 255 (0xFF) in 8-bit 2's complement
    assert _run_unary_fn('negate', 1) == 255


def test_unary_and_reduce():
    # and_reduce(0xFF) = 1, and_reduce(0xFE) = 0
    assert _run_unary_fn('and_reduce', 0xFF) == 1
    assert _run_unary_fn('and_reduce', 0xFE) == 0


def test_unary_or_reduce():
    assert _run_unary_fn('or_reduce', 0) == 0
    assert _run_unary_fn('or_reduce', 1) == 1


def test_unary_xor_reduce():
    # xor_reduce(0b101) = 0, xor_reduce(0b110) = 0, xor_reduce(0b111) = 1
    assert _run_unary_fn('xor_reduce', 0b101) == 0  # even parity
    assert _run_unary_fn('xor_reduce', 0b001) == 1  # odd parity


def test_unary_identity():
    assert _run_unary_fn('identity', 42) == 42


def test_unary_clz():
    # count leading zeros of 0b00001000 = 4 leading zeros in 8-bit
    result = _run_unary_fn('clz', 0b00001000)
    assert result == 4


def test_unary_ctz():
    # count trailing zeros of 0b00001000 = 3 trailing zeros
    result = _run_unary_fn('ctz', 0b00001000)
    assert result == 3


def test_unary_reverse():
    # reverse(0b10000000) in 8-bit = 0b00000001
    assert _run_unary_fn('reverse', 0b10000000) == 0b00000001


# ============================================================
# Literal
# ============================================================


def test_literal():
    pkg = ib.xls_package_create('test')
    # t32 = ib.xls_package_get_bits_type(pkg, 32)
    fb = ib.xls_function_builder_create('lit_fn', pkg)
    bb = ib.xls_function_builder_as_builder_base(fb)
    val = ca.xls_value_make_ubits(32, 42)
    lit = ib.xls_builder_base_add_literal(bb, val)
    fn = ib.xls_function_builder_build_with_return_value(fb, lit)
    jit = ca.xls_make_function_jit(fn)
    result = ca.xls_function_jit_run(jit, [])
    bits = ca.xls_value_get_bits(result)
    assert ca.xls_bits_to_uint64(bits) == 42


# ============================================================
# Concat
# ============================================================


def test_concat():
    pkg = ib.xls_package_create('test')
    t8 = ib.xls_package_get_bits_type(pkg, 8)
    fb = ib.xls_function_builder_create('concat_fn', pkg)
    bb = ib.xls_function_builder_as_builder_base(fb)
    x = ib.xls_function_builder_add_parameter(fb, 'x', t8)
    y = ib.xls_function_builder_add_parameter(fb, 'y', t8)
    concat = ib.xls_builder_base_add_concat(bb, [x, y])
    fn = ib.xls_function_builder_build_with_return_value(fb, concat)
    jit = ca.xls_make_function_jit(fn)
    a = ca.xls_value_make_ubits(8, 0xAB)
    b = ca.xls_value_make_ubits(8, 0xCD)
    result = ca.xls_function_jit_run(jit, [a, b])
    bits = ca.xls_value_get_bits(result)
    val = ca.xls_bits_to_uint64(bits)
    # concat(0xAB, 0xCD) -> 0xABCD (x is high bits, y is low bits)
    assert val == 0xABCD


# ============================================================
# Tuple operations
# ============================================================


def test_tuple_operations():
    pkg = ib.xls_package_create('test')
    t8 = ib.xls_package_get_bits_type(pkg, 8)
    t16 = ib.xls_package_get_bits_type(pkg, 16)
    fb = ib.xls_function_builder_create('tuple_fn', pkg)
    bb = ib.xls_function_builder_as_builder_base(fb)
    x = ib.xls_function_builder_add_parameter(fb, 'x', t8)
    y = ib.xls_function_builder_add_parameter(fb, 'y', t16)
    tup = ib.xls_builder_base_add_tuple(bb, [x, y])
    # Extract index 0
    elem = ib.xls_builder_base_add_tuple_index(bb, tup, 0)
    fn = ib.xls_function_builder_build_with_return_value(fb, elem)
    jit = ca.xls_make_function_jit(fn)
    a = ca.xls_value_make_ubits(8, 77)
    b = ca.xls_value_make_ubits(16, 1234)
    result = ca.xls_function_jit_run(jit, [a, b])
    bits = ca.xls_value_get_bits(result)
    assert ca.xls_bits_to_uint64(bits) == 77


def test_tuple_index_1():
    pkg = ib.xls_package_create('test')
    t8 = ib.xls_package_get_bits_type(pkg, 8)
    t16 = ib.xls_package_get_bits_type(pkg, 16)
    fb = ib.xls_function_builder_create('tuple_fn2', pkg)
    bb = ib.xls_function_builder_as_builder_base(fb)
    x = ib.xls_function_builder_add_parameter(fb, 'x', t8)
    y = ib.xls_function_builder_add_parameter(fb, 'y', t16)
    tup = ib.xls_builder_base_add_tuple(bb, [x, y])
    elem = ib.xls_builder_base_add_tuple_index(bb, tup, 1)
    fn = ib.xls_function_builder_build_with_return_value(fb, elem)
    jit = ca.xls_make_function_jit(fn)
    a = ca.xls_value_make_ubits(8, 5)
    b = ca.xls_value_make_ubits(16, 9999)
    result = ca.xls_function_jit_run(jit, [a, b])
    bits = ca.xls_value_get_bits(result)
    assert ca.xls_bits_to_uint64(bits) == 9999


# ============================================================
# Array operations
# ============================================================


def test_array_creation_and_index():
    pkg = ib.xls_package_create('test')
    t8 = ib.xls_package_get_bits_type(pkg, 8)
    fb = ib.xls_function_builder_create('arr_fn', pkg)
    bb = ib.xls_function_builder_as_builder_base(fb)
    x = ib.xls_function_builder_add_parameter(fb, 'x', t8)
    y = ib.xls_function_builder_add_parameter(fb, 'y', t8)
    arr = ib.xls_builder_base_add_array(bb, t8, [x, y])
    idx_val = ca.xls_value_make_ubits(8, 0)
    idx_lit = ib.xls_builder_base_add_literal(bb, idx_val)
    elem = ib.xls_builder_base_add_array_index(bb, arr, [idx_lit], True)
    fn = ib.xls_function_builder_build_with_return_value(fb, elem)
    jit = ca.xls_make_function_jit(fn)
    a = ca.xls_value_make_ubits(8, 100)
    b = ca.xls_value_make_ubits(8, 200)
    result = ca.xls_function_jit_run(jit, [a, b])
    bits = ca.xls_value_get_bits(result)
    assert ca.xls_bits_to_uint64(bits) == 100


def test_array_update():
    pkg = ib.xls_package_create('test')
    t8 = ib.xls_package_get_bits_type(pkg, 8)
    fb = ib.xls_function_builder_create('arr_update', pkg)
    bb = ib.xls_function_builder_as_builder_base(fb)
    x = ib.xls_function_builder_add_parameter(fb, 'x', t8)
    y = ib.xls_function_builder_add_parameter(fb, 'y', t8)
    new_val = ib.xls_function_builder_add_parameter(fb, 'new', t8)
    arr = ib.xls_builder_base_add_array(bb, t8, [x, y])
    idx_val = ca.xls_value_make_ubits(8, 0)
    idx_lit = ib.xls_builder_base_add_literal(bb, idx_val)
    updated = ib.xls_builder_base_add_array_update(bb, arr, new_val, [idx_lit], True)
    # Index into updated array at 0
    elem = ib.xls_builder_base_add_array_index(bb, updated, [idx_lit], True)
    fn = ib.xls_function_builder_build_with_return_value(fb, elem)
    jit = ca.xls_make_function_jit(fn)
    a = ca.xls_value_make_ubits(8, 10)
    b = ca.xls_value_make_ubits(8, 20)
    new = ca.xls_value_make_ubits(8, 99)
    result = ca.xls_function_jit_run(jit, [a, b, new])
    bits = ca.xls_value_get_bits(result)
    assert ca.xls_bits_to_uint64(bits) == 99


def test_array_slice():
    pkg = ib.xls_package_create('test')
    t8 = ib.xls_package_get_bits_type(pkg, 8)
    fb = ib.xls_function_builder_create('arr_slice', pkg)
    bb = ib.xls_function_builder_as_builder_base(fb)
    # Build array [a, b, c, d]
    a = ib.xls_function_builder_add_parameter(fb, 'a', t8)
    b = ib.xls_function_builder_add_parameter(fb, 'b', t8)
    c = ib.xls_function_builder_add_parameter(fb, 'c', t8)
    d = ib.xls_function_builder_add_parameter(fb, 'd', t8)
    arr = ib.xls_builder_base_add_array(bb, t8, [a, b, c, d])
    start_val = ca.xls_value_make_ubits(8, 1)
    start = ib.xls_builder_base_add_literal(bb, start_val)
    sliced = ib.xls_builder_base_add_array_slice(bb, arr, start, 2)
    fn = ib.xls_function_builder_build_with_return_value(fb, sliced)
    assert fn is not None


# ============================================================
# Bit slice
# ============================================================


def test_bit_slice():
    pkg = ib.xls_package_create('test')
    t16 = ib.xls_package_get_bits_type(pkg, 16)
    fb = ib.xls_function_builder_create('bslice_fn', pkg)
    bb = ib.xls_function_builder_as_builder_base(fb)
    x = ib.xls_function_builder_add_parameter(fb, 'x', t16)
    # Take bits [4:8) = 4 bits starting at bit 4
    sliced = ib.xls_builder_base_add_bit_slice(bb, x, 4, 4)
    fn = ib.xls_function_builder_build_with_return_value(fb, sliced)
    jit = ca.xls_make_function_jit(fn)
    # Input 0b0000_1111_0000_0000 = 0x0F00
    # bits[4:8) = 0b1111 = 0xF
    val = ca.xls_value_make_ubits(16, 0x00F0)
    result = ca.xls_function_jit_run(jit, [val])
    bits = ca.xls_value_get_bits(result)
    assert ca.xls_bits_to_uint64(bits) == 0xF


def test_zero_extend():
    pkg = ib.xls_package_create('test')
    t8 = ib.xls_package_get_bits_type(pkg, 8)
    fb = ib.xls_function_builder_create('zext', pkg)
    bb = ib.xls_function_builder_as_builder_base(fb)
    x = ib.xls_function_builder_add_parameter(fb, 'x', t8)
    extended = ib.xls_builder_base_add_zero_extend(bb, x, 32)
    fn = ib.xls_function_builder_build_with_return_value(fb, extended)
    jit = ca.xls_make_function_jit(fn)
    val = ca.xls_value_make_ubits(8, 255)
    result = ca.xls_function_jit_run(jit, [val])
    bits = ca.xls_value_get_bits(result)
    assert ca.xls_bits_to_uint64(bits) == 255
    assert ca.xls_bits_get_bit_count(bits) == 32


def test_sign_extend():
    pkg = ib.xls_package_create('test')
    t8 = ib.xls_package_get_bits_type(pkg, 8)
    fb = ib.xls_function_builder_create('sext', pkg)
    bb = ib.xls_function_builder_as_builder_base(fb)
    x = ib.xls_function_builder_add_parameter(fb, 'x', t8)
    extended = ib.xls_builder_base_add_sign_extend(bb, x, 16)
    fn = ib.xls_function_builder_build_with_return_value(fb, extended)
    jit = ca.xls_make_function_jit(fn)
    # -1 in 8-bit should sign extend to -1 in 16-bit
    val = ca.xls_value_make_sbits(8, -1)
    result = ca.xls_function_jit_run(jit, [val])
    bits = ca.xls_value_get_bits(result)
    assert ca.xls_bits_to_int64(bits) == -1
    assert ca.xls_bits_get_bit_count(bits) == 16


# ============================================================
# Select operation
# ============================================================


def test_select():
    pkg = ib.xls_package_create('test')
    t1 = ib.xls_package_get_bits_type(pkg, 1)
    t8 = ib.xls_package_get_bits_type(pkg, 8)
    fb = ib.xls_function_builder_create('sel_fn', pkg)
    bb = ib.xls_function_builder_as_builder_base(fb)
    sel = ib.xls_function_builder_add_parameter(fb, 's', t1)
    a = ib.xls_function_builder_add_parameter(fb, 'a', t8)
    b = ib.xls_function_builder_add_parameter(fb, 'b', t8)
    result = ib.xls_builder_base_add_select(bb, sel, [a, b])
    fn = ib.xls_function_builder_build_with_return_value(fb, result)
    jit = ca.xls_make_function_jit(fn)
    s0 = ca.xls_value_make_ubits(1, 0)
    s1 = ca.xls_value_make_ubits(1, 1)
    av = ca.xls_value_make_ubits(8, 10)
    bv = ca.xls_value_make_ubits(8, 20)
    r0 = ca.xls_function_jit_run(jit, [s0, av, bv])
    r1 = ca.xls_function_jit_run(jit, [s1, av, bv])
    assert ca.xls_bits_to_uint64(ca.xls_value_get_bits(r0)) == 10
    assert ca.xls_bits_to_uint64(ca.xls_value_get_bits(r1)) == 20


# ============================================================
# One-hot operation
# ============================================================


def test_one_hot():
    pkg = ib.xls_package_create('test')
    t4 = ib.xls_package_get_bits_type(pkg, 4)
    fb = ib.xls_function_builder_create('oh_fn', pkg)
    bb = ib.xls_function_builder_as_builder_base(fb)
    x = ib.xls_function_builder_add_parameter(fb, 'x', t4)
    oh = ib.xls_builder_base_add_one_hot(bb, x, True)
    fn = ib.xls_function_builder_build_with_return_value(fb, oh)
    jit = ca.xls_make_function_jit(fn)
    # Input 0b0001 (lowest bit set): one_hot with LSB priority -> position 0
    val = ca.xls_value_make_ubits(4, 0b0001)
    result = ca.xls_function_jit_run(jit, [val])
    bits = ca.xls_value_get_bits(result)
    assert ca.xls_bits_to_uint64(bits) == 1  # bit 0 set


def test_one_hot_zero():
    pkg = ib.xls_package_create('test')
    t4 = ib.xls_package_get_bits_type(pkg, 4)
    fb = ib.xls_function_builder_create('oh_zero', pkg)
    bb = ib.xls_function_builder_as_builder_base(fb)
    x = ib.xls_function_builder_add_parameter(fb, 'x', t4)
    oh = ib.xls_builder_base_add_one_hot(bb, x, True)
    fn = ib.xls_function_builder_build_with_return_value(fb, oh)
    jit = ca.xls_make_function_jit(fn)
    # Input 0: no bit set, so highest bit (the "no match" bit) is set
    val = ca.xls_value_make_ubits(4, 0)
    result = ca.xls_function_jit_run(jit, [val])
    bits = ca.xls_value_get_bits(result)
    assert ca.xls_bits_get_bit_count(bits) == 5  # one_hot output is n+1 bits


# ============================================================
# Builder type introspection
# ============================================================


def test_builder_get_type():
    pkg = ib.xls_package_create('test')
    t32 = ib.xls_package_get_bits_type(pkg, 32)
    fb = ib.xls_function_builder_create('fn', pkg)
    bb = ib.xls_function_builder_as_builder_base(fb)
    x = ib.xls_function_builder_add_parameter(fb, 'x', t32)
    t = ib.xls_builder_base_get_type(bb, x)
    assert ca.xls_type_to_string(t) == 'bits[32]'


def test_builder_get_last_value():
    pkg = ib.xls_package_create('test')
    t8 = ib.xls_package_get_bits_type(pkg, 8)
    fb = ib.xls_function_builder_create('fn', pkg)
    bb = ib.xls_function_builder_as_builder_base(fb)
    x = ib.xls_function_builder_add_parameter(fb, 'x', t8)
    y = ib.xls_function_builder_add_parameter(fb, 'y', t8)
    ib.xls_builder_base_add_add(bb, x, y)
    last = ib.xls_builder_base_get_last_value(bb)
    assert last is not None
