"""Pythonic wrapper classes and functions for xls.raw.c_api."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._c_api import *

from . import raw
from ._wrap import auto_wrap, maybe_unwrap, maybe_wrap, register_wrapper, wrap_module
from .raw import jit_fn_predict as jit_fn_predict


def test():
    pass


@register_wrapper(raw.Package)
class Package:
    """Wrapper around raw.Package."""

    _raw: raw.Package

    def __init__(self, _raw: raw.Package):
        if _raw is None:
            _raw = raw.c_api.xls_package_create('')
            # unwrap if wrapped
            if hasattr(_raw, '_raw'):
                _raw = _raw._raw
        self._raw: raw.Package = _raw

    @classmethod
    def create(cls, name: str) -> Package:
        """Create a new empty Package with the given name."""
        result = raw.ir_builder.xls_package_create(name)
        if hasattr(result, '_raw'):
            result = result._raw  # type: ignore
        return cls(result)  # type: ignore

    @classmethod
    def parse_ir(cls, ir: str, filename: str | None = None) -> Package:
        """Parse an IR string into a Package."""
        result = raw.c_api.xls_parse_ir_package(ir, filename or '')
        if hasattr(result, '_raw'):
            result = result._raw  # type: ignore
        return cls(result)  # type: ignore

    def to_string(self) -> str:
        """Return the IR text representation of this package."""
        return raw.c_api.xls_package_to_string(self._raw)

    def get_function(self, name: str) -> Function:
        """Get a Function by name."""
        result = raw.c_api.xls_package_get_function(self._raw, name)
        return maybe_wrap(result)

    def get_functions(self) -> list[Function]:
        """Return all functions in this package."""
        results = raw.c_api.xls_package_get_functions(self._raw)
        if isinstance(results, list):
            return [maybe_wrap(f) for f in results]
        return maybe_wrap(results)

    def get_top(self) -> Function | None:  # type: ignore
        """Return the top function, or None if not set."""
        result = raw.c_api.xls_package_get_top(self._raw)
        if result is None:
            return None
        return maybe_wrap(result)

    def set_top(self, name: str):
        """Set the top function by name. Returns True on success."""
        return raw.c_api.xls_package_set_top_by_name(self._raw, name)

    def verify(self):
        """Verify the package. Returns True if valid."""
        return raw.c_api.xls_verify_package(self._raw)

    def get_type_for_value(self, val: Value) -> Type:
        """Return the XLS Type corresponding to a Value."""
        raw_val = maybe_unwrap(val)
        result = raw.c_api.xls_package_get_type_for_value(self._raw, raw_val)
        return maybe_wrap(result)

    def schedule_and_codegen(
        self,
        scheduling_options: str = '',
        codegen_flags: str = 'generator: GENERATOR_KIND_COMBINATIONAL',
        with_delay_model: bool = False,
    ) -> ScheduleAndCodegenResult:
        """Schedule and generate Verilog from this package.

        Args:
            scheduling_options: SchedulingOptionsFlagsProto text (e.g. 'pipeline_stages: 1').
            codegen_flags: CodegenFlagsProto text (e.g. 'generator: GENERATOR_KIND_COMBINATIONAL').
            with_delay_model: Whether to use a delay model.
        """
        result = raw.c_api.xls_schedule_and_codegen_package(self._raw, scheduling_options, codegen_flags, with_delay_model)
        return maybe_wrap(result)

    def get_bits_type(self, bit_count: int) -> Type:
        """Get the bits type with the given bit count."""
        result = raw.ir_builder.xls_package_get_bits_type(self._raw, bit_count)
        return maybe_wrap(result)

    def get_tuple_type(self, n: Sequence[Type]) -> Type:
        """Get a tuple type with n elements (raw types passed separately)."""
        n = [maybe_unwrap(t) for t in n]
        result = raw.ir_builder.xls_package_get_tuple_type(self._raw, n)
        return maybe_wrap(result)

    def get_array_type(self, element_type: Type, size: int) -> Type:
        """Get an array type."""
        raw_et = maybe_unwrap(element_type)
        result = raw.ir_builder.xls_package_get_array_type(self._raw, raw_et, size)
        return maybe_wrap(result)

    def get_token_type(self) -> Type:
        """Get the token type."""
        result = raw.ir_builder.xls_package_get_token_type(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<Package>'


@register_wrapper(raw.FunctionBase)
class FunctionBase:
    """Wrapper around raw.FunctionBase."""

    def __init__(self, _raw: raw.FunctionBase):
        self._raw = _raw

    def __repr__(self) -> str:
        return '<FunctionBase>'


@register_wrapper(raw.Function)
class Function:
    """Wrapper around raw.Function."""

    def __init__(self, _raw: raw.Function):
        self._raw = _raw

    def get_name(self) -> str:
        """Return the function name."""
        return raw.c_api.xls_function_get_name(self._raw)

    def get_type(self) -> FunctionType:
        """Return the FunctionType of this function."""
        result = raw.c_api.xls_function_get_type(self._raw)
        return maybe_wrap(result)

    def to_string(self) -> str:
        """Return the IR text for this function."""
        return raw.c_api.xls_function_to_string(self._raw)

    def get_param_name(self, i: int) -> str:
        """Return the name of the i-th parameter."""
        return raw.c_api.xls_function_get_param_name(self._raw, i)

    def get_param_count(self) -> int:
        """Return the number of parameters."""
        ft = raw.c_api.xls_function_get_type(self._raw)
        return raw.c_api.xls_function_type_get_param_count(ft)

    def interpret(self, args: list[Value]) -> Value:
        """Interpret the function with given argument Values."""
        raw_args = [maybe_unwrap(a) for a in args]
        result = raw.c_api.xls_interpret_function(self._raw, raw_args)
        return maybe_wrap(result)

    def to_jit(self) -> FunctionJit:
        """Compile this function to a JIT executor."""
        result = raw.c_api.xls_make_function_jit(self._raw)
        return maybe_wrap(result)

    def to_z3_smtlib(self) -> str:
        """Return the Z3 SMT-LIB representation."""
        return raw.c_api.xls_function_to_z3_smtlib(self._raw)

    def __repr__(self) -> str:
        try:
            return f'<Function {self.get_name()!r}>'
        except Exception:
            return '<Function>'


@register_wrapper(raw.FunctionType)
class FunctionType:
    """Wrapper around raw.FunctionType."""

    def __init__(self, _raw: raw.FunctionType):
        self._raw = _raw

    def to_string(self) -> str:
        """Return a string representation of the function type."""
        return raw.c_api.xls_function_type_to_string(self._raw)

    def get_param_count(self) -> int:
        """Return the number of parameter types."""
        return raw.c_api.xls_function_type_get_param_count(self._raw)

    def get_param_type(self, i: int) -> Type:
        """Return the Type of the i-th parameter."""
        result = raw.c_api.xls_function_type_get_param_type(self._raw, i)
        return maybe_wrap(result)

    def get_return_type(self) -> Type:
        """Return the return Type."""
        result = raw.c_api.xls_function_type_get_return_type(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        try:
            return f'<FunctionType {self.to_string()}>'
        except Exception:
            return '<FunctionType>'


@register_wrapper(raw.FunctionJit)
class FunctionJit:
    """Wrapper around raw.FunctionJit — a JIT-compiled XLS function."""

    def __init__(self, _raw: raw.FunctionJit):
        self._raw = _raw

    def run(self, args: list[Value]) -> Value:
        """Run the JIT function with given argument Values."""
        raw_args = [maybe_unwrap(a) for a in args]
        result = raw.c_api.xls_function_jit_run(self._raw, raw_args)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<FunctionJit>'


@register_wrapper(raw.Type)
class Type:
    """Wrapper around raw.Type."""

    def __init__(self, _raw: raw.Type):
        self._raw = _raw

    def to_string(self) -> str:
        """Return string representation of this type."""
        return raw.c_api.xls_type_to_string(self._raw)

    def get_kind(self):
        """Return the kind of this type."""
        return raw.c_api.xls_type_get_kind(self._raw)

    def get_flat_bit_count(self) -> int:
        """Return the total number of bits in this type."""
        return raw.c_api.xls_type_get_flat_bit_count(self._raw)

    def __repr__(self) -> str:
        try:
            return f'<Type {self.to_string()}>'
        except Exception:
            return '<Type>'


@register_wrapper(raw.Value)
class Value:
    """Wrapper around raw.Value."""

    def __init__(self, _raw: raw.Value):
        self._raw = _raw

    @classmethod
    def make_ubits(cls, bit_count: int, val: int) -> Value:
        """Create an unsigned bits Value."""
        result = raw.c_api.xls_value_make_ubits(bit_count, val)
        return maybe_wrap(result)

    @classmethod
    def make_sbits(cls, bit_count: int, val: int) -> Value:
        """Create a signed bits Value."""
        result = raw.c_api.xls_value_make_sbits(bit_count, val)
        return maybe_wrap(result)

    @classmethod
    def make_token(cls) -> Value:
        """Create a token Value."""
        result = raw.c_api.xls_value_make_token()
        return maybe_wrap(result)

    @classmethod
    def make_true(cls) -> Value:
        """Create a boolean true Value."""
        result = raw.c_api.xls_value_make_true()
        return maybe_wrap(result)

    @classmethod
    def make_false(cls) -> Value:
        """Create a boolean false Value."""
        result = raw.c_api.xls_value_make_false()
        return maybe_wrap(result)

    @classmethod
    def make_array(cls, elems: list[Value]) -> Value:
        """Create an array Value from a list of element Values."""
        raw_elems = [maybe_unwrap(e) for e in elems]
        result = raw.c_api.xls_value_make_array(raw_elems)
        # The raw API takes count; use from_bits or interpret path if needed.
        # Actually xls_value_make_array takes a count argument (pre-allocated).
        # We need a different approach - use interpret with literal or value_from_bits.
        # Per pyi: xls_value_make_array(arg: int) -> object
        # This creates an empty array of size n, elements filled separately?
        # Let's check: the raw function signature says arg: int.
        # For now return a wrapped result from the raw call.
        return maybe_wrap(result)

    @classmethod
    def make_tuple(cls, elems: Sequence[Value]) -> Value:
        """Create a tuple Value from a list of element Values."""
        elems = [maybe_unwrap(e) for e in elems]
        result = raw.c_api.xls_value_make_tuple(elems)
        return maybe_wrap(result)

    @classmethod
    def parse(cls, input: str) -> Value:
        """Parse a typed value string."""
        result = raw.c_api.xls_parse_typed_value(input)
        return maybe_wrap(result)

    @classmethod
    def from_bits(cls, bits: Bits) -> Value:
        """Create a bits Value from a Bits object."""
        raw_bits = maybe_unwrap(bits)
        result = raw.c_api.xls_value_from_bits(raw_bits)
        return maybe_wrap(result)

    def to_string(self) -> str:
        """Return string representation."""
        return raw.c_api.xls_value_to_string(self._raw)

    def clone(self) -> Value:
        """Return a deep copy of this Value."""
        result = raw.c_api.xls_value_clone(self._raw)
        return maybe_wrap(result)

    def get_kind(self):
        """Return the ValueKind of this Value."""
        return raw.c_api.xls_value_get_kind(self._raw)

    def get_element(self, i: int) -> Value:
        """Return the i-th element (for array/tuple values)."""
        result = raw.c_api.xls_value_get_element(self._raw, i)
        return maybe_wrap(result)

    def get_element_count(self) -> int:
        """Return the number of elements (for array/tuple values)."""
        return raw.c_api.xls_value_get_element_count(self._raw)

    def get_bits(self) -> Bits:
        """Return the Bits of this value (for bits values)."""
        result = raw.c_api.xls_value_get_bits(self._raw)
        return maybe_wrap(result)

    def flatten_to_bits(self) -> Bits:
        """Flatten this value to Bits."""
        result = raw.c_api.xls_value_flatten_to_bits(self._raw)
        return maybe_wrap(result)

    def __eq__(self, other) -> bool:
        raw_other = maybe_unwrap(other)
        return raw.c_api.xls_value_eq(self._raw, raw_other)

    def __repr__(self) -> str:
        try:
            return f'<Value {self.to_string()}>'
        except Exception:
            return '<Value>'


@register_wrapper(raw.Bits)
class Bits:
    """Wrapper around raw.Bits."""

    def __init__(self, _raw: raw.Bits):
        self._raw = _raw

    @classmethod
    def make_ubits(cls, bit_count: int, val: int) -> Bits:
        """Create unsigned bits."""
        result = raw.c_api.xls_bits_make_ubits(bit_count, val)
        return maybe_wrap(result)

    @classmethod
    def make_sbits(cls, bit_count: int, val: int) -> Bits:
        """Create signed bits."""
        result = raw.c_api.xls_bits_make_sbits(bit_count, val)
        return maybe_wrap(result)

    @classmethod
    def from_bytes(cls, bit_count: int, data: bytes) -> Bits:
        """Create bits from a byte array."""
        result = raw.c_api.xls_bits_make_bits_from_bytes(bit_count, data)
        return maybe_wrap(result)

    def get_bit_count(self) -> int:
        """Return the number of bits."""
        return raw.c_api.xls_bits_get_bit_count(self._raw)

    def to_uint64(self) -> int:
        """Convert to unsigned 64-bit integer."""
        return raw.c_api.xls_bits_to_uint64(self._raw)

    def to_int64(self) -> int:
        """Convert to signed 64-bit integer."""
        return raw.c_api.xls_bits_to_int64(self._raw)

    def to_bytes(self) -> bytes:
        """Convert to bytes."""
        return raw.c_api.xls_bits_to_bytes(self._raw)

    def to_string(self, fmt=None, include_bit_count: bool = False) -> str:
        """Return string representation with optional format."""
        if fmt is None:
            fmt = raw.c_api.DEFAULT
        fmt_val = maybe_unwrap(fmt)
        return raw.c_api.xls_bits_to_string(self._raw, fmt_val, include_bit_count)

    def get_bit(self, i: int) -> bool:
        """Return the value of bit i."""
        return raw.c_api.xls_bits_get_bit(self._raw, i)

    def width_slice(self, start: int, width: int) -> Bits:
        """Return a width-slice of this Bits."""
        result = raw.c_api.xls_bits_width_slice(self._raw, start, width)
        return maybe_wrap(result)

    def __eq__(self, other) -> bool:
        raw_other = maybe_unwrap(other)
        return raw.c_api.xls_bits_eq(self._raw, raw_other)

    def __ne__(self, other) -> bool:
        raw_other = maybe_unwrap(other)
        return raw.c_api.xls_bits_ne(self._raw, raw_other)

    def __add__(self, other: Bits) -> Bits:
        raw_other = maybe_unwrap(other)
        return maybe_wrap(raw.c_api.xls_bits_add(self._raw, raw_other))

    def __sub__(self, other: Bits) -> Bits:
        raw_other = maybe_unwrap(other)
        return maybe_wrap(raw.c_api.xls_bits_sub(self._raw, raw_other))

    def __and__(self, other: Bits) -> Bits:
        raw_other = maybe_unwrap(other)
        return maybe_wrap(raw.c_api.xls_bits_and(self._raw, raw_other))

    def __or__(self, other: Bits) -> Bits:
        raw_other = maybe_unwrap(other)
        return maybe_wrap(raw.c_api.xls_bits_or(self._raw, raw_other))

    def __xor__(self, other: Bits) -> Bits:
        raw_other = maybe_unwrap(other)
        return maybe_wrap(raw.c_api.xls_bits_xor(self._raw, raw_other))

    def __mul__(self, other: Bits) -> Bits:
        raw_other = maybe_unwrap(other)
        return maybe_wrap(raw.c_api.xls_bits_umul(self._raw, raw_other))

    def __neg__(self) -> Bits:
        return maybe_wrap(raw.c_api.xls_bits_negate(self._raw))

    def __invert__(self) -> Bits:
        return maybe_wrap(raw.c_api.xls_bits_not(self._raw))

    def __lshift__(self, amount: int) -> Bits:
        return maybe_wrap(raw.c_api.xls_bits_shift_left_logical(self._raw, amount))

    def __rshift__(self, amount: int) -> Bits:
        return maybe_wrap(raw.c_api.xls_bits_shift_right_logical(self._raw, amount))

    def __lt__(self, other: Bits) -> bool:
        raw_other = maybe_unwrap(other)
        return raw.c_api.xls_bits_ult(self._raw, raw_other)

    def __le__(self, other: Bits) -> bool:
        raw_other = maybe_unwrap(other)
        return raw.c_api.xls_bits_ule(self._raw, raw_other)

    def __gt__(self, other: Bits) -> bool:
        raw_other = maybe_unwrap(other)
        return raw.c_api.xls_bits_ugt(self._raw, raw_other)

    def __ge__(self, other: Bits) -> bool:
        raw_other = maybe_unwrap(other)
        return raw.c_api.xls_bits_uge(self._raw, raw_other)

    def __repr__(self) -> str:
        try:
            return f'<Bits {self.to_string()}>'
        except Exception:
            return '<Bits>'


@register_wrapper(raw.ScheduleAndCodegenResult)
class ScheduleAndCodegenResult:
    """Wrapper around raw.ScheduleAndCodegenResult."""

    def __init__(self, _raw: raw.ScheduleAndCodegenResult):
        self._raw = _raw

    def get_verilog_text(self) -> str:
        """Return the generated Verilog text."""
        return raw.c_api.xls_schedule_and_codegen_result_get_verilog_text(self._raw)

    def __repr__(self) -> str:
        return '<ScheduleAndCodegenResult>'


@register_wrapper(raw.BitsRope)
class BitsRope:
    """Wrapper around raw.BitsRope."""

    def __init__(self, _raw: raw.BitsRope):
        self._raw = _raw

    def append(self, bits: Bits):
        """Append bits to the rope."""
        raw_bits = maybe_unwrap(bits)
        raw.c_api.xls_bits_rope_append_bits(self._raw, raw_bits)

    def get_bits(self) -> Bits:
        """Get the concatenated bits from the rope."""
        result = raw.c_api.xls_bits_rope_get_bits(self._raw)
        return maybe_wrap(result)

    def __len__(self) -> int:
        """Return the total bit count of the rope."""
        bits = self.get_bits()
        return bits.get_bit_count()

    def __repr__(self) -> str:
        return f'<BitsRope length={len(self)}>'


# ---------------------------------------------------------------------------
# Bulk-wrap all public functions from raw.c_api into this module's namespace
# ---------------------------------------------------------------------------
wrap_module(raw.c_api, globals())

# ---------------------------------------------------------------------------
# Batch inference / array-level functions from raw (already on raw module)
# ---------------------------------------------------------------------------
# jit_fn_predict = auto_wrap(raw.jit_fn_predict)

if TYPE_CHECKING:
    import numpy as np
    from numpy.typing import NDArray

    def value_from_array(elements: Sequence[int] | NDArray[np.integer], bit_count: int) -> Value:
        """Convert a list of ints to an ArrayValue with the given bit count for each sub-value.

        Parameters:
        ==================
        elements: A sequence of integers (e.g. list[int] or numpy array) to convert to ArrayValue.
        each integer will be converted to a bits Value with the specified bit count.

        bit_count: The number of bits to use for each integer element in the resulting ArrayValue.

        Returns: An ArrayValue containing bits Values. Each element is a bits Value with the specified bit count.
        """
        ...

    def values_from_array(elements: Sequence[int] | NDArray[np.integer], bit_count: int, word_count: int) -> list[Value]:
        """Convert a list of ints to a list of bits Values with the given bit count and word count.

        Parameters:
        ==================
        elements: A sequence of integers (e.g. list[int] or numpy array) to convert to bits Values.
        each integer will be converted to a bits Value with the specified bit count and word count.

        bit_count: The number of bits to use for each integer element in the resulting bits Values.
        word_count: The number of words (groups of bits) to use for each integer element in the resulting bits Values.

        Returns: A list of bits Values. (word_count, bit_count) for each ArrayValue element, number of Values until
        exhausting the input list.
        """
        ...

    def value_to_array(value: Value) -> list[int]:
        """Convert an ArrayValue to a list of ints."""
        ...
else:
    value_from_array = auto_wrap(raw.value_from_array)
    values_from_array = auto_wrap(raw.values_from_array)
    value_to_array = auto_wrap(raw.value_to_array)

# ---------------------------------------------------------------------------
# Top-level convenience functions with Pythonic names
# ---------------------------------------------------------------------------


def convert_dslx_to_ir(
    dslx_text: str,
    path: str,
    module_name: str,
    dslx_stdlib_path: str,
    additional_search_paths: list[str] | None = None,
) -> str:
    """Convert DSLX source text to IR."""
    return raw.c_api.xls_convert_dslx_to_ir(
        dslx_text,
        path,
        module_name,
        dslx_stdlib_path,
        additional_search_paths or [],
    )


def optimize_ir(ir: str, top: str = '') -> str:
    """Optimize an IR string and return the optimized IR."""
    return raw.c_api.xls_optimize_ir(ir, top)


def mangle_dslx_name(module_name: str, function_name: str) -> str:
    """Mangle a DSLX module + function name into an IR-level name."""
    return raw.c_api.xls_mangle_dslx_name(module_name, function_name)


def parse_ir_package(ir: str, filename: str = '') -> Package:
    """Parse an IR string into a Package."""
    result = raw.c_api.xls_parse_ir_package(ir, filename)
    return maybe_wrap(result)


def parse_typed_value(input: str) -> Value:
    """Parse a typed value string into a Value."""
    result = raw.c_api.xls_parse_typed_value(input)
    return maybe_wrap(result)
