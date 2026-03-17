#include "_dslx.h"
#include "_types.h"
#include "_helpers.h"
#include "nanobind/nanobind.h"
#include <map>
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>
#include <nanobind/stl/bind_map.h>

using namespace nb::literals;

void bind_dslx(nb::module_ &m) {
    // ============================================================
    // Enums
    // ============================================================
    nb::enum_<XlsDslxTypeDefinitionKind>(m, "TypeDefinitionKind")
        // .value("TYPE_ALIAS", XlsDslxTypeDefinitionKind::TYPE_ALIAS)
        // .value("STRUCT_DEF", XlsDslxTypeDefinitionKind::STRUCT_DEF)
        // .value("ENUM_DEF", XlsDslxTypeDefinitionKind::ENUM_DEF)
        // .value("COLON_REF", XlsDslxTypeDefinitionKind::COLON_REF)
        // .value("PROC_DEF", XlsDslxTypeDefinitionKind::PROC_DEF)
        // .value("USE_TREE_ENTRY", XlsDslxTypeDefinitionKind::USE_TREE_ENTRY)
        .export_values();

    nb::enum_<XlsDslxModuleMemberKind>(m, "ModuleMemberKind")
        // .value("FUNCTION", XlsDslxModuleMemberKind::FUNCTION)
        // .value("PROC", XlsDslxModuleMemberKind::PROC)
        // .value("TEST_FUNCTION", XlsDslxModuleMemberKind::TEST_FUNCTION)
        // .value("TEST_PROC", XlsDslxModuleMemberKind::TEST_PROC)
        // .value("QUICK_CHECK", XlsDslxModuleMemberKind::QUICK_CHECK)
        // .value("TYPE_ALIAS", XlsDslxModuleMemberKind::TYPE_ALIAS)
        // .value("STRUCT_DEF", XlsDslxModuleMemberKind::STRUCT_DEF)
        // .value("PROC_DEF", XlsDslxModuleMemberKind::PROC_DEF)
        // .value("ENUM_DEF", XlsDslxModuleMemberKind::ENUM_DEF)
        // .value("CONSTANT_DEF", XlsDslxModuleMemberKind::CONSTANT_DEF)
        // .value("IMPORT", XlsDslxModuleMemberKind::IMPORT)
        // .value("CONST_ASSERT", XlsDslxModuleMemberKind::CONST_ASSERT)
        // .value("IMPL", XlsDslxModuleMemberKind::IMPL)
        // .value("TRAIT", XlsDslxModuleMemberKind::TRAIT)
        // .value("VERBATIM_NODE", XlsDslxModuleMemberKind::VERBATIM_NODE)
        // .value("USE", XlsDslxModuleMemberKind::USE)
        // .value("PROC_ALIAS", XlsDslxModuleMemberKind::PROC_ALIAS)
        .export_values();

    nb::enum_<XlsDslxAttributeKind>(m, "AttributeKind")
        // .value("CFG", XlsDslxAttributeKind::CFG)
        // .value("DSLX_FORMAT_DISABLE",
        // XlsDslxAttributeKind::DSLX_FORMAT_DISABLE) .value("EXTERN_VERILOG",
        // XlsDslxAttributeKind::EXTERN_VERILOG) .value("SV_TYPE",
        // XlsDslxAttributeKind::SV_TYPE) .value("TEST",
        // XlsDslxAttributeKind::TEST) .value("TEST_PROC",
        // XlsDslxAttributeKind::TEST_PROC) .value("QUICKCHECK",
        // XlsDslxAttributeKind::QUICKCHECK)
        .export_values();

    nb::enum_<XlsDslxAttributeArgumentKind>(m, "AttributeArgumentKind")
        // .value("STRING", XlsDslxAttributeArgumentKind::STRING)
        // .value(
        //     "STRING_KEY_VALUE", XlsDslxAttributeArgumentKind::STRING_KEY_VALUE
        // )
        // .value("INT_KEY_VALUE", XlsDslxAttributeArgumentKind::INT_KEY_VALUE)
        // .value("STRING_LITERAL", XlsDslxAttributeArgumentKind::STRING_LITERAL)
        .export_values();

    // ============================================================
    // ParametricEnv
    // ============================================================
    m.def(
        "xls_dslx_parametric_env_create",
        // [](std::vector<std::pair<std::string, _DslxInterpValue *>> items)
        [](const std::vector<std::string> &names,
           const std::vector<_DslxInterpValue *> values) -> _DslxParametricEnv {
            std::vector<xls_dslx_parametric_env_item> c_items;
            for (size_t i = 0; i < names.size(); ++i) {
                c_items.push_back(
                    xls_dslx_parametric_env_item{
                        names[i].c_str(), values[i]->ptr.get()
                    }
                );
            }
            char *error = nullptr;
            xls_dslx_parametric_env *env = nullptr;
            bool ok = xls_dslx_parametric_env_create(
                c_items.data(), c_items.size(), &error, &env
            );
            check_result(ok, error);
            return _DslxParametricEnv(env);
        },
        "names"_a,
        "values"_a
    );

    m.def(
        "xls_dslx_parametric_env_clone",
        [](const _DslxParametricEnv &env) -> _DslxParametricEnv {
            return _DslxParametricEnv(
                xls_dslx_parametric_env_clone(env.ptr.get())
            );
        },
        "env"_a
    );

    m.def(
        "xls_dslx_parametric_env_equals",
        [](const _DslxParametricEnv &a, const _DslxParametricEnv &b) -> bool {
            return xls_dslx_parametric_env_equals(a.ptr.get(), b.ptr.get());
        },
        "lhs"_a,
        "rhs"_a
    );

    m.def(
        "xls_dslx_parametric_env_less_than",
        [](const _DslxParametricEnv &a, const _DslxParametricEnv &b) -> bool {
            return xls_dslx_parametric_env_less_than(a.ptr.get(), b.ptr.get());
        },
        "lhs"_a,
        "rhs"_a
    );

    m.def(
        "xls_dslx_parametric_env_hash",
        [](const _DslxParametricEnv &env) -> uint64_t {
            return xls_dslx_parametric_env_hash(env.ptr.get());
        },
        "env"_a
    );

    m.def(
        "xls_dslx_parametric_env_to_string",
        [](const _DslxParametricEnv &env) -> std::string {
            return own_c_str(xls_dslx_parametric_env_to_string(env.ptr.get()));
        },
        "env"_a
    );

    m.def(
        "xls_dslx_parametric_env_get_binding_count",
        [](const _DslxParametricEnv &env) -> int64_t {
            return xls_dslx_parametric_env_get_binding_count(env.ptr.get());
        },
        "env"_a
    );

    m.def(
        "xls_dslx_parametric_env_get_binding_identifier",
        [](const _DslxParametricEnv &env, int64_t index) -> std::string {
            return xls_dslx_parametric_env_get_binding_identifier(
                env.ptr.get(), index
            );
        },
        "env"_a,
        "index"_a
    );

    m.def(
        "xls_dslx_parametric_env_get_binding_value",
        [](const _DslxParametricEnv &env, int64_t index) -> _DslxInterpValue {
            return _DslxInterpValue(
                xls_dslx_parametric_env_get_binding_value(env.ptr.get(), index)
            );
        },
        "env"_a,
        "index"_a
    );

    // ============================================================
    // InterpValue
    // ============================================================
    m.def(
        "xls_dslx_interp_value_make_ubits",
        [](int64_t bit_count, uint64_t value) -> _DslxInterpValue {
            return _DslxInterpValue(
                xls_dslx_interp_value_make_ubits(bit_count, value)
            );
        },
        "bit_count"_a,
        "value"_a
    );

    m.def(
        "xls_dslx_interp_value_make_sbits",
        [](int64_t bit_count, int64_t value) -> _DslxInterpValue {
            return _DslxInterpValue(
                xls_dslx_interp_value_make_sbits(bit_count, value)
            );
        },
        "bit_count"_a,
        "value"_a
    );

    m.def(
        "xls_dslx_interp_value_make_enum",
        [](const _DslxEnumDef &def,
           bool is_signed,
           const _Bits &bits) -> _DslxInterpValue {
            char *error = nullptr;
            xls_dslx_interp_value *result = nullptr;
            bool ok = xls_dslx_interp_value_make_enum(
                def.ptr, is_signed, bits.ptr.get(), &error, &result
            );
            check_result(ok, error);
            return _DslxInterpValue(result);
        },
        "enum_def"_a,
        "is_signed"_a,
        "bits"_a
    );

    m.def(
        "xls_dslx_interp_value_make_tuple",
        [](std::vector<_DslxInterpValue *> elements) -> _DslxInterpValue {
            char *error = nullptr;
            xls_dslx_interp_value *result = nullptr;
            std::vector<xls_dslx_interp_value *> c_elems;
            for (auto *v : elements)
                c_elems.push_back(v->ptr.get());
            bool ok = xls_dslx_interp_value_make_tuple(
                c_elems.size(), c_elems.data(), &error, &result
            );
            check_result(ok, error);
            return _DslxInterpValue(result);
        },
        "elements"_a
    );

    m.def(
        "xls_dslx_interp_value_make_array",
        [](std::vector<_DslxInterpValue *> elements) -> _DslxInterpValue {
            char *error = nullptr;
            xls_dslx_interp_value *result = nullptr;
            std::vector<xls_dslx_interp_value *> c_elems;
            for (auto *v : elements)
                c_elems.push_back(v->ptr.get());
            bool ok = xls_dslx_interp_value_make_array(
                c_elems.size(), c_elems.data(), &error, &result
            );
            check_result(ok, error);
            return _DslxInterpValue(result);
        },
        "elements"_a
    );

    m.def(
        "xls_dslx_interp_value_clone",
        [](const _DslxInterpValue &v) -> _DslxInterpValue {
            return _DslxInterpValue(xls_dslx_interp_value_clone(v.ptr.get()));
        },
        "value"_a
    );

    m.def(
        "xls_dslx_interp_value_from_string",
        [](const std::string &text,
           const std::string &dslx_stdlib_path) -> _DslxInterpValue {
            char *error = nullptr;
            xls_dslx_interp_value *result = nullptr;
            bool ok = xls_dslx_interp_value_from_string(
                text.c_str(), dslx_stdlib_path.c_str(), &error, &result
            );
            check_result(ok, error);
            return _DslxInterpValue(result);
        },
        "text"_a,
        "dslx_stdlib_path"_a
    );

    m.def(
        "xls_dslx_interp_value_to_string",
        [](const _DslxInterpValue &v) -> std::string {
            return own_c_str(xls_dslx_interp_value_to_string(v.ptr.get()));
        },
        "value"_a
    );

    m.def(
        "xls_dslx_interp_value_convert_to_ir",
        [](const _DslxInterpValue &v) -> _Value {
            char *error = nullptr;
            xls_value *result = nullptr;
            bool ok = xls_dslx_interp_value_convert_to_ir(
                v.ptr.get(), &error, &result
            );
            check_result(ok, error);
            return _Value(result);
        },
        "value"_a
    );

    // ============================================================
    // ImportData
    // ============================================================
    m.def(
        "xls_dslx_import_data_create",
        [](const std::string &dslx_stdlib_path,
           std::vector<std::string> additional_search_paths) -> _DslxImportData {
            std::vector<const char *> c_paths;
            for (auto &s : additional_search_paths)
                c_paths.push_back(s.c_str());
            return _DslxImportData(xls_dslx_import_data_create(
                dslx_stdlib_path.c_str(), c_paths.data(), c_paths.size()
            ));
        },
        "dslx_stdlib_path"_a,
        "additional_search_paths"_a = std::vector<std::string>()
    );

    // ============================================================
    // TypecheckedModule
    // ============================================================
    m.def(
        "xls_dslx_parse_and_typecheck",
        [](const std::string &text,
           const std::string &path,
           const std::string &module_name,
           _DslxImportData &import_data) -> _DslxTypecheckedModule {
            char *error = nullptr;
            xls_dslx_typechecked_module *result = nullptr;
            bool ok = xls_dslx_parse_and_typecheck(
                text.c_str(),
                path.c_str(),
                module_name.c_str(),
                import_data.ptr.get(),
                &error,
                &result
            );
            check_result(ok, error);
            return _DslxTypecheckedModule(result);
        },
        nb::keep_alive<0, 4>(),
        "text"_a,
        "path"_a,
        "module_name"_a,
        "import_data"_a
    );

    m.def(
        "xls_dslx_typechecked_module_get_module",
        [](const _DslxTypecheckedModule &tm) -> _DslxModule {
            return _DslxModule(
                xls_dslx_typechecked_module_get_module(tm.ptr.get())
            );
        },
        nb::keep_alive<0, 1>(),
        "typechecked_module"_a
    );

    m.def(
        "xls_dslx_typechecked_module_get_type_info",
        [](const _DslxTypecheckedModule &tm) -> _DslxTypeInfo {
            return _DslxTypeInfo(
                xls_dslx_typechecked_module_get_type_info(tm.ptr.get())
            );
        },
        nb::keep_alive<0, 1>(),
        "typechecked_module"_a
    );

    // ============================================================
    // Module
    // ============================================================
    m.def(
        "xls_dslx_module_get_member_count",
        [](const _DslxModule &mod) -> int64_t {
            return xls_dslx_module_get_member_count(mod.ptr);
        },
        "module"_a
    );

    m.def(
        "xls_dslx_module_get_member",
        [](const _DslxModule &mod, int64_t index) -> _DslxModuleMember {
            return _DslxModuleMember(
                xls_dslx_module_get_member(mod.ptr, index)
            );
        },
        nb::keep_alive<0, 1>(),
        "module"_a,
        "index"_a
    );

    m.def(
        "xls_dslx_module_member_get_kind",
        [](const _DslxModuleMember &mm) -> XlsDslxModuleMemberKind {
            return static_cast<XlsDslxModuleMemberKind>(
                xls_dslx_module_member_get_kind(mm.ptr)
            );
        },
        "member"_a
    );

    m.def(
        "xls_dslx_module_member_get_function",
        [](const _DslxModuleMember &mm) -> nb::object {
            auto *fn = xls_dslx_module_member_get_function(mm.ptr);
            if (!fn)
                return nb::none();
            return nb::cast(_DslxFunction(fn));
        },
        nb::keep_alive<0, 1>(),
        "member"_a
    );

    m.def(
        "xls_dslx_module_member_get_struct_def",
        [](const _DslxModuleMember &mm) -> _DslxStructDef {
            return _DslxStructDef(
                xls_dslx_module_member_get_struct_def(mm.ptr)
            );
        },
        nb::keep_alive<0, 1>(),
        "member"_a
    );

    m.def(
        "xls_dslx_module_member_get_enum_def",
        [](const _DslxModuleMember &mm) -> _DslxEnumDef {
            return _DslxEnumDef(xls_dslx_module_member_get_enum_def(mm.ptr));
        },
        nb::keep_alive<0, 1>(),
        "member"_a
    );

    m.def(
        "xls_dslx_module_member_get_type_alias",
        [](const _DslxModuleMember &mm) -> _DslxTypeAlias {
            return _DslxTypeAlias(
                xls_dslx_module_member_get_type_alias(mm.ptr)
            );
        },
        nb::keep_alive<0, 1>(),
        "member"_a
    );

    m.def(
        "xls_dslx_module_member_get_constant_def",
        [](const _DslxModuleMember &mm) -> _DslxConstantDef {
            return _DslxConstantDef(
                xls_dslx_module_member_get_constant_def(mm.ptr)
            );
        },
        nb::keep_alive<0, 1>(),
        "member"_a
    );

    m.def(
        "xls_dslx_module_member_get_quickcheck",
        [](const _DslxModuleMember &mm) -> _DslxQuickcheck {
            return _DslxQuickcheck(
                xls_dslx_module_member_get_quickcheck(mm.ptr)
            );
        },
        nb::keep_alive<0, 1>(),
        "member"_a
    );

    // member_from_* conversions
    m.def(
        "xls_dslx_module_member_from_function",
        [](const _DslxFunction &fn) -> _DslxModuleMember {
            return _DslxModuleMember(
                xls_dslx_module_member_from_function(fn.ptr)
            );
        },
        "function"_a
    );
    m.def(
        "xls_dslx_module_member_from_struct_def",
        [](const _DslxStructDef &sd) -> _DslxModuleMember {
            return _DslxModuleMember(
                xls_dslx_module_member_from_struct_def(sd.ptr)
            );
        },
        "struct_def"_a
    );
    m.def(
        "xls_dslx_module_member_from_enum_def",
        [](const _DslxEnumDef &ed) -> _DslxModuleMember {
            return _DslxModuleMember(
                xls_dslx_module_member_from_enum_def(ed.ptr)
            );
        },
        "enum_def"_a
    );
    m.def(
        "xls_dslx_module_member_from_type_alias",
        [](const _DslxTypeAlias &ta) -> _DslxModuleMember {
            return _DslxModuleMember(
                xls_dslx_module_member_from_type_alias(ta.ptr)
            );
        },
        "type_alias"_a
    );
    m.def(
        "xls_dslx_module_member_from_constant_def",
        [](const _DslxConstantDef &cd) -> _DslxModuleMember {
            return _DslxModuleMember(
                xls_dslx_module_member_from_constant_def(cd.ptr)
            );
        },
        "constant_def"_a
    );
    m.def(
        "xls_dslx_module_member_from_quickcheck",
        [](const _DslxQuickcheck &qc) -> _DslxModuleMember {
            return _DslxModuleMember(
                xls_dslx_module_member_from_quickcheck(qc.ptr)
            );
        },
        "quickcheck"_a
    );

    m.def(
        "xls_dslx_module_get_name",
        [](const _DslxModule &mod) -> std::string {
            return own_c_str(xls_dslx_module_get_name(mod.ptr));
        },
        "module"_a
    );

    m.def(
        "xls_dslx_module_to_string",
        [](const _DslxModule &mod) -> std::string {
            return own_c_str(xls_dslx_module_to_string(mod.ptr));
        },
        "module"_a
    );

    m.def(
        "xls_dslx_module_get_type_definition_count",
        [](const _DslxModule &mod) -> int64_t {
            return xls_dslx_module_get_type_definition_count(mod.ptr);
        },
        "module"_a
    );

    m.def(
        "xls_dslx_module_get_type_definition_kind",
        [](const _DslxModule &mod, int64_t i) -> XlsDslxTypeDefinitionKind {
            return static_cast<XlsDslxTypeDefinitionKind>(
                xls_dslx_module_get_type_definition_kind(mod.ptr, i)
            );
        },
        "module"_a,
        "index"_a
    );

    m.def(
        "xls_dslx_module_get_type_definition_as_struct_def",
        [](const _DslxModule &mod, int64_t i) -> _DslxStructDef {
            return _DslxStructDef(
                xls_dslx_module_get_type_definition_as_struct_def(mod.ptr, i)
            );
        },
        nb::keep_alive<0, 1>(),
        "module"_a,
        "index"_a
    );

    m.def(
        "xls_dslx_module_get_type_definition_as_enum_def",
        [](const _DslxModule &mod, int64_t i) -> _DslxEnumDef {
            return _DslxEnumDef(
                xls_dslx_module_get_type_definition_as_enum_def(mod.ptr, i)
            );
        },
        nb::keep_alive<0, 1>(),
        "module"_a,
        "index"_a
    );

    m.def(
        "xls_dslx_module_get_type_definition_as_type_alias",
        [](const _DslxModule &mod, int64_t i) -> _DslxTypeAlias {
            return _DslxTypeAlias(
                xls_dslx_module_get_type_definition_as_type_alias(mod.ptr, i)
            );
        },
        nb::keep_alive<0, 1>(),
        "module"_a,
        "index"_a
    );

    // ============================================================
    // Function (DSLX)
    // ============================================================
    m.def(
        "xls_dslx_function_is_parametric",
        [](const _DslxFunction &fn) -> bool {
            return xls_dslx_function_is_parametric(fn.ptr);
        },
        "function"_a
    );

    m.def(
        "xls_dslx_function_is_public",
        [](const _DslxFunction &fn) -> bool {
            return xls_dslx_function_is_public(fn.ptr);
        },
        "function"_a
    );

    m.def(
        "xls_dslx_function_get_identifier",
        [](const _DslxFunction &fn) -> std::string {
            return own_c_str(xls_dslx_function_get_identifier(fn.ptr));
        },
        "function"_a
    );

    m.def(
        "xls_dslx_function_get_param_count",
        [](const _DslxFunction &fn) -> int64_t {
            return xls_dslx_function_get_param_count(fn.ptr);
        },
        "function"_a
    );

    m.def(
        "xls_dslx_function_get_parametric_binding_count",
        [](const _DslxFunction &fn) -> int64_t {
            return xls_dslx_function_get_parametric_binding_count(fn.ptr);
        },
        "function"_a
    );

    m.def(
        "xls_dslx_function_get_param",
        [](const _DslxFunction &fn, int64_t index) -> _DslxParam {
            return _DslxParam(xls_dslx_function_get_param(fn.ptr, index));
        },
        nb::keep_alive<0, 1>(),
        "function"_a,
        "index"_a
    );

    m.def(
        "xls_dslx_function_get_parametric_binding",
        [](const _DslxFunction &fn, int64_t index) -> _DslxParametricBinding {
            return _DslxParametricBinding(
                xls_dslx_function_get_parametric_binding(fn.ptr, index)
            );
        },
        nb::keep_alive<0, 1>(),
        "function"_a,
        "index"_a
    );

    m.def(
        "xls_dslx_function_get_body",
        [](const _DslxFunction &fn) -> _DslxExpr {
            return _DslxExpr(xls_dslx_function_get_body(fn.ptr));
        },
        nb::keep_alive<0, 1>(),
        "function"_a
    );

    m.def(
        "xls_dslx_function_get_return_type",
        [](const _DslxFunction &fn) -> nb::object {
            auto *ta = xls_dslx_function_get_return_type(fn.ptr);
            if (!ta)
                return nb::none();
            return nb::cast(_DslxTypeAnnotation(ta));
        },
        nb::keep_alive<0, 1>(),
        "function"_a
    );

    m.def(
        "xls_dslx_function_get_attribute_count",
        [](const _DslxFunction &fn) -> int64_t {
            return xls_dslx_function_get_attribute_count(fn.ptr);
        },
        "function"_a
    );

    m.def(
        "xls_dslx_function_get_attribute",
        [](const _DslxFunction &fn, int64_t index) -> _DslxAttribute {
            return _DslxAttribute(
                xls_dslx_function_get_attribute(fn.ptr, index)
            );
        },
        nb::keep_alive<0, 1>(),
        "function"_a,
        "index"_a
    );

    m.def(
        "xls_dslx_function_to_string",
        [](const _DslxFunction &fn) -> std::string {
            return own_c_str(xls_dslx_function_to_string(fn.ptr));
        },
        "function"_a
    );

    // ============================================================
    // Param, ParametricBinding
    // ============================================================
    m.def(
        "xls_dslx_param_get_name",
        [](const _DslxParam &p) -> std::string {
            return own_c_str(xls_dslx_param_get_name(p.ptr));
        },
        "param"_a
    );

    m.def(
        "xls_dslx_param_get_type_annotation",
        [](const _DslxParam &p) -> _DslxTypeAnnotation {
            return _DslxTypeAnnotation(
                xls_dslx_param_get_type_annotation(p.ptr)
            );
        },
        nb::keep_alive<0, 1>(),
        "param"_a
    );

    m.def(
        "xls_dslx_parametric_binding_get_identifier",
        [](const _DslxParametricBinding &b) -> std::string {
            return own_c_str(xls_dslx_parametric_binding_get_identifier(b.ptr));
        },
        "binding"_a
    );

    m.def(
        "xls_dslx_parametric_binding_get_type_annotation",
        [](const _DslxParametricBinding &b) -> _DslxTypeAnnotation {
            return _DslxTypeAnnotation(
                xls_dslx_parametric_binding_get_type_annotation(b.ptr)
            );
        },
        nb::keep_alive<0, 1>(),
        "binding"_a
    );

    m.def(
        "xls_dslx_parametric_binding_get_expr",
        [](const _DslxParametricBinding &b) -> nb::object {
            auto *e = xls_dslx_parametric_binding_get_expr(b.ptr);
            if (!e)
                return nb::none();
            return nb::cast(_DslxExpr(e));
        },
        nb::keep_alive<0, 1>(),
        "binding"_a
    );

    // ============================================================
    // Expr
    // ============================================================
    m.def(
        "xls_dslx_expr_to_string",
        [](const _DslxExpr &e) -> std::string {
            return own_c_str(xls_dslx_expr_to_string(e.ptr));
        },
        "expr"_a
    );

    m.def(
        "xls_dslx_expr_get_owner_module",
        [](const _DslxExpr &e) -> _DslxModule {
            return _DslxModule(xls_dslx_expr_get_owner_module(e.ptr));
        },
        nb::keep_alive<0, 1>(),
        "expr"_a
    );

    // ============================================================
    // Attribute
    // ============================================================
    m.def(
        "xls_dslx_attribute_get_kind",
        [](const _DslxAttribute &a) -> XlsDslxAttributeKind {
            return static_cast<XlsDslxAttributeKind>(
                xls_dslx_attribute_get_kind(a.ptr)
            );
        },
        "attribute"_a
    );

    m.def(
        "xls_dslx_attribute_get_argument_count",
        [](const _DslxAttribute &a) -> int64_t {
            return xls_dslx_attribute_get_argument_count(a.ptr);
        },
        "attribute"_a
    );

    m.def(
        "xls_dslx_attribute_get_argument_kind",
        [](const _DslxAttribute &a,
           int64_t index) -> XlsDslxAttributeArgumentKind {
            return static_cast<XlsDslxAttributeArgumentKind>(
                xls_dslx_attribute_get_argument_kind(a.ptr, index)
            );
        },
        "attribute"_a,
        "index"_a
    );

    m.def(
        "xls_dslx_attribute_get_string_argument",
        [](const _DslxAttribute &a, int64_t index) -> std::string {
            return own_c_str(
                xls_dslx_attribute_get_string_argument(a.ptr, index)
            );
        },
        "attribute"_a,
        "index"_a
    );

    m.def(
        "xls_dslx_attribute_get_string_literal_argument",
        [](const _DslxAttribute &a, int64_t index) -> std::string {
            return own_c_str(
                xls_dslx_attribute_get_string_literal_argument(a.ptr, index)
            );
        },
        "attribute"_a,
        "index"_a
    );

    m.def(
        "xls_dslx_attribute_get_key_value_argument_key",
        [](const _DslxAttribute &a, int64_t index) -> std::string {
            return own_c_str(
                xls_dslx_attribute_get_key_value_argument_key(a.ptr, index)
            );
        },
        "attribute"_a,
        "index"_a
    );

    m.def(
        "xls_dslx_attribute_get_key_value_string_argument_value",
        [](const _DslxAttribute &a, int64_t index) -> std::string {
            return own_c_str(
                xls_dslx_attribute_get_key_value_string_argument_value(
                    a.ptr, index
                )
            );
        },
        "attribute"_a,
        "index"_a
    );

    m.def(
        "xls_dslx_attribute_get_key_value_int_argument_value",
        [](const _DslxAttribute &a, int64_t index) -> int64_t {
            return xls_dslx_attribute_get_key_value_int_argument_value(
                a.ptr, index
            );
        },
        "attribute"_a,
        "index"_a
    );

    m.def(
        "xls_dslx_attribute_to_string",
        [](const _DslxAttribute &a) -> std::string {
            return own_c_str(xls_dslx_attribute_to_string(a.ptr));
        },
        "attribute"_a
    );

    // ============================================================
    // StructDef
    // ============================================================
    m.def(
        "xls_dslx_struct_def_get_identifier",
        [](const _DslxStructDef &sd) -> std::string {
            return own_c_str(xls_dslx_struct_def_get_identifier(sd.ptr));
        },
        "struct_def"_a
    );

    m.def(
        "xls_dslx_struct_def_is_parametric",
        [](const _DslxStructDef &sd) -> bool {
            return xls_dslx_struct_def_is_parametric(sd.ptr);
        },
        "struct_def"_a
    );

    m.def(
        "xls_dslx_struct_def_get_member_count",
        [](const _DslxStructDef &sd) -> int64_t {
            return xls_dslx_struct_def_get_member_count(sd.ptr);
        },
        "struct_def"_a
    );

    m.def(
        "xls_dslx_struct_def_get_member",
        [](const _DslxStructDef &sd, int64_t index) -> _DslxStructMember {
            return _DslxStructMember(
                xls_dslx_struct_def_get_member(sd.ptr, index)
            );
        },
        nb::keep_alive<0, 1>(),
        "struct_def"_a,
        "index"_a
    );

    m.def(
        "xls_dslx_struct_member_get_name",
        [](const _DslxStructMember &sm) -> std::string {
            return own_c_str(xls_dslx_struct_member_get_name(sm.ptr));
        },
        "member"_a
    );

    m.def(
        "xls_dslx_struct_member_get_type",
        [](const _DslxStructMember &sm) -> _DslxTypeAnnotation {
            return _DslxTypeAnnotation(xls_dslx_struct_member_get_type(sm.ptr));
        },
        nb::keep_alive<0, 1>(),
        "member"_a
    );

    m.def(
        "xls_dslx_struct_def_to_string",
        [](const _DslxStructDef &sd) -> std::string {
            return own_c_str(xls_dslx_struct_def_to_string(sd.ptr));
        },
        "struct_def"_a
    );

    // ============================================================
    // EnumDef
    // ============================================================
    m.def(
        "xls_dslx_enum_def_get_identifier",
        [](const _DslxEnumDef &ed) -> std::string {
            return own_c_str(xls_dslx_enum_def_get_identifier(ed.ptr));
        },
        "enum_def"_a
    );

    m.def(
        "xls_dslx_enum_def_get_member_count",
        [](const _DslxEnumDef &ed) -> int64_t {
            return xls_dslx_enum_def_get_member_count(ed.ptr);
        },
        "enum_def"_a
    );

    m.def(
        "xls_dslx_enum_def_get_member",
        [](const _DslxEnumDef &ed, int64_t index) -> _DslxEnumMember {
            return _DslxEnumMember(xls_dslx_enum_def_get_member(ed.ptr, index));
        },
        nb::keep_alive<0, 1>(),
        "enum_def"_a,
        "index"_a
    );

    m.def(
        "xls_dslx_enum_def_get_underlying",
        [](const _DslxEnumDef &ed) -> _DslxTypeAnnotation {
            return _DslxTypeAnnotation(
                xls_dslx_enum_def_get_underlying(ed.ptr)
            );
        },
        nb::keep_alive<0, 1>(),
        "enum_def"_a
    );

    m.def(
        "xls_dslx_enum_member_get_name",
        [](const _DslxEnumMember &em) -> std::string {
            return own_c_str(xls_dslx_enum_member_get_name(em.ptr));
        },
        "member"_a
    );

    m.def(
        "xls_dslx_enum_member_get_value",
        [](const _DslxEnumMember &em) -> _DslxExpr {
            return _DslxExpr(xls_dslx_enum_member_get_value(em.ptr));
        },
        nb::keep_alive<0, 1>(),
        "member"_a
    );

    m.def(
        "xls_dslx_enum_def_to_string",
        [](const _DslxEnumDef &ed) -> std::string {
            return own_c_str(xls_dslx_enum_def_to_string(ed.ptr));
        },
        "enum_def"_a
    );

    // ============================================================
    // ConstantDef
    // ============================================================
    m.def(
        "xls_dslx_constant_def_get_name",
        [](const _DslxConstantDef &cd) -> std::string {
            return own_c_str(xls_dslx_constant_def_get_name(cd.ptr));
        },
        "constant_def"_a
    );

    m.def(
        "xls_dslx_constant_def_get_value",
        [](const _DslxConstantDef &cd) -> _DslxExpr {
            return _DslxExpr(xls_dslx_constant_def_get_value(cd.ptr));
        },
        nb::keep_alive<0, 1>(),
        "constant_def"_a
    );

    m.def(
        "xls_dslx_constant_def_to_string",
        [](const _DslxConstantDef &cd) -> std::string {
            return own_c_str(xls_dslx_constant_def_to_string(cd.ptr));
        },
        "constant_def"_a
    );

    // ============================================================
    // TypeAlias
    // ============================================================
    m.def(
        "xls_dslx_type_alias_get_identifier",
        [](const _DslxTypeAlias &ta) -> std::string {
            return own_c_str(xls_dslx_type_alias_get_identifier(ta.ptr));
        },
        "type_alias"_a
    );

    m.def(
        "xls_dslx_type_alias_get_type_annotation",
        [](const _DslxTypeAlias &ta) -> _DslxTypeAnnotation {
            return _DslxTypeAnnotation(
                xls_dslx_type_alias_get_type_annotation(ta.ptr)
            );
        },
        nb::keep_alive<0, 1>(),
        "type_alias"_a
    );

    m.def(
        "xls_dslx_type_alias_to_string",
        [](const _DslxTypeAlias &ta) -> std::string {
            return own_c_str(xls_dslx_type_alias_to_string(ta.ptr));
        },
        "type_alias"_a
    );

    // ============================================================
    // TypeAnnotation / TypeRef / ColonRef / Import
    // ============================================================
    m.def(
        "xls_dslx_type_annotation_get_type_ref_type_annotation",
        [](const _DslxTypeAnnotation &ta) -> nb::object {
            auto *r =
                xls_dslx_type_annotation_get_type_ref_type_annotation(ta.ptr);
            if (!r)
                return nb::none();
            return nb::cast(_DslxTypeRefTypeAnnotation(r));
        },
        nb::keep_alive<0, 1>(),
        "type_annotation"_a
    );

    m.def(
        "xls_dslx_type_ref_type_annotation_get_type_ref",
        [](const _DslxTypeRefTypeAnnotation &trta) -> _DslxTypeRef {
            return _DslxTypeRef(
                xls_dslx_type_ref_type_annotation_get_type_ref(trta.ptr)
            );
        },
        nb::keep_alive<0, 1>(),
        "type_ref_type_annotation"_a
    );

    m.def(
        "xls_dslx_type_ref_get_type_definition",
        [](const _DslxTypeRef &tr) -> _DslxTypeDefinition {
            return _DslxTypeDefinition(
                xls_dslx_type_ref_get_type_definition(tr.ptr)
            );
        },
        nb::keep_alive<0, 1>(),
        "type_ref"_a
    );

    m.def(
        "xls_dslx_type_definition_get_colon_ref",
        [](const _DslxTypeDefinition &td) -> nb::object {
            auto *r = xls_dslx_type_definition_get_colon_ref(td.ptr);
            if (!r)
                return nb::none();
            return nb::cast(_DslxColonRef(r));
        },
        nb::keep_alive<0, 1>(),
        "type_definition"_a
    );

    m.def(
        "xls_dslx_type_definition_get_type_alias",
        [](const _DslxTypeDefinition &td) -> nb::object {
            auto *r = xls_dslx_type_definition_get_type_alias(td.ptr);
            if (!r)
                return nb::none();
            return nb::cast(_DslxTypeAlias(r));
        },
        nb::keep_alive<0, 1>(),
        "type_definition"_a
    );

    m.def(
        "xls_dslx_colon_ref_resolve_import_subject",
        [](const _DslxColonRef &cr) -> nb::object {
            auto *r = xls_dslx_colon_ref_resolve_import_subject(cr.ptr);
            if (!r)
                return nb::none();
            return nb::cast(_DslxImport(r));
        },
        nb::keep_alive<0, 1>(),
        "colon_ref"_a
    );

    m.def(
        "xls_dslx_colon_ref_get_attr",
        [](const _DslxColonRef &cr) -> std::string {
            return own_c_str(xls_dslx_colon_ref_get_attr(cr.ptr));
        },
        "colon_ref"_a
    );

    m.def(
        "xls_dslx_import_get_subject_count",
        [](const _DslxImport &imp) -> int64_t {
            return xls_dslx_import_get_subject_count(imp.ptr);
        },
        "imp"_a
    );

    m.def(
        "xls_dslx_import_get_subject",
        [](const _DslxImport &imp, int64_t index) -> std::string {
            return own_c_str(xls_dslx_import_get_subject(imp.ptr, index));
        },
        "imp"_a,
        "index"_a
    );

    // ============================================================
    // TypeInfo
    // ============================================================
    m.def(
        "xls_dslx_type_info_get_type_struct_def",
        [](const _DslxTypeInfo &ti, const _DslxStructDef &sd) -> nb::object {
            auto *t = xls_dslx_type_info_get_type_struct_def(ti.ptr, sd.ptr);
            if (!t)
                return nb::none();
            return nb::cast(_DslxType(t));
        },
        nb::keep_alive<0, 1>(),
        "type_info"_a,
        "struct_def"_a
    );

    m.def(
        "xls_dslx_type_info_get_type_struct_member",
        [](const _DslxTypeInfo &ti, const _DslxStructMember &sm) -> nb::object {
            auto *t = xls_dslx_type_info_get_type_struct_member(ti.ptr, sm.ptr);
            if (!t)
                return nb::none();
            return nb::cast(_DslxType(t));
        },
        nb::keep_alive<0, 1>(),
        "type_info"_a,
        "struct_member"_a
    );

    m.def(
        "xls_dslx_type_info_get_type_enum_def",
        [](const _DslxTypeInfo &ti, const _DslxEnumDef &ed) -> nb::object {
            auto *t = xls_dslx_type_info_get_type_enum_def(ti.ptr, ed.ptr);
            if (!t)
                return nb::none();
            return nb::cast(_DslxType(t));
        },
        nb::keep_alive<0, 1>(),
        "type_info"_a,
        "enum_def"_a
    );

    m.def(
        "xls_dslx_type_info_get_type_constant_def",
        [](const _DslxTypeInfo &ti, const _DslxConstantDef &cd) -> nb::object {
            auto *t = xls_dslx_type_info_get_type_constant_def(ti.ptr, cd.ptr);
            if (!t)
                return nb::none();
            return nb::cast(_DslxType(t));
        },
        nb::keep_alive<0, 1>(),
        "type_info"_a,
        "constant_def"_a
    );

    m.def(
        "xls_dslx_type_info_get_type_type_annotation",
        [](const _DslxTypeInfo &ti,
           const _DslxTypeAnnotation &ta) -> nb::object {
            auto *t =
                xls_dslx_type_info_get_type_type_annotation(ti.ptr, ta.ptr);
            if (!t)
                return nb::none();
            return nb::cast(_DslxType(t));
        },
        nb::keep_alive<0, 1>(),
        "type_info"_a,
        "type_annotation"_a
    );

    m.def(
        "xls_dslx_type_info_get_const_expr",
        [](const _DslxTypeInfo &ti, const _DslxExpr &e) -> _DslxInterpValue {
            char *error = nullptr;
            xls_dslx_interp_value *result = nullptr;
            bool ok = xls_dslx_type_info_get_const_expr(
                ti.ptr, e.ptr, &error, &result
            );
            check_result(ok, error);
            return _DslxInterpValue(result);
        },
        "type_info"_a,
        "expr"_a
    );

    m.def(
        "xls_dslx_type_info_get_imported_type_info",
        [](const _DslxTypeInfo &ti, const _DslxModule &mod) -> nb::object {
            auto *r =
                xls_dslx_type_info_get_imported_type_info(ti.ptr, mod.ptr);
            if (!r)
                return nb::none();
            return nb::cast(_DslxTypeInfo(r));
        },
        nb::keep_alive<0, 1>(),
        "type_info"_a,
        "module"_a
    );

    m.def(
        "xls_dslx_type_info_get_requires_implicit_token",
        [](const _DslxTypeInfo &ti, const _DslxFunction &fn) -> bool {
            char *error = nullptr;
            bool result;
            bool ok = xls_dslx_type_info_get_requires_implicit_token(
                ti.ptr, fn.ptr, &error, &result
            );
            check_result(ok, error);
            return result;
        },
        "type_info"_a,
        "function"_a
    );

    // ============================================================
    // Invocation callee data
    // ============================================================
    m.def(
        "xls_dslx_type_info_get_unique_invocation_callee_data",
        [](const _DslxTypeInfo &ti,
           const _DslxFunction &fn) -> _DslxInvocationCalleeDataArray {
            return _DslxInvocationCalleeDataArray(
                xls_dslx_type_info_get_unique_invocation_callee_data(
                    ti.ptr, fn.ptr
                )
            );
        },
        "type_info"_a,
        "function"_a
    );

    m.def(
        "xls_dslx_type_info_get_all_invocation_callee_data",
        [](const _DslxTypeInfo &ti,
           const _DslxFunction &fn) -> _DslxInvocationCalleeDataArray {
            return _DslxInvocationCalleeDataArray(
                xls_dslx_type_info_get_all_invocation_callee_data(ti.ptr, fn.ptr)
            );
        },
        "type_info"_a,
        "function"_a
    );

    m.def(
        "xls_dslx_invocation_callee_data_array_get_count",
        [](const _DslxInvocationCalleeDataArray &arr) -> int64_t {
            return xls_dslx_invocation_callee_data_array_get_count(
                arr.ptr.get()
            );
        },
        "array"_a
    );

    m.def(
        "xls_dslx_invocation_callee_data_array_get",
        [](const _DslxInvocationCalleeDataArray &arr,
           int64_t index) -> _DslxInvocationCalleeData {
            return _DslxInvocationCalleeData(
                xls_dslx_invocation_callee_data_array_get(arr.ptr.get(), index),
                false
            );
        },
        nb::keep_alive<0, 1>(),
        "array"_a,
        "index"_a
    );

    m.def(
        "xls_dslx_invocation_callee_data_get_callee_bindings",
        [](const _DslxInvocationCalleeData &d) -> _DslxParametricEnvBorrowed {
            return _DslxParametricEnvBorrowed(
                xls_dslx_invocation_callee_data_get_callee_bindings(d.ptr)
            );
        },
        nb::keep_alive<0, 1>(),
        "data"_a
    );

    m.def(
        "xls_dslx_invocation_callee_data_get_caller_bindings",
        [](const _DslxInvocationCalleeData &d) -> _DslxParametricEnvBorrowed {
            return _DslxParametricEnvBorrowed(
                xls_dslx_invocation_callee_data_get_caller_bindings(d.ptr)
            );
        },
        nb::keep_alive<0, 1>(),
        "data"_a
    );

    m.def(
        "xls_dslx_invocation_callee_data_get_invocation",
        [](const _DslxInvocationCalleeData &d) -> _DslxInvocation {
            return _DslxInvocation(
                xls_dslx_invocation_callee_data_get_invocation(d.ptr)
            );
        },
        nb::keep_alive<0, 1>(),
        "data"_a
    );

    // ============================================================
    // DslxType
    // ============================================================
    m.def(
        "xls_dslx_type_get_total_bit_count",
        [](const _DslxType &t) -> int64_t {
            char *error = nullptr;
            int64_t result;
            bool ok = xls_dslx_type_get_total_bit_count(t.ptr, &error, &result);
            check_result(ok, error);
            return result;
        },
        "type"_a
    );

    m.def(
        "xls_dslx_type_is_signed_bits",
        [](const _DslxType &t) -> bool {
            char *error = nullptr;
            bool result;
            bool ok = xls_dslx_type_is_signed_bits(t.ptr, &error, &result);
            check_result(ok, error);
            return result;
        },
        "type"_a
    );

    m.def(
        "xls_dslx_type_to_string",
        [](const _DslxType &t) -> std::string {
            char *error = nullptr, *str = nullptr;
            bool ok = xls_dslx_type_to_string(t.ptr, &error, &str);
            check_result(ok, error);
            return own_c_str(str);
        },
        "type"_a
    );

    m.def(
        "xls_dslx_type_is_enum",
        [](const _DslxType &t) -> bool { return xls_dslx_type_is_enum(t.ptr); },
        "type"_a
    );

    m.def(
        "xls_dslx_type_is_struct",
        [](const _DslxType &t) -> bool {
            return xls_dslx_type_is_struct(t.ptr);
        },
        "type"_a
    );

    m.def(
        "xls_dslx_type_is_array",
        [](const _DslxType &t) -> bool {
            return xls_dslx_type_is_array(t.ptr);
        },
        "type"_a
    );

    m.def(
        "xls_dslx_type_get_enum_def",
        [](const _DslxType &t) -> _DslxEnumDef {
            return _DslxEnumDef(
                xls_dslx_type_get_enum_def(const_cast<xls_dslx_type *>(t.ptr))
            );
        },
        nb::keep_alive<0, 1>(),
        "type"_a
    );

    m.def(
        "xls_dslx_type_get_struct_def",
        [](const _DslxType &t) -> _DslxStructDef {
            return _DslxStructDef(
                xls_dslx_type_get_struct_def(const_cast<xls_dslx_type *>(t.ptr))
            );
        },
        nb::keep_alive<0, 1>(),
        "type"_a
    );

    m.def(
        "xls_dslx_type_array_get_element_type",
        [](const _DslxType &t) -> _DslxType {
            return _DslxType(xls_dslx_type_array_get_element_type(
                const_cast<xls_dslx_type *>(t.ptr)
            ));
        },
        nb::keep_alive<0, 1>(),
        "type"_a
    );

    m.def(
        "xls_dslx_type_array_get_size",
        [](const _DslxType &t) -> _DslxTypeDim {
            return _DslxTypeDim(
                xls_dslx_type_array_get_size(const_cast<xls_dslx_type *>(t.ptr))
            );
        },
        "type"_a
    );

    // ============================================================
    // TypeDim
    // ============================================================
    m.def(
        "xls_dslx_type_dim_get_as_bool",
        [](const _DslxTypeDim &td) -> bool {
            char *error = nullptr;
            bool result;
            bool ok =
                xls_dslx_type_dim_get_as_bool(td.ptr.get(), &error, &result);
            check_result(ok, error);
            return result;
        },
        "type_dim"_a
    );

    m.def(
        "xls_dslx_type_dim_get_as_int64",
        [](const _DslxTypeDim &td) -> int64_t {
            char *error = nullptr;
            int64_t result;
            bool ok =
                xls_dslx_type_dim_get_as_int64(td.ptr.get(), &error, &result);
            check_result(ok, error);
            return result;
        },
        "type_dim"_a
    );

    // ============================================================
    // CallGraph
    // ============================================================
    m.def(
        "xls_dslx_type_info_build_function_call_graph",
        [](const _DslxTypeInfo &ti) -> _DslxCallGraph {
            char *error = nullptr;
            xls_dslx_call_graph *result = nullptr;
            bool ok = xls_dslx_type_info_build_function_call_graph(
                ti.ptr, &error, &result
            );
            check_result(ok, error);
            return _DslxCallGraph(result);
        },
        "type_info"_a
    );

    m.def(
        "xls_dslx_call_graph_get_function_count",
        [](const _DslxCallGraph &cg) -> int64_t {
            return xls_dslx_call_graph_get_function_count(cg.ptr.get());
        },
        "call_graph"_a
    );

    m.def(
        "xls_dslx_call_graph_get_function",
        [](const _DslxCallGraph &cg, int64_t index) -> _DslxFunction {
            return _DslxFunction(
                xls_dslx_call_graph_get_function(cg.ptr.get(), index)
            );
        },
        nb::keep_alive<0, 1>(),
        "call_graph"_a,
        "index"_a
    );

    m.def(
        "xls_dslx_call_graph_get_callee_count",
        [](const _DslxCallGraph &cg, const _DslxFunction &caller) -> int64_t {
            return xls_dslx_call_graph_get_callee_count(
                cg.ptr.get(), caller.ptr
            );
        },
        "call_graph"_a,
        "caller"_a
    );

    m.def(
        "xls_dslx_call_graph_get_callee_function",
        [](const _DslxCallGraph &cg,
           const _DslxFunction &caller,
           int64_t callee_index) -> _DslxFunction {
            return _DslxFunction(xls_dslx_call_graph_get_callee_function(
                cg.ptr.get(), caller.ptr, callee_index
            ));
        },
        nb::keep_alive<0, 1>(),
        "call_graph"_a,
        "caller"_a,
        "callee_index"_a
    );

    // ============================================================
    // Quickcheck
    // ============================================================
    m.def(
        "xls_dslx_quickcheck_get_function",
        [](const _DslxQuickcheck &qc) -> _DslxFunction {
            return _DslxFunction(xls_dslx_quickcheck_get_function(qc.ptr));
        },
        nb::keep_alive<0, 1>(),
        "quickcheck"_a
    );

    m.def(
        "xls_dslx_quickcheck_is_exhaustive",
        [](const _DslxQuickcheck &qc) -> bool {
            return xls_dslx_quickcheck_is_exhaustive(qc.ptr);
        },
        "quickcheck"_a
    );

    m.def(
        "xls_dslx_quickcheck_get_count",
        [](const _DslxQuickcheck &qc) -> nb::object {
            int64_t count;
            if (xls_dslx_quickcheck_get_count(qc.ptr, &count))
                return nb::cast(count);
            return nb::none();
        },
        "quickcheck"_a
    );

    m.def(
        "xls_dslx_quickcheck_to_string",
        [](const _DslxQuickcheck &qc) -> std::string {
            return own_c_str(xls_dslx_quickcheck_to_string(qc.ptr));
        },
        "quickcheck"_a
    );
}
