#include "_types.h"
#include "_helpers.h"
#include "_c_api.h"
#include "_ir_builder.h"
#include "_dslx.h"
#include "_vast.h"
#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>
#include <nanobind/stl/pair.h>
#include <iostream>

namespace nb = nanobind;
using namespace nb::literals;

template <typename T>
_Value value_from_array(const std::vector<T> &elements, size_t bit_count) {
    if (bit_count == 0)
        throw std::runtime_error("Bit width must be greater than zero");
    if (bit_count > sizeof(T) * 8)
        throw std::runtime_error(
            "Bit width exceeds the size of the element type: " +
            std::to_string(bit_count) + " > " + std::to_string(sizeof(T) * 8)
        );
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
    for (auto *v : c_values)
        xls_value_free(v);
    return _Value(result);
}

template <typename T>
std::vector<_Value> values_from_array(
    const std::vector<T> &elements,
    size_t bit_count,
    size_t word_count
) {
    if (bit_count == 0)
        throw std::runtime_error("Bit width must be greater than zero");
    if (bit_count > sizeof(T) * 8)
        throw std::runtime_error(
            "Bit width exceeds the size of the element type: " +
            std::to_string(bit_count) + " > " + std::to_string(sizeof(T) * 8)
        );
    if (elements.size() % word_count != 0)
        throw std::runtime_error(
            "Total number of elements must be a multiple of the word count"
        );
    std::vector<_Value> result(elements.size() / word_count);
    for (size_t i = 0; i < result.size(); ++i) {
        std::vector<T> word_elements(
            &elements[i * word_count], &elements[(i + 1) * word_count]
        );
        result[i] = value_from_array(word_elements, bit_count);
    }
    return result;
}

static std::vector<int64_t> value_to_array_impl(const _Value &value) {
    char *error = nullptr;
    const xls_value *c_value = value.ptr.get();
    xls_value_kind kind;
    bool ok = xls_value_get_kind(c_value, &error, &kind);
    check_result(ok, error);
    if (kind != xls_value_kind_array)
        throw std::runtime_error(
            "Expected an array value, got kind: " + std::to_string(kind)
        );
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

static _Value
function_jit_run_impl(const _FunctionJit &fn_jit, std::vector<_Value *> args) {
    char *error = nullptr;
    xls_value *result = nullptr;
    std::vector<const xls_value *> c_args;
    c_args.reserve(args.size());
    for (auto *v : args) {
        if (!v)
            throw std::runtime_error("Null value pointer in args");
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
    if (trace_msgs) {
        for (size_t i = 0; i < trace_count; ++i)
            std::cerr << "[Trace] " << trace_msgs[i].message << std::endl;
        xls_trace_messages_free(trace_msgs, trace_count);
    }
    if (assert_msgs) {
        for (size_t i = 0; i < assert_count; ++i)
            std::cerr << "[Assert] " << assert_msgs[i] << std::endl;
        xls_c_strs_free(assert_msgs, assert_count);
    }
    check_result(ok, error);
    return _Value(result);
}

static std::vector<int64_t> jit_fn_predict_impl(
    const _FunctionJit &fn_jit,
    const std::vector<int64_t> &input,
    size_t in_bit_count,
    size_t in_word_count,
    size_t out_word_count
) {
    if (input.size() % in_word_count != 0)
        throw std::runtime_error(
            "Input size must be a multiple of the word count"
        );
    size_t n_samples = input.size() / in_word_count;
    size_t n_output = n_samples * out_word_count;
    std::vector<int64_t> output(n_output);
    for (size_t i = 0; i < n_samples; ++i) {
        std::vector<int64_t> word_input(
            input.begin() + i * in_word_count,
            input.begin() + (i + 1) * in_word_count
        );
        _Value input_value = value_from_array(word_input, in_bit_count);
        _Value output_value = function_jit_run_impl(fn_jit, {&input_value});
        std::vector<int64_t> output_word = value_to_array_impl(output_value);
        if (output_word.size() != out_word_count)
            throw std::runtime_error(
                "Expected output word count: " +
                std::to_string(out_word_count) +
                ", got: " + std::to_string(output_word.size())
            );
        std::copy(
            output_word.begin(),
            output_word.end(),
            output.begin() + i * out_word_count
        );
    }
    return output;
}

static nb::ndarray<nb::numpy, int64_t> jit_fn_predict_ndarray(
    const _FunctionJit &fn_jit,
    const nb::ndarray<int64_t> &input,
    size_t in_bit_count,
    size_t in_word_count,
    size_t out_word_count
) {
    size_t n_samples = input.size() / in_word_count;
    if (input.size() % in_word_count != 0)
        throw std::runtime_error(
            "Input size must be a multiple of the word count"
        );
    std::vector<int64_t> input_vec(input.size());
    std::copy(input.data(), input.data() + input.size(), input_vec.begin());
    auto *output_vec = new std::vector<int64_t>(jit_fn_predict_impl(
        fn_jit, input_vec, in_bit_count, in_word_count, out_word_count
    ));
    size_t shape[] = {n_samples, out_word_count};
    nb::capsule owner(output_vec, [](void *p) noexcept {
        delete static_cast<std::vector<int64_t> *>(p);
    });
    return nb::ndarray<nb::numpy, int64_t>(output_vec->data(), 2, shape, owner);
}

// ============================================================
// Module definition
// ============================================================
NB_MODULE(raw, m) {
    // --- Register all wrapper types at top-level module ---
    // c_api types
    nb::class_<_Package>(m, "Package").def(nb::init<>());
    nb::class_<_FunctionBase>(m, "FunctionBase").def(nb::init<>());
    nb::class_<_Function>(m, "Function").def(nb::init<>());
    nb::class_<_FunctionType>(m, "FunctionType").def(nb::init<>());
    nb::class_<_FunctionJit>(m, "FunctionJit").def(nb::init<>());
    nb::class_<_Type>(m, "Type").def(nb::init<>());
    nb::class_<_Value>(m, "Value").def(nb::init<>());
    nb::class_<_Bits>(m, "Bits").def(nb::init<>());
    nb::class_<_BitsRope>(m, "BitsRope").def(nb::init<>());
    nb::class_<_ScheduleAndCodegenResult>(m, "ScheduleAndCodegenResult")
        .def(nb::init<>());

    // ir_builder types
    nb::class_<_FunctionBuilder>(m, "FunctionBuilder").def(nb::init<>());
    nb::class_<_BuilderBase>(m, "BuilderBase").def(nb::init<>());
    nb::class_<_BValue>(m, "BValue").def(nb::init<>());

    // dslx types
    nb::class_<_DslxTypecheckedModule>(m, "DslxTypecheckedModule")
        .def(nb::init<>());
    nb::class_<_DslxImportData>(m, "DslxImportData").def(nb::init<>());
    nb::class_<_DslxModule>(m, "DslxModule").def(nb::init<>());
    nb::class_<_DslxTypeDefinition>(m, "DslxTypeDefinition").def(nb::init<>());
    nb::class_<_DslxStructDef>(m, "DslxStructDef").def(nb::init<>());
    nb::class_<_DslxEnumDef>(m, "DslxEnumDef").def(nb::init<>());
    nb::class_<_DslxTypeAlias>(m, "DslxTypeAlias").def(nb::init<>());
    nb::class_<_DslxTypeInfo>(m, "DslxTypeInfo").def(nb::init<>());
    nb::class_<_DslxType>(m, "DslxType").def(nb::init<>());
    nb::class_<_DslxTypeAnnotation>(m, "DslxTypeAnnotation").def(nb::init<>());
    nb::class_<_DslxConstantDef>(m, "DslxConstantDef").def(nb::init<>());
    nb::class_<_DslxFunction>(m, "DslxFunction").def(nb::init<>());
    nb::class_<_DslxQuickcheck>(m, "DslxQuickcheck").def(nb::init<>());
    nb::class_<_DslxParam>(m, "DslxParam").def(nb::init<>());
    nb::class_<_DslxParametricBinding>(m, "DslxParametricBinding")
        .def(nb::init<>());
    nb::class_<_DslxExpr>(m, "DslxExpr").def(nb::init<>());
    nb::class_<_DslxInvocation>(m, "DslxInvocation").def(nb::init<>());
    nb::class_<_DslxInvocationCalleeDataArray>(
        m, "DslxInvocationCalleeDataArray"
    )
        .def(nb::init<>());
    nb::class_<_DslxInvocationCalleeData>( // NOLINT(bugprone-unused-raii)
        m, "DslxInvocationCalleeData"
    );
    nb::class_<_DslxInvocationData>(m, "DslxInvocationData").def(nb::init<>());
    nb::class_<_DslxModuleMember>(m, "DslxModuleMember").def(nb::init<>());
    nb::class_<_DslxTypeDim>(m, "DslxTypeDim").def(nb::init<>());
    nb::class_<_DslxParametricEnv>(m, "DslxParametricEnv").def(nb::init<>());
    nb::class_<_DslxParametricEnvBorrowed>(m, "DslxParametricEnvBorrowed")
        .def(nb::init<>());
    nb::class_<_DslxInterpValue>(m, "DslxInterpValue").def(nb::init<>());
    nb::class_<_DslxCallGraph>(m, "DslxCallGraph").def(nb::init<>());
    nb::class_<_DslxAttribute>(m, "DslxAttribute").def(nb::init<>());
    nb::class_<_DslxStructMember>(m, "DslxStructMember").def(nb::init<>());
    nb::class_<_DslxEnumMember>(m, "DslxEnumMember").def(nb::init<>());
    nb::class_<_DslxTypeRefTypeAnnotation>(m, "DslxTypeRefTypeAnnotation")
        .def(nb::init<>());
    nb::class_<_DslxTypeRef>(m, "DslxTypeRef").def(nb::init<>());
    nb::class_<_DslxColonRef>(m, "DslxColonRef").def(nb::init<>());
    nb::class_<_DslxImport>(m, "DslxImport").def(nb::init<>());

    // vast types
    nb::class_<_VastVerilogFile>(m, "VastVerilogFile").def(nb::init<>());
    nb::class_<_VastVerilogModule>(m, "VastVerilogModule").def(nb::init<>());
    nb::class_<_VastExpression>(m, "VastExpression").def(nb::init<>());
    nb::class_<_VastLogicRef>(m, "VastLogicRef").def(nb::init<>());
    nb::class_<_VastDataType>(m, "VastDataType").def(nb::init<>());
    nb::class_<_VastIndexableExpression>(m, "VastIndexableExpression")
        .def(nb::init<>());
    nb::class_<_VastSlice>(m, "VastSlice").def(nb::init<>());
    nb::class_<_VastLiteral>(m, "VastLiteral").def(nb::init<>());
    nb::class_<_VastInstantiation>(m, "VastInstantiation").def(nb::init<>());
    nb::class_<_VastContinuousAssignment>(m, "VastContinuousAssignment")
        .def(nb::init<>());
    nb::class_<_VastComment>(m, "VastComment").def(nb::init<>());
    nb::class_<_VastInlineVerilogStatement>(m, "VastInlineVerilogStatement")
        .def(nb::init<>());
    nb::class_<_VastMacroRef>(m, "VastMacroRef").def(nb::init<>());
    nb::class_<_VastMacroStatement>(m, "VastMacroStatement").def(nb::init<>());
    nb::class_<_VastAlwaysBase>(m, "VastAlwaysBase").def(nb::init<>());
    nb::class_<_VastStatement>(m, "VastStatement").def(nb::init<>());
    nb::class_<_VastStatementBlock>(m, "VastStatementBlock").def(nb::init<>());
    nb::class_<_VastGenerateLoop>(m, "VastGenerateLoop").def(nb::init<>());
    nb::class_<_VastModulePort>(m, "VastModulePort").def(nb::init<>());
    nb::class_<_VastDef>(m, "VastDef").def(nb::init<>());
    nb::class_<_VastParameterRef>(m, "VastParameterRef").def(nb::init<>());
    nb::class_<_VastConditional>(m, "VastConditional").def(nb::init<>());
    nb::class_<_VastCaseStatement>(m, "VastCaseStatement").def(nb::init<>());
    nb::class_<_VastLocalparamRef>(m, "VastLocalparamRef").def(nb::init<>());
    nb::class_<_VastBlankLine>(m, "VastBlankLine").def(nb::init<>());
    nb::class_<_VastConcat>(m, "VastConcat").def(nb::init<>());
    nb::class_<_VastIndex>(m, "VastIndex").def(nb::init<>());

    // --- Create submodules ---
    auto c_api_m = m.def_submodule("c_api", "XLS C API bindings");
    auto ir_builder_m =
        m.def_submodule("ir_builder", "XLS IR Builder bindings");
    auto dslx_m = m.def_submodule("dslx", "XLS DSLX bindings");
    auto vast_m = m.def_submodule("vast", "XLS VAST bindings");

    // --- Bind each submodule ---
    bind_c_api(c_api_m);
    bind_ir_builder(ir_builder_m);
    bind_dslx(dslx_m);
    bind_vast(vast_m);

    // --- Batch inference functions (top-level) ---
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

    m.def("value_to_array", &value_to_array_impl, "value"_a);

    m.def(
        "jit_fn_predict",
        &jit_fn_predict_ndarray,
        "fn_jit"_a,
        "input"_a,
        "in_bit_count"_a,
        "in_word_count"_a,
        "out_word_count"_a
    );
}
