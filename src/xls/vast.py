"""Pythonic wrapper classes and functions for xls.raw.vast."""

from __future__ import annotations

from collections.abc import Sequence

from xls import raw
from xls._wrap import maybe_unwrap, maybe_wrap, register_wrapper, wrap_module


@register_wrapper(raw.VastVerilogFile)
class VerilogFile:
    """Wrapper around raw.VastVerilogFile."""

    def __init__(self, _raw: raw.VastVerilogFile):
        self._raw = _raw

    @classmethod
    def create(cls, file_type=None) -> VerilogFile:
        """Create a new VerilogFile. file_type defaults to VERILOG."""
        if file_type is None:
            file_type = raw.vast.FileType.VERILOG
        raw_ft = maybe_unwrap(file_type)
        result = raw.vast.xls_vast_make_verilog_file(raw_ft)
        obj = object.__new__(cls)
        obj._raw = result
        return obj

    def emit(self) -> str:
        """Emit the Verilog text."""
        return raw.vast.xls_vast_verilog_file_emit(self._raw)

    def add_module(self, name: str) -> VerilogModule:
        result = raw.vast.xls_vast_verilog_file_add_module(self._raw, name)
        return maybe_wrap(result)

    def make_scalar_type(self) -> DataType:
        result = raw.vast.xls_vast_verilog_file_make_scalar_type(self._raw)
        return maybe_wrap(result)

    def make_bit_vector_type(self, width, is_signed: bool = False) -> DataType:
        raw_width = maybe_unwrap(width)
        result = raw.vast.xls_vast_verilog_file_make_bit_vector_type(self._raw, raw_width, is_signed)
        return maybe_wrap(result)

    def make_integer_type(self) -> DataType:
        result = raw.vast.xls_vast_verilog_file_make_integer_type(self._raw)
        return maybe_wrap(result)

    def make_plain_literal(self, value: int) -> Expression:
        result = raw.vast.xls_vast_verilog_file_make_plain_literal(self._raw, value)
        return maybe_wrap(result)

    def make_literal(self, value, format_pref=None) -> Expression:
        raw_val = maybe_unwrap(value)
        if format_pref is None:
            result = raw.vast.xls_vast_verilog_file_make_plain_literal(self._raw, raw_val)
        else:
            result = raw.vast.xls_vast_verilog_file_make_literal(self._raw, raw_val, maybe_unwrap(format_pref))
        return maybe_wrap(result)

    def make_unary(self, op, operand) -> Expression:
        raw_op = maybe_unwrap(op)
        raw_operand = maybe_unwrap(operand)
        result = raw.vast.xls_vast_verilog_file_make_unary(self._raw, raw_op, raw_operand)
        return maybe_wrap(result)

    def make_binary(self, op, lhs, rhs) -> Expression:
        raw_op = maybe_unwrap(op)
        raw_lhs = maybe_unwrap(lhs)
        raw_rhs = maybe_unwrap(rhs)
        result = raw.vast.xls_vast_verilog_file_make_binary(self._raw, raw_op, raw_lhs, raw_rhs)
        return maybe_wrap(result)

    def make_ternary(self, cond, lhs, rhs) -> Expression:
        result = raw.vast.xls_vast_verilog_file_make_ternary(self._raw, maybe_unwrap(cond), maybe_unwrap(lhs), maybe_unwrap(rhs))
        return maybe_wrap(result)

    def make_concat(self, parts: list[Expression]) -> Expression:
        raw_parts = [maybe_unwrap(p) for p in parts]
        result = raw.vast.xls_vast_verilog_file_make_concat(self._raw, raw_parts)
        return maybe_wrap(result)

    def make_index_i64(self, subject, index: int) -> Expression:
        result = raw.vast.xls_vast_verilog_file_make_index_i64(self._raw, maybe_unwrap(subject), index)
        return maybe_wrap(result)

    def make_index(self, subject, index) -> Expression:
        result = raw.vast.xls_vast_verilog_file_make_index(self._raw, maybe_unwrap(subject), maybe_unwrap(index))
        return maybe_wrap(result)

    def make_slice_i64(self, subject, hi: int, lo: int) -> Expression:
        result = raw.vast.xls_vast_verilog_file_make_slice_i64(self._raw, maybe_unwrap(subject), hi, lo)
        return maybe_wrap(result)

    def make_slice(self, subject, hi, lo) -> Expression:
        result = raw.vast.xls_vast_verilog_file_make_slice(self._raw, maybe_unwrap(subject), maybe_unwrap(hi), maybe_unwrap(lo))
        return maybe_wrap(result)

    def make_continuous_assignment(self, lhs, rhs) -> VastContinuousAssignment:
        result = raw.vast.xls_vast_verilog_file_make_continuous_assignment(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs))
        return maybe_wrap(result)

    def make_comment(self, text: str) -> VastComment:
        result = raw.vast.xls_vast_verilog_file_make_comment(self._raw, text)
        return maybe_wrap(result)

    def make_blank_line(self) -> VastBlankLine:
        result = raw.vast.xls_vast_verilog_file_make_blank_line(self._raw)
        return maybe_wrap(result)

    def add_include(self, path: str) -> None:
        raw.vast.xls_vast_verilog_file_add_include(self._raw, path)

    def add_blank_line(self) -> None:
        raw.vast.xls_vast_verilog_file_add_blank_line(self._raw)

    def add_comment(self, text: str) -> None:
        raw.vast.xls_vast_verilog_file_add_comment(self._raw, text)

    def make_instantiation(
        self,
        module_name: str,
        inst_name: str,
        param_names: list[str],
        params_exprs: list[Expression],
        port_names: list[str],
        port_exprs: list[Expression],
    ) -> VastInstantiation:
        result = raw.vast.xls_vast_verilog_file_make_instantiation(
            self._raw,
            module_name,
            inst_name,
            param_names,
            [maybe_unwrap(e) for e in params_exprs],
            port_names,
            [maybe_unwrap(e) for e in port_exprs],
        )
        return maybe_wrap(result)

    def make_pos_edge(self, signal) -> Expression:
        result = raw.vast.xls_vast_verilog_file_make_pos_edge(self._raw, maybe_unwrap(signal))
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<VerilogFile>'


@register_wrapper(raw.VastVerilogModule)
class VerilogModule:
    """Wrapper around raw.VastVerilogModule."""

    def __init__(self, _raw: raw.VastVerilogModule):
        self._raw = _raw

    def get_name(self) -> str:
        return raw.vast.xls_vast_verilog_module_get_name(self._raw)

    def get_ports(self) -> list:
        result = raw.vast.xls_vast_verilog_module_get_ports(self._raw)
        if isinstance(result, list):
            return [maybe_wrap(p) for p in result]
        return maybe_wrap(result)

    def add_input(self, name: str, data_type) -> LogicRef:
        result = raw.vast.xls_vast_verilog_module_add_input(self._raw, name, maybe_unwrap(data_type))
        return maybe_wrap(result)

    def add_output(self, name: str, data_type) -> LogicRef:
        result = raw.vast.xls_vast_verilog_module_add_output(self._raw, name, maybe_unwrap(data_type))
        return maybe_wrap(result)

    def add_logic_input(self, name: str, data_type) -> LogicRef:
        result = raw.vast.xls_vast_verilog_module_add_logic_input(self._raw, name, maybe_unwrap(data_type))
        return maybe_wrap(result)

    def add_logic_output(self, name: str, data_type) -> LogicRef:
        result = raw.vast.xls_vast_verilog_module_add_logic_output(self._raw, name, maybe_unwrap(data_type))
        return maybe_wrap(result)

    def add_wire(self, name: str, data_type) -> LogicRef:
        result = raw.vast.xls_vast_verilog_module_add_wire(self._raw, name, maybe_unwrap(data_type))
        return maybe_wrap(result)

    def add_reg(self, name: str, data_type) -> LogicRef:
        result = raw.vast.xls_vast_verilog_module_add_reg(self._raw, name, maybe_unwrap(data_type))
        return maybe_wrap(result)

    def add_logic(self, name: str, data_type) -> LogicRef:
        result = raw.vast.xls_vast_verilog_module_add_logic(self._raw, name, maybe_unwrap(data_type))
        return maybe_wrap(result)

    def add_inout(self, name: str, data_type) -> LogicRef:
        result = raw.vast.xls_vast_verilog_module_add_inout(self._raw, name, maybe_unwrap(data_type))
        return maybe_wrap(result)

    def add_parameter(self, name: str, value) -> VastParameterRef:
        result = raw.vast.xls_vast_verilog_module_add_parameter(self._raw, name, maybe_unwrap(value))
        return maybe_wrap(result)

    def add_localparam(self, name: str, value) -> VastLocalparamRef:
        result = raw.vast.xls_vast_verilog_module_add_localparam(self._raw, name, maybe_unwrap(value))
        return maybe_wrap(result)

    def add_member_instantiation(self, inst) -> None:
        raw.vast.xls_vast_verilog_module_add_member_instantiation(self._raw, maybe_unwrap(inst))

    def add_member_continuous_assignment(self, assign) -> None:
        raw.vast.xls_vast_verilog_module_add_member_continuous_assignment(self._raw, maybe_unwrap(assign))

    def add_member_comment(self, comment) -> None:
        raw.vast.xls_vast_verilog_module_add_member_comment(self._raw, maybe_unwrap(comment))

    def add_member_blank_line(self, blank_line: VastBlankLine) -> None:
        raw.vast.xls_vast_verilog_module_add_member_blank_line(self._raw, maybe_unwrap(blank_line))

    def add_generate_loop(self, genvar_name: str, init, limit, step) -> GenerateLoop:
        result = raw.vast.xls_vast_verilog_module_add_generate_loop(
            self._raw, genvar_name, maybe_unwrap(init), maybe_unwrap(limit), maybe_unwrap(step)
        )
        return maybe_wrap(result)

    def add_always_ff(self, sensitivity_list: list[Expression]) -> AlwaysBase:
        raw_sl = [maybe_unwrap(s) for s in sensitivity_list]
        result = raw.vast.xls_vast_verilog_module_add_always_ff(self._raw, raw_sl)
        return maybe_wrap(result)

    def add_always_at(self, sensitivity_list: list[Expression]) -> AlwaysBase:
        raw_sl = [maybe_unwrap(s) for s in sensitivity_list]
        result = raw.vast.xls_vast_verilog_module_add_always_at(self._raw, raw_sl)
        return maybe_wrap(result)

    def add_always_comb(self) -> AlwaysBase:
        result = raw.vast.xls_vast_verilog_module_add_always_comb(self._raw)
        return maybe_wrap(result)

    def add_conditional(self, condition) -> Conditional:
        result = raw.vast.xls_vast_verilog_module_add_conditional(self._raw, maybe_unwrap(condition))
        return maybe_wrap(result)

    def __repr__(self) -> str:
        try:
            return f'<VerilogModule {self.get_name()!r}>'
        except Exception:
            return '<VerilogModule>'


@register_wrapper(raw.VastExpression)
class Expression:
    """Wrapper around raw.VastExpression."""

    def __init__(self, _raw: raw.VastExpression):
        self._raw = _raw

    def emit(self) -> str:
        return raw.vast.xls_vast_expression_emit(self._raw)

    def __repr__(self) -> str:
        try:
            return f'<Expression {self.emit()}>'
        except Exception:
            return '<Expression>'


@register_wrapper(raw.VastLogicRef)
class LogicRef:
    """Wrapper around raw.VastLogicRef."""

    def __init__(self, _raw: raw.VastLogicRef):
        self._raw = _raw

    def get_name(self) -> str:
        return raw.vast.xls_vast_logic_ref_get_name(self._raw)

    def as_expression(self) -> Expression:
        result = raw.vast.xls_vast_logic_ref_as_expression(self._raw)
        return maybe_wrap(result)

    def as_indexable_expression(self):
        result = raw.vast.xls_vast_logic_ref_as_indexable_expression(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        try:
            return f'<LogicRef {self.get_name()!r}>'
        except Exception:
            return '<LogicRef>'


@register_wrapper(raw.VastDataType)
class DataType:
    """Wrapper around raw.VastDataType."""

    def __init__(self, _raw):
        self._raw = _raw

    def width_as_int64(self) -> int:
        return raw.vast.xls_vast_data_type_width_as_int64(self._raw)

    def flat_bit_count_as_int64(self) -> int:
        return raw.vast.xls_vast_data_type_flat_bit_count_as_int64(self._raw)

    def width(self) -> Expression:
        result = raw.vast.xls_vast_data_type_width(self._raw)
        return maybe_wrap(result)

    def is_signed(self) -> bool:
        return raw.vast.xls_vast_data_type_is_signed(self._raw)

    def __repr__(self) -> str:
        return '<DataType>'


@register_wrapper(raw.VastStatementBlock)
class StatementBlock:
    """Wrapper around raw.VastStatementBlock."""

    def __init__(self, _raw):
        self._raw = _raw

    def add_nonblocking_assignment(self, lhs, rhs) -> None:
        raw.vast.xls_vast_statement_block_add_nonblocking_assignment(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs))

    def add_blocking_assignment(self, lhs, rhs) -> None:
        raw.vast.xls_vast_statement_block_add_blocking_assignment(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs))

    def add_continuous_assignment(self, lhs, rhs) -> None:
        raw.vast.xls_vast_statement_block_add_continuous_assignment(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs))

    def add_comment_text(self, text: str) -> None:
        raw.vast.xls_vast_statement_block_add_comment_text(self._raw, text)

    def add_blank_line(self) -> None:
        raw.vast.xls_vast_statement_block_add_blank_line(self._raw)

    def add_inline_text(self, text: str) -> None:
        raw.vast.xls_vast_statement_block_add_inline_text(self._raw, text)

    def add_conditional(self, condition) -> Conditional:
        result = raw.vast.xls_vast_statement_block_add_conditional(self._raw, maybe_unwrap(condition))
        return maybe_wrap(result)

    def add_case(self, subject) -> CaseStatement:
        result = raw.vast.xls_vast_statement_block_add_case(self._raw, maybe_unwrap(subject))
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<StatementBlock>'


@register_wrapper(raw.VastAlwaysBase)
class AlwaysBase:
    """Wrapper around raw.VastAlwaysBase."""

    def __init__(self, _raw):
        self._raw = _raw

    def get_statement_block(self) -> StatementBlock:
        result = raw.vast.xls_vast_always_base_get_statement_block(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<AlwaysBase>'


@register_wrapper(raw.VastGenerateLoop)
class GenerateLoop:
    """Wrapper around raw.VastGenerateLoop."""

    def __init__(self, _raw):
        self._raw = _raw

    def get_genvar(self) -> LogicRef:
        result = raw.vast.xls_vast_generate_loop_get_genvar(self._raw)
        return maybe_wrap(result)

    def add_generate_loop(self, genvar_name: str, init, limit, step) -> GenerateLoop:
        result = raw.vast.xls_vast_generate_loop_add_generate_loop(
            self._raw, genvar_name, maybe_unwrap(init), maybe_unwrap(limit), maybe_unwrap(step)
        )
        return maybe_wrap(result)

    def add_blank_line(self) -> None:
        raw.vast.xls_vast_generate_loop_add_blank_line(self._raw)

    def add_comment(self, comment: VastComment) -> None:
        raw.vast.xls_vast_generate_loop_add_comment(self._raw, comment)

    def add_instantiation(self, inst) -> None:
        raw.vast.xls_vast_generate_loop_add_instantiation(self._raw, maybe_unwrap(inst))

    def add_always_comb(self) -> AlwaysBase:
        result = raw.vast.xls_vast_generate_loop_add_always_comb(self._raw)
        return maybe_wrap(result)

    def add_always_ff(self, sensitivity_list: Sequence[Expression]) -> AlwaysBase:
        raw_sl = [maybe_unwrap(s) for s in sensitivity_list]
        result = raw.vast.xls_vast_generate_loop_add_always_ff(self._raw, raw_sl)
        return maybe_wrap(result)

    def add_localparam(self, name: str, value) -> VastLocalparamRef:
        result = raw.vast.xls_vast_generate_loop_add_localparam(self._raw, name, maybe_unwrap(value))
        return maybe_wrap(result)

    def add_continuous_assignment(self, lhs, rhs) -> None:
        raw.vast.xls_vast_generate_loop_add_continuous_assignment(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs))

    def add_conditional(self, condition) -> Conditional:
        result = raw.vast.xls_vast_generate_loop_add_conditional(self._raw, maybe_unwrap(condition))
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<GenerateLoop>'


@register_wrapper(raw.VastConditional)
class Conditional:
    """Wrapper around raw.VastConditional."""

    def __init__(self, _raw):
        self._raw = _raw

    def get_then_block(self) -> StatementBlock:
        result = raw.vast.xls_vast_conditional_get_then_block(self._raw)
        return maybe_wrap(result)

    def add_else_if(self, condition) -> StatementBlock:
        result = raw.vast.xls_vast_conditional_add_else_if(self._raw, maybe_unwrap(condition))
        return maybe_wrap(result)

    def add_else(self) -> StatementBlock:
        result = raw.vast.xls_vast_conditional_add_else(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<Conditional>'


@register_wrapper(raw.VastCaseStatement)
class CaseStatement:
    """Wrapper around raw.VastCaseStatement."""

    def __init__(self, _raw):
        self._raw = _raw

    def add_item(self, pattern, body) -> StatementBlock:
        result = raw.vast.xls_vast_case_statement_add_item(self._raw, maybe_unwrap(pattern))
        return maybe_wrap(result)

    def add_default(self) -> StatementBlock:
        result = raw.vast.xls_vast_case_statement_add_default(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<CaseStatement>'


# Register remaining raw VAST types without dedicated wrappers above
@register_wrapper(raw.VastIndexableExpression)
class VastIndexableExpression:
    def __init__(self, _raw):
        self._raw = _raw

    def as_expression(self) -> Expression:
        result = raw.vast.xls_vast_indexable_expression_as_expression(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<VastIndexableExpression>'


@register_wrapper(raw.VastSlice)
class VastSlice:
    def __init__(self, _raw):
        self._raw = _raw

    def as_expression(self) -> Expression:
        result = raw.vast.xls_vast_slice_as_expression(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<VastSlice>'


@register_wrapper(raw.VastLiteral)
class VastLiteral:
    def __init__(self, _raw):
        self._raw = _raw

    def as_expression(self) -> Expression:
        result = raw.vast.xls_vast_literal_as_expression(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<VastLiteral>'


@register_wrapper(raw.VastInstantiation)
class VastInstantiation:
    def __init__(self, _raw):
        self._raw = _raw

    def __repr__(self) -> str:
        return '<VastInstantiation>'


@register_wrapper(raw.VastContinuousAssignment)
class VastContinuousAssignment:
    def __init__(self, _raw):
        self._raw = _raw

    def __repr__(self) -> str:
        return '<VastContinuousAssignment>'


@register_wrapper(raw.VastComment)
class VastComment:
    def __init__(self, _raw):
        self._raw = _raw

    def __repr__(self) -> str:
        return '<VastComment>'


@register_wrapper(raw.VastBlankLine)
class VastBlankLine:
    def __init__(self, _raw):
        self._raw = _raw

    def __repr__(self) -> str:
        return '<VastBlankLine>'


@register_wrapper(raw.VastStatement)
class VastStatement:
    def __init__(self, _raw):
        self._raw = _raw

    def __repr__(self) -> str:
        return '<VastStatement>'


@register_wrapper(raw.VastModulePort)
class VastModulePort:
    def __init__(self, _raw):
        self._raw = _raw

    def get_direction(self):
        return raw.vast.xls_vast_verilog_module_port_get_direction(self._raw)

    def get_def(self) -> VastDef:
        result = raw.vast.xls_vast_verilog_module_port_get_def(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<VastModulePort>'


@register_wrapper(raw.VastDef)
class VastDef:
    def __init__(self, _raw):
        self._raw = _raw

    def get_name(self) -> str:
        return raw.vast.xls_vast_def_get_name(self._raw)

    def get_data_type(self) -> DataType:
        result = raw.vast.xls_vast_def_get_data_type(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        try:
            return f'<VastDef {self.get_name()!r}>'
        except Exception:
            return '<VastDef>'


@register_wrapper(raw.VastParameterRef)
class VastParameterRef:
    def __init__(self, _raw):
        self._raw = _raw

    def as_expression(self) -> Expression:
        result = raw.vast.xls_vast_parameter_ref_as_expression(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<VastParameterRef>'


@register_wrapper(raw.VastLocalparamRef)
class VastLocalparamRef:
    def __init__(self, _raw):
        self._raw = _raw

    def as_expression(self) -> Expression:
        result = raw.vast.xls_vast_localparam_ref_as_expression(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<VastLocalparamRef>'


@register_wrapper(raw.VastMacroRef)
class VastMacroRef:
    def __init__(self, _raw):
        self._raw = _raw

    def as_expression(self) -> Expression:
        result = raw.vast.xls_vast_macro_ref_as_expression(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<VastMacroRef>'


@register_wrapper(raw.VastMacroStatement)
class VastMacroStatement:
    def __init__(self, _raw):
        self._raw = _raw

    def __repr__(self) -> str:
        return '<VastMacroStatement>'


@register_wrapper(raw.VastInlineVerilogStatement)
class VastInlineVerilogStatement:
    def __init__(self, _raw):
        self._raw = _raw

    def __repr__(self) -> str:
        return '<VastInlineVerilogStatement>'


@register_wrapper(raw.VastConcat)
class VastConcat:
    def __init__(self, _raw):
        self._raw = _raw

    def as_expression(self) -> Expression:
        result = raw.vast.xls_vast_concat_as_expression(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<VastConcat>'


@register_wrapper(raw.VastIndex)
class VastIndex:
    def __init__(self, _raw):
        self._raw = _raw

    def as_expression(self) -> Expression:
        result = raw.vast.xls_vast_index_as_expression(self._raw)
        return maybe_wrap(result)

    def as_indexable_expression(self):
        result = raw.vast.xls_vast_index_as_indexable_expression(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<VastIndex>'


# ---------------------------------------------------------------------------
# Bulk-wrap all public functions from raw.vast into this module's namespace
# ---------------------------------------------------------------------------
wrap_module(raw.vast, globals())
