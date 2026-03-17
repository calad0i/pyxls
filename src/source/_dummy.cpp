#include <string>
#include <xls/public/c_api.h>
#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>
#include <stdexcept>
#include <memory>
#include <iostream>
#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>
#include <nanobind/stl/optional.h>

namespace nb = nanobind;
using namespace nb::literals;
// --- Deleters ---
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
struct ScheduleResultDeleter {
    void operator()(xls_schedule_and_codegen_result *p) const {
        xls_schedule_and_codegen_result_free(p);
    }
};

// --- Wrapper Structs ---

struct _Package {
    std::unique_ptr<xls_package, PackageDeleter> ptr;
    _Package() = default;
    _Package(xls_package *p) : ptr(p) {}
};

struct _Function {
    xls_function *ptr = nullptr; // Borrowed
    _Function() = default;
    _Function(xls_function *p) : ptr(p) {}
};

struct _FunctionType {
    xls_function_type *ptr = nullptr; // Borrowed
    _FunctionType() = default;
    _FunctionType(xls_function_type *p) : ptr(p) {}
};

struct _FunctionJit {
    std::unique_ptr<xls_function_jit, FunctionJitDeleter> ptr;
    _FunctionJit() = default;
    _FunctionJit(xls_function_jit *p) : ptr(p) {}
};

struct _Type {
    xls_type *ptr = nullptr; // Borrowed
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

struct _ScheduleAndCodegenResult {
    std::unique_ptr<xls_schedule_and_codegen_result, ScheduleResultDeleter> ptr;
    _ScheduleAndCodegenResult() = default;
    _ScheduleAndCodegenResult(xls_schedule_and_codegen_result *p) : ptr(p) {}
};

// --- Helper ---
void check_result(bool ok, char *error_msg) {
    if (ok) {
        return;
    }
    std::string err = error_msg ? error_msg : "Unknown XLS error";
    if (error_msg)
        xls_c_str_free(error_msg);
    throw std::runtime_error(err);
}

_Package parse_ir_package(nb::str ir, nb::object filename) {
    char *error = nullptr;
    xls_package *package = nullptr;
    const char *filename_ =
        filename.is_none() ? nullptr : nb::cast<nb::str>(filename).c_str();
    bool ok = xls_parse_ir_package(ir.c_str(), filename_, &error, &package);
    check_result(ok, error);
    return _Package(package);
}

std::string convert_dslx_to_ir(
    const nb::str &dslx,
    const nb::str &path,
    const nb::str &module_name,
    const nb::str &dslx_stdlib_path,
    std::vector<std::string> additional_search_paths
) {
    char *error = nullptr;
    char *ir = nullptr;
    std::vector<const char *> c_paths;
    c_paths.reserve(additional_search_paths.size());
    for (const auto &s : additional_search_paths)
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
}

std::string
mangle_dslx_name(const nb::str &module_name, const nb::str &function_name) {
    char *error = nullptr;
    char *mangled = nullptr;
    bool ok = xls_mangle_dslx_name(
        module_name.c_str(), function_name.c_str(), &error, &mangled
    );
    check_result(ok, error);
    std::string res(mangled);
    xls_c_str_free(mangled);
    return res;
}

int test(nb::object x) {
    int value = nb::cast<int>(x);
    std::cout << "Test called with: " << value << std::endl;
    return value * 2;
}

_Function package_get_function(const _Package &pkg, const nb::str &name) {
    char *error = nullptr;
    xls_function *func = nullptr;
    bool ok =
        xls_package_get_function(pkg.ptr.get(), name.c_str(), &error, &func);
    check_result(ok, error);
    return _Function(func);
}

std::string package_to_string(const _Package &pkg) {
    char *str = nullptr;
    if (xls_package_to_string(pkg.ptr.get(), &str)) {
        std::string s(str);
        xls_c_str_free(str);
        return s;
    }
    throw std::runtime_error("Failed to convert package to string");
}

std::string function_get_name(const _Function &fn) {
    char *error = nullptr;
    char *name = nullptr;
    bool ok = xls_function_get_name(fn.ptr, &error, &name);
    check_result(ok, error);
    std::string s(name);
    xls_c_str_free(name);
    return s;
}

_FunctionType function_get_type(const _Function &fn) {
    char *error = nullptr;
    xls_function_type *type = nullptr;
    bool ok = xls_function_get_type(fn.ptr, &error, &type);
    check_result(ok, error);
    return _FunctionType(type);
}

_Value parse_typed_value(const nb::str input) {
    char *error = nullptr;
    xls_value *val = nullptr;
    bool ok = xls_parse_typed_value(input.c_str(), &error, &val);
    check_result(ok, error);
    return _Value(val);
}

std::string value_to_string(const _Value &value) {
    char *str = nullptr;
    if (xls_value_to_string(value.ptr.get(), &str)) {
        std::string s(str);
        xls_c_str_free(str);
        return s;
    }
    throw std::runtime_error("Failed to convert value to string");
}

_Value value_make_ubits(int64_t bit_count, uint64_t value) {
    char *error = nullptr;
    xls_value *val = nullptr;
    bool ok = xls_value_make_ubits(bit_count, value, &error, &val);
    check_result(ok, error);
    return _Value(val);
}

_Value value_make_sbits(int64_t bit_count, int64_t value) {
    char *error = nullptr;
    xls_value *val = nullptr;
    bool ok = xls_value_make_sbits(bit_count, value, &error, &val);
    check_result(ok, error);
    return _Value(val);
}

_Value value_make_array(std::vector<_Value *> elements) {
    char *error = nullptr;
    xls_value *result = nullptr;
    std::vector<xls_value *> c_elements;
    c_elements.reserve(elements.size());
    for (auto *v : elements) {
        if (!v) {
            throw std::runtime_error("Null value pointer in elements");
        }
        c_elements.push_back(v->ptr.get());
    }

    bool ok = xls_value_make_array(
        c_elements.size(), c_elements.data(), &error, &result
    );
    check_result(ok, error);
    return _Value(result);
}

_Value interpret_function(const _Function &fn, std::vector<_Value *> args) {
    char *error = nullptr;
    xls_value *result = nullptr;
    std::vector<const xls_value *> c_args;
    c_args.reserve(args.size());
    for (auto *v : args) {
        if (!v) {
            throw std::runtime_error("Null value pointer in arguments");
        }
        c_args.push_back(v->ptr.get());
    }

    bool ok = xls_interpret_function(
        fn.ptr, c_args.size(), c_args.data(), &error, &result
    );
    check_result(ok, error);
    return _Value(result);
}

_FunctionJit make_function_jit(const _Function &fn) {
    char *error = nullptr;
    xls_function_jit *jit = nullptr;
    bool ok = xls_make_function_jit(fn.ptr, &error, &jit);
    check_result(ok, error);
    return _FunctionJit(jit);
}

_Value
function_jit_run(const _FunctionJit &fn_jit, std::vector<_Value *> args) {
    char *error = nullptr;
    xls_value *result = nullptr;

    std::vector<const xls_value *> c_args;
    c_args.reserve(args.size());
    for (auto *v : args) {
        if (!v) {
            throw std::runtime_error("Null value pointer in args");
        }
        c_args.push_back(v->ptr.get());
    }

    xls_trace_message *trace_msgs = nullptr;
    size_t trace_count = 0;
    char **assert_msgs = nullptr;
    size_t assert_count = 0;

    bool ok = xls_function_jit_run(
        fn_jit.ptr.get(),
        c_args.size(),
        c_args.data(),
        &error,
        &trace_msgs,
        &trace_count,
        &assert_msgs,
        &assert_count,
        &result
    );

    if (trace_msgs != nullptr) {
        if (trace_count > 0) {
            for (size_t i = 0; i < trace_count; ++i) {
                std::cerr << "[Trace] " << trace_msgs[i].message << std::endl;
            }
        }
        xls_trace_messages_free(trace_msgs, trace_count);
    }

    if (assert_msgs != nullptr) {
        if (assert_count > 0) {
            for (size_t i = 0; i < assert_count; ++i) {
                std::cerr << "[Assert] " << assert_msgs[i] << std::endl;
            }
        }
        xls_c_strs_free(assert_msgs, assert_count);
    }

    check_result(ok, error);
    return _Value(result);
}

_Bits make_bits_from_bytes(const nb::bytes &data, size_t bit_count) {
    char *error = nullptr;
    xls_bits *bits = nullptr;
    if (bit_count > data.size() * 8) {
        throw std::runtime_error(
            "Bit count exceeds the number of bits in the provided byte data"
        );
    }
    const uint8_t *bytes = reinterpret_cast<const uint8_t *>(data.data());
    bool ok = xls_bits_make_bits_from_bytes(
        bit_count, bytes, data.size(), &error, &bits
    );
    check_result(ok, error);
    return _Bits(bits);
}

_Value value_from_bits(const _Bits &bits) {
    return _Value(xls_value_from_bits(bits.ptr.get()));
}

template <typename T>
_Value value_from_array(const std::vector<T> &elements, size_t bit_count) {
    if (bit_count == 0) {
        throw std::runtime_error("Bit width must be greater than zero");
    }
    if (bit_count > sizeof(T) * 8) {
        throw std::runtime_error(
            "Bit width exceeds the size of the element type" +
            std::to_string(bit_count) + " > " + std::to_string(sizeof(T) * 8)
        );
    }
    std::vector<xls_value *> c_values(elements.size());
    char *error = nullptr;
    xls_value *result = nullptr;

    for (size_t i = 0; i < elements.size(); ++i) {
        xls_bits *bits = nullptr;
        bool ok = xls_bits_make_bits_from_bytes(
            bit_count,
            reinterpret_cast<const uint8_t *>(&elements[i]),
            sizeof(T),
            &error,
            &bits
        );
        check_result(ok, error);
        c_values[i] = xls_value_from_bits(bits);
        xls_bits_free(bits);
    }
    bool ok =
        xls_value_make_array(c_values.size(), c_values.data(), &error, &result);
    check_result(ok, error);
    for (auto *v : c_values) {
        xls_value_free(v);
    }
    return _Value(result);
}

template <typename T>
std::vector<_Value> values_from_array(
    const std::vector<T> &elements,
    size_t bit_count,
    size_t word_count
) {
    if (bit_count == 0) {
        throw std::runtime_error("Bit width must be greater than zero");
    }
    if (bit_count > sizeof(T) * 8) {
        throw std::runtime_error(
            "Bit width exceeds the size of the element type" +
            std::to_string(bit_count) + " > " + std::to_string(sizeof(T) * 8)
        );
    }
    if (elements.size() % word_count != 0) {
        throw std::runtime_error(
            "Total number of elements must be a multiple of the word count"
        );
    }
    std::vector<_Value> result(elements.size() / word_count);
    for (size_t i = 0; i < result.size(); ++i) {
        std::vector<T> word_elements(
            &elements[i * word_count], &elements[(i + 1) * word_count]
        );
        result[i] = value_from_array(word_elements, bit_count);
    }
    return result;
}

std::vector<int64_t> value_to_array(const _Value &value) {
    char *error = nullptr;
    const xls_value *c_value = value.ptr.get();
    xls_value_kind kind;
    bool ok = xls_value_get_kind(c_value, &error, &kind);
    check_result(ok, error);
    if (kind != xls_value_kind_array) {
        throw std::runtime_error(
            "Expected an array value, got kind: " + std::to_string(kind)
        );
    }
    int64_t element_count;
    ok = xls_value_get_element_count(c_value, &error, &element_count);
    check_result(ok, error);
    std::vector<int64_t> result(element_count);
    for (int64_t i = 0; i < element_count; ++i) {
        xls_value *element = nullptr;
        ok = xls_value_get_element(c_value, i, &error, &element);
        check_result(ok, error);
        xls_bits *bits = nullptr;
        ok = xls_value_get_bits(element, &error, &bits);
        xls_value_free(element);
        check_result(ok, error);
        ok = xls_bits_to_int64(bits, &error, &result[i]);
        xls_bits_free(bits);
        check_result(ok, error);
    }
    return result;
}

std::vector<int64_t> jit_fn_predict(
    const _FunctionJit &fn_jit,
    const std::vector<int64_t> &input,
    size_t bit_count,
    size_t in_word_count,
    size_t out_word_count

) {
    if (input.size() % in_word_count != 0) {
        throw std::runtime_error(
            "Input size must be a multiple of the word count"
        );
    }
    size_t n_samples = input.size() / in_word_count;
    size_t n_output = n_samples * out_word_count;
    std::vector<int64_t> output(n_output);
    for (size_t i = 0; i < n_samples; ++i) {
        std::vector<int64_t> word_input(
            input.begin() + i * in_word_count,
            input.begin() + (i + 1) * in_word_count
        );
        _Value input_value = value_from_array(word_input, bit_count);
        _Value output_value = function_jit_run(fn_jit, {&input_value});
        std::vector<int64_t> output_word = value_to_array(output_value);
        if (output_word.size() != out_word_count) {
            throw std::runtime_error(
                "Expected output word count: " +
                std::to_string(out_word_count) +
                ", got: " + std::to_string(output_word.size())
            );
        }
        std::copy(
            output_word.begin(),
            output_word.end(),
            output.begin() + i * out_word_count
        );
    }
    return output;
}

nb::ndarray<nb::numpy, int64_t> jit_fn_predict_ndarray(
    const _FunctionJit &fn_jit,
    const nb::ndarray<int64_t> &input,
    size_t bit_count,
    size_t in_word_count,
    size_t out_word_count
) {
    size_t n_samples = input.size() / in_word_count;
    if (input.size() % in_word_count != 0) {
        throw std::runtime_error(
            "Input size must be a multiple of the word count"
        );
    }
    std::vector<int64_t> input_vec(input.size());
    std::copy(input.data(), input.data() + input.size(), input_vec.begin());
    std::vector<int64_t> output_vec = jit_fn_predict(
        fn_jit, input_vec, bit_count, in_word_count, out_word_count
    );
    std::vector<size_t> shape = {n_samples, out_word_count};
    // nb::capsule owner(output_vec, [](void *p) noexcept {
    //     delete static_cast<std::vector<int64_t> *>(p);
    // });
    return nb::ndarray<nb::numpy, int64_t>(
        output_vec.data(), shape.size(), shape.data()
    );
}

std::string optimize_ir(const std::string &ir, nb::object top_name_obj) {
    char *error = nullptr;
    char *optimized_ir = nullptr;
    std::string top_name;
    if (top_name_obj.is_none()) {
        // find function/proc denoted prefixed with "top "
        size_t top_pos = ir.find("top ");
        if (top_pos == std::string::npos) {
            throw std::runtime_error(
                "top is not specified and no top module is found in the IR"
            );
        }
        size_t _name_start = top_pos + 4; // length of "top "
        if (ir[_name_start] == 'c') {
            _name_start += 5; // "proc "
        }
        else {
            _name_start += 3; // "fn "
        }
        size_t _name_end = ir.find_first_of(" (", _name_start);
        if (_name_end == std::string::npos) {
            throw std::runtime_error(
                "Failed to parse top module name from IR after 'top ' prefix"
            );
        }
        top_name = ir.substr(_name_start, _name_end - _name_start);
    }
    else {
        top_name = nb::cast<nb::str>(top_name_obj).c_str();
    }

    bool ok =
        xls_optimize_ir(ir.c_str(), top_name.c_str(), &error, &optimized_ir);
    check_result(ok, error);
    std::string result(optimized_ir);
    xls_c_str_free(optimized_ir);
    return result;
}

NB_MODULE(raw, m) {
    // Bind Wrappers
    auto pkg_cls = nb::class_<_Package>(m, "Package");
    auto fn_cls = nb::class_<_Function>(m, "Function");
    auto jit_cls = nb::class_<_FunctionJit>(m, "FunctionJit");
    auto type_cls = nb::class_<_Type>(m, "Type");
    auto val_cls = nb::class_<_Value>(m, "Value");
    auto bits_cls = nb::class_<_Bits>(m, "Bits");
    auto res_cls =
        nb::class_<_ScheduleAndCodegenResult>(m, "ScheduleAndCodegenResult");

    // Default constructors
    pkg_cls.def(nb::init<>());
    fn_cls.def(nb::init<>());
    jit_cls.def(nb::init<>());
    type_cls.def(nb::init<>());
    val_cls.def(nb::init<>());
    bits_cls.def(nb::init<>());
    res_cls.def(nb::init<>());

    // --- Module Functions ---

    m.def(
        "parse_ir_package", &parse_ir_package, "ir"_a, "filename"_a = nb::none()
    );

    m.def(
        "convert_dslx_to_ir",
        &convert_dslx_to_ir,
        "dslx"_a,
        "path"_a,
        "module_name"_a,
        "dslx_stdlib_path"_a,
        "additional_search_paths"_a = std::vector<std::string>()
    );

    m.def("optimize_ir", &optimize_ir, "ir"_a, "top_name"_a = nb::none());

    m.def(
        "mangle_dslx_name", &mangle_dslx_name, "module_name"_a, "function_name"_a
    );

    m.def(
        "package_get_function",
        &package_get_function,
        nb::keep_alive<0, 1>(), // ret keeps pkg alive
        "pkg"_a,
        "name"_a
    );

    m.def("package_to_string", &package_to_string, "pkg"_a);

    m.def("function_get_name", &function_get_name, "fn"_a);

    m.def(
        "function_get_type",
        &function_get_type,
        nb::keep_alive<0, 1>(), // ret keeps fn alive
        "fn"_a
    );

    m.def("parse_typed_value", &parse_typed_value, "inp"_a);

    m.def("value_to_string", &value_to_string, "value"_a);

    m.def("value_make_ubits", &value_make_ubits, "bit_count"_a, "value"_a);

    m.def("value_make_sbits", &value_make_sbits, "bit_count"_a, "value"_a);

    m.def("value_make_array", &value_make_array, "elements"_a);

    m.def("interpret_function", &interpret_function, "fn"_a, "args"_a);

    m.def("make_function_jit", &make_function_jit, "fn"_a);

    m.def("function_jit_run", &function_jit_run, "fn_jit"_a, "args"_a);

    m.def(
        "make_bits_from_bytes", &make_bits_from_bytes, "data"_a, "bit_count"_a
    );

    m.def("value_from_bits", &value_from_bits, "bits"_a);

    m.def("value_from_array", &value_from_array<uint64_t>);
    m.def("value_from_array", &value_from_array<int64_t>);
    m.def("value_from_array", &value_from_array<uint32_t>);
    m.def("value_from_array", &value_from_array<int32_t>);
    m.def("value_from_array", &value_from_array<uint16_t>);
    m.def("value_from_array", &value_from_array<int16_t>);
    m.def("value_from_array", &value_from_array<uint8_t>);
    m.def("value_from_array", &value_from_array<int8_t>);

    m.def("values_from_array", &values_from_array<uint64_t>);
    m.def("values_from_array", &values_from_array<int64_t>);
    m.def("values_from_array", &values_from_array<uint32_t>);
    m.def("values_from_array", &values_from_array<int32_t>);
    m.def("values_from_array", &values_from_array<uint16_t>);
    m.def("values_from_array", &values_from_array<int16_t>);
    m.def("values_from_array", &values_from_array<uint8_t>);
    m.def("values_from_array", &values_from_array<int8_t>);

    m.def("value_to_array", &value_to_array, "value"_a);

    m.def(
        "jit_fn_predict",
        &jit_fn_predict_ndarray,
        "fn_jit"_a,
        "input"_a,
        "bit_count"_a,
        "in_word_count"_a,
        "out_word_count"_a
    );
}

// // --- Package Methods as Functions ---

// // --- Function Methods as Functions ---
