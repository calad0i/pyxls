#include "_ir_builder.h"
#include "_types.h"
#include "_helpers.h"
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>

using namespace nb::literals;

// Macros to reduce boilerplate for builder operations
#define BIND_BUILDER_BINARY(m, c_fn, py_name)                                  \
    m.def(                                                                     \
        py_name,                                                               \
        [](const _BuilderBase &bb,                                             \
           _BValue &lhs,                                                       \
           _BValue &rhs,                                                       \
           nb::object name) -> _BValue {                                       \
            const char *n = name.is_none()                                     \
                                ? nullptr                                      \
                                : nb::cast<std::string>(name).c_str();         \
            return _BValue(c_fn(bb.ptr, lhs.ptr.get(), rhs.ptr.get(), n));     \
        },                                                                     \
        "builder"_a,                                                           \
        "lhs"_a,                                                               \
        "rhs"_a,                                                               \
        "name"_a = nb::none()                                                  \
    )

#define BIND_BUILDER_UNARY(m, c_fn, py_name)                                   \
    m.def(                                                                     \
        py_name,                                                               \
        [](const _BuilderBase &bb, _BValue &val, nb::object name) -> _BValue { \
            const char *n = name.is_none()                                     \
                                ? nullptr                                      \
                                : nb::cast<std::string>(name).c_str();         \
            return _BValue(c_fn(bb.ptr, val.ptr.get(), n));                    \
        },                                                                     \
        "builder"_a,                                                           \
        "value"_a,                                                             \
        "name"_a = nb::none()                                                  \
    )

void bind_ir_builder(nb::module_ &m) {
    // ============================================================
    // Package type creation (from ir_builder.h but creates Package types)
    // ============================================================
    m.def(
        "xls_package_create",
        [](const std::string &name) -> _Package {
            return _Package(xls_package_create(name.c_str()));
        },
        "name"_a
    );

    m.def(
        "xls_package_get_bits_type",
        [](const _Package &pkg, int64_t bit_count) -> _Type {
            return _Type(xls_package_get_bits_type(
                const_cast<xls_package *>(pkg.ptr.get()), bit_count
            ));
        },
        nb::keep_alive<0, 1>(),
        "package"_a,
        "bit_count"_a
    );

    m.def(
        "xls_package_get_tuple_type",
        [](const _Package &pkg, std::vector<_Type *> members) -> _Type {
            std::vector<xls_type *> c_members;
            for (auto *t : members)
                c_members.push_back(t->ptr);
            return _Type(xls_package_get_tuple_type(
                const_cast<xls_package *>(pkg.ptr.get()),
                c_members.data(),
                c_members.size()
            ));
        },
        nb::keep_alive<0, 1>(),
        "package"_a,
        "members"_a
    );

    m.def(
        "xls_package_get_array_type",
        [](const _Package &pkg,
           const _Type &element_type,
           int64_t size) -> _Type {
            return _Type(xls_package_get_array_type(
                const_cast<xls_package *>(pkg.ptr.get()), element_type.ptr, size
            ));
        },
        nb::keep_alive<0, 1>(),
        "package"_a,
        "element_type"_a,
        "size"_a
    );

    m.def(
        "xls_package_get_token_type",
        [](const _Package &pkg) -> _Type {
            return _Type(xls_package_get_token_type(
                const_cast<xls_package *>(pkg.ptr.get())
            ));
        },
        nb::keep_alive<0, 1>(),
        "package"_a
    );

    // ============================================================
    // FunctionBuilder
    // ============================================================
    m.def(
        "xls_function_builder_create",
        [](const std::string &name,
           const _Package &pkg,
           bool should_verify) -> _FunctionBuilder {
            return _FunctionBuilder(xls_function_builder_create(
                name.c_str(),
                const_cast<xls_package *>(pkg.ptr.get()),
                should_verify
            ));
        },
        nb::keep_alive<0, 2>(),
        "name"_a,
        "package"_a,
        "should_verify"_a = true
    );

    m.def(
        "xls_function_builder_as_builder_base",
        [](const _FunctionBuilder &fb) -> _BuilderBase {
            return _BuilderBase(
                xls_function_builder_as_builder_base(fb.ptr.get())
            );
        },
        nb::keep_alive<0, 1>(),
        "builder"_a
    );

    m.def(
        "xls_function_builder_add_parameter",
        [](const _FunctionBuilder &fb,
           const std::string &name,
           const _Type &type) -> _BValue {
            return _BValue(xls_function_builder_add_parameter(
                fb.ptr.get(), name.c_str(), type.ptr
            ));
        },
        "builder"_a,
        "name"_a,
        "type"_a
    );

    m.def(
        "xls_function_builder_build",
        [](const _FunctionBuilder &fb) -> _Function {
            char *error = nullptr;
            xls_function *fn = nullptr;
            bool ok = xls_function_builder_build(fb.ptr.get(), &error, &fn);
            check_result(ok, error);
            return _Function(fn);
        },
        "builder"_a
    );

    m.def(
        "xls_function_builder_build_with_return_value",
        [](const _FunctionBuilder &fb, _BValue &ret_val) -> _Function {
            char *error = nullptr;
            xls_function *fn = nullptr;
            bool ok = xls_function_builder_build_with_return_value(
                fb.ptr.get(), ret_val.ptr.get(), &error, &fn
            );
            check_result(ok, error);
            return _Function(fn);
        },
        "builder"_a,
        "return_value"_a
    );

    // ============================================================
    // BuilderBase operations — binary ops
    // ============================================================
    BIND_BUILDER_BINARY(
        m, xls_builder_base_add_add, "xls_builder_base_add_add"
    );
    BIND_BUILDER_BINARY(
        m, xls_builder_base_add_sub, "xls_builder_base_add_sub"
    );
    BIND_BUILDER_BINARY(
        m, xls_builder_base_add_umul, "xls_builder_base_add_umul"
    );
    BIND_BUILDER_BINARY(
        m, xls_builder_base_add_smul, "xls_builder_base_add_smul"
    );
    BIND_BUILDER_BINARY(
        m, xls_builder_base_add_umulp, "xls_builder_base_add_umulp"
    );
    BIND_BUILDER_BINARY(
        m, xls_builder_base_add_smulp, "xls_builder_base_add_smulp"
    );
    BIND_BUILDER_BINARY(
        m, xls_builder_base_add_udiv, "xls_builder_base_add_udiv"
    );
    BIND_BUILDER_BINARY(
        m, xls_builder_base_add_sdiv, "xls_builder_base_add_sdiv"
    );
    BIND_BUILDER_BINARY(
        m, xls_builder_base_add_umod, "xls_builder_base_add_umod"
    );
    BIND_BUILDER_BINARY(
        m, xls_builder_base_add_smod, "xls_builder_base_add_smod"
    );
    BIND_BUILDER_BINARY(
        m, xls_builder_base_add_and, "xls_builder_base_add_and"
    );
    BIND_BUILDER_BINARY(m, xls_builder_base_add_or, "xls_builder_base_add_or");
    BIND_BUILDER_BINARY(
        m, xls_builder_base_add_xor, "xls_builder_base_add_xor"
    );
    BIND_BUILDER_BINARY(
        m, xls_builder_base_add_nand, "xls_builder_base_add_nand"
    );
    BIND_BUILDER_BINARY(
        m, xls_builder_base_add_nor, "xls_builder_base_add_nor"
    );
    BIND_BUILDER_BINARY(m, xls_builder_base_add_eq, "xls_builder_base_add_eq");
    BIND_BUILDER_BINARY(m, xls_builder_base_add_ne, "xls_builder_base_add_ne");
    BIND_BUILDER_BINARY(
        m, xls_builder_base_add_ult, "xls_builder_base_add_ult"
    );
    BIND_BUILDER_BINARY(
        m, xls_builder_base_add_ule, "xls_builder_base_add_ule"
    );
    BIND_BUILDER_BINARY(
        m, xls_builder_base_add_ugt, "xls_builder_base_add_ugt"
    );
    BIND_BUILDER_BINARY(
        m, xls_builder_base_add_uge, "xls_builder_base_add_uge"
    );
    BIND_BUILDER_BINARY(
        m, xls_builder_base_add_slt, "xls_builder_base_add_slt"
    );
    BIND_BUILDER_BINARY(
        m, xls_builder_base_add_sle, "xls_builder_base_add_sle"
    );
    BIND_BUILDER_BINARY(
        m, xls_builder_base_add_sgt, "xls_builder_base_add_sgt"
    );
    BIND_BUILDER_BINARY(
        m, xls_builder_base_add_sge, "xls_builder_base_add_sge"
    );
    BIND_BUILDER_BINARY(
        m, xls_builder_base_add_shll, "xls_builder_base_add_shll"
    );
    BIND_BUILDER_BINARY(
        m, xls_builder_base_add_shrl, "xls_builder_base_add_shrl"
    );
    BIND_BUILDER_BINARY(
        m, xls_builder_base_add_shra, "xls_builder_base_add_shra"
    );

    // ============================================================
    // BuilderBase operations — unary ops
    // ============================================================
    BIND_BUILDER_UNARY(
        m, xls_builder_base_add_negate, "xls_builder_base_add_negate"
    );
    BIND_BUILDER_UNARY(m, xls_builder_base_add_not, "xls_builder_base_add_not");
    BIND_BUILDER_UNARY(
        m, xls_builder_base_add_and_reduce, "xls_builder_base_add_and_reduce"
    );
    BIND_BUILDER_UNARY(
        m, xls_builder_base_add_or_reduce, "xls_builder_base_add_or_reduce"
    );
    BIND_BUILDER_UNARY(
        m, xls_builder_base_add_xor_reduce, "xls_builder_base_add_xor_reduce"
    );
    BIND_BUILDER_UNARY(m, xls_builder_base_add_clz, "xls_builder_base_add_clz");
    BIND_BUILDER_UNARY(m, xls_builder_base_add_ctz, "xls_builder_base_add_ctz");
    BIND_BUILDER_UNARY(
        m, xls_builder_base_add_reverse, "xls_builder_base_add_reverse"
    );
    BIND_BUILDER_UNARY(
        m, xls_builder_base_add_identity, "xls_builder_base_add_identity"
    );
    BIND_BUILDER_UNARY(
        m, xls_builder_base_add_encode, "xls_builder_base_add_encode"
    );

    // ============================================================
    // BuilderBase — other operations
    // ============================================================
    m.def(
        "xls_builder_base_add_literal",
        [](const _BuilderBase &bb,
           const _Value &val,
           nb::object name) -> _BValue {
            const char *n =
                name.is_none() ? nullptr : nb::cast<std::string>(name).c_str();
            return _BValue(xls_builder_base_add_literal(
                bb.ptr, const_cast<xls_value *>(val.ptr.get()), n
            ));
        },
        "builder"_a,
        "value"_a,
        "name"_a = nb::none()
    );

    m.def(
        "xls_builder_base_add_concat",
        [](const _BuilderBase &bb,
           std::vector<_BValue *> operands,
           nb::object name) -> _BValue {
            const char *n =
                name.is_none() ? nullptr : nb::cast<std::string>(name).c_str();
            std::vector<xls_bvalue *> c_ops;
            for (auto *v : operands)
                c_ops.push_back(v->ptr.get());
            return _BValue(xls_builder_base_add_concat(
                bb.ptr, c_ops.data(), c_ops.size(), n
            ));
        },
        "builder"_a,
        "operands"_a,
        "name"_a = nb::none()
    );

    m.def(
        "xls_builder_base_add_tuple",
        [](const _BuilderBase &bb,
           std::vector<_BValue *> operands,
           nb::object name) -> _BValue {
            const char *n =
                name.is_none() ? nullptr : nb::cast<std::string>(name).c_str();
            std::vector<xls_bvalue *> c_ops;
            for (auto *v : operands)
                c_ops.push_back(v->ptr.get());
            return _BValue(xls_builder_base_add_tuple(
                bb.ptr, c_ops.data(), c_ops.size(), n
            ));
        },
        "builder"_a,
        "operands"_a,
        "name"_a = nb::none()
    );

    m.def(
        "xls_builder_base_add_after_all",
        [](const _BuilderBase &bb,
           std::vector<_BValue *> deps,
           nb::object name) -> _BValue {
            const char *n =
                name.is_none() ? nullptr : nb::cast<std::string>(name).c_str();
            std::vector<xls_bvalue *> c_deps;
            for (auto *v : deps)
                c_deps.push_back(v->ptr.get());
            return _BValue(xls_builder_base_add_after_all(
                bb.ptr, c_deps.data(), c_deps.size(), n
            ));
        },
        "builder"_a,
        "dependencies"_a,
        "name"_a = nb::none()
    );

    m.def(
        "xls_builder_base_add_array",
        [](const _BuilderBase &bb,
           const _Type &elem_type,
           std::vector<_BValue *> elements,
           nb::object name) -> _BValue {
            const char *n =
                name.is_none() ? nullptr : nb::cast<std::string>(name).c_str();
            std::vector<xls_bvalue *> c_elems;
            for (auto *v : elements)
                c_elems.push_back(v->ptr.get());
            return _BValue(xls_builder_base_add_array(
                bb.ptr, elem_type.ptr, c_elems.data(), c_elems.size(), n
            ));
        },
        "builder"_a,
        "element_type"_a,
        "elements"_a,
        "name"_a = nb::none()
    );

    m.def(
        "xls_builder_base_add_tuple_index",
        [](const _BuilderBase &bb,
           _BValue &tuple,
           int64_t index,
           nb::object name) -> _BValue {
            const char *n =
                name.is_none() ? nullptr : nb::cast<std::string>(name).c_str();
            return _BValue(xls_builder_base_add_tuple_index(
                bb.ptr, tuple.ptr.get(), index, n
            ));
        },
        "builder"_a,
        "tuple"_a,
        "index"_a,
        "name"_a = nb::none()
    );

    m.def(
        "xls_builder_base_add_array_index",
        [](const _BuilderBase &bb,
           _BValue &array,
           std::vector<_BValue *> indices,
           bool assumed_in_bounds,
           nb::object name) -> _BValue {
            const char *n =
                name.is_none() ? nullptr : nb::cast<std::string>(name).c_str();
            std::vector<xls_bvalue *> c_idx;
            for (auto *v : indices)
                c_idx.push_back(v->ptr.get());
            return _BValue(xls_builder_base_add_array_index(
                bb.ptr,
                array.ptr.get(),
                c_idx.data(),
                c_idx.size(),
                assumed_in_bounds,
                n
            ));
        },
        "builder"_a,
        "array"_a,
        "indices"_a,
        "assumed_in_bounds"_a = false,
        "name"_a = nb::none()
    );

    m.def(
        "xls_builder_base_add_array_slice",
        [](const _BuilderBase &bb,
           _BValue &array,
           _BValue &start,
           int64_t width,
           nb::object name) -> _BValue {
            const char *n =
                name.is_none() ? nullptr : nb::cast<std::string>(name).c_str();
            return _BValue(xls_builder_base_add_array_slice(
                bb.ptr, array.ptr.get(), start.ptr.get(), width, n
            ));
        },
        "builder"_a,
        "array"_a,
        "start"_a,
        "width"_a,
        "name"_a = nb::none()
    );

    m.def(
        "xls_builder_base_add_array_update",
        [](const _BuilderBase &bb,
           _BValue &array,
           _BValue &update_value,
           std::vector<_BValue *> indices,
           bool assumed_in_bounds,
           nb::object name) -> _BValue {
            const char *n =
                name.is_none() ? nullptr : nb::cast<std::string>(name).c_str();
            std::vector<xls_bvalue *> c_idx;
            for (auto *v : indices)
                c_idx.push_back(v->ptr.get());
            return _BValue(xls_builder_base_add_array_update(
                bb.ptr,
                array.ptr.get(),
                update_value.ptr.get(),
                c_idx.data(),
                c_idx.size(),
                assumed_in_bounds,
                n
            ));
        },
        "builder"_a,
        "array"_a,
        "update_value"_a,
        "indices"_a,
        "assumed_in_bounds"_a = false,
        "name"_a = nb::none()
    );

    m.def(
        "xls_builder_base_add_array_concat",
        [](const _BuilderBase &bb,
           std::vector<_BValue *> arrays,
           nb::object name) -> _BValue {
            const char *n =
                name.is_none() ? nullptr : nb::cast<std::string>(name).c_str();
            std::vector<xls_bvalue *> c_arrs;
            for (auto *v : arrays)
                c_arrs.push_back(v->ptr.get());
            return _BValue(xls_builder_base_add_array_concat(
                bb.ptr, c_arrs.data(), c_arrs.size(), n
            ));
        },
        "builder"_a,
        "arrays"_a,
        "name"_a = nb::none()
    );

    m.def(
        "xls_builder_base_add_sign_extend",
        [](const _BuilderBase &bb,
           _BValue &val,
           int64_t new_bit_count,
           nb::object name) -> _BValue {
            const char *n =
                name.is_none() ? nullptr : nb::cast<std::string>(name).c_str();
            return _BValue(xls_builder_base_add_sign_extend(
                bb.ptr, val.ptr.get(), new_bit_count, n
            ));
        },
        "builder"_a,
        "value"_a,
        "new_bit_count"_a,
        "name"_a = nb::none()
    );

    m.def(
        "xls_builder_base_add_zero_extend",
        [](const _BuilderBase &bb,
           _BValue &val,
           int64_t new_bit_count,
           nb::object name) -> _BValue {
            const char *n =
                name.is_none() ? nullptr : nb::cast<std::string>(name).c_str();
            return _BValue(xls_builder_base_add_zero_extend(
                bb.ptr, val.ptr.get(), new_bit_count, n
            ));
        },
        "builder"_a,
        "value"_a,
        "new_bit_count"_a,
        "name"_a = nb::none()
    );

    m.def(
        "xls_builder_base_add_bit_slice",
        [](const _BuilderBase &bb,
           _BValue &val,
           int64_t start,
           int64_t width,
           nb::object name) -> _BValue {
            const char *n =
                name.is_none() ? nullptr : nb::cast<std::string>(name).c_str();
            return _BValue(xls_builder_base_add_bit_slice(
                bb.ptr, val.ptr.get(), start, width, n
            ));
        },
        "builder"_a,
        "value"_a,
        "start"_a,
        "width"_a,
        "name"_a = nb::none()
    );

    m.def(
        "xls_builder_base_add_bit_slice_update",
        [](const _BuilderBase &bb,
           _BValue &arg,
           _BValue &start,
           _BValue &update_value,
           nb::object name) -> _BValue {
            const char *n =
                name.is_none() ? nullptr : nb::cast<std::string>(name).c_str();
            return _BValue(xls_builder_base_add_bit_slice_update(
                bb.ptr, arg.ptr.get(), start.ptr.get(), update_value.ptr.get(), n
            ));
        },
        "builder"_a,
        "arg"_a,
        "start"_a,
        "update_value"_a,
        "name"_a = nb::none()
    );

    m.def(
        "xls_builder_base_add_dynamic_bit_slice",
        [](const _BuilderBase &bb,
           _BValue &val,
           _BValue &start,
           int64_t width,
           nb::object name) -> _BValue {
            const char *n =
                name.is_none() ? nullptr : nb::cast<std::string>(name).c_str();
            return _BValue(xls_builder_base_add_dynamic_bit_slice(
                bb.ptr, val.ptr.get(), start.ptr.get(), width, n
            ));
        },
        "builder"_a,
        "value"_a,
        "start"_a,
        "width"_a,
        "name"_a = nb::none()
    );

    m.def(
        "xls_builder_base_add_decode",
        [](const _BuilderBase &bb,
           _BValue &val,
           nb::object width,
           nb::object name) -> _BValue {
            const char *n =
                name.is_none() ? nullptr : nb::cast<std::string>(name).c_str();
            int64_t w_val;
            int64_t *w_ptr = nullptr;
            if (!width.is_none()) {
                w_val = nb::cast<int64_t>(width);
                w_ptr = &w_val;
            }
            return _BValue(
                xls_builder_base_add_decode(bb.ptr, val.ptr.get(), w_ptr, n)
            );
        },
        "builder"_a,
        "value"_a,
        "width"_a = nb::none(),
        "name"_a = nb::none()
    );

    m.def(
        "xls_builder_base_add_select",
        [](const _BuilderBase &bb,
           _BValue &selector,
           std::vector<_BValue *> cases,
           nb::object default_value,
           nb::object name) -> _BValue {
            const char *n =
                name.is_none() ? nullptr : nb::cast<std::string>(name).c_str();
            std::vector<xls_bvalue *> c_cases;
            for (auto *v : cases)
                c_cases.push_back(v->ptr.get());
            xls_bvalue *def = nullptr;
            if (!default_value.is_none())
                def = nb::cast<_BValue &>(default_value).ptr.get();
            return _BValue(xls_builder_base_add_select(
                bb.ptr, selector.ptr.get(), c_cases.data(), c_cases.size(), def, n
            ));
        },
        "builder"_a,
        "selector"_a,
        "cases"_a,
        "default_value"_a = nb::none(),
        "name"_a = nb::none()
    );

    m.def(
        "xls_builder_base_add_one_hot",
        [](const _BuilderBase &bb,
           _BValue &input,
           bool lsb_is_priority,
           nb::object name) -> _BValue {
            const char *n =
                name.is_none() ? nullptr : nb::cast<std::string>(name).c_str();
            return _BValue(xls_builder_base_add_one_hot(
                bb.ptr, input.ptr.get(), lsb_is_priority, n
            ));
        },
        "builder"_a,
        "input"_a,
        "lsb_is_priority"_a = true,
        "name"_a = nb::none()
    );

    m.def(
        "xls_builder_base_add_one_hot_select",
        [](const _BuilderBase &bb,
           _BValue &selector,
           std::vector<_BValue *> cases,
           nb::object name) -> _BValue {
            const char *n =
                name.is_none() ? nullptr : nb::cast<std::string>(name).c_str();
            std::vector<xls_bvalue *> c_cases;
            for (auto *v : cases)
                c_cases.push_back(v->ptr.get());
            return _BValue(xls_builder_base_add_one_hot_select(
                bb.ptr, selector.ptr.get(), c_cases.data(), c_cases.size(), n
            ));
        },
        "builder"_a,
        "selector"_a,
        "cases"_a,
        "name"_a = nb::none()
    );

    m.def(
        "xls_builder_base_add_priority_select",
        [](const _BuilderBase &bb,
           _BValue &selector,
           std::vector<_BValue *> cases,
           _BValue &default_value,
           nb::typed<nb::object, nb::str> name) -> _BValue {
            const char *n =
                name.is_none() ? nullptr : nb::cast<nb::str>(name).c_str();
            std::vector<xls_bvalue *> c_cases;
            for (auto *v : cases)
                c_cases.push_back(v->ptr.get());
            return _BValue(xls_builder_base_add_priority_select(
                bb.ptr,
                selector.ptr.get(),
                c_cases.data(),
                c_cases.size(),
                default_value.ptr.get(),
                n
            ));
        },
        "builder"_a,
        "selector"_a,
        "cases"_a,
        "default_value"_a,
        "name"_a = nb::none()
    );

    m.def(
        "xls_builder_base_get_type",
        [](const _BuilderBase &bb, _BValue &val) -> _Type {
            return _Type(xls_builder_base_get_type(bb.ptr, val.ptr.get()));
        },
        nb::keep_alive<0, 1>(),
        "builder"_a,
        "value"_a
    );

    m.def(
        "xls_builder_base_get_last_value",
        [](const _BuilderBase &bb) -> _BValue {
            char *error = nullptr;
            xls_bvalue *val = nullptr;
            bool ok = xls_builder_base_get_last_value(bb.ptr, &error, &val);
            check_result(ok, error);
            return _BValue(val);
        },
        "builder"_a
    );
}
