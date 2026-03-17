#pragma once
#include <memory>
#include <xls/public/c_api.h>
#include <xls/public/c_api_ir_builder.h>
#include <xls/public/c_api_dslx.h>
#include <xls/public/c_api_vast.h>

// ============================================================
// Deleters
// ============================================================
struct PackageDeleter {
    void operator()(xls_package *p) const { xls_package_free(p); }
};
struct FunctionJitDeleter {
    void operator()(xls_function_jit *p) const { xls_function_jit_free(p); }
};
struct ValueDeleter {
    void operator()(xls_value *p) const { xls_value_free(p); }
};
struct BitsDeleter {
    void operator()(xls_bits *p) const { xls_bits_free(p); }
};
struct BitsRopeDeleter {
    void operator()(xls_bits_rope *p) const { xls_bits_rope_free(p); }
};
struct ScheduleResultDeleter {
    void operator()(xls_schedule_and_codegen_result *p) const {
        xls_schedule_and_codegen_result_free(p);
    }
};
struct FunctionBuilderDeleter {
    void operator()(xls_function_builder *p) const {
        xls_function_builder_free(p);
    }
};
struct BValueDeleter {
    void operator()(xls_bvalue *p) const { xls_bvalue_free(p); }
};
struct DslxTypecheckedModuleDeleter {
    void operator()(xls_dslx_typechecked_module *p) const {
        xls_dslx_typechecked_module_free(p);
    }
};
struct DslxImportDataDeleter {
    void operator()(xls_dslx_import_data *p) const {
        xls_dslx_import_data_free(p);
    }
};
struct DslxParametricEnvDeleter {
    void operator()(xls_dslx_parametric_env *p) const {
        xls_dslx_parametric_env_free(p);
    }
};
struct DslxInterpValueDeleter {
    void operator()(xls_dslx_interp_value *p) const {
        xls_dslx_interp_value_free(p);
    }
};
struct DslxCallGraphDeleter {
    void operator()(xls_dslx_call_graph *p) const {
        xls_dslx_call_graph_free(p);
    }
};
struct DslxTypeDimDeleter {
    void operator()(xls_dslx_type_dim *p) const { xls_dslx_type_dim_free(p); }
};
struct DslxInvocationCalleeDataArrayDeleter {
    void operator()(xls_dslx_invocation_callee_data_array *p) const {
        xls_dslx_invocation_callee_data_array_free(p);
    }
};
struct DslxInvocationCalleeDataDeleter {
    void operator()(xls_dslx_invocation_callee_data *p) const {
        xls_dslx_invocation_callee_data_free(p);
    }
};
struct VastVerilogFileDeleter {
    void operator()(xls_vast_verilog_file *p) const {
        xls_vast_verilog_file_free(p);
    }
};

// ============================================================
// Wrapper structs — owned (unique_ptr) or borrowed (raw ptr)
// ============================================================

// --- c_api types ---
struct _Package {
    std::unique_ptr<xls_package, PackageDeleter> ptr;
    _Package() = default;
    _Package(xls_package *p) : ptr(p) {}
};

struct _FunctionBase {
    xls_function_base *ptr = nullptr;
    _FunctionBase() = default;
    _FunctionBase(xls_function_base *p) : ptr(p) {}
};

struct _Function {
    xls_function *ptr = nullptr;
    _Function() = default;
    _Function(xls_function *p) : ptr(p) {}
};

struct _FunctionType {
    xls_function_type *ptr = nullptr;
    _FunctionType() = default;
    _FunctionType(xls_function_type *p) : ptr(p) {}
};

struct _FunctionJit {
    std::unique_ptr<xls_function_jit, FunctionJitDeleter> ptr;
    _FunctionJit() = default;
    _FunctionJit(xls_function_jit *p) : ptr(p) {}
};

struct _Type {
    xls_type *ptr = nullptr;
    _Type() = default;
    _Type(xls_type *p) : ptr(p) {}
};

struct _Value {
    std::unique_ptr<xls_value, ValueDeleter> ptr;
    _Value() = default;
    _Value(xls_value *p) : ptr(p) {}
};

struct _Bits {
    std::unique_ptr<xls_bits, BitsDeleter> ptr;
    _Bits() = default;
    _Bits(xls_bits *p) : ptr(p) {}
};

struct _BitsRope {
    std::unique_ptr<xls_bits_rope, BitsRopeDeleter> ptr;
    _BitsRope() = default;
    _BitsRope(xls_bits_rope *p) : ptr(p) {}
};

struct _ScheduleAndCodegenResult {
    std::unique_ptr<xls_schedule_and_codegen_result, ScheduleResultDeleter> ptr;
    _ScheduleAndCodegenResult() = default;
    _ScheduleAndCodegenResult(xls_schedule_and_codegen_result *p) : ptr(p) {}
};

// --- ir_builder types ---
struct _FunctionBuilder {
    std::unique_ptr<xls_function_builder, FunctionBuilderDeleter> ptr;
    _FunctionBuilder() = default;
    _FunctionBuilder(xls_function_builder *p) : ptr(p) {}
};

struct _BuilderBase {
    xls_builder_base *ptr = nullptr;
    _BuilderBase() = default;
    _BuilderBase(xls_builder_base *p) : ptr(p) {}
};

struct _BValue {
    std::unique_ptr<xls_bvalue, BValueDeleter> ptr;
    _BValue() = default;
    _BValue(xls_bvalue *p) : ptr(p) {}
};

// --- dslx types ---
struct _DslxTypecheckedModule {
    std::unique_ptr<xls_dslx_typechecked_module, DslxTypecheckedModuleDeleter>
        ptr;
    _DslxTypecheckedModule() = default;
    _DslxTypecheckedModule(xls_dslx_typechecked_module *p) : ptr(p) {}
};

struct _DslxImportData {
    std::unique_ptr<xls_dslx_import_data, DslxImportDataDeleter> ptr;
    _DslxImportData() = default;
    _DslxImportData(xls_dslx_import_data *p) : ptr(p) {}
};

struct _DslxModule {
    xls_dslx_module *ptr = nullptr;
    _DslxModule() = default;
    _DslxModule(xls_dslx_module *p) : ptr(p) {}
};

struct _DslxTypeDefinition {
    xls_dslx_type_definition *ptr = nullptr;
    _DslxTypeDefinition() = default;
    _DslxTypeDefinition(xls_dslx_type_definition *p) : ptr(p) {}
};

struct _DslxStructDef {
    xls_dslx_struct_def *ptr = nullptr;
    _DslxStructDef() = default;
    _DslxStructDef(xls_dslx_struct_def *p) : ptr(p) {}
};

struct _DslxEnumDef {
    xls_dslx_enum_def *ptr = nullptr;
    _DslxEnumDef() = default;
    _DslxEnumDef(xls_dslx_enum_def *p) : ptr(p) {}
};

struct _DslxTypeAlias {
    xls_dslx_type_alias *ptr = nullptr;
    _DslxTypeAlias() = default;
    _DslxTypeAlias(xls_dslx_type_alias *p) : ptr(p) {}
};

struct _DslxTypeInfo {
    xls_dslx_type_info *ptr = nullptr;
    _DslxTypeInfo() = default;
    _DslxTypeInfo(xls_dslx_type_info *p) : ptr(p) {}
};

struct _DslxType {
    const xls_dslx_type *ptr = nullptr;
    _DslxType() = default;
    _DslxType(const xls_dslx_type *p) : ptr(p) {}
};

struct _DslxTypeAnnotation {
    xls_dslx_type_annotation *ptr = nullptr;
    _DslxTypeAnnotation() = default;
    _DslxTypeAnnotation(xls_dslx_type_annotation *p) : ptr(p) {}
};

struct _DslxConstantDef {
    xls_dslx_constant_def *ptr = nullptr;
    _DslxConstantDef() = default;
    _DslxConstantDef(xls_dslx_constant_def *p) : ptr(p) {}
};

struct _DslxFunction {
    xls_dslx_function *ptr = nullptr;
    _DslxFunction() = default;
    _DslxFunction(xls_dslx_function *p) : ptr(p) {}
};

struct _DslxQuickcheck {
    xls_dslx_quickcheck *ptr = nullptr;
    _DslxQuickcheck() = default;
    _DslxQuickcheck(xls_dslx_quickcheck *p) : ptr(p) {}
};

struct _DslxParam {
    xls_dslx_param *ptr = nullptr;
    _DslxParam() = default;
    _DslxParam(xls_dslx_param *p) : ptr(p) {}
};

struct _DslxParametricBinding {
    xls_dslx_parametric_binding *ptr = nullptr;
    _DslxParametricBinding() = default;
    _DslxParametricBinding(xls_dslx_parametric_binding *p) : ptr(p) {}
};

struct _DslxExpr {
    xls_dslx_expr *ptr = nullptr;
    _DslxExpr() = default;
    _DslxExpr(xls_dslx_expr *p) : ptr(p) {}
};

struct _DslxInvocation {
    xls_dslx_invocation *ptr = nullptr;
    _DslxInvocation() = default;
    _DslxInvocation(xls_dslx_invocation *p) : ptr(p) {}
};

struct _DslxInvocationCalleeDataArray {
    std::unique_ptr<
        xls_dslx_invocation_callee_data_array,
        DslxInvocationCalleeDataArrayDeleter>
        ptr;
    _DslxInvocationCalleeDataArray() = default;
    _DslxInvocationCalleeDataArray(xls_dslx_invocation_callee_data_array *p)
        : ptr(p) {}
};

struct _DslxInvocationCalleeData {
    // Can be borrowed (from array) or owned (from clone)
    xls_dslx_invocation_callee_data *ptr = nullptr;
    bool owned = false;
    _DslxInvocationCalleeData() = default;
    _DslxInvocationCalleeData(
        xls_dslx_invocation_callee_data *p,
        bool own = false
    )
        : ptr(p), owned(own) {}
    ~_DslxInvocationCalleeData() {
        if (owned && ptr)
            xls_dslx_invocation_callee_data_free(ptr);
    }
    _DslxInvocationCalleeData(const _DslxInvocationCalleeData &) = delete;
    _DslxInvocationCalleeData &
    operator=(const _DslxInvocationCalleeData &) = delete;
    _DslxInvocationCalleeData(_DslxInvocationCalleeData &&o) noexcept
        : ptr(o.ptr), owned(o.owned) {
        o.ptr = nullptr;
        o.owned = false;
    }
    _DslxInvocationCalleeData &
    operator=(_DslxInvocationCalleeData &&o) noexcept {
        if (this != &o) {
            if (owned && ptr)
                xls_dslx_invocation_callee_data_free(ptr);
            ptr = o.ptr;
            owned = o.owned;
            o.ptr = nullptr;
            o.owned = false;
        }
        return *this;
    }
};

struct _DslxInvocationData {
    xls_dslx_invocation_data *ptr = nullptr;
    _DslxInvocationData() = default;
    _DslxInvocationData(xls_dslx_invocation_data *p) : ptr(p) {}
};

struct _DslxModuleMember {
    xls_dslx_module_member *ptr = nullptr;
    _DslxModuleMember() = default;
    _DslxModuleMember(xls_dslx_module_member *p) : ptr(p) {}
};

struct _DslxTypeDim {
    std::unique_ptr<xls_dslx_type_dim, DslxTypeDimDeleter> ptr;
    _DslxTypeDim() = default;
    _DslxTypeDim(xls_dslx_type_dim *p) : ptr(p) {}
};

struct _DslxParametricEnv {
    std::unique_ptr<xls_dslx_parametric_env, DslxParametricEnvDeleter> ptr;
    _DslxParametricEnv() = default;
    _DslxParametricEnv(xls_dslx_parametric_env *p) : ptr(p) {}
};

struct _DslxParametricEnvBorrowed {
    const xls_dslx_parametric_env *ptr = nullptr;
    _DslxParametricEnvBorrowed() = default;
    _DslxParametricEnvBorrowed(const xls_dslx_parametric_env *p) : ptr(p) {}
};

struct _DslxInterpValue {
    std::unique_ptr<xls_dslx_interp_value, DslxInterpValueDeleter> ptr;
    _DslxInterpValue() = default;
    _DslxInterpValue(xls_dslx_interp_value *p) : ptr(p) {}
};

struct _DslxCallGraph {
    std::unique_ptr<xls_dslx_call_graph, DslxCallGraphDeleter> ptr;
    _DslxCallGraph() = default;
    _DslxCallGraph(xls_dslx_call_graph *p) : ptr(p) {}
};

struct _DslxAttribute {
    xls_dslx_attribute *ptr = nullptr;
    _DslxAttribute() = default;
    _DslxAttribute(xls_dslx_attribute *p) : ptr(p) {}
};

struct _DslxStructMember {
    xls_dslx_struct_member *ptr = nullptr;
    _DslxStructMember() = default;
    _DslxStructMember(xls_dslx_struct_member *p) : ptr(p) {}
};

struct _DslxEnumMember {
    xls_dslx_enum_member *ptr = nullptr;
    _DslxEnumMember() = default;
    _DslxEnumMember(xls_dslx_enum_member *p) : ptr(p) {}
};

struct _DslxTypeRefTypeAnnotation {
    xls_dslx_type_ref_type_annotation *ptr = nullptr;
    _DslxTypeRefTypeAnnotation() = default;
    _DslxTypeRefTypeAnnotation(xls_dslx_type_ref_type_annotation *p) : ptr(p) {}
};

struct _DslxTypeRef {
    xls_dslx_type_ref *ptr = nullptr;
    _DslxTypeRef() = default;
    _DslxTypeRef(xls_dslx_type_ref *p) : ptr(p) {}
};

struct _DslxColonRef {
    xls_dslx_colon_ref *ptr = nullptr;
    _DslxColonRef() = default;
    _DslxColonRef(xls_dslx_colon_ref *p) : ptr(p) {}
};

struct _DslxImport {
    xls_dslx_import *ptr = nullptr;
    _DslxImport() = default;
    _DslxImport(xls_dslx_import *p) : ptr(p) {}
};

// ============================================================
// C++ enum wrappers for C-style typedef'd int enums
// ============================================================

// c_api enums
enum class XlsValueKind : int32_t {
    INVALID = xls_value_kind_invalid,
    BITS = xls_value_kind_bits,
    ARRAY = xls_value_kind_array,
    TUPLE = xls_value_kind_tuple,
    TOKEN = xls_value_kind_token,
};

enum class XlsCallingConvention : int32_t {
    TYPICAL = xls_calling_convention_typical,
    IMPLICIT_TOKEN = xls_calling_convention_implicit_token,
    PROC_NEXT = xls_calling_convention_proc_next,
};

enum class XlsFormatPreference : int32_t {
    DEFAULT = xls_format_preference_default,
    BINARY = xls_format_preference_binary,
    SIGNED_DECIMAL = xls_format_preference_signed_decimal,
    UNSIGNED_DECIMAL = xls_format_preference_unsigned_decimal,
    HEX = xls_format_preference_hex,
    PLAIN_BINARY = xls_format_preference_plain_binary,
    PLAIN_HEX = xls_format_preference_plain_hex,
    ZERO_PADDED_BINARY = xls_format_preference_zero_padded_binary,
    ZERO_PADDED_HEX = xls_format_preference_zero_padded_hex,
};

// dslx enums
enum class XlsDslxTypeDefinitionKind : int32_t {
    TYPE_ALIAS = xls_dslx_type_definition_kind_type_alias,
    STRUCT_DEF = xls_dslx_type_definition_kind_struct_def,
    ENUM_DEF = xls_dslx_type_definition_kind_enum_def,
    COLON_REF = xls_dslx_type_definition_kind_colon_ref,
    PROC_DEF = xls_dslx_type_definition_kind_proc_def,
    USE_TREE_ENTRY = xls_dslx_type_definition_kind_use_tree_entry,
};

enum class XlsDslxModuleMemberKind : int32_t {
    FUNCTION = xls_dslx_module_member_kind_function,
    PROC = xls_dslx_module_member_kind_proc,
    TEST_FUNCTION = xls_dslx_module_member_kind_test_function,
    TEST_PROC = xls_dslx_module_member_kind_test_proc,
    QUICK_CHECK = xls_dslx_module_member_kind_quick_check,
    TYPE_ALIAS = xls_dslx_module_member_kind_type_alias,
    STRUCT_DEF = xls_dslx_module_member_kind_struct_def,
    PROC_DEF = xls_dslx_module_member_kind_proc_def,
    ENUM_DEF = xls_dslx_module_member_kind_enum_def,
    CONSTANT_DEF = xls_dslx_module_member_kind_constant_def,
    IMPORT = xls_dslx_module_member_kind_import,
    CONST_ASSERT = xls_dslx_module_member_kind_const_assert,
    IMPL = xls_dslx_module_member_kind_impl,
    TRAIT = xls_dslx_module_member_kind_trait,
    VERBATIM_NODE = xls_dslx_module_member_kind_verbatim_node,
    USE = xls_dslx_module_member_kind_use,
    PROC_ALIAS = xls_dslx_module_member_kind_proc_alias,
};

enum class XlsDslxAttributeKind : int32_t {
    CFG = xls_dslx_attribute_kind_cfg,
    DSLX_FORMAT_DISABLE = xls_dslx_attribute_kind_dslx_format_disable,
    EXTERN_VERILOG = xls_dslx_attribute_kind_extern_verilog,
    SV_TYPE = xls_dslx_attribute_kind_sv_type,
    TEST = xls_dslx_attribute_kind_test,
    TEST_PROC = xls_dslx_attribute_kind_test_proc,
    QUICKCHECK = xls_dslx_attribute_kind_quickcheck,
};

enum class XlsDslxAttributeArgumentKind : int32_t {
    STRING = xls_dslx_attribute_argument_kind_string,
    STRING_KEY_VALUE = xls_dslx_attribute_argument_kind_string_key_value,
    INT_KEY_VALUE = xls_dslx_attribute_argument_kind_int_key_value,
    STRING_LITERAL = xls_dslx_attribute_argument_kind_string_literal,
};

// vast enums
enum class XlsVastFileType : int32_t {
    VERILOG = xls_vast_file_type_verilog,
    SYSTEM_VERILOG = xls_vast_file_type_system_verilog,
};

enum class XlsVastOperatorKind : int32_t {
    NEGATE = xls_vast_operator_kind_negate,
    BITWISE_NOT = xls_vast_operator_kind_bitwise_not,
    LOGICAL_NOT = xls_vast_operator_kind_logical_not,
    AND_REDUCE = xls_vast_operator_kind_and_reduce,
    OR_REDUCE = xls_vast_operator_kind_or_reduce,
    XOR_REDUCE = xls_vast_operator_kind_xor_reduce,
    ADD = xls_vast_operator_kind_add,
    LOGICAL_AND = xls_vast_operator_kind_logical_and,
    BITWISE_AND = xls_vast_operator_kind_bitwise_and,
    NE = xls_vast_operator_kind_ne,
    CASE_NE = xls_vast_operator_kind_case_ne,
    EQ = xls_vast_operator_kind_eq,
    CASE_EQ = xls_vast_operator_kind_case_eq,
    GE = xls_vast_operator_kind_ge,
    GT = xls_vast_operator_kind_gt,
    LE = xls_vast_operator_kind_le,
    LT = xls_vast_operator_kind_lt,
    DIV = xls_vast_operator_kind_div,
    MOD = xls_vast_operator_kind_mod,
    MUL = xls_vast_operator_kind_mul,
    POWER = xls_vast_operator_kind_power,
    BITWISE_OR = xls_vast_operator_kind_bitwise_or,
    LOGICAL_OR = xls_vast_operator_kind_logical_or,
    BITWISE_XOR = xls_vast_operator_kind_bitwise_xor,
    SHLL = xls_vast_operator_kind_shll,
    SHRA = xls_vast_operator_kind_shra,
    SHRL = xls_vast_operator_kind_shrl,
    SUB = xls_vast_operator_kind_sub,
    NE_X = xls_vast_operator_kind_ne_x,
    EQ_X = xls_vast_operator_kind_eq_x,
};

enum class XlsVastModulePortDirection : int32_t {
    INPUT = xls_vast_module_port_direction_input,
    OUTPUT = xls_vast_module_port_direction_output,
    INOUT = xls_vast_module_port_direction_inout,
};

enum class XlsVastDataKind : int32_t {
    REG = xls_vast_data_kind_reg,
    WIRE = xls_vast_data_kind_wire,
    LOGIC = xls_vast_data_kind_logic,
    INTEGER = xls_vast_data_kind_integer,
    INT = xls_vast_data_kind_int,
    USER = xls_vast_data_kind_user,
    UNTYPED_ENUM = xls_vast_data_kind_untyped_enum,
    GENVAR = xls_vast_data_kind_genvar,
};

// --- vast types ---
struct _VastVerilogFile {
    std::unique_ptr<xls_vast_verilog_file, VastVerilogFileDeleter> ptr;
    _VastVerilogFile() = default;
    _VastVerilogFile(xls_vast_verilog_file *p) : ptr(p) {}
};

struct _VastVerilogModule {
    xls_vast_verilog_module *ptr = nullptr;
    _VastVerilogModule() = default;
    _VastVerilogModule(xls_vast_verilog_module *p) : ptr(p) {}
};

struct _VastExpression {
    xls_vast_expression *ptr = nullptr;
    _VastExpression() = default;
    _VastExpression(xls_vast_expression *p) : ptr(p) {}
};

struct _VastLogicRef {
    xls_vast_logic_ref *ptr = nullptr;
    _VastLogicRef() = default;
    _VastLogicRef(xls_vast_logic_ref *p) : ptr(p) {}
};

struct _VastDataType {
    xls_vast_data_type *ptr = nullptr;
    _VastDataType() = default;
    _VastDataType(xls_vast_data_type *p) : ptr(p) {}
};

struct _VastIndexableExpression {
    xls_vast_indexable_expression *ptr = nullptr;
    _VastIndexableExpression() = default;
    _VastIndexableExpression(xls_vast_indexable_expression *p) : ptr(p) {}
};

struct _VastSlice {
    xls_vast_slice *ptr = nullptr;
    _VastSlice() = default;
    _VastSlice(xls_vast_slice *p) : ptr(p) {}
};

struct _VastLiteral {
    xls_vast_literal *ptr = nullptr;
    _VastLiteral() = default;
    _VastLiteral(xls_vast_literal *p) : ptr(p) {}
};

struct _VastInstantiation {
    xls_vast_instantiation *ptr = nullptr;
    _VastInstantiation() = default;
    _VastInstantiation(xls_vast_instantiation *p) : ptr(p) {}
};

struct _VastContinuousAssignment {
    xls_vast_continuous_assignment *ptr = nullptr;
    _VastContinuousAssignment() = default;
    _VastContinuousAssignment(xls_vast_continuous_assignment *p) : ptr(p) {}
};

struct _VastComment {
    xls_vast_comment *ptr = nullptr;
    _VastComment() = default;
    _VastComment(xls_vast_comment *p) : ptr(p) {}
};

struct _VastInlineVerilogStatement {
    xls_vast_inline_verilog_statement *ptr = nullptr;
    _VastInlineVerilogStatement() = default;
    _VastInlineVerilogStatement(xls_vast_inline_verilog_statement *p)
        : ptr(p) {}
};

struct _VastMacroRef {
    xls_vast_macro_ref *ptr = nullptr;
    _VastMacroRef() = default;
    _VastMacroRef(xls_vast_macro_ref *p) : ptr(p) {}
};

struct _VastMacroStatement {
    xls_vast_macro_statement *ptr = nullptr;
    _VastMacroStatement() = default;
    _VastMacroStatement(xls_vast_macro_statement *p) : ptr(p) {}
};

struct _VastAlwaysBase {
    xls_vast_always_base *ptr = nullptr;
    _VastAlwaysBase() = default;
    _VastAlwaysBase(xls_vast_always_base *p) : ptr(p) {}
};

struct _VastStatement {
    xls_vast_statement *ptr = nullptr;
    _VastStatement() = default;
    _VastStatement(xls_vast_statement *p) : ptr(p) {}
};

struct _VastStatementBlock {
    xls_vast_statement_block *ptr = nullptr;
    _VastStatementBlock() = default;
    _VastStatementBlock(xls_vast_statement_block *p) : ptr(p) {}
};

struct _VastGenerateLoop {
    xls_vast_generate_loop *ptr = nullptr;
    _VastGenerateLoop() = default;
    _VastGenerateLoop(xls_vast_generate_loop *p) : ptr(p) {}
};

struct _VastModulePort {
    xls_vast_module_port *ptr = nullptr;
    _VastModulePort() = default;
    _VastModulePort(xls_vast_module_port *p) : ptr(p) {}
};

struct _VastDef {
    xls_vast_def *ptr = nullptr;
    _VastDef() = default;
    _VastDef(xls_vast_def *p) : ptr(p) {}
};

struct _VastParameterRef {
    xls_vast_parameter_ref *ptr = nullptr;
    _VastParameterRef() = default;
    _VastParameterRef(xls_vast_parameter_ref *p) : ptr(p) {}
};

struct _VastConditional {
    xls_vast_conditional *ptr = nullptr;
    _VastConditional() = default;
    _VastConditional(xls_vast_conditional *p) : ptr(p) {}
};

struct _VastCaseStatement {
    xls_vast_case_statement *ptr = nullptr;
    _VastCaseStatement() = default;
    _VastCaseStatement(xls_vast_case_statement *p) : ptr(p) {}
};

struct _VastLocalparamRef {
    xls_vast_localparam_ref *ptr = nullptr;
    _VastLocalparamRef() = default;
    _VastLocalparamRef(xls_vast_localparam_ref *p) : ptr(p) {}
};

struct _VastBlankLine {
    xls_vast_blank_line *ptr = nullptr;
    _VastBlankLine() = default;
    _VastBlankLine(xls_vast_blank_line *p) : ptr(p) {}
};

struct _VastConcat {
    xls_vast_concat *ptr = nullptr;
    _VastConcat() = default;
    _VastConcat(xls_vast_concat *p) : ptr(p) {}
};

struct _VastIndex {
    xls_vast_index *ptr = nullptr;
    _VastIndex() = default;
    _VastIndex(xls_vast_index *p) : ptr(p) {}
};
