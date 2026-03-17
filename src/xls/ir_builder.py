"""Pythonic wrapper classes and functions for xls.raw.ir_builder."""

import typing

from xls import raw
from xls._wrap import maybe_unwrap, maybe_wrap, register_wrapper, wrap_module

from .c_api import Function, Type

if typing.TYPE_CHECKING:
    from ._ir_builder import *


@register_wrapper(raw.BValue)
class BValue:
    """Wrapper around raw.BValue — a builder value node."""

    def __init__(self, _raw):
        self._raw = _raw

    def __repr__(self) -> str:
        return '<BValue>'


@register_wrapper(raw.BuilderBase)
class BuilderBase:
    """Wrapper around raw.BuilderBase — base class for IR builders."""

    def __init__(self, _raw):
        self._raw = _raw

    def get_type(self, val: BValue) -> object:
        """Return the type of the given BValue."""
        raw_val = maybe_unwrap(val)
        result = raw.ir_builder.xls_builder_base_get_type(self._raw, raw_val)
        return maybe_wrap(result)

    def get_last_value(self) -> BValue:
        """Return the last value added to this builder."""
        result = raw.ir_builder.xls_builder_base_get_last_value(self._raw)
        return maybe_wrap(result)

    # ------------------------------------------------------------------ #
    # Binary arithmetic / logical operations                               #
    # ------------------------------------------------------------------ #

    def add_add(self, lhs: BValue, rhs: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_add(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs), name)
        return maybe_wrap(result)

    def add_sub(self, lhs: BValue, rhs: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_sub(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs), name)
        return maybe_wrap(result)

    def add_umul(self, lhs: BValue, rhs: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_umul(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs), name)
        return maybe_wrap(result)

    def add_smul(self, lhs: BValue, rhs: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_smul(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs), name)
        return maybe_wrap(result)

    def add_umulp(self, lhs: BValue, rhs: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_umulp(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs), name)
        return maybe_wrap(result)

    def add_smulp(self, lhs: BValue, rhs: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_smulp(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs), name)
        return maybe_wrap(result)

    def add_udiv(self, lhs: BValue, rhs: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_udiv(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs), name)
        return maybe_wrap(result)

    def add_sdiv(self, lhs: BValue, rhs: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_sdiv(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs), name)
        return maybe_wrap(result)

    def add_umod(self, lhs: BValue, rhs: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_umod(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs), name)
        return maybe_wrap(result)

    def add_smod(self, lhs: BValue, rhs: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_smod(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs), name)
        return maybe_wrap(result)

    def add_and(self, lhs: BValue, rhs: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_and(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs), name)
        return maybe_wrap(result)

    def add_nand(self, lhs: BValue, rhs: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_nand(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs), name)
        return maybe_wrap(result)

    def add_or(self, lhs: BValue, rhs: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_or(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs), name)
        return maybe_wrap(result)

    def add_nor(self, lhs: BValue, rhs: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_nor(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs), name)
        return maybe_wrap(result)

    def add_xor(self, lhs: BValue, rhs: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_xor(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs), name)
        return maybe_wrap(result)

    def add_shll(self, lhs: BValue, rhs: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_shll(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs), name)
        return maybe_wrap(result)

    def add_shrl(self, lhs: BValue, rhs: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_shrl(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs), name)
        return maybe_wrap(result)

    def add_shra(self, lhs: BValue, rhs: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_shra(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs), name)
        return maybe_wrap(result)

    def add_ule(self, lhs: BValue, rhs: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_ule(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs), name)
        return maybe_wrap(result)

    def add_ult(self, lhs: BValue, rhs: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_ult(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs), name)
        return maybe_wrap(result)

    def add_uge(self, lhs: BValue, rhs: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_uge(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs), name)
        return maybe_wrap(result)

    def add_ugt(self, lhs: BValue, rhs: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_ugt(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs), name)
        return maybe_wrap(result)

    def add_sle(self, lhs: BValue, rhs: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_sle(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs), name)
        return maybe_wrap(result)

    def add_slt(self, lhs: BValue, rhs: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_slt(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs), name)
        return maybe_wrap(result)

    def add_sge(self, lhs: BValue, rhs: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_sge(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs), name)
        return maybe_wrap(result)

    def add_sgt(self, lhs: BValue, rhs: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_sgt(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs), name)
        return maybe_wrap(result)

    def add_eq(self, lhs: BValue, rhs: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_eq(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs), name)
        return maybe_wrap(result)

    def add_ne(self, lhs: BValue, rhs: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_ne(self._raw, maybe_unwrap(lhs), maybe_unwrap(rhs), name)
        return maybe_wrap(result)

    # ------------------------------------------------------------------ #
    # Unary operations                                                     #
    # ------------------------------------------------------------------ #

    def add_negate(self, operand: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_negate(self._raw, maybe_unwrap(operand), name)
        return maybe_wrap(result)

    def add_not(self, operand: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_not(self._raw, maybe_unwrap(operand), name)
        return maybe_wrap(result)

    def add_and_reduce(self, operand: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_and_reduce(self._raw, maybe_unwrap(operand), name)
        return maybe_wrap(result)

    def add_or_reduce(self, operand: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_or_reduce(self._raw, maybe_unwrap(operand), name)
        return maybe_wrap(result)

    def add_xor_reduce(self, operand: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_xor_reduce(self._raw, maybe_unwrap(operand), name)
        return maybe_wrap(result)

    def add_clz(self, operand: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_clz(self._raw, maybe_unwrap(operand), name)
        return maybe_wrap(result)

    def add_ctz(self, operand: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_ctz(self._raw, maybe_unwrap(operand), name)
        return maybe_wrap(result)

    def add_reverse(self, operand: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_reverse(self._raw, maybe_unwrap(operand), name)
        return maybe_wrap(result)

    def add_identity(self, operand: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_identity(self._raw, maybe_unwrap(operand), name)
        return maybe_wrap(result)

    def add_encode(self, operand: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_encode(self._raw, maybe_unwrap(operand), name)
        return maybe_wrap(result)

    def add_decode(self, operand: BValue, width: int, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_decode(self._raw, maybe_unwrap(operand), width, name)
        return maybe_wrap(result)

    # ------------------------------------------------------------------ #
    # Extend / slice operations                                            #
    # ------------------------------------------------------------------ #

    def add_sign_extend(self, operand: BValue, new_bit_count: int, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_sign_extend(self._raw, maybe_unwrap(operand), new_bit_count, name)
        return maybe_wrap(result)

    def add_zero_extend(self, operand: BValue, new_bit_count: int, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_zero_extend(self._raw, maybe_unwrap(operand), new_bit_count, name)
        return maybe_wrap(result)

    def add_bit_slice(self, operand: BValue, start: int, width: int, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_bit_slice(self._raw, maybe_unwrap(operand), start, width, name)
        return maybe_wrap(result)

    def add_bit_slice_update(self, operand: BValue, update_start: BValue, update_value: BValue, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_bit_slice_update(
            self._raw, maybe_unwrap(operand), maybe_unwrap(update_start), maybe_unwrap(update_value), name
        )
        return maybe_wrap(result)

    def add_dynamic_bit_slice(self, operand: BValue, start: BValue, width: int, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_dynamic_bit_slice(
            self._raw, maybe_unwrap(operand), maybe_unwrap(start), width, name
        )
        return maybe_wrap(result)

    # ------------------------------------------------------------------ #
    # Literal / concat / select                                           #
    # ------------------------------------------------------------------ #

    def add_literal(self, value, name: str = '') -> BValue:
        """Add a literal value node. value may be a wrapped or raw Value."""
        result = raw.ir_builder.xls_builder_base_add_literal(self._raw, maybe_unwrap(value), name)
        return maybe_wrap(result)

    def add_concat(self, ops: list[BValue], name: str = '') -> BValue:
        """Concatenate a list of BValues."""
        raw_ops = [maybe_unwrap(o) for o in ops]
        result = raw.ir_builder.xls_builder_base_add_concat(self._raw, raw_ops, name)
        return maybe_wrap(result)

    def add_select(
        self,
        selector: BValue,
        cases: list[BValue],
        default: BValue | None = None,
        name: str = '',
    ) -> BValue:
        raw_cases = [maybe_unwrap(c) for c in cases]
        raw_default = maybe_unwrap(default) if default is not None else None
        result = raw.ir_builder.xls_builder_base_add_select(self._raw, maybe_unwrap(selector), raw_cases, raw_default, name)
        return maybe_wrap(result)

    def add_one_hot(self, input: BValue, lsb_prio: bool, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_one_hot(self._raw, maybe_unwrap(input), lsb_prio, name)
        return maybe_wrap(result)

    def add_one_hot_select(self, selector: BValue, cases: list[BValue], name: str = '') -> BValue:
        raw_cases = [maybe_unwrap(c) for c in cases]
        result = raw.ir_builder.xls_builder_base_add_one_hot_select(self._raw, maybe_unwrap(selector), raw_cases, name)
        return maybe_wrap(result)

    def add_priority_select(self, selector: BValue, cases: list[BValue], default: BValue, name: str = '') -> BValue:
        raw_cases = [maybe_unwrap(c) for c in cases]
        result = raw.ir_builder.xls_builder_base_add_priority_select(
            self._raw, maybe_unwrap(selector), raw_cases, maybe_unwrap(default), name
        )
        return maybe_wrap(result)

    # ------------------------------------------------------------------ #
    # Tuple / array operations                                             #
    # ------------------------------------------------------------------ #

    def add_tuple(self, elems: list[BValue], name: str = '') -> BValue:
        raw_elems = [maybe_unwrap(e) for e in elems]
        result = raw.ir_builder.xls_builder_base_add_tuple(self._raw, raw_elems, name)
        return maybe_wrap(result)

    def add_tuple_index(self, tuple_val: BValue, index: int, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_tuple_index(self._raw, maybe_unwrap(tuple_val), index, name)
        return maybe_wrap(result)

    def add_array(self, element_type: Type, elems: list[BValue], name: str = '') -> BValue:
        raw_et = maybe_unwrap(element_type)
        raw_elems = [maybe_unwrap(e) for e in elems]
        result = raw.ir_builder.xls_builder_base_add_array(self._raw, raw_et, raw_elems, name)
        return maybe_wrap(result)

    def add_array_index(self, array: BValue, indices: list[BValue], assumed_in_bounds: bool = False, name: str = '') -> BValue:
        raw_indices = [maybe_unwrap(i) for i in indices]
        result = raw.ir_builder.xls_builder_base_add_array_index(
            self._raw, maybe_unwrap(array), raw_indices, assumed_in_bounds, name
        )
        return maybe_wrap(result)

    def add_array_slice(self, array: BValue, start: BValue, width: int, name: str = '') -> BValue:
        result = raw.ir_builder.xls_builder_base_add_array_slice(self._raw, maybe_unwrap(array), maybe_unwrap(start), width, name)
        return maybe_wrap(result)

    def add_array_update(
        self,
        array: BValue,
        update_value: BValue,
        indices: list[BValue],
        assumed_in_bounds: bool = False,
        name: str = '',
    ) -> BValue:
        raw_indices = [maybe_unwrap(i) for i in indices]
        result = raw.ir_builder.xls_builder_base_add_array_update(
            self._raw, maybe_unwrap(array), maybe_unwrap(update_value), raw_indices, assumed_in_bounds, name
        )
        return maybe_wrap(result)

    def add_array_concat(self, arrays: list[BValue], name: str = '') -> BValue:
        raw_arrays = [maybe_unwrap(a) for a in arrays]
        result = raw.ir_builder.xls_builder_base_add_array_concat(self._raw, raw_arrays, name)
        return maybe_wrap(result)

    def add_after_all(self, tokens: list[BValue], name: str = '') -> BValue:
        raw_tokens = [maybe_unwrap(t) for t in tokens]
        result = raw.ir_builder.xls_builder_base_add_after_all(self._raw, raw_tokens, name)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<BuilderBase>'


@register_wrapper(raw.FunctionBuilder)
class FunctionBuilder:
    """Wrapper around raw.FunctionBuilder."""

    def __init__(self, _raw):
        self._raw = _raw

    @classmethod
    def create(cls, name: str, package, should_verify: bool = True) -> 'FunctionBuilder':
        """Create a new FunctionBuilder."""
        raw_pkg = maybe_unwrap(package)
        result = raw.ir_builder.xls_function_builder_create(name, raw_pkg, should_verify)
        obj = object.__new__(cls)
        obj._raw = result
        return obj

    def as_builder_base(self) -> BuilderBase:
        """Return this builder as a BuilderBase."""
        result = raw.ir_builder.xls_function_builder_as_builder_base(self._raw)
        return maybe_wrap(result)

    def add_parameter(self, name: str, type_) -> BValue:
        """Add a parameter with the given name and type."""
        raw_type = maybe_unwrap(type_)
        result = raw.ir_builder.xls_function_builder_add_parameter(self._raw, name, raw_type)
        return maybe_wrap(result)

    def build(self) -> Function:
        """Build the function."""
        result = raw.ir_builder.xls_function_builder_build(self._raw)
        return maybe_wrap(result)

    def build_with_return_value(self, ret_val: BValue) -> Function:
        """Build the function with an explicit return value."""
        raw_ret = maybe_unwrap(ret_val)
        result = raw.ir_builder.xls_function_builder_build_with_return_value(self._raw, raw_ret)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<FunctionBuilder>'


# ---------------------------------------------------------------------------
# Bulk-wrap all public functions from raw.ir_builder into this module's namespace
# ---------------------------------------------------------------------------
wrap_module(raw.ir_builder, globals())
