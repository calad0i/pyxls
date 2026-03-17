"""Tests for xls.raw.vast bindings."""

import xls.raw as raw

va = raw.vast
ca = raw.c_api


def make_sv_file():
    """Helper: create a SystemVerilog file."""
    return va.xls_vast_make_verilog_file(va.FileType.SYSTEM_VERILOG)


def make_v_file():
    """Helper: create a Verilog file."""
    return va.xls_vast_make_verilog_file(va.FileType.VERILOG)


# ============================================================
# VerilogFile creation
# ============================================================


def test_make_verilog_file_sv():
    vf = va.xls_vast_make_verilog_file(va.FileType.SYSTEM_VERILOG)
    assert vf is not None
    assert isinstance(vf, raw.VastVerilogFile)


def test_make_verilog_file_v():
    vf = va.xls_vast_make_verilog_file(va.FileType.VERILOG)
    assert vf is not None


def test_verilog_file_emit_empty():
    vf = make_sv_file()
    s = va.xls_vast_verilog_file_emit(vf)
    assert isinstance(s, str)


# ============================================================
# Module creation
# ============================================================


def test_add_module():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'my_module')
    assert mod is not None
    assert isinstance(mod, raw.VastVerilogModule)


def test_module_get_name():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'test_mod')
    name = va.xls_vast_verilog_module_get_name(mod)
    assert name == 'test_mod'


def test_emit_empty_module():
    vf = make_sv_file()
    _ = va.xls_vast_verilog_file_add_module(vf, 'empty_mod')
    s = va.xls_vast_verilog_file_emit(vf)
    assert 'empty_mod' in s


def test_multiple_modules():
    vf = make_sv_file()
    _ = va.xls_vast_verilog_file_add_module(vf, 'module_a')
    _ = va.xls_vast_verilog_file_add_module(vf, 'module_b')
    s = va.xls_vast_verilog_file_emit(vf)
    assert 'module_a' in s
    assert 'module_b' in s


# ============================================================
# Data types
# ============================================================


def test_make_scalar_type():
    vf = make_sv_file()
    t = va.xls_vast_verilog_file_make_scalar_type(vf)
    assert t is not None
    assert isinstance(t, raw.VastDataType)


def test_make_bit_vector_type():
    vf = make_sv_file()
    t = va.xls_vast_verilog_file_make_bit_vector_type(vf, 8, False)
    assert t is not None
    assert isinstance(t, raw.VastDataType)


def test_make_bit_vector_type_signed():
    vf = make_sv_file()
    t = va.xls_vast_verilog_file_make_bit_vector_type(vf, 16, True)
    assert va.xls_vast_data_type_is_signed(t)


def test_make_bit_vector_type_unsigned():
    vf = make_sv_file()
    t = va.xls_vast_verilog_file_make_bit_vector_type(vf, 16, False)
    assert not va.xls_vast_data_type_is_signed(t)


def test_data_type_flat_bit_count():
    vf = make_sv_file()
    t = va.xls_vast_verilog_file_make_bit_vector_type(vf, 16, False)
    count = va.xls_vast_data_type_flat_bit_count_as_int64(t)
    assert count == 16


def test_data_type_width_as_int64():
    vf = make_sv_file()
    t = va.xls_vast_verilog_file_make_bit_vector_type(vf, 8, False)
    w = va.xls_vast_data_type_width_as_int64(t)
    assert w == 8


# ============================================================
# Ports
# ============================================================


def test_add_input_output():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'io_mod')
    t8 = va.xls_vast_verilog_file_make_bit_vector_type(vf, 8, False)
    inp = va.xls_vast_verilog_module_add_input(mod, 'data_in', t8)
    out = va.xls_vast_verilog_module_add_output(mod, 'data_out', t8)
    assert inp is not None
    assert out is not None
    s = va.xls_vast_verilog_file_emit(vf)
    assert 'data_in' in s
    assert 'data_out' in s


def test_add_logic_input_output():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'logic_mod')
    t = va.xls_vast_verilog_file_make_bit_vector_type(vf, 4, False)
    li = va.xls_vast_verilog_module_add_logic_input(mod, 'a', t)
    lo = va.xls_vast_verilog_module_add_logic_output(mod, 'b', t)
    assert li is not None
    assert lo is not None


def test_add_wire():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'wire_mod')
    t = va.xls_vast_verilog_file_make_bit_vector_type(vf, 8, False)
    wire = va.xls_vast_verilog_module_add_wire(mod, 'my_wire', t)
    assert wire is not None
    s = va.xls_vast_verilog_file_emit(vf)
    assert 'my_wire' in s


def test_module_get_ports():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'port_mod')
    t = va.xls_vast_verilog_file_make_bit_vector_type(vf, 8, False)
    va.xls_vast_verilog_module_add_input(mod, 'a', t)
    va.xls_vast_verilog_module_add_output(mod, 'b', t)
    ports = va.xls_vast_verilog_module_get_ports(mod)
    assert isinstance(ports, list)
    assert len(ports) == 2


def test_port_get_direction():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'dir_mod')
    t = va.xls_vast_verilog_file_make_scalar_type(vf)
    va.xls_vast_verilog_module_add_input(mod, 'in_sig', t)
    va.xls_vast_verilog_module_add_output(mod, 'out_sig', t)
    ports = va.xls_vast_verilog_module_get_ports(mod)
    directions = {va.xls_vast_verilog_module_port_get_direction(p) for p in ports}
    assert va.ModulePortDirection.INPUT in directions
    assert va.ModulePortDirection.OUTPUT in directions


def test_logic_ref_get_name():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'lr_mod')
    t = va.xls_vast_verilog_file_make_scalar_type(vf)
    lr = va.xls_vast_verilog_module_add_input(mod, 'named_sig', t)
    name = va.xls_vast_logic_ref_get_name(lr)
    assert name == 'named_sig'


# ============================================================
# Literals
# ============================================================


def test_make_plain_literal():
    vf = make_sv_file()
    lit = va.xls_vast_verilog_file_make_plain_literal(vf, 42)
    assert lit is not None
    assert isinstance(lit, raw.VastLiteral)


def test_make_literal_with_bits():
    vf = make_sv_file()
    bits = ca.xls_bits_make_ubits(8, 0xAB)
    lit = va.xls_vast_verilog_file_make_literal(vf, bits, ca.FormatPreference.HEX, True)
    assert lit is not None


def test_literal_as_expression():
    vf = make_sv_file()
    lit = va.xls_vast_verilog_file_make_plain_literal(vf, 10)
    expr = va.xls_vast_literal_as_expression(lit)
    assert expr is not None
    assert isinstance(expr, raw.VastExpression)


def test_expression_emit_literal():
    vf = make_sv_file()
    lit = va.xls_vast_verilog_file_make_plain_literal(vf, 99)
    expr = va.xls_vast_literal_as_expression(lit)
    s = va.xls_vast_expression_emit(expr)
    assert '99' in s


def test_make_unsized_zero_literal():
    vf = make_sv_file()
    expr = va.xls_vast_verilog_file_make_unsized_zero_literal(vf)
    assert expr is not None
    s = va.xls_vast_expression_emit(expr)
    assert '0' in s


def test_make_unsized_one_literal():
    vf = make_sv_file()
    expr = va.xls_vast_verilog_file_make_unsized_one_literal(vf)
    assert expr is not None
    s = va.xls_vast_expression_emit(expr)
    assert '1' in s


# ============================================================
# LogicRef as expression
# ============================================================


def test_logic_ref_as_expression():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'expr_mod')
    t = va.xls_vast_verilog_file_make_scalar_type(vf)
    lr = va.xls_vast_verilog_module_add_input(mod, 'sig', t)
    expr = va.xls_vast_logic_ref_as_expression(lr)
    assert expr is not None
    assert isinstance(expr, raw.VastExpression)
    s = va.xls_vast_expression_emit(expr)
    assert 'sig' in s


def test_logic_ref_as_indexable_expression():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'idx_mod')
    t = va.xls_vast_verilog_file_make_bit_vector_type(vf, 8, False)
    lr = va.xls_vast_verilog_module_add_input(mod, 'vec', t)
    idx_expr = va.xls_vast_logic_ref_as_indexable_expression(lr)
    assert idx_expr is not None


# ============================================================
# Binary and Unary operators
# ============================================================


def test_make_binary_op():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'binop_mod')
    t = va.xls_vast_verilog_file_make_bit_vector_type(vf, 8, False)
    lr_a = va.xls_vast_verilog_module_add_input(mod, 'a', t)
    lr_b = va.xls_vast_verilog_module_add_input(mod, 'b', t)
    expr_a = va.xls_vast_logic_ref_as_expression(lr_a)
    expr_b = va.xls_vast_logic_ref_as_expression(lr_b)
    add_expr = va.xls_vast_verilog_file_make_binary(vf, expr_a, expr_b, va.OperatorKind.ADD)
    assert add_expr is not None
    s = va.xls_vast_expression_emit(add_expr)
    assert 'a' in s
    assert 'b' in s


def test_make_binary_op_and():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'and_mod')
    t = va.xls_vast_verilog_file_make_scalar_type(vf)
    lr_a = va.xls_vast_verilog_module_add_input(mod, 'x', t)
    lr_b = va.xls_vast_verilog_module_add_input(mod, 'y', t)
    ea = va.xls_vast_logic_ref_as_expression(lr_a)
    eb = va.xls_vast_logic_ref_as_expression(lr_b)
    expr = va.xls_vast_verilog_file_make_binary(vf, ea, eb, va.OperatorKind.BITWISE_AND)
    s = va.xls_vast_expression_emit(expr)
    assert '&' in s


def test_make_unary_op():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'unop_mod')
    t = va.xls_vast_verilog_file_make_scalar_type(vf)
    lr = va.xls_vast_verilog_module_add_input(mod, 'sig', t)
    expr = va.xls_vast_logic_ref_as_expression(lr)
    not_expr = va.xls_vast_verilog_file_make_unary(vf, expr, va.OperatorKind.BITWISE_NOT)
    assert not_expr is not None
    s = va.xls_vast_expression_emit(not_expr)
    assert '~' in s or '!' in s or 'sig' in s


def test_make_ternary():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'tern_mod')
    t = va.xls_vast_verilog_file_make_scalar_type(vf)
    cond = va.xls_vast_logic_ref_as_expression(va.xls_vast_verilog_module_add_input(mod, 'cond', t))
    cons = va.xls_vast_logic_ref_as_expression(va.xls_vast_verilog_module_add_input(mod, 'true_val', t))
    alt = va.xls_vast_logic_ref_as_expression(va.xls_vast_verilog_module_add_input(mod, 'false_val', t))
    tern = va.xls_vast_verilog_file_make_ternary(vf, cond, cons, alt)
    assert tern is not None
    s = va.xls_vast_expression_emit(tern)
    assert '?' in s
    assert ':' in s


# ============================================================
# Continuous assignment
# ============================================================


def test_make_continuous_assignment():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'assign_mod')
    t = va.xls_vast_verilog_file_make_bit_vector_type(vf, 8, False)
    inp = va.xls_vast_verilog_module_add_input(mod, 'data_in', t)
    out = va.xls_vast_verilog_module_add_output(mod, 'data_out', t)
    lhs = va.xls_vast_logic_ref_as_expression(out)
    rhs = va.xls_vast_logic_ref_as_expression(inp)
    assign = va.xls_vast_verilog_file_make_continuous_assignment(vf, lhs, rhs)
    assert assign is not None
    va.xls_vast_verilog_module_add_member_continuous_assignment(mod, assign)
    s = va.xls_vast_verilog_file_emit(vf)
    assert 'assign' in s
    assert 'data_out' in s
    assert 'data_in' in s


# ============================================================
# always_comb
# ============================================================


def test_always_comb():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'comb_mod')
    ab = va.xls_vast_verilog_module_add_always_comb(mod)
    assert ab is not None
    assert isinstance(ab, raw.VastAlwaysBase)
    s = va.xls_vast_verilog_file_emit(vf)
    assert 'always_comb' in s


def test_always_comb_with_assignment():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'comb_assign')
    t = va.xls_vast_verilog_file_make_bit_vector_type(vf, 8, False)
    inp = va.xls_vast_verilog_module_add_input(mod, 'in_sig', t)
    out = va.xls_vast_verilog_module_add_output(mod, 'out_sig', t)
    ab = va.xls_vast_verilog_module_add_always_comb(mod)
    block = va.xls_vast_always_base_get_statement_block(ab)
    lhs = va.xls_vast_logic_ref_as_expression(out)
    rhs = va.xls_vast_logic_ref_as_expression(inp)
    va.xls_vast_statement_block_add_blocking_assignment(block, lhs, rhs)
    s = va.xls_vast_verilog_file_emit(vf)
    assert 'always_comb' in s
    assert 'out_sig' in s
    assert 'in_sig' in s


# ============================================================
# always_ff
# ============================================================


def test_always_ff():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'ff_mod')
    t = va.xls_vast_verilog_file_make_scalar_type(vf)
    clk = va.xls_vast_verilog_module_add_input(mod, 'clk', t)
    clk_expr = va.xls_vast_logic_ref_as_expression(clk)
    posedge = va.xls_vast_verilog_file_make_pos_edge(vf, clk_expr)
    ab = va.xls_vast_verilog_module_add_always_ff(mod, [posedge])
    assert ab is not None
    s = va.xls_vast_verilog_file_emit(vf)
    assert 'always_ff' in s
    assert 'posedge' in s


# ============================================================
# Statement block assignments
# ============================================================


def test_statement_block_nonblocking():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'nb_mod')
    t = va.xls_vast_verilog_file_make_bit_vector_type(vf, 8, False)
    # clk = va.xls_vast_verilog_module_add_input(mod, 'clk', t)
    inp = va.xls_vast_verilog_module_add_input(mod, 'd', t)
    out = va.xls_vast_verilog_module_add_output(mod, 'q', t)
    clk_expr = va.xls_vast_logic_ref_as_expression(
        va.xls_vast_verilog_module_add_input(mod, 'clk2', va.xls_vast_verilog_file_make_scalar_type(vf))
    )
    posedge = va.xls_vast_verilog_file_make_pos_edge(vf, clk_expr)
    ab = va.xls_vast_verilog_module_add_always_ff(mod, [posedge])
    block = va.xls_vast_always_base_get_statement_block(ab)
    lhs = va.xls_vast_logic_ref_as_expression(out)
    rhs = va.xls_vast_logic_ref_as_expression(inp)
    stmt = va.xls_vast_statement_block_add_nonblocking_assignment(block, lhs, rhs)
    assert stmt is not None
    s = va.xls_vast_verilog_file_emit(vf)
    assert '<=' in s


def test_statement_block_blocking():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'b_mod')
    t = va.xls_vast_verilog_file_make_bit_vector_type(vf, 8, False)
    ab = va.xls_vast_verilog_module_add_always_comb(mod)
    block = va.xls_vast_always_base_get_statement_block(ab)
    inp = va.xls_vast_verilog_module_add_input(mod, 'src', t)
    out = va.xls_vast_verilog_module_add_output(mod, 'dst', t)
    lhs = va.xls_vast_logic_ref_as_expression(out)
    rhs = va.xls_vast_logic_ref_as_expression(inp)
    stmt = va.xls_vast_statement_block_add_blocking_assignment(block, lhs, rhs)
    assert stmt is not None
    s = va.xls_vast_verilog_file_emit(vf)
    assert '=' in s


# ============================================================
# Conditional
# ============================================================


def test_conditional():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'cond_mod')
    t = va.xls_vast_verilog_file_make_bit_vector_type(vf, 8, False)
    t1 = va.xls_vast_verilog_file_make_scalar_type(vf)
    sel = va.xls_vast_verilog_module_add_input(mod, 'sel', t1)
    a_sig = va.xls_vast_verilog_module_add_input(mod, 'a', t)
    b_sig = va.xls_vast_verilog_module_add_input(mod, 'b', t)
    out = va.xls_vast_verilog_module_add_output(mod, 'out', t)
    ab = va.xls_vast_verilog_module_add_always_comb(mod)
    block = va.xls_vast_always_base_get_statement_block(ab)
    cond_expr = va.xls_vast_logic_ref_as_expression(sel)
    cond = va.xls_vast_statement_block_add_conditional(block, cond_expr)
    then_block = va.xls_vast_conditional_get_then_block(cond)
    assert then_block is not None
    lhs = va.xls_vast_logic_ref_as_expression(out)
    rhs_a = va.xls_vast_logic_ref_as_expression(a_sig)
    va.xls_vast_statement_block_add_blocking_assignment(then_block, lhs, rhs_a)
    else_block = va.xls_vast_conditional_add_else(cond)
    rhs_b = va.xls_vast_logic_ref_as_expression(b_sig)
    va.xls_vast_statement_block_add_blocking_assignment(else_block, lhs, rhs_b)
    s = va.xls_vast_verilog_file_emit(vf)
    assert 'if' in s
    assert 'else' in s


def test_conditional_else_if():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'elseif_mod')
    t1 = va.xls_vast_verilog_file_make_scalar_type(vf)
    s1 = va.xls_vast_verilog_module_add_input(mod, 's1', t1)
    s2 = va.xls_vast_verilog_module_add_input(mod, 's2', t1)
    ab = va.xls_vast_verilog_module_add_always_comb(mod)
    block = va.xls_vast_always_base_get_statement_block(ab)
    c1 = va.xls_vast_logic_ref_as_expression(s1)
    cond = va.xls_vast_statement_block_add_conditional(block, c1)
    c2 = va.xls_vast_logic_ref_as_expression(s2)
    elif_block = va.xls_vast_conditional_add_else_if(cond, c2)
    assert elif_block is not None
    s = va.xls_vast_verilog_file_emit(vf)
    assert 'if' in s


# ============================================================
# Case statement
# ============================================================


def test_case_statement():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'case_mod')
    t = va.xls_vast_verilog_file_make_bit_vector_type(vf, 2, False)
    sel = va.xls_vast_verilog_module_add_input(mod, 'sel', t)
    ab = va.xls_vast_verilog_module_add_always_comb(mod)
    block = va.xls_vast_always_base_get_statement_block(ab)
    sel_expr = va.xls_vast_logic_ref_as_expression(sel)
    case = va.xls_vast_statement_block_add_case(block, sel_expr)
    assert case is not None
    # Add item for value 0
    zero_lit = va.xls_vast_verilog_file_make_plain_literal(vf, 0)
    zero_expr = va.xls_vast_literal_as_expression(zero_lit)
    item_block = va.xls_vast_case_statement_add_item(case, zero_expr)
    assert item_block is not None
    # Add default
    default_block = va.xls_vast_case_statement_add_default(case)
    assert default_block is not None
    s = va.xls_vast_verilog_file_emit(vf)
    assert 'case' in s


# ============================================================
# Generate loop
# ============================================================


def test_generate_loop():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'gen_mod')
    zero = va.xls_vast_verilog_file_make_plain_literal(vf, 0)
    eight = va.xls_vast_verilog_file_make_plain_literal(vf, 8)
    init_expr = va.xls_vast_literal_as_expression(zero)
    limit_expr = va.xls_vast_literal_as_expression(eight)
    loop = va.xls_vast_verilog_module_add_generate_loop(mod, 'i', init_expr, limit_expr, 'gen_label')
    assert loop is not None
    assert isinstance(loop, raw.VastGenerateLoop)
    genvar = va.xls_vast_generate_loop_get_genvar(loop)
    assert genvar is not None


def test_generate_loop_genvar_name():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'gen_mod2')
    zero = va.xls_vast_literal_as_expression(va.xls_vast_verilog_file_make_plain_literal(vf, 0))
    limit = va.xls_vast_literal_as_expression(va.xls_vast_verilog_file_make_plain_literal(vf, 4))
    loop = va.xls_vast_verilog_module_add_generate_loop(mod, 'idx', zero, limit, 'lbl')
    genvar = va.xls_vast_generate_loop_get_genvar(loop)
    name = va.xls_vast_logic_ref_get_name(genvar)
    assert name == 'idx'


# ============================================================
# Macro reference
# ============================================================


def test_macro_ref():
    vf = make_sv_file()
    macro = va.xls_vast_verilog_file_make_macro_ref(vf, 'MY_MACRO')
    assert macro is not None
    assert isinstance(macro, raw.VastMacroRef)


def test_macro_ref_as_expression():
    vf = make_sv_file()
    macro = va.xls_vast_verilog_file_make_macro_ref(vf, 'SOME_MACRO')
    expr = va.xls_vast_macro_ref_as_expression(macro)
    assert expr is not None
    s = va.xls_vast_expression_emit(expr)
    assert 'SOME_MACRO' in s


def test_macro_statement():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'macro_mod')
    macro = va.xls_vast_verilog_file_make_macro_ref(vf, 'MY_MACRO')
    stmt = va.xls_vast_verilog_file_make_macro_statement(vf, macro, True)
    assert stmt is not None
    va.xls_vast_verilog_module_add_member_macro_statement(mod, stmt)
    s = va.xls_vast_verilog_file_emit(vf)
    assert 'MY_MACRO' in s


# ============================================================
# Concat
# ============================================================


def test_concat():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'concat_mod')
    t = va.xls_vast_verilog_file_make_bit_vector_type(vf, 4, False)
    lr_a = va.xls_vast_verilog_module_add_input(mod, 'a_sig', t)
    lr_b = va.xls_vast_verilog_module_add_input(mod, 'b_sig', t)
    ea = va.xls_vast_logic_ref_as_expression(lr_a)
    eb = va.xls_vast_logic_ref_as_expression(lr_b)
    cat = va.xls_vast_verilog_file_make_concat(vf, [ea, eb])
    assert cat is not None
    assert isinstance(cat, raw.VastConcat)
    expr = va.xls_vast_concat_as_expression(cat)
    s = va.xls_vast_expression_emit(expr)
    assert '{' in s
    assert 'a_sig' in s
    assert 'b_sig' in s


def test_concat_as_expression():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'cat_expr_mod')
    t = va.xls_vast_verilog_file_make_scalar_type(vf)
    lr = va.xls_vast_verilog_module_add_input(mod, 'x', t)
    expr = va.xls_vast_logic_ref_as_expression(lr)
    cat = va.xls_vast_verilog_file_make_concat(vf, [expr])
    as_expr = va.xls_vast_concat_as_expression(cat)
    assert isinstance(as_expr, raw.VastExpression)


# ============================================================
# Parameters and localparams
# ============================================================


def test_add_parameter():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'param_mod')
    lit = va.xls_vast_literal_as_expression(va.xls_vast_verilog_file_make_plain_literal(vf, 8))
    param = va.xls_vast_verilog_module_add_parameter(mod, 'WIDTH', lit)
    assert param is not None


def test_add_localparam():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'lp_mod')
    lit = va.xls_vast_literal_as_expression(va.xls_vast_verilog_file_make_plain_literal(vf, 16))
    lp = va.xls_vast_verilog_module_add_localparam(mod, 'DEPTH', lit)
    assert lp is not None
    s = va.xls_vast_verilog_file_emit(vf)
    assert 'localparam' in s


# ============================================================
# Comments and blank lines
# ============================================================


def test_add_comment_to_module():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'comment_mod')
    comment = va.xls_vast_verilog_file_make_comment(vf, 'This is a comment')
    va.xls_vast_verilog_module_add_member_comment(mod, comment)
    s = va.xls_vast_verilog_file_emit(vf)
    assert 'This is a comment' in s


def test_add_blank_line_to_module():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'blank_mod')
    blank = va.xls_vast_verilog_file_make_blank_line(vf)
    va.xls_vast_verilog_module_add_member_blank_line(mod, blank)
    s = va.xls_vast_verilog_file_emit(vf)
    assert s is not None


# ============================================================
# Def operations
# ============================================================


def test_def_get_name():
    vf = make_sv_file()
    mod = va.xls_vast_verilog_file_add_module(vf, 'def_mod')
    t = va.xls_vast_verilog_file_make_bit_vector_type(vf, 8, False)
    _ = va.xls_vast_verilog_module_add_input(mod, 'port_name', t)
    ports = va.xls_vast_verilog_module_get_ports(mod)
    assert len(ports) > 0
    defn = va.xls_vast_verilog_module_port_get_def(ports[0])
    name = va.xls_vast_def_get_name(defn)
    assert name == 'port_name'


def test_file_type_enum():
    assert va.FileType.VERILOG != va.FileType.SYSTEM_VERILOG


def test_operator_kind_enum():
    assert va.OperatorKind.ADD != va.OperatorKind.SUB
    assert va.OperatorKind.BITWISE_AND != va.OperatorKind.BITWISE_OR
