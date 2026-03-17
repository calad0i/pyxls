#include "_c_api.h"
#include "_types.h"
#include "_helpers.h"
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>
#include <nanobind/stl/optional.h>
#include <nanobind/ndarray.h>
#include <iostream>

using namespace nb::literals;

void bind_c_api(nb::module_ &m) {
    // ============================================================
    // Enums
    // ============================================================
    nb::enum_<XlsValueKind>(m, "ValueKind")
        .value("INVALID", XlsValueKind::INVALID)
        .value("BITS", XlsValueKind::BITS)
        .value("ARRAY", XlsValueKind::ARRAY)
        .value("TUPLE", XlsValueKind::TUPLE)
        .value("TOKEN", XlsValueKind::TOKEN)
        .export_values();

    nb::enum_<XlsCallingConvention>(m, "CallingConvention")
        .value("TYPICAL", XlsCallingConvention::TYPICAL)
        .value("IMPLICIT_TOKEN", XlsCallingConvention::IMPLICIT_TOKEN)
        .value("PROC_NEXT", XlsCallingConvention::PROC_NEXT)
        .export_values();

    nb::enum_<XlsFormatPreference>(m, "FormatPreference")
        .value("DEFAULT", XlsFormatPreference::DEFAULT)
        .value("BINARY", XlsFormatPreference::BINARY)
        .value("SIGNED_DECIMAL", XlsFormatPreference::SIGNED_DECIMAL)
        .value("UNSIGNED_DECIMAL", XlsFormatPreference::UNSIGNED_DECIMAL)
        .value("HEX", XlsFormatPreference::HEX)
        .value("PLAIN_BINARY", XlsFormatPreference::PLAIN_BINARY)
        .value("PLAIN_HEX", XlsFormatPreference::PLAIN_HEX)
        .value("ZERO_PADDED_BINARY", XlsFormatPreference::ZERO_PADDED_BINARY)
        .value("ZERO_PADDED_HEX", XlsFormatPreference::ZERO_PADDED_HEX)
        .export_values();

    // ============================================================
    // Initialization
    // ============================================================
    m.def(
        "xls_init_xls",
        [](const std::string &usage) {
            // Note: argc/argv not practical from Python, just pass usage
            xls_init_xls(usage.c_str(), 0, nullptr);
        },
        "usage"_a = ""
    );

    // ============================================================
    // DSLX Conversion
    // ============================================================
    m.def(
        "xls_convert_dslx_to_ir",
        [](const std::string &dslx,
           const std::string &path,
           const std::string &module_name,
           const std::string &dslx_stdlib_path,
           std::vector<std::string> additional_search_paths) -> std::string {
            char *error = nullptr, *ir = nullptr;
            std::vector<const char *> c_paths;
            for (auto &s : additional_search_paths)
                c_paths.push_back(s.c_str());
            bool ok = xls_convert_dslx_to_ir(
                dslx.c_str(),
                path.c_str(),
                module_name.c_str(),
                dslx_stdlib_path.c_str(),
                c_paths.data(),
                c_paths.size(),
                &error,
                &ir
            );
            check_result(ok, error);
            std::string result(ir);
            xls_c_str_free(ir);
            return result;
        },
        "dslx"_a,
        "path"_a,
        "module_name"_a,
        "dslx_stdlib_path"_a,
        "additional_search_paths"_a = std::vector<std::string>()
    );

    m.def(
        "xls_convert_dslx_to_ir_with_warnings",
        [](const std::string &dslx,
           const std::string &path,
           const std::string &module_name,
           const std::string &dslx_stdlib_path,
           std::vector<std::string> additional_search_paths,
           std::vector<std::string> enable_warnings,
           std::vector<std::string> disable_warnings,
           bool warnings_as_errors,
           bool force_implicit_token) -> nb::tuple {
            char *error = nullptr, *ir = nullptr;
            char **warnings_out = nullptr;
            size_t warnings_count = 0;
            std::vector<const char *> c_paths, c_enable, c_disable;
            for (auto &s : additional_search_paths)
                c_paths.push_back(s.c_str());
            for (auto &s : enable_warnings)
                c_enable.push_back(s.c_str());
            for (auto &s : disable_warnings)
                c_disable.push_back(s.c_str());
            bool ok = xls_convert_dslx_to_ir_with_warnings(
                dslx.c_str(),
                path.c_str(),
                module_name.c_str(),
                dslx_stdlib_path.c_str(),
                c_paths.data(),
                c_paths.size(),
                c_enable.data(),
                c_enable.size(),
                c_disable.data(),
                c_disable.size(),
                warnings_as_errors,
                force_implicit_token,
                &warnings_out,
                &warnings_count,
                &error,
                &ir
            );
            check_result(ok, error);
            std::string ir_str(ir);
            xls_c_str_free(ir);
            std::vector<std::string> warns;
            if (warnings_out) {
                for (size_t i = 0; i < warnings_count; ++i)
                    warns.emplace_back(warnings_out[i]);
                xls_c_strs_free(warnings_out, warnings_count);
            }
            return nb::make_tuple(ir_str, warns);
        },
        "dslx"_a,
        "path"_a,
        "module_name"_a,
        "dslx_stdlib_path"_a,
        "additional_search_paths"_a = std::vector<std::string>(),
        "enable_warnings"_a = std::vector<std::string>(),
        "disable_warnings"_a = std::vector<std::string>(),
        "warnings_as_errors"_a = false,
        "force_implicit_token"_a = false
    );

    m.def(
        "xls_convert_dslx_path_to_ir",
        [](const std::string &path,
           const std::string &dslx_stdlib_path,
           std::vector<std::string> additional_search_paths) -> std::string {
            char *error = nullptr, *ir = nullptr;
            std::vector<const char *> c_paths;
            for (auto &s : additional_search_paths)
                c_paths.push_back(s.c_str());
            bool ok = xls_convert_dslx_path_to_ir(
                path.c_str(),
                dslx_stdlib_path.c_str(),
                c_paths.data(),
                c_paths.size(),
                &error,
                &ir
            );
            check_result(ok, error);
            std::string result(ir);
            xls_c_str_free(ir);
            return result;
        },
        "path"_a,
        "dslx_stdlib_path"_a,
        "additional_search_paths"_a = std::vector<std::string>()
    );

    m.def(
        "xls_convert_dslx_path_to_ir_with_warnings",
        [](const std::string &path,
           const std::string &dslx_stdlib_path,
           std::vector<std::string> additional_search_paths,
           std::vector<std::string> enable_warnings,
           std::vector<std::string> disable_warnings,
           bool warnings_as_errors,
           bool force_implicit_token) -> nb::tuple {
            char *error = nullptr, *ir = nullptr;
            char **warnings_out = nullptr;
            size_t warnings_count = 0;
            std::vector<const char *> c_paths, c_enable, c_disable;
            for (auto &s : additional_search_paths)
                c_paths.push_back(s.c_str());
            for (auto &s : enable_warnings)
                c_enable.push_back(s.c_str());
            for (auto &s : disable_warnings)
                c_disable.push_back(s.c_str());
            bool ok = xls_convert_dslx_path_to_ir_with_warnings(
                path.c_str(),
                dslx_stdlib_path.c_str(),
                c_paths.data(),
                c_paths.size(),
                c_enable.data(),
                c_enable.size(),
                c_disable.data(),
                c_disable.size(),
                warnings_as_errors,
                force_implicit_token,
                &warnings_out,
                &warnings_count,
                &error,
                &ir
            );
            check_result(ok, error);
            std::string ir_str(ir);
            xls_c_str_free(ir);
            std::vector<std::string> warns;
            if (warnings_out) {
                for (size_t i = 0; i < warnings_count; ++i)
                    warns.emplace_back(warnings_out[i]);
                xls_c_strs_free(warnings_out, warnings_count);
            }
            return nb::make_tuple(ir_str, warns);
        },
        "path"_a,
        "dslx_stdlib_path"_a,
        "additional_search_paths"_a = std::vector<std::string>(),
        "enable_warnings"_a = std::vector<std::string>(),
        "disable_warnings"_a = std::vector<std::string>(),
        "warnings_as_errors"_a = false,
        "force_implicit_token"_a = false
    );

    m.def(
        "xls_optimize_ir",
        [](const std::string &ir, const std::string &top) -> std::string {
            char *error = nullptr, *optimized = nullptr;
            bool ok =
                xls_optimize_ir(ir.c_str(), top.c_str(), &error, &optimized);
            check_result(ok, error);
            std::string result(optimized);
            xls_c_str_free(optimized);
            return result;
        },
        "ir"_a,
        "top"_a
    );

    m.def(
        "xls_mangle_dslx_name",
        [](const std::string &module_name,
           const std::string &function_name) -> std::string {
            char *error = nullptr, *mangled = nullptr;
            bool ok = xls_mangle_dslx_name(
                module_name.c_str(), function_name.c_str(), &error, &mangled
            );
            check_result(ok, error);
            return own_c_str(mangled);
        },
        "module_name"_a,
        "function_name"_a
    );

    m.def(
        "xls_mangle_dslx_name_full",
        [](const std::string &module_name,
           const std::string &function_name,
           XlsCallingConvention convention,
           std::vector<std::string> free_keys,
           nb::object param_env,
           const std::string &scope) -> std::string {
            char *error = nullptr, *mangled = nullptr;
            std::vector<const char *> c_keys;
            for (auto &s : free_keys)
                c_keys.push_back(s.c_str());
            const xls_dslx_parametric_env *env = nullptr;
            if (!param_env.is_none())
                env = nb::cast<const _DslxParametricEnv &>(param_env).ptr.get();
            bool ok = xls_mangle_dslx_name_full(
                module_name.c_str(),
                function_name.c_str(),
                static_cast<xls_calling_convention>(convention),
                c_keys.data(),
                c_keys.size(),
                env,
                scope.c_str(),
                &error,
                &mangled
            );
            check_result(ok, error);
            return own_c_str(mangled);
        },
        "module_name"_a,
        "function_name"_a,
        "convention"_a,
        "free_keys"_a = std::vector<std::string>(),
        "param_env"_a = nb::none(),
        "scope"_a = ""
    );

    // ============================================================
    // Package operations
    // ============================================================
    m.def(
        "xls_parse_ir_package",
        [](const std::string &ir, nb::object filename) -> _Package {
            char *error = nullptr;
            xls_package *pkg = nullptr;
            const char *fn = filename.is_none()
                                 ? nullptr
                                 : nb::cast<nb::str>(filename).c_str();
            bool ok = xls_parse_ir_package(ir.c_str(), fn, &error, &pkg);
            check_result(ok, error);
            return _Package(pkg);
        },
        "ir"_a,
        "filename"_a = nb::none()
    );

    m.def(
        "xls_package_to_string",
        [](const _Package &pkg) -> std::string {
            char *str = nullptr;
            if (xls_package_to_string(pkg.ptr.get(), &str)) {
                return own_c_str(str);
            }
            throw std::runtime_error("Failed to convert package to string");
        },
        "package"_a
    );

    m.def(
        "xls_function_to_string",
        [](const _Function &fn) -> std::string {
            char *str = nullptr;
            if (xls_function_to_string(fn.ptr, &str)) {
                return own_c_str(str);
            }
            throw std::runtime_error("Failed to convert function to string");
        },
        "function"_a
    );

    m.def(
        "xls_package_get_top",
        [](const _Package &pkg) -> _FunctionBase {
            return _FunctionBase(
                xls_package_get_top(const_cast<xls_package *>(pkg.ptr.get()))
            );
        },
        nb::keep_alive<0, 1>(),
        "package"_a
    );

    m.def(
        "xls_package_set_top_by_name",
        [](const _Package &pkg, const std::string &name) {
            char *error = nullptr;
            bool ok = xls_package_set_top_by_name(
                const_cast<xls_package *>(pkg.ptr.get()), name.c_str(), &error
            );
            check_result(ok, error);
        },
        "package"_a,
        "name"_a
    );

    m.def(
        "xls_package_get_function",
        [](const _Package &pkg, const std::string &name) -> _Function {
            char *error = nullptr;
            xls_function *fn = nullptr;
            bool ok = xls_package_get_function(
                const_cast<xls_package *>(pkg.ptr.get()),
                name.c_str(),
                &error,
                &fn
            );
            check_result(ok, error);
            return _Function(fn);
        },
        nb::keep_alive<0, 1>(),
        "package"_a,
        "name"_a
    );

    m.def(
        "xls_package_get_functions",
        [](const _Package &pkg) -> std::vector<_Function> {
            char *error = nullptr;
            xls_function **fns = nullptr;
            size_t count = 0;
            bool ok = xls_package_get_functions(
                const_cast<xls_package *>(pkg.ptr.get()), &error, &fns, &count
            );
            check_result(ok, error);
            std::vector<_Function> result;
            result.reserve(count);
            for (size_t i = 0; i < count; ++i)
                result.emplace_back(fns[i]);
            xls_function_ptr_array_free(fns);
            return result;
        },
        "package"_a
    );

    m.def(
        "xls_package_get_type_for_value",
        [](const _Package &pkg, const _Value &value) -> _Type {
            char *error = nullptr;
            xls_type *type = nullptr;
            bool ok = xls_package_get_type_for_value(
                const_cast<xls_package *>(pkg.ptr.get()),
                const_cast<xls_value *>(value.ptr.get()),
                &error,
                &type
            );
            check_result(ok, error);
            return _Type(type);
        },
        nb::keep_alive<0, 1>(),
        "package"_a,
        "value"_a
    );

    m.def(
        "xls_verify_package",
        [](const _Package &pkg) {
            char *error = nullptr;
            bool ok = xls_verify_package(
                const_cast<xls_package *>(pkg.ptr.get()), &error
            );
            check_result(ok, error);
        },
        "package"_a
    );

    // ============================================================
    // Schedule and Codegen
    // ============================================================
    m.def(
        "xls_schedule_and_codegen_package",
        [](const _Package &pkg,
           const std::string &scheduling_options,
           const std::string &codegen_flags,
           bool with_delay_model) -> _ScheduleAndCodegenResult {
            char *error = nullptr;
            xls_schedule_and_codegen_result *result = nullptr;
            bool ok = xls_schedule_and_codegen_package(
                const_cast<xls_package *>(pkg.ptr.get()),
                scheduling_options.c_str(),
                codegen_flags.c_str(),
                with_delay_model,
                &error,
                &result
            );
            check_result(ok, error);
            return _ScheduleAndCodegenResult(result);
        },
        "package"_a,
        "scheduling_options"_a,
        "codegen_flags"_a,
        "with_delay_model"_a = false
    );

    m.def(
        "xls_schedule_and_codegen_result_get_verilog_text",
        [](const _ScheduleAndCodegenResult &r) -> std::string {
            char *s =
                xls_schedule_and_codegen_result_get_verilog_text(r.ptr.get());
            return own_c_str(s);
        },
        "result"_a
    );

    // ============================================================
    // Function operations
    // ============================================================
    m.def(
        "xls_function_get_name",
        [](const _Function &fn) -> std::string {
            char *error = nullptr, *name = nullptr;
            bool ok = xls_function_get_name(fn.ptr, &error, &name);
            check_result(ok, error);
            return own_c_str(name);
        },
        "function"_a
    );

    m.def(
        "xls_function_get_param_name",
        [](const _Function &fn, size_t index) -> std::string {
            char *error = nullptr, *name = nullptr;
            bool ok = xls_function_get_param_name(fn.ptr, index, &error, &name);
            check_result(ok, error);
            return own_c_str(name);
        },
        "function"_a,
        "index"_a
    );

    m.def(
        "xls_function_get_type",
        [](const _Function &fn) -> _FunctionType {
            char *error = nullptr;
            xls_function_type *type = nullptr;
            bool ok = xls_function_get_type(fn.ptr, &error, &type);
            check_result(ok, error);
            return _FunctionType(type);
        },
        nb::keep_alive<0, 1>(),
        "function"_a
    );

    m.def(
        "xls_function_type_to_string",
        [](const _FunctionType &ft) -> std::string {
            char *error = nullptr, *str = nullptr;
            bool ok = xls_function_type_to_string(ft.ptr, &error, &str);
            check_result(ok, error);
            return own_c_str(str);
        },
        "function_type"_a
    );

    m.def(
        "xls_function_type_get_param_count",
        [](const _FunctionType &ft) -> int64_t {
            return xls_function_type_get_param_count(ft.ptr);
        },
        "function_type"_a
    );

    m.def(
        "xls_function_type_get_param_type",
        [](const _FunctionType &ft, size_t index) -> _Type {
            char *error = nullptr;
            xls_type *type = nullptr;
            bool ok =
                xls_function_type_get_param_type(ft.ptr, index, &error, &type);
            check_result(ok, error);
            return _Type(type);
        },
        nb::keep_alive<0, 1>(),
        "function_type"_a,
        "index"_a
    );

    m.def(
        "xls_function_type_get_return_type",
        [](const _FunctionType &ft) -> _Type {
            return _Type(xls_function_type_get_return_type(ft.ptr));
        },
        nb::keep_alive<0, 1>(),
        "function_type"_a
    );

    m.def(
        "xls_function_to_z3_smtlib",
        [](const _Function &fn) -> std::string {
            char *error = nullptr, *str = nullptr;
            bool ok = xls_function_to_z3_smtlib(fn.ptr, &error, &str);
            check_result(ok, error);
            return own_c_str(str);
        },
        "function"_a
    );

    // ============================================================
    // Type operations
    // ============================================================
    m.def(
        "xls_type_get_kind",
        [](const _Type &t) -> XlsValueKind {
            char *error = nullptr;
            xls_value_kind kind;
            bool ok = xls_type_get_kind(t.ptr, &error, &kind);
            check_result(ok, error);
            return static_cast<XlsValueKind>(kind);
        },
        "type"_a
    );

    m.def(
        "xls_type_to_string",
        [](const _Type &t) -> std::string {
            char *error = nullptr, *str = nullptr;
            bool ok = xls_type_to_string(t.ptr, &error, &str);
            check_result(ok, error);
            return own_c_str(str);
        },
        "type"_a
    );

    m.def(
        "xls_type_get_flat_bit_count",
        [](const _Type &t) -> int64_t {
            return xls_type_get_flat_bit_count(t.ptr);
        },
        "type"_a
    );

    m.def(
        "xls_type_get_leaf_count",
        [](const _Type &t) -> int64_t {
            return xls_type_get_leaf_count(t.ptr);
        },
        "type"_a
    );

    // ============================================================
    // Value operations
    // ============================================================
    m.def(
        "xls_parse_typed_value",
        [](const std::string &input) -> _Value {
            char *error = nullptr;
            xls_value *val = nullptr;
            bool ok = xls_parse_typed_value(input.c_str(), &error, &val);
            check_result(ok, error);
            return _Value(val);
        },
        "input"_a
    );

    m.def(
        "xls_value_make_ubits",
        [](int64_t bit_count, uint64_t value) -> _Value {
            char *error = nullptr;
            xls_value *val = nullptr;
            bool ok = xls_value_make_ubits(bit_count, value, &error, &val);
            check_result(ok, error);
            return _Value(val);
        },
        "bit_count"_a,
        "value"_a
    );

    m.def(
        "xls_value_make_sbits",
        [](int64_t bit_count, int64_t value) -> _Value {
            char *error = nullptr;
            xls_value *val = nullptr;
            bool ok = xls_value_make_sbits(bit_count, value, &error, &val);
            check_result(ok, error);
            return _Value(val);
        },
        "bit_count"_a,
        "value"_a
    );

    m.def("xls_value_make_token", []() -> _Value {
        return _Value(xls_value_make_token());
    });

    m.def("xls_value_make_true", []() -> _Value {
        return _Value(xls_value_make_true());
    });

    m.def("xls_value_make_false", []() -> _Value {
        return _Value(xls_value_make_false());
    });

    m.def(
        "xls_value_make_array",
        [](std::vector<_Value *> elements) -> _Value {
            char *error = nullptr;
            xls_value *result = nullptr;
            std::vector<xls_value *> c_elems;
            c_elems.reserve(elements.size());
            for (auto *v : elements) {
                if (!v)
                    throw std::runtime_error("Null value in elements");
                c_elems.push_back(v->ptr.get());
            }
            bool ok = xls_value_make_array(
                c_elems.size(), c_elems.data(), &error, &result
            );
            check_result(ok, error);
            return _Value(result);
        },
        "elements"_a
    );

    m.def(
        "xls_value_make_tuple",
        [](std::vector<_Value *> elements) -> _Value {
            std::vector<xls_value *> c_elems;
            c_elems.reserve(elements.size());
            for (auto *v : elements) {
                if (!v)
                    throw std::runtime_error("Null value in elements");
                c_elems.push_back(v->ptr.get());
            }
            return _Value(xls_value_make_tuple(c_elems.size(), c_elems.data()));
        },
        "elements"_a
    );

    m.def(
        "xls_value_clone",
        [](const _Value &v) -> _Value {
            return _Value(xls_value_clone(v.ptr.get()));
        },
        "value"_a
    );

    m.def(
        "xls_value_get_kind",
        [](const _Value &v) -> XlsValueKind {
            char *error = nullptr;
            xls_value_kind kind;
            bool ok = xls_value_get_kind(v.ptr.get(), &error, &kind);
            check_result(ok, error);
            return static_cast<XlsValueKind>(kind);
        },
        "value"_a
    );

    m.def(
        "xls_value_get_element",
        [](const _Value &v, size_t index) -> _Value {
            char *error = nullptr;
            xls_value *elem = nullptr;
            bool ok = xls_value_get_element(v.ptr.get(), index, &error, &elem);
            check_result(ok, error);
            return _Value(elem);
        },
        "value"_a,
        "index"_a
    );

    m.def(
        "xls_value_get_element_count",
        [](const _Value &v) -> int64_t {
            char *error = nullptr;
            int64_t count;
            bool ok = xls_value_get_element_count(v.ptr.get(), &error, &count);
            check_result(ok, error);
            return count;
        },
        "value"_a
    );

    m.def(
        "xls_value_get_bits",
        [](const _Value &v) -> _Bits {
            char *error = nullptr;
            xls_bits *bits = nullptr;
            bool ok = xls_value_get_bits(v.ptr.get(), &error, &bits);
            check_result(ok, error);
            return _Bits(bits);
        },
        "value"_a
    );

    m.def(
        "xls_value_to_string",
        [](const _Value &v) -> std::string {
            char *str = nullptr;
            if (xls_value_to_string(v.ptr.get(), &str)) {
                return own_c_str(str);
            }
            throw std::runtime_error("Failed to convert value to string");
        },
        "value"_a
    );

    m.def(
        "xls_value_eq",
        [](const _Value &a, const _Value &b) -> bool {
            return xls_value_eq(a.ptr.get(), b.ptr.get());
        },
        "lhs"_a,
        "rhs"_a
    );

    m.def(
        "xls_value_from_bits",
        [](const _Bits &b) -> _Value {
            return _Value(xls_value_from_bits(b.ptr.get()));
        },
        "bits"_a
    );

    m.def(
        "xls_value_from_bits_owned",
        [](const _Bits &b) -> _Value {
            // Clone the bits since the _Bits wrapper still owns the original
            xls_bits *cloned =
                xls_value_flatten_to_bits(xls_value_from_bits(b.ptr.get()));
            return _Value(xls_value_from_bits_owned(cloned));
        },
        "bits"_a
    );

    m.def(
        "xls_value_flatten_to_bits",
        [](const _Value &v) -> _Bits {
            return _Bits(xls_value_flatten_to_bits(v.ptr.get()));
        },
        "value"_a
    );

    m.def(
        "xls_value_to_string_format_preference",
        [](const _Value &v, XlsFormatPreference pref) -> std::string {
            char *error = nullptr, *str = nullptr;
            bool ok = xls_value_to_string_format_preference(
                v.ptr.get(),
                static_cast<xls_format_preference>(pref),
                &error,
                &str
            );
            check_result(ok, error);
            return own_c_str(str);
        },
        "value"_a,
        "format_preference"_a
    );

    m.def(
        "xls_format_preference_from_string",
        [](const std::string &s) -> XlsFormatPreference {
            char *error = nullptr;
            xls_format_preference pref;
            bool ok =
                xls_format_preference_from_string(s.c_str(), &error, &pref);
            check_result(ok, error);
            return static_cast<XlsFormatPreference>(pref);
        },
        "s"_a
    );

    // ============================================================
    // Bits operations
    // ============================================================
    m.def(
        "xls_bits_get_bit_count",
        [](const _Bits &b) -> int64_t {
            return xls_bits_get_bit_count(b.ptr.get());
        },
        "bits"_a
    );

    m.def(
        "xls_bits_to_debug_string",
        [](const _Bits &b) -> std::string {
            return own_c_str(xls_bits_to_debug_string(b.ptr.get()));
        },
        "bits"_a
    );

    m.def(
        "xls_bits_make_bits_from_bytes",
        [](size_t bit_count, const nb::bytes &data) -> _Bits {
            char *error = nullptr;
            xls_bits *bits = nullptr;
            const uint8_t *bytes =
                reinterpret_cast<const uint8_t *>(data.data());
            bool ok = xls_bits_make_bits_from_bytes(
                bit_count, bytes, data.size(), &error, &bits
            );
            check_result(ok, error);
            return _Bits(bits);
        },
        "bit_count"_a,
        "data"_a
    );

    m.def(
        "xls_bits_make_ubits",
        [](int64_t bit_count, uint64_t value) -> _Bits {
            char *error = nullptr;
            xls_bits *bits = nullptr;
            bool ok = xls_bits_make_ubits(bit_count, value, &error, &bits);
            check_result(ok, error);
            return _Bits(bits);
        },
        "bit_count"_a,
        "value"_a
    );

    m.def(
        "xls_bits_make_sbits",
        [](int64_t bit_count, int64_t value) -> _Bits {
            char *error = nullptr;
            xls_bits *bits = nullptr;
            bool ok = xls_bits_make_sbits(bit_count, value, &error, &bits);
            check_result(ok, error);
            return _Bits(bits);
        },
        "bit_count"_a,
        "value"_a
    );

    m.def(
        "xls_bits_get_bit",
        [](const _Bits &b, int64_t index) -> bool {
            return xls_bits_get_bit(b.ptr.get(), index);
        },
        "bits"_a,
        "index"_a
    );

    m.def(
        "xls_bits_to_bytes",
        [](const _Bits &b) -> nb::bytes {
            char *error = nullptr;
            uint8_t *bytes = nullptr;
            size_t byte_count = 0;
            bool ok =
                xls_bits_to_bytes(b.ptr.get(), &error, &bytes, &byte_count);
            check_result(ok, error);
            nb::bytes result(reinterpret_cast<const char *>(bytes), byte_count);
            xls_bytes_free(bytes);
            return result;
        },
        "bits"_a
    );

    m.def(
        "xls_bits_to_uint64",
        [](const _Bits &b) -> uint64_t {
            char *error = nullptr;
            uint64_t value;
            bool ok = xls_bits_to_uint64(b.ptr.get(), &error, &value);
            check_result(ok, error);
            return value;
        },
        "bits"_a
    );

    m.def(
        "xls_bits_to_int64",
        [](const _Bits &b) -> int64_t {
            char *error = nullptr;
            int64_t value;
            bool ok = xls_bits_to_int64(b.ptr.get(), &error, &value);
            check_result(ok, error);
            return value;
        },
        "bits"_a
    );

    m.def(
        "xls_bits_to_string",
        [](const _Bits &b,
           XlsFormatPreference pref,
           bool include_bit_count) -> std::string {
            char *error = nullptr, *str = nullptr;
            bool ok = xls_bits_to_string(
                b.ptr.get(),
                static_cast<xls_format_preference>(pref),
                include_bit_count,
                &error,
                &str
            );
            check_result(ok, error);
            return own_c_str(str);
        },
        "bits"_a,
        "format_preference"_a,
        "include_bit_count"_a = true
    );

    // Bits comparisons
    m.def(
        "xls_bits_eq",
        [](const _Bits &a, const _Bits &b) -> bool {
            return xls_bits_eq(a.ptr.get(), b.ptr.get());
        },
        "lhs"_a,
        "rhs"_a
    );
    m.def(
        "xls_bits_ne",
        [](const _Bits &a, const _Bits &b) -> bool {
            return xls_bits_ne(a.ptr.get(), b.ptr.get());
        },
        "lhs"_a,
        "rhs"_a
    );
    m.def(
        "xls_bits_ult",
        [](const _Bits &a, const _Bits &b) -> bool {
            return xls_bits_ult(a.ptr.get(), b.ptr.get());
        },
        "lhs"_a,
        "rhs"_a
    );
    m.def(
        "xls_bits_ule",
        [](const _Bits &a, const _Bits &b) -> bool {
            return xls_bits_ule(a.ptr.get(), b.ptr.get());
        },
        "lhs"_a,
        "rhs"_a
    );
    m.def(
        "xls_bits_ugt",
        [](const _Bits &a, const _Bits &b) -> bool {
            return xls_bits_ugt(a.ptr.get(), b.ptr.get());
        },
        "lhs"_a,
        "rhs"_a
    );
    m.def(
        "xls_bits_uge",
        [](const _Bits &a, const _Bits &b) -> bool {
            return xls_bits_uge(a.ptr.get(), b.ptr.get());
        },
        "lhs"_a,
        "rhs"_a
    );
    m.def(
        "xls_bits_slt",
        [](const _Bits &a, const _Bits &b) -> bool {
            return xls_bits_slt(a.ptr.get(), b.ptr.get());
        },
        "lhs"_a,
        "rhs"_a
    );
    m.def(
        "xls_bits_sle",
        [](const _Bits &a, const _Bits &b) -> bool {
            return xls_bits_sle(a.ptr.get(), b.ptr.get());
        },
        "lhs"_a,
        "rhs"_a
    );
    m.def(
        "xls_bits_sgt",
        [](const _Bits &a, const _Bits &b) -> bool {
            return xls_bits_sgt(a.ptr.get(), b.ptr.get());
        },
        "lhs"_a,
        "rhs"_a
    );
    m.def(
        "xls_bits_sge",
        [](const _Bits &a, const _Bits &b) -> bool {
            return xls_bits_sge(a.ptr.get(), b.ptr.get());
        },
        "lhs"_a,
        "rhs"_a
    );

    // Bits slice/shift
    m.def(
        "xls_bits_width_slice",
        [](const _Bits &b, int64_t start, int64_t width) -> _Bits {
            return _Bits(xls_bits_width_slice(b.ptr.get(), start, width));
        },
        "bits"_a,
        "start"_a,
        "width"_a
    );

    m.def(
        "xls_bits_shift_left_logical",
        [](const _Bits &b, int64_t amount) -> _Bits {
            return _Bits(xls_bits_shift_left_logical(b.ptr.get(), amount));
        },
        "bits"_a,
        "amount"_a
    );
    m.def(
        "xls_bits_shift_right_logical",
        [](const _Bits &b, int64_t amount) -> _Bits {
            return _Bits(xls_bits_shift_right_logical(b.ptr.get(), amount));
        },
        "bits"_a,
        "amount"_a
    );
    m.def(
        "xls_bits_shift_right_arithmetic",
        [](const _Bits &b, int64_t amount) -> _Bits {
            return _Bits(xls_bits_shift_right_arithmetic(b.ptr.get(), amount));
        },
        "bits"_a,
        "amount"_a
    );

    // Bits arithmetic
    m.def(
        "xls_bits_negate",
        [](const _Bits &b) -> _Bits {
            return _Bits(xls_bits_negate(b.ptr.get()));
        },
        "bits"_a
    );
    m.def(
        "xls_bits_abs",
        [](const _Bits &b) -> _Bits {
            return _Bits(xls_bits_abs(b.ptr.get()));
        },
        "bits"_a
    );
    m.def(
        "xls_bits_not",
        [](const _Bits &b) -> _Bits {
            return _Bits(xls_bits_not(b.ptr.get()));
        },
        "bits"_a
    );
    m.def(
        "xls_bits_add",
        [](const _Bits &a, const _Bits &b) -> _Bits {
            return _Bits(xls_bits_add(a.ptr.get(), b.ptr.get()));
        },
        "lhs"_a,
        "rhs"_a
    );
    m.def(
        "xls_bits_sub",
        [](const _Bits &a, const _Bits &b) -> _Bits {
            return _Bits(xls_bits_sub(a.ptr.get(), b.ptr.get()));
        },
        "lhs"_a,
        "rhs"_a
    );
    m.def(
        "xls_bits_and",
        [](const _Bits &a, const _Bits &b) -> _Bits {
            return _Bits(xls_bits_and(a.ptr.get(), b.ptr.get()));
        },
        "lhs"_a,
        "rhs"_a
    );
    m.def(
        "xls_bits_or",
        [](const _Bits &a, const _Bits &b) -> _Bits {
            return _Bits(xls_bits_or(a.ptr.get(), b.ptr.get()));
        },
        "lhs"_a,
        "rhs"_a
    );
    m.def(
        "xls_bits_xor",
        [](const _Bits &a, const _Bits &b) -> _Bits {
            return _Bits(xls_bits_xor(a.ptr.get(), b.ptr.get()));
        },
        "lhs"_a,
        "rhs"_a
    );
    m.def(
        "xls_bits_umul",
        [](const _Bits &a, const _Bits &b) -> _Bits {
            return _Bits(xls_bits_umul(a.ptr.get(), b.ptr.get()));
        },
        "lhs"_a,
        "rhs"_a
    );
    m.def(
        "xls_bits_smul",
        [](const _Bits &a, const _Bits &b) -> _Bits {
            return _Bits(xls_bits_smul(a.ptr.get(), b.ptr.get()));
        },
        "lhs"_a,
        "rhs"_a
    );

    // BitsRope
    m.def(
        "xls_create_bits_rope",
        [](int64_t bit_count) -> _BitsRope {
            return _BitsRope(xls_create_bits_rope(bit_count));
        },
        "bit_count"_a
    );

    m.def(
        "xls_bits_rope_append_bits",
        [](const _BitsRope &rope, const _Bits &bits) {
            xls_bits_rope_append_bits(rope.ptr.get(), bits.ptr.get());
        },
        "rope"_a,
        "bits"_a
    );

    m.def(
        "xls_bits_rope_get_bits",
        [](const _BitsRope &rope) -> _Bits {
            return _Bits(xls_bits_rope_get_bits(rope.ptr.get()));
        },
        "rope"_a
    );

    // ============================================================
    // Interpret & JIT
    // ============================================================
    m.def(
        "xls_interpret_function",
        [](const _Function &fn, std::vector<_Value *> args) -> _Value {
            char *error = nullptr;
            xls_value *result = nullptr;
            std::vector<const xls_value *> c_args;
            c_args.reserve(args.size());
            for (auto *v : args) {
                if (!v)
                    throw std::runtime_error("Null value in args");
                c_args.push_back(v->ptr.get());
            }
            bool ok = xls_interpret_function(
                fn.ptr, c_args.size(), c_args.data(), &error, &result
            );
            check_result(ok, error);
            return _Value(result);
        },
        "function"_a,
        "args"_a
    );

    m.def(
        "xls_make_function_jit",
        [](const _Function &fn) -> _FunctionJit {
            char *error = nullptr;
            xls_function_jit *jit = nullptr;
            bool ok = xls_make_function_jit(fn.ptr, &error, &jit);
            check_result(ok, error);
            return _FunctionJit(jit);
        },
        "function"_a
    );

    m.def(
        "xls_function_jit_run",
        [](const _FunctionJit &jit, std::vector<_Value *> args) -> _Value {
            char *error = nullptr;
            xls_value *result = nullptr;
            std::vector<const xls_value *> c_args;
            c_args.reserve(args.size());
            for (auto *v : args) {
                if (!v)
                    throw std::runtime_error("Null value in args");
                c_args.push_back(v->ptr.get());
            }
            xls_trace_message *trace_msgs = nullptr;
            size_t trace_count = 0;
            char **assert_msgs = nullptr;
            size_t assert_count = 0;
            bool ok = xls_function_jit_run(
                jit.ptr.get(),
                c_args.size(),
                c_args.data(),
                &error,
                &trace_msgs,
                &trace_count,
                &assert_msgs,
                &assert_count,
                &result
            );
            if (trace_msgs) {
                for (size_t i = 0; i < trace_count; ++i)
                    std::cerr << "[Trace] " << trace_msgs[i].message
                              << std::endl;
                xls_trace_messages_free(trace_msgs, trace_count);
            }
            if (assert_msgs) {
                for (size_t i = 0; i < assert_count; ++i)
                    std::cerr << "[Assert] " << assert_msgs[i] << std::endl;
                xls_c_strs_free(assert_msgs, assert_count);
            }
            check_result(ok, error);
            return _Value(result);
        },
        "jit"_a,
        "args"_a
    );
}
