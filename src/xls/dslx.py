"""Pythonic wrapper classes and functions for xls.raw.dslx."""

from __future__ import annotations

from collections.abc import Sequence
from math import ceil, log2

from xls import raw
from xls._wrap import maybe_unwrap, maybe_wrap, register_wrapper, wrap_module


@register_wrapper(raw.DslxTypecheckedModule)
class TypecheckedModule:
    """Wrapper around raw.DslxTypecheckedModule."""

    def __init__(self, _raw):
        self._raw = _raw

    def get_module(self) -> DslxModule:
        result = raw.dslx.xls_dslx_typechecked_module_get_module(self._raw)
        return maybe_wrap(result)

    def get_type_info(self) -> TypeInfo:
        result = raw.dslx.xls_dslx_typechecked_module_get_type_info(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<TypecheckedModule>'


@register_wrapper(raw.DslxImportData)
class ImportData:
    """Wrapper around raw.DslxImportData."""

    def __init__(self, _raw):
        self._raw = _raw

    @classmethod
    def create(cls, dslx_stdlib_path: str, additional_search_paths: list[str] | None = None) -> ImportData:
        """Create an ImportData with the given stdlib path."""
        result = raw.dslx.xls_dslx_import_data_create(dslx_stdlib_path, additional_search_paths or [])
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<ImportData>'


@register_wrapper(raw.DslxModule)
class DslxModule:
    """Wrapper around raw.DslxModule."""

    def __init__(self, _raw):
        self._raw = _raw

    def get_name(self) -> str:
        return raw.dslx.xls_dslx_module_get_name(self._raw)

    def get_member_count(self) -> int:
        return raw.dslx.xls_dslx_module_get_member_count(self._raw)

    def get_member(self, i: int) -> DslxModuleMember:
        result = raw.dslx.xls_dslx_module_get_member(self._raw, i)
        return maybe_wrap(result)

    def get_type_definition_count(self) -> int:
        return raw.dslx.xls_dslx_module_get_type_definition_count(self._raw)

    def get_type_definition_kind(self, i: int):
        return raw.dslx.xls_dslx_module_get_type_definition_kind(self._raw, i)

    def get_type_definition_as_struct_def(self, i: int) -> StructDef:
        result = raw.dslx.xls_dslx_module_get_type_definition_as_struct_def(self._raw, i)
        return maybe_wrap(result)

    def get_type_definition_as_enum_def(self, i: int) -> EnumDef:
        result = raw.dslx.xls_dslx_module_get_type_definition_as_enum_def(self._raw, i)
        return maybe_wrap(result)

    def get_type_definition_as_type_alias(self, i: int) -> DslxTypeAlias:
        result = raw.dslx.xls_dslx_module_get_type_definition_as_type_alias(self._raw, i)
        return maybe_wrap(result)

    def to_string(self) -> str:
        return raw.dslx.xls_dslx_module_to_string(self._raw)

    def __repr__(self) -> str:
        try:
            return f'<DslxModule {self.get_name()!r}>'
        except Exception:
            return '<DslxModule>'


@register_wrapper(raw.DslxFunction)
class DslxFunction:
    """Wrapper around raw.DslxFunction."""

    def __init__(self, _raw):
        self._raw = _raw

    def get_identifier(self) -> str:
        return raw.dslx.xls_dslx_function_get_identifier(self._raw)

    def is_public(self) -> bool:
        return raw.dslx.xls_dslx_function_is_public(self._raw)

    def is_parametric(self) -> bool:
        return raw.dslx.xls_dslx_function_is_parametric(self._raw)

    def get_param_count(self) -> int:
        return raw.dslx.xls_dslx_function_get_param_count(self._raw)

    def get_param(self, i: int) -> DslxParam:
        result = raw.dslx.xls_dslx_function_get_param(self._raw, i)
        return maybe_wrap(result)

    def get_return_type(self) -> DslxTypeAnnotation:
        result = raw.dslx.xls_dslx_function_get_return_type(self._raw)
        return maybe_wrap(result)

    def get_body(self) -> DslxExpr:
        result = raw.dslx.xls_dslx_function_get_body(self._raw)
        return maybe_wrap(result)

    def get_parametric_binding_count(self) -> int:
        return raw.dslx.xls_dslx_function_get_parametric_binding_count(self._raw)

    def get_parametric_binding(self, i: int) -> DslxParametricBinding:
        result = raw.dslx.xls_dslx_function_get_parametric_binding(self._raw, i)
        return maybe_wrap(result)

    def get_attribute_count(self) -> int:
        return raw.dslx.xls_dslx_function_get_attribute_count(self._raw)

    def get_attribute(self, i: int) -> DslxAttribute:
        result = raw.dslx.xls_dslx_function_get_attribute(self._raw, i)
        return maybe_wrap(result)

    def to_string(self) -> str:
        return raw.dslx.xls_dslx_function_to_string(self._raw)

    def __repr__(self) -> str:
        try:
            return f'<DslxFunction {self.get_identifier()!r}>'
        except Exception:
            return '<DslxFunction>'


@register_wrapper(raw.DslxStructDef)
class StructDef:
    """Wrapper around raw.DslxStructDef."""

    def __init__(self, _raw):
        self._raw = _raw

    def get_identifier(self) -> str:
        return raw.dslx.xls_dslx_struct_def_get_identifier(self._raw)

    def is_parametric(self) -> bool:
        return raw.dslx.xls_dslx_struct_def_is_parametric(self._raw)

    def get_member_count(self) -> int:
        return raw.dslx.xls_dslx_struct_def_get_member_count(self._raw)

    def get_member(self, i: int) -> DslxStructMember:
        result = raw.dslx.xls_dslx_struct_def_get_member(self._raw, i)
        return maybe_wrap(result)

    def to_string(self) -> str:
        return raw.dslx.xls_dslx_struct_def_to_string(self._raw)

    def __repr__(self) -> str:
        try:
            return f'<StructDef {self.get_identifier()!r}>'
        except Exception:
            return '<StructDef>'


@register_wrapper(raw.DslxEnumDef)
class EnumDef:
    """Wrapper around raw.DslxEnumDef."""

    def __init__(self, _raw):
        self._raw = _raw

    def get_identifier(self) -> str:
        return raw.dslx.xls_dslx_enum_def_get_identifier(self._raw)

    def get_member_count(self) -> int:
        return raw.dslx.xls_dslx_enum_def_get_member_count(self._raw)

    def get_member(self, i: int) -> DslxEnumMember:
        result = raw.dslx.xls_dslx_enum_def_get_member(self._raw, i)
        return maybe_wrap(result)

    def get_underlying(self) -> DslxTypeAnnotation:
        result = raw.dslx.xls_dslx_enum_def_get_underlying(self._raw)
        return maybe_wrap(result)

    def to_string(self) -> str:
        return raw.dslx.xls_dslx_enum_def_to_string(self._raw)

    def __repr__(self) -> str:
        try:
            return f'<EnumDef {self.get_identifier()!r}>'
        except Exception:
            return '<EnumDef>'


@register_wrapper(raw.DslxType)
class DslxType:
    """Wrapper around raw.DslxType."""

    def __init__(self, _raw):
        self._raw = _raw

    def is_array(self) -> bool:
        return raw.dslx.xls_dslx_type_is_array(self._raw)

    def is_enum(self) -> bool:
        return raw.dslx.xls_dslx_type_is_enum(self._raw)

    def is_struct(self) -> bool:
        return raw.dslx.xls_dslx_type_is_struct(self._raw)

    def is_signed_bits(self) -> bool:
        return raw.dslx.xls_dslx_type_is_signed_bits(self._raw)

    def get_total_bit_count(self):
        return raw.dslx.xls_dslx_type_get_total_bit_count(self._raw)

    def get_struct_def(self) -> StructDef:
        result = raw.dslx.xls_dslx_type_get_struct_def(self._raw)
        return maybe_wrap(result)

    def get_enum_def(self) -> EnumDef:
        result = raw.dslx.xls_dslx_type_get_enum_def(self._raw)
        return maybe_wrap(result)

    def to_string(self) -> str:
        return raw.dslx.xls_dslx_type_to_string(self._raw)

    def __repr__(self) -> str:
        try:
            return f'<DslxType {self.to_string()}>'
        except Exception:
            return '<DslxType>'


@register_wrapper(raw.DslxTypeInfo)
class TypeInfo:
    """Wrapper around raw.DslxTypeInfo."""

    def __init__(self, _raw):
        self._raw = _raw

    def get_type_struct_def(self, node) -> DslxType:
        raw_node = maybe_unwrap(node)
        result = raw.dslx.xls_dslx_type_info_get_type_struct_def(self._raw, raw_node)
        return maybe_wrap(result)

    def get_type_enum_def(self, node) -> DslxType:
        raw_node = maybe_unwrap(node)
        result = raw.dslx.xls_dslx_type_info_get_type_enum_def(self._raw, raw_node)
        return maybe_wrap(result)

    def get_type_struct_member(self, member) -> DslxType:
        raw_node = maybe_unwrap(member)
        result = raw.dslx.xls_dslx_type_info_get_type_struct_member(self._raw, raw_node)
        return maybe_wrap(result)

    def get_type_constant_def(self, node) -> DslxType:
        raw_node = maybe_unwrap(node)
        result = raw.dslx.xls_dslx_type_info_get_type_constant_def(self._raw, raw_node)
        return maybe_wrap(result)

    def get_type_type_annotation(self, node) -> DslxType:
        raw_node = maybe_unwrap(node)
        result = raw.dslx.xls_dslx_type_info_get_type_type_annotation(self._raw, raw_node)
        return maybe_wrap(result)

    def get_const_expr(self, node) -> InterpValue:
        raw_node = maybe_unwrap(node)
        result = raw.dslx.xls_dslx_type_info_get_const_expr(self._raw, raw_node)
        return maybe_wrap(result)

    def get_requires_implicit_token(self, fn) -> bool:
        raw_fn = maybe_unwrap(fn)
        return raw.dslx.xls_dslx_type_info_get_requires_implicit_token(self._raw, raw_fn)

    def get_imported_type_info(self, import_node) -> TypeInfo:
        raw_node = maybe_unwrap(import_node)
        result = raw.dslx.xls_dslx_type_info_get_imported_type_info(self._raw, raw_node)
        return maybe_wrap(result)

    def get_all_invocation_callee_data(self, fn) -> DslxInvocationCalleeDataArray:
        raw_fn = maybe_unwrap(fn)
        result = raw.dslx.xls_dslx_type_info_get_all_invocation_callee_data(self._raw, raw_fn)
        return maybe_wrap(result)

    def get_unique_invocation_callee_data(self, fn) -> DslxInvocationCalleeData:
        raw_fn = maybe_unwrap(fn)
        result = raw.dslx.xls_dslx_type_info_get_unique_invocation_callee_data(self._raw, raw_fn)
        return maybe_wrap(result)

    def build_function_call_graph(self) -> CallGraph:
        result = raw.dslx.xls_dslx_type_info_build_function_call_graph(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<TypeInfo>'


@register_wrapper(raw.DslxParametricEnv)
class ParametricEnv:
    """Wrapper around raw.DslxParametricEnv."""

    def __init__(self, _raw):
        self._raw = _raw

    @classmethod
    def create(cls, names: list[str], values: Sequence[InterpValue]) -> ParametricEnv:
        """Create an empty parametric environment."""
        values = [maybe_unwrap(v) for v in values]
        result = raw.dslx.xls_dslx_parametric_env_create(names, values)
        return maybe_wrap(result)

    def clone(self) -> ParametricEnv:
        result = raw.dslx.xls_dslx_parametric_env_clone(self._raw)
        return maybe_wrap(result)

    def equals(self, other: ParametricEnv) -> bool:
        raw_other = maybe_unwrap(other)
        return raw.dslx.xls_dslx_parametric_env_equals(self._raw, raw_other)

    def get_binding_count(self) -> int:
        return raw.dslx.xls_dslx_parametric_env_get_binding_count(self._raw)

    def get_binding_identifier(self, i: int) -> str:
        return raw.dslx.xls_dslx_parametric_env_get_binding_identifier(self._raw, i)

    def get_binding_value(self, i: int) -> InterpValue:
        result = raw.dslx.xls_dslx_parametric_env_get_binding_value(self._raw, i)
        return maybe_wrap(result)

    def to_string(self) -> str:
        return raw.dslx.xls_dslx_parametric_env_to_string(self._raw)

    def __eq__(self, other) -> bool:
        return self.equals(other)

    def __repr__(self) -> str:
        try:
            return f'<ParametricEnv {self.to_string()}>'
        except Exception:
            return '<ParametricEnv>'


@register_wrapper(raw.DslxParametricEnvBorrowed)
class ParametricEnvBorrowed:
    """Wrapper around raw.DslxParametricEnvBorrowed."""

    def __init__(self, _raw):
        self._raw = _raw

    def __repr__(self) -> str:
        return '<ParametricEnvBorrowed>'


@register_wrapper(raw.DslxInterpValue)
class InterpValue:
    """Wrapper around raw.DslxInterpValue."""

    def __init__(self, _raw):
        self._raw = _raw

    @classmethod
    def make_ubits(cls, bit_count: int, val: int) -> InterpValue:
        result = raw.dslx.xls_dslx_interp_value_make_ubits(bit_count, val)
        return maybe_wrap(result)

    @classmethod
    def make_sbits(cls, bit_count: int, val: int) -> InterpValue:
        result = raw.dslx.xls_dslx_interp_value_make_sbits(bit_count, val)
        return maybe_wrap(result)

    @classmethod
    def make_array(cls, elems: list[InterpValue]) -> InterpValue:
        raw_elems = [maybe_unwrap(e) for e in elems]
        result = raw.dslx.xls_dslx_interp_value_make_array(raw_elems)
        return maybe_wrap(result)

    @classmethod
    def make_tuple(cls, elems: list[InterpValue]) -> InterpValue:
        raw_elems = [maybe_unwrap(e) for e in elems]
        result = raw.dslx.xls_dslx_interp_value_make_tuple(raw_elems)
        return maybe_wrap(result)

    @classmethod
    def make_enum(cls, enum_def, val: int) -> InterpValue:
        raw_def = maybe_unwrap(enum_def)
        is_signed = val < 0
        n_bits = ceil(log2(abs(val)) + 1) + is_signed
        if is_signed:
            bits = raw.c_api.xls_bits_make_sbits(n_bits, val)
        else:
            bits = raw.c_api.xls_bits_make_ubits(n_bits, val)
        result = raw.dslx.xls_dslx_interp_value_make_enum(raw_def, is_signed, bits)
        return maybe_wrap(result)

    @classmethod
    def from_string(cls, s: str, stl_path: str) -> InterpValue:
        result = raw.dslx.xls_dslx_interp_value_from_string(s, stl_path)
        return maybe_wrap(result)

    def clone(self) -> InterpValue:
        result = raw.dslx.xls_dslx_interp_value_clone(self._raw)
        return maybe_wrap(result)

    def to_string(self) -> str:
        return raw.dslx.xls_dslx_interp_value_to_string(self._raw)

    def convert_to_ir(self):
        """Convert to an IR Value."""
        result = raw.dslx.xls_dslx_interp_value_convert_to_ir(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        try:
            return f'<InterpValue {self.to_string()}>'
        except Exception:
            return '<InterpValue>'


@register_wrapper(raw.DslxCallGraph)
class CallGraph:
    """Wrapper around raw.DslxCallGraph."""

    def __init__(self, _raw):
        self._raw = _raw

    def get_function_count(self) -> int:
        return raw.dslx.xls_dslx_call_graph_get_function_count(self._raw)

    def get_function(self, i: int) -> DslxFunction:
        result = raw.dslx.xls_dslx_call_graph_get_function(self._raw, i)
        return maybe_wrap(result)

    def get_callee_count(self, fn) -> int:
        raw_fn = maybe_unwrap(fn)
        return raw.dslx.xls_dslx_call_graph_get_callee_count(self._raw, raw_fn)

    def get_callee_function(self, fn, i: int) -> DslxFunction:
        raw_fn = maybe_unwrap(fn)
        result = raw.dslx.xls_dslx_call_graph_get_callee_function(self._raw, raw_fn, i)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<CallGraph>'


# Register remaining raw DSLX types that don't have dedicated wrapper classes above
@register_wrapper(raw.DslxTypeDefinition)
class DslxTypeDefinition:
    def __init__(self, _raw):
        self._raw = _raw

    def get_colon_ref(self):
        result = raw.dslx.xls_dslx_type_definition_get_colon_ref(self._raw)
        return maybe_wrap(result)

    def get_type_alias(self):
        result = raw.dslx.xls_dslx_type_definition_get_type_alias(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<DslxTypeDefinition>'


@register_wrapper(raw.DslxTypeAlias)
class DslxTypeAlias:
    def __init__(self, _raw):
        self._raw = _raw

    def get_identifier(self) -> str:
        return raw.dslx.xls_dslx_type_alias_get_identifier(self._raw)

    def get_type_annotation(self):
        result = raw.dslx.xls_dslx_type_alias_get_type_annotation(self._raw)
        return maybe_wrap(result)

    def to_string(self) -> str:
        return raw.dslx.xls_dslx_type_alias_to_string(self._raw)

    def __repr__(self) -> str:
        try:
            return f'<DslxTypeAlias {self.get_identifier()!r}>'
        except Exception:
            return '<DslxTypeAlias>'


@register_wrapper(raw.DslxTypeAnnotation)
class DslxTypeAnnotation:
    def __init__(self, _raw):
        self._raw = _raw

    def get_type_ref_type_annotation(self):
        result = raw.dslx.xls_dslx_type_annotation_get_type_ref_type_annotation(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<DslxTypeAnnotation>'


@register_wrapper(raw.DslxTypeRefTypeAnnotation)
class DslxTypeRefTypeAnnotation:
    def __init__(self, _raw):
        self._raw = _raw

    def get_type_ref(self):
        result = raw.dslx.xls_dslx_type_ref_type_annotation_get_type_ref(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<DslxTypeRefTypeAnnotation>'


@register_wrapper(raw.DslxTypeRef)
class DslxTypeRef:
    def __init__(self, _raw):
        self._raw = _raw

    def get_type_definition(self):
        result = raw.dslx.xls_dslx_type_ref_get_type_definition(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<DslxTypeRef>'


@register_wrapper(raw.DslxConstantDef)
class DslxConstantDef:
    def __init__(self, _raw):
        self._raw = _raw

    def get_name(self) -> str:
        return raw.dslx.xls_dslx_constant_def_get_name(self._raw)

    def get_value(self):
        result = raw.dslx.xls_dslx_constant_def_get_value(self._raw)
        return maybe_wrap(result)

    def to_string(self) -> str:
        return raw.dslx.xls_dslx_constant_def_to_string(self._raw)

    def __repr__(self) -> str:
        try:
            return f'<DslxConstantDef {self.get_name()!r}>'
        except Exception:
            return '<DslxConstantDef>'


@register_wrapper(raw.DslxParam)
class DslxParam:
    def __init__(self, _raw):
        self._raw = _raw

    def get_name(self) -> str:
        return raw.dslx.xls_dslx_param_get_name(self._raw)

    def get_type_annotation(self):
        result = raw.dslx.xls_dslx_param_get_type_annotation(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        try:
            return f'<DslxParam {self.get_name()!r}>'
        except Exception:
            return '<DslxParam>'


@register_wrapper(raw.DslxParametricBinding)
class DslxParametricBinding:
    def __init__(self, _raw):
        self._raw = _raw

    def get_identifier(self) -> str:
        return raw.dslx.xls_dslx_parametric_binding_get_identifier(self._raw)

    def get_type_annotation(self):
        result = raw.dslx.xls_dslx_parametric_binding_get_type_annotation(self._raw)
        return maybe_wrap(result)

    def get_expr(self):
        result = raw.dslx.xls_dslx_parametric_binding_get_expr(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        try:
            return f'<DslxParametricBinding {self.get_identifier()!r}>'
        except Exception:
            return '<DslxParametricBinding>'


@register_wrapper(raw.DslxExpr)
class DslxExpr:
    def __init__(self, _raw):
        self._raw = _raw

    def to_string(self) -> str:
        return raw.dslx.xls_dslx_expr_to_string(self._raw)

    def get_owner_module(self):
        result = raw.dslx.xls_dslx_expr_get_owner_module(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<DslxExpr>'


@register_wrapper(raw.DslxQuickcheck)
class DslxQuickcheck:
    def __init__(self, _raw):
        self._raw = _raw

    def get_function(self):
        result = raw.dslx.xls_dslx_quickcheck_get_function(self._raw)
        return maybe_wrap(result)

    def get_count(self):
        return raw.dslx.xls_dslx_quickcheck_get_count(self._raw)

    def is_exhaustive(self) -> bool:
        return raw.dslx.xls_dslx_quickcheck_is_exhaustive(self._raw)

    def to_string(self) -> str:
        return raw.dslx.xls_dslx_quickcheck_to_string(self._raw)

    def __repr__(self) -> str:
        return '<DslxQuickcheck>'


@register_wrapper(raw.DslxModuleMember)
class DslxModuleMember:
    def __init__(self, _raw):
        self._raw = _raw

    def get_kind(self):
        return raw.dslx.xls_dslx_module_member_get_kind(self._raw)

    def get_function(self):
        result = raw.dslx.xls_dslx_module_member_get_function(self._raw)
        return maybe_wrap(result)

    def get_struct_def(self):
        result = raw.dslx.xls_dslx_module_member_get_struct_def(self._raw)
        return maybe_wrap(result)

    def get_enum_def(self):
        result = raw.dslx.xls_dslx_module_member_get_enum_def(self._raw)
        return maybe_wrap(result)

    def get_constant_def(self):
        result = raw.dslx.xls_dslx_module_member_get_constant_def(self._raw)
        return maybe_wrap(result)

    def get_type_alias(self):
        result = raw.dslx.xls_dslx_module_member_get_type_alias(self._raw)
        return maybe_wrap(result)

    def get_quickcheck(self):
        result = raw.dslx.xls_dslx_module_member_get_quickcheck(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<DslxModuleMember>'


@register_wrapper(raw.DslxStructMember)
class DslxStructMember:
    def __init__(self, _raw):
        self._raw = _raw

    def get_name(self) -> str:
        return raw.dslx.xls_dslx_struct_member_get_name(self._raw)

    def get_type(self):
        result = raw.dslx.xls_dslx_struct_member_get_type(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        try:
            return f'<DslxStructMember {self.get_name()!r}>'
        except Exception:
            return '<DslxStructMember>'


@register_wrapper(raw.DslxEnumMember)
class DslxEnumMember:
    def __init__(self, _raw):
        self._raw = _raw

    def get_name(self) -> str:
        return raw.dslx.xls_dslx_enum_member_get_name(self._raw)

    def get_value(self):
        result = raw.dslx.xls_dslx_enum_member_get_value(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        try:
            return f'<DslxEnumMember {self.get_name()!r}>'
        except Exception:
            return '<DslxEnumMember>'


@register_wrapper(raw.DslxTypeDim)
class DslxTypeDim:
    def __init__(self, _raw):
        self._raw = _raw

    def get_as_int64(self) -> int:
        return raw.dslx.xls_dslx_type_dim_get_as_int64(self._raw)

    def get_as_bool(self) -> bool:
        return raw.dslx.xls_dslx_type_dim_get_as_bool(self._raw)

    def __repr__(self) -> str:
        return '<DslxTypeDim>'


@register_wrapper(raw.DslxInvocation)
class DslxInvocation:
    def __init__(self, _raw):
        self._raw = _raw

    def __repr__(self) -> str:
        return '<DslxInvocation>'


@register_wrapper(raw.DslxInvocationData)
class DslxInvocationData:
    def __init__(self, _raw):
        self._raw = _raw

    def __repr__(self) -> str:
        return '<DslxInvocationData>'


@register_wrapper(raw.DslxInvocationCalleeData)
class DslxInvocationCalleeData:
    def __init__(self, _raw):
        self._raw = _raw

    def get_invocation(self):
        result = raw.dslx.xls_dslx_invocation_callee_data_get_invocation(self._raw)
        return maybe_wrap(result)

    def get_caller_bindings(self):
        result = raw.dslx.xls_dslx_invocation_callee_data_get_caller_bindings(self._raw)
        return maybe_wrap(result)

    def get_callee_bindings(self):
        result = raw.dslx.xls_dslx_invocation_callee_data_get_callee_bindings(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<DslxInvocationCalleeData>'


@register_wrapper(raw.DslxInvocationCalleeDataArray)
class DslxInvocationCalleeDataArray:
    def __init__(self, _raw):
        self._raw = _raw

    def get_count(self) -> int:
        return raw.dslx.xls_dslx_invocation_callee_data_array_get_count(self._raw)

    def get(self, i: int) -> DslxInvocationCalleeData:
        result = raw.dslx.xls_dslx_invocation_callee_data_array_get(self._raw, i)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<DslxInvocationCalleeDataArray>'


@register_wrapper(raw.DslxAttribute)
class DslxAttribute:
    def __init__(self, _raw):
        self._raw = _raw

    def get_kind(self):
        return raw.dslx.xls_dslx_attribute_get_kind(self._raw)

    def get_argument_count(self) -> int:
        return raw.dslx.xls_dslx_attribute_get_argument_count(self._raw)

    def get_argument_kind(self, i: int):
        return raw.dslx.xls_dslx_attribute_get_argument_kind(self._raw, i)

    def to_string(self) -> str:
        return raw.dslx.xls_dslx_attribute_to_string(self._raw)

    def __repr__(self) -> str:
        return '<DslxAttribute>'


@register_wrapper(raw.DslxColonRef)
class DslxColonRef:
    def __init__(self, _raw):
        self._raw = _raw

    def get_attr(self) -> str:
        return raw.dslx.xls_dslx_colon_ref_get_attr(self._raw)

    def resolve_import_subject(self):
        result = raw.dslx.xls_dslx_colon_ref_resolve_import_subject(self._raw)
        return maybe_wrap(result)

    def __repr__(self) -> str:
        return '<DslxColonRef>'


@register_wrapper(raw.DslxImport)
class DslxImport:
    def __init__(self, _raw):
        self._raw = _raw

    def get_subject_count(self) -> int:
        return raw.dslx.xls_dslx_import_get_subject_count(self._raw)

    def get_subject(self, i: int) -> str:
        return raw.dslx.xls_dslx_import_get_subject(self._raw, i)

    def __repr__(self) -> str:
        return '<DslxImport>'


# Convenience function: parse and typecheck DSLX
def parse_and_typecheck(
    text: str,
    path: str,
    module_name: str,
    import_data: ImportData,
) -> TypecheckedModule:
    """Parse DSLX source text and typecheck it."""
    raw_id = maybe_unwrap(import_data)
    result = raw.dslx.xls_dslx_parse_and_typecheck(text, path, module_name, raw_id)
    return maybe_wrap(result)


# ---------------------------------------------------------------------------
# Bulk-wrap all public functions from raw.dslx into this module's namespace
# ---------------------------------------------------------------------------
wrap_module(raw.dslx, globals())
