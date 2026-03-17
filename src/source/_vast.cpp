#include "_vast.h"
#include "_types.h"
#include "_helpers.h"
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>

using namespace nb::literals;

void bind_vast(nb::module_ &m) {
    // ============================================================
    // Enums
    // ============================================================
    nb::enum_<XlsVastFileType>(m, "FileType")
        .value("VERILOG", XlsVastFileType::VERILOG)
        .value("SYSTEM_VERILOG", XlsVastFileType::SYSTEM_VERILOG)
        .export_values();

    nb::enum_<XlsVastOperatorKind>(m, "OperatorKind")
        .value("NEGATE", XlsVastOperatorKind::NEGATE)
        .value("BITWISE_NOT", XlsVastOperatorKind::BITWISE_NOT)
        .value("LOGICAL_NOT", XlsVastOperatorKind::LOGICAL_NOT)
        .value("AND_REDUCE", XlsVastOperatorKind::AND_REDUCE)
        .value("OR_REDUCE", XlsVastOperatorKind::OR_REDUCE)
        .value("XOR_REDUCE", XlsVastOperatorKind::XOR_REDUCE)
        .value("ADD", XlsVastOperatorKind::ADD)
        .value("LOGICAL_AND", XlsVastOperatorKind::LOGICAL_AND)
        .value("BITWISE_AND", XlsVastOperatorKind::BITWISE_AND)
        .value("NE", XlsVastOperatorKind::NE)
        .value("CASE_NE", XlsVastOperatorKind::CASE_NE)
        .value("EQ", XlsVastOperatorKind::EQ)
        .value("CASE_EQ", XlsVastOperatorKind::CASE_EQ)
        .value("GE", XlsVastOperatorKind::GE)
        .value("GT", XlsVastOperatorKind::GT)
        .value("LE", XlsVastOperatorKind::LE)
        .value("LT", XlsVastOperatorKind::LT)
        .value("DIV", XlsVastOperatorKind::DIV)
        .value("MOD", XlsVastOperatorKind::MOD)
        .value("MUL", XlsVastOperatorKind::MUL)
        .value("POWER", XlsVastOperatorKind::POWER)
        .value("BITWISE_OR", XlsVastOperatorKind::BITWISE_OR)
        .value("LOGICAL_OR", XlsVastOperatorKind::LOGICAL_OR)
        .value("BITWISE_XOR", XlsVastOperatorKind::BITWISE_XOR)
        .value("SHLL", XlsVastOperatorKind::SHLL)
        .value("SHRA", XlsVastOperatorKind::SHRA)
        .value("SHRL", XlsVastOperatorKind::SHRL)
        .value("SUB", XlsVastOperatorKind::SUB)
        .value("NE_X", XlsVastOperatorKind::NE_X)
        .value("EQ_X", XlsVastOperatorKind::EQ_X)
        .export_values();

    nb::enum_<XlsVastModulePortDirection>(m, "ModulePortDirection")
        .value("INPUT", XlsVastModulePortDirection::INPUT)
        .value("OUTPUT", XlsVastModulePortDirection::OUTPUT)
        .value("INOUT", XlsVastModulePortDirection::INOUT)
        .export_values();

    nb::enum_<XlsVastDataKind>(m, "DataKind")
        .value("REG", XlsVastDataKind::REG)
        .value("WIRE", XlsVastDataKind::WIRE)
        .value("LOGIC", XlsVastDataKind::LOGIC)
        .value("INTEGER", XlsVastDataKind::INTEGER)
        .value("INT", XlsVastDataKind::INT)
        .value("USER", XlsVastDataKind::USER)
        .value("UNTYPED_ENUM", XlsVastDataKind::UNTYPED_ENUM)
        .value("GENVAR", XlsVastDataKind::GENVAR)
        .export_values();

    // ============================================================
    // VerilogFile — creation & emit
    // ============================================================
    m.def(
        "xls_vast_make_verilog_file",
        [](XlsVastFileType file_type) -> _VastVerilogFile {
            return _VastVerilogFile(xls_vast_make_verilog_file(
                static_cast<xls_vast_file_type>(file_type)
            ));
        },
        "file_type"_a
    );

    m.def(
        "xls_vast_verilog_file_emit",
        [](const _VastVerilogFile &f) -> std::string {
            return own_c_str(xls_vast_verilog_file_emit(f.ptr.get()));
        },
        "file"_a
    );

    m.def(
        "xls_vast_verilog_file_add_module",
        [](const _VastVerilogFile &f,
           const std::string &name) -> _VastVerilogModule {
            return _VastVerilogModule(
                xls_vast_verilog_file_add_module(f.ptr.get(), name.c_str())
            );
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "name"_a
    );

    // ============================================================
    // VerilogFile — Make*Type
    // ============================================================
    m.def(
        "xls_vast_verilog_file_make_scalar_type",
        [](const _VastVerilogFile &f) -> _VastDataType {
            return _VastDataType(
                xls_vast_verilog_file_make_scalar_type(f.ptr.get())
            );
        },
        nb::keep_alive<0, 1>(),
        "file"_a
    );

    m.def(
        "xls_vast_verilog_file_make_bit_vector_type",
        [](const _VastVerilogFile &f,
           int64_t bit_count,
           bool is_signed) -> _VastDataType {
            return _VastDataType(xls_vast_verilog_file_make_bit_vector_type(
                f.ptr.get(), bit_count, is_signed
            ));
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "bit_count"_a,
        "is_signed"_a = false
    );

    m.def(
        "xls_vast_verilog_file_make_bit_vector_type_with_expression",
        [](const _VastVerilogFile &f,
           const _VastExpression &expr,
           bool is_signed) -> _VastDataType {
            return _VastDataType(
                xls_vast_verilog_file_make_bit_vector_type_with_expression(
                    f.ptr.get(), expr.ptr, is_signed
                )
            );
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "expression"_a,
        "is_signed"_a = false
    );

    m.def(
        "xls_vast_verilog_file_make_integer_type",
        [](const _VastVerilogFile &f, bool is_signed) -> _VastDataType {
            return _VastDataType(
                xls_vast_verilog_file_make_integer_type(f.ptr.get(), is_signed)
            );
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "is_signed"_a = false
    );

    m.def(
        "xls_vast_verilog_file_make_int_type",
        [](const _VastVerilogFile &f, bool is_signed) -> _VastDataType {
            return _VastDataType(
                xls_vast_verilog_file_make_int_type(f.ptr.get(), is_signed)
            );
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "is_signed"_a = false
    );

    m.def(
        "xls_vast_verilog_file_make_integer_def",
        [](const _VastVerilogFile &f,
           const std::string &name,
           bool is_signed) -> _VastDef {
            return _VastDef(xls_vast_verilog_file_make_integer_def(
                f.ptr.get(), name.c_str(), is_signed
            ));
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "name"_a,
        "is_signed"_a = false
    );

    m.def(
        "xls_vast_verilog_file_make_int_def",
        [](const _VastVerilogFile &f,
           const std::string &name,
           bool is_signed) -> _VastDef {
            return _VastDef(xls_vast_verilog_file_make_int_def(
                f.ptr.get(), name.c_str(), is_signed
            ));
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "name"_a,
        "is_signed"_a = false
    );

    m.def(
        "xls_vast_verilog_file_make_extern_package_type",
        [](const _VastVerilogFile &f,
           const std::string &package_name,
           const std::string &entity_name) -> _VastDataType {
            return _VastDataType(xls_vast_verilog_file_make_extern_package_type(
                f.ptr.get(), package_name.c_str(), entity_name.c_str()
            ));
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "package_name"_a,
        "entity_name"_a
    );

    m.def(
        "xls_vast_verilog_file_make_extern_type",
        [](const _VastVerilogFile &f,
           const std::string &entity_name) -> _VastDataType {
            return _VastDataType(xls_vast_verilog_file_make_extern_type(
                f.ptr.get(), entity_name.c_str()
            ));
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "entity_name"_a
    );

    m.def(
        "xls_vast_verilog_file_make_packed_array_type",
        [](const _VastVerilogFile &f,
           const _VastDataType &element_type,
           std::vector<int64_t> packed_dims) -> _VastDataType {
            return _VastDataType(xls_vast_verilog_file_make_packed_array_type(
                f.ptr.get(),
                element_type.ptr,
                packed_dims.data(),
                packed_dims.size()
            ));
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "element_type"_a,
        "packed_dims"_a
    );

    m.def(
        "xls_vast_verilog_file_make_def",
        [](const _VastVerilogFile &f,
           const std::string &name,
           XlsVastDataKind kind,
           const _VastDataType &type) -> _VastDef {
            return _VastDef(xls_vast_verilog_file_make_def(
                f.ptr.get(),
                name.c_str(),
                static_cast<xls_vast_data_kind>(kind),
                type.ptr
            ));
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "name"_a,
        "kind"_a,
        "type"_a
    );

    // ============================================================
    // VerilogFile — Make expressions/literals
    // ============================================================
    m.def(
        "xls_vast_verilog_file_make_plain_literal",
        [](const _VastVerilogFile &f, int32_t value) -> _VastLiteral {
            return _VastLiteral(
                xls_vast_verilog_file_make_plain_literal(f.ptr.get(), value)
            );
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "value"_a
    );

    m.def(
        "xls_vast_verilog_file_make_literal",
        [](const _VastVerilogFile &f,
           const _Bits &bits,
           XlsFormatPreference format_preference,
           bool emit_bit_count) -> _VastLiteral {
            char *error = nullptr;
            xls_vast_literal *lit = nullptr;
            bool ok = xls_vast_verilog_file_make_literal(
                f.ptr.get(),
                bits.ptr.get(),
                static_cast<xls_format_preference>(format_preference),
                emit_bit_count,
                &error,
                &lit
            );
            check_result(ok, error);
            return _VastLiteral(lit);
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "bits"_a,
        "format_preference"_a,
        "emit_bit_count"_a = true
    );

    m.def(
        "xls_vast_verilog_file_make_unsized_one_literal",
        [](const _VastVerilogFile &f) -> _VastExpression {
            return _VastExpression(
                xls_vast_verilog_file_make_unsized_one_literal(f.ptr.get())
            );
        },
        nb::keep_alive<0, 1>(),
        "file"_a
    );

    m.def(
        "xls_vast_verilog_file_make_unsized_zero_literal",
        [](const _VastVerilogFile &f) -> _VastExpression {
            return _VastExpression(
                xls_vast_verilog_file_make_unsized_zero_literal(f.ptr.get())
            );
        },
        nb::keep_alive<0, 1>(),
        "file"_a
    );

    m.def(
        "xls_vast_verilog_file_make_unsized_x_literal",
        [](const _VastVerilogFile &f) -> _VastExpression {
            return _VastExpression(
                xls_vast_verilog_file_make_unsized_x_literal(f.ptr.get())
            );
        },
        nb::keep_alive<0, 1>(),
        "file"_a
    );

    // ============================================================
    // VerilogFile — Make operators
    // ============================================================
    m.def(
        "xls_vast_verilog_file_make_unary",
        [](const _VastVerilogFile &f,
           const _VastExpression &arg,
           XlsVastOperatorKind op) -> _VastExpression {
            return _VastExpression(xls_vast_verilog_file_make_unary(
                f.ptr.get(), arg.ptr, static_cast<xls_vast_operator_kind>(op)
            ));
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "arg"_a,
        "op"_a
    );

    m.def(
        "xls_vast_verilog_file_make_binary",
        [](const _VastVerilogFile &f,
           const _VastExpression &lhs,
           const _VastExpression &rhs,
           XlsVastOperatorKind op) -> _VastExpression {
            return _VastExpression(xls_vast_verilog_file_make_binary(
                f.ptr.get(),
                lhs.ptr,
                rhs.ptr,
                static_cast<xls_vast_operator_kind>(op)
            ));
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "lhs"_a,
        "rhs"_a,
        "op"_a
    );

    m.def(
        "xls_vast_verilog_file_make_ternary",
        [](const _VastVerilogFile &f,
           const _VastExpression &cond,
           const _VastExpression &consequent,
           const _VastExpression &alternate) -> _VastExpression {
            return _VastExpression(xls_vast_verilog_file_make_ternary(
                f.ptr.get(), cond.ptr, consequent.ptr, alternate.ptr
            ));
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "cond"_a,
        "consequent"_a,
        "alternate"_a
    );

    m.def(
        "xls_vast_verilog_file_make_width_cast",
        [](const _VastVerilogFile &f,
           const _VastExpression &width,
           const _VastExpression &value) -> _VastExpression {
            return _VastExpression(xls_vast_verilog_file_make_width_cast(
                f.ptr.get(), width.ptr, value.ptr
            ));
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "width"_a,
        "value"_a
    );

    m.def(
        "xls_vast_verilog_file_make_type_cast",
        [](const _VastVerilogFile &f,
           const _VastDataType &type,
           const _VastExpression &value) -> _VastExpression {
            return _VastExpression(xls_vast_verilog_file_make_type_cast(
                f.ptr.get(), type.ptr, value.ptr
            ));
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "type"_a,
        "value"_a
    );

    // ============================================================
    // VerilogFile — Index/Slice
    // ============================================================
    m.def(
        "xls_vast_verilog_file_make_index_i64",
        [](const _VastVerilogFile &f,
           const _VastIndexableExpression &subject,
           int64_t index) -> _VastIndex {
            return _VastIndex(xls_vast_verilog_file_make_index_i64(
                f.ptr.get(), subject.ptr, index
            ));
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "subject"_a,
        "index"_a
    );

    m.def(
        "xls_vast_verilog_file_make_index",
        [](const _VastVerilogFile &f,
           const _VastIndexableExpression &subject,
           const _VastExpression &index) -> _VastIndex {
            return _VastIndex(xls_vast_verilog_file_make_index(
                f.ptr.get(), subject.ptr, index.ptr
            ));
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "subject"_a,
        "index"_a
    );

    m.def(
        "xls_vast_verilog_file_make_slice_i64",
        [](const _VastVerilogFile &f,
           const _VastIndexableExpression &subject,
           int64_t hi,
           int64_t lo) -> _VastSlice {
            return _VastSlice(xls_vast_verilog_file_make_slice_i64(
                f.ptr.get(), subject.ptr, hi, lo
            ));
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "subject"_a,
        "hi"_a,
        "lo"_a
    );

    m.def(
        "xls_vast_verilog_file_make_slice",
        [](const _VastVerilogFile &f,
           const _VastIndexableExpression &subject,
           const _VastExpression &hi,
           const _VastExpression &lo) -> _VastSlice {
            return _VastSlice(xls_vast_verilog_file_make_slice(
                f.ptr.get(), subject.ptr, hi.ptr, lo.ptr
            ));
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "subject"_a,
        "hi"_a,
        "lo"_a
    );

    // ============================================================
    // VerilogFile — Concat
    // ============================================================
    m.def(
        "xls_vast_verilog_file_make_concat",
        [](const _VastVerilogFile &f,
           std::vector<_VastExpression *> elements) -> _VastConcat {
            std::vector<xls_vast_expression *> c_elems;
            for (auto *e : elements)
                c_elems.push_back(e->ptr);
            return _VastConcat(xls_vast_verilog_file_make_concat(
                f.ptr.get(), c_elems.data(), c_elems.size()
            ));
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "elements"_a
    );

    m.def(
        "xls_vast_verilog_file_make_replicated_concat",
        [](const _VastVerilogFile &f,
           const _VastExpression &replication,
           std::vector<_VastExpression *> elements) -> _VastConcat {
            std::vector<xls_vast_expression *> c_elems;
            for (auto *e : elements)
                c_elems.push_back(e->ptr);
            return _VastConcat(xls_vast_verilog_file_make_replicated_concat(
                f.ptr.get(), replication.ptr, c_elems.data(), c_elems.size()
            ));
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "replication"_a,
        "elements"_a
    );

    m.def(
        "xls_vast_verilog_file_make_replicated_concat_i64",
        [](const _VastVerilogFile &f,
           int64_t replication_count,
           std::vector<_VastExpression *> elements) -> _VastConcat {
            std::vector<xls_vast_expression *> c_elems;
            for (auto *e : elements)
                c_elems.push_back(e->ptr);
            return _VastConcat(xls_vast_verilog_file_make_replicated_concat_i64(
                f.ptr.get(), replication_count, c_elems.data(), c_elems.size()
            ));
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "replication_count"_a,
        "elements"_a
    );

    // ============================================================
    // VerilogFile — Assignments
    // ============================================================
    m.def(
        "xls_vast_verilog_file_make_continuous_assignment",
        [](const _VastVerilogFile &f,
           const _VastExpression &lhs,
           const _VastExpression &rhs) -> _VastContinuousAssignment {
            return _VastContinuousAssignment(
                xls_vast_verilog_file_make_continuous_assignment(
                    f.ptr.get(), lhs.ptr, rhs.ptr
                )
            );
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "lhs"_a,
        "rhs"_a
    );

    m.def(
        "xls_vast_verilog_file_make_nonblocking_assignment",
        [](const _VastVerilogFile &f,
           const _VastExpression &lhs,
           const _VastExpression &rhs) -> _VastStatement {
            return _VastStatement(
                xls_vast_verilog_file_make_nonblocking_assignment(
                    f.ptr.get(), lhs.ptr, rhs.ptr
                )
            );
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "lhs"_a,
        "rhs"_a
    );

    m.def(
        "xls_vast_verilog_file_make_blocking_assignment",
        [](const _VastVerilogFile &f,
           const _VastExpression &lhs,
           const _VastExpression &rhs) -> _VastStatement {
            return _VastStatement(
                xls_vast_verilog_file_make_blocking_assignment(
                    f.ptr.get(), lhs.ptr, rhs.ptr
                )
            );
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "lhs"_a,
        "rhs"_a
    );

    // ============================================================
    // VerilogFile — Comments, blank lines, inline statements
    // ============================================================
    m.def(
        "xls_vast_verilog_file_make_comment",
        [](const _VastVerilogFile &f, const std::string &text) -> _VastComment {
            return _VastComment(
                xls_vast_verilog_file_make_comment(f.ptr.get(), text.c_str())
            );
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "text"_a
    );

    m.def(
        "xls_vast_verilog_file_make_blank_line",
        [](const _VastVerilogFile &f) -> _VastBlankLine {
            return _VastBlankLine(
                xls_vast_verilog_file_make_blank_line(f.ptr.get())
            );
        },
        nb::keep_alive<0, 1>(),
        "file"_a
    );

    m.def(
        "xls_vast_verilog_file_make_inline_verilog_statement",
        [](const _VastVerilogFile &f,
           const std::string &text) -> _VastInlineVerilogStatement {
            return _VastInlineVerilogStatement(
                xls_vast_verilog_file_make_inline_verilog_statement(
                    f.ptr.get(), text.c_str()
                )
            );
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "text"_a
    );

    m.def(
        "xls_vast_verilog_file_add_include",
        [](const _VastVerilogFile &f, const std::string &path) {
            xls_vast_verilog_file_add_include(f.ptr.get(), path.c_str());
        },
        "file"_a,
        "path"_a
    );

    m.def(
        "xls_vast_verilog_file_add_blank_line",
        [](const _VastVerilogFile &f) {
            xls_vast_verilog_file_add_blank_line(f.ptr.get());
        },
        "file"_a
    );

    m.def(
        "xls_vast_verilog_file_add_comment",
        [](const _VastVerilogFile &f, const std::string &text) {
            xls_vast_verilog_file_add_comment(f.ptr.get(), text.c_str());
        },
        "file"_a,
        "text"_a
    );

    // ============================================================
    // VerilogFile — Macro
    // ============================================================
    m.def(
        "xls_vast_verilog_file_make_macro_ref",
        [](const _VastVerilogFile &f,
           const std::string &name) -> _VastMacroRef {
            return _VastMacroRef(
                xls_vast_verilog_file_make_macro_ref(f.ptr.get(), name.c_str())
            );
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "name"_a
    );

    m.def(
        "xls_vast_verilog_file_make_macro_ref_with_args",
        [](const _VastVerilogFile &f,
           const std::string &name,
           std::vector<_VastExpression *> args) -> _VastMacroRef {
            std::vector<xls_vast_expression *> c_args;
            for (auto *a : args)
                c_args.push_back(a->ptr);
            return _VastMacroRef(xls_vast_verilog_file_make_macro_ref_with_args(
                f.ptr.get(), name.c_str(), c_args.data(), c_args.size()
            ));
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "name"_a,
        "args"_a
    );

    m.def(
        "xls_vast_verilog_file_make_macro_statement",
        [](const _VastVerilogFile &f,
           const _VastMacroRef &ref,
           bool emit_semicolon) -> _VastMacroStatement {
            return _VastMacroStatement(
                xls_vast_verilog_file_make_macro_statement(
                    f.ptr.get(), ref.ptr, emit_semicolon
                )
            );
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "macro_ref"_a,
        "emit_semicolon"_a = true
    );

    // ============================================================
    // VerilogFile — Instantiation
    // ============================================================
    m.def(
        "xls_vast_verilog_file_make_instantiation",
        [](const _VastVerilogFile &f,
           const std::string &module_name,
           const std::string &instance_name,
           std::vector<std::string> param_port_names,
           std::vector<_VastExpression *> param_expressions,
           std::vector<std::string> conn_port_names,
           std::vector<_VastExpression *> conn_expressions)
            -> _VastInstantiation {
            std::vector<const char *> c_ppn, c_cpn;
            for (auto &s : param_port_names)
                c_ppn.push_back(s.c_str());
            for (auto &s : conn_port_names)
                c_cpn.push_back(s.c_str());
            std::vector<xls_vast_expression *> c_pe, c_ce;
            for (auto *e : param_expressions)
                c_pe.push_back(e->ptr);
            for (auto *e : conn_expressions)
                c_ce.push_back(e->ptr);
            return _VastInstantiation(xls_vast_verilog_file_make_instantiation(
                f.ptr.get(),
                module_name.c_str(),
                instance_name.c_str(),
                c_ppn.data(),
                c_pe.data(),
                c_ppn.size(),
                c_cpn.data(),
                c_ce.data(),
                c_cpn.size()
            ));
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "module_name"_a,
        "instance_name"_a,
        "parameter_port_names"_a = std::vector<std::string>(),
        "parameter_expressions"_a = std::vector<_VastExpression *>(),
        "connection_port_names"_a = std::vector<std::string>(),
        "connection_expressions"_a = std::vector<_VastExpression *>()
    );

    // ============================================================
    // VerilogFile — PosEdge
    // ============================================================
    m.def(
        "xls_vast_verilog_file_make_pos_edge",
        [](const _VastVerilogFile &f,
           const _VastExpression &signal) -> _VastExpression {
            return _VastExpression(
                xls_vast_verilog_file_make_pos_edge(f.ptr.get(), signal.ptr)
            );
        },
        nb::keep_alive<0, 1>(),
        "file"_a,
        "signal"_a
    );

    // ============================================================
    // VerilogModule — ports
    // ============================================================
    m.def(
        "xls_vast_verilog_module_add_input",
        [](const _VastVerilogModule &mod,
           const std::string &name,
           const _VastDataType &type) -> _VastLogicRef {
            return _VastLogicRef(xls_vast_verilog_module_add_input(
                mod.ptr, name.c_str(), type.ptr
            ));
        },
        nb::keep_alive<0, 1>(),
        "module"_a,
        "name"_a,
        "type"_a
    );

    m.def(
        "xls_vast_verilog_module_add_output",
        [](const _VastVerilogModule &mod,
           const std::string &name,
           const _VastDataType &type) -> _VastLogicRef {
            return _VastLogicRef(xls_vast_verilog_module_add_output(
                mod.ptr, name.c_str(), type.ptr
            ));
        },
        nb::keep_alive<0, 1>(),
        "module"_a,
        "name"_a,
        "type"_a
    );

    m.def(
        "xls_vast_verilog_module_add_logic_input",
        [](const _VastVerilogModule &mod,
           const std::string &name,
           const _VastDataType &type) -> _VastLogicRef {
            return _VastLogicRef(xls_vast_verilog_module_add_logic_input(
                mod.ptr, name.c_str(), type.ptr
            ));
        },
        nb::keep_alive<0, 1>(),
        "module"_a,
        "name"_a,
        "type"_a
    );

    m.def(
        "xls_vast_verilog_module_add_logic_output",
        [](const _VastVerilogModule &mod,
           const std::string &name,
           const _VastDataType &type) -> _VastLogicRef {
            return _VastLogicRef(xls_vast_verilog_module_add_logic_output(
                mod.ptr, name.c_str(), type.ptr
            ));
        },
        nb::keep_alive<0, 1>(),
        "module"_a,
        "name"_a,
        "type"_a
    );

    m.def(
        "xls_vast_verilog_module_add_wire",
        [](const _VastVerilogModule &mod,
           const std::string &name,
           const _VastDataType &type) -> _VastLogicRef {
            return _VastLogicRef(xls_vast_verilog_module_add_wire(
                mod.ptr, name.c_str(), type.ptr
            ));
        },
        nb::keep_alive<0, 1>(),
        "module"_a,
        "name"_a,
        "type"_a
    );

    m.def(
        "xls_vast_verilog_module_add_inout",
        [](const _VastVerilogModule &mod,
           const std::string &name,
           const _VastDataType &type) -> _VastLogicRef {
            return _VastLogicRef(xls_vast_verilog_module_add_inout(
                mod.ptr, name.c_str(), type.ptr
            ));
        },
        nb::keep_alive<0, 1>(),
        "module"_a,
        "name"_a,
        "type"_a
    );

    m.def(
        "xls_vast_verilog_module_add_reg",
        [](const _VastVerilogModule &mod,
           const std::string &name,
           const _VastDataType &type) -> _VastLogicRef {
            char *error = nullptr;
            xls_vast_logic_ref *ref = nullptr;
            bool ok = xls_vast_verilog_module_add_reg(
                mod.ptr, name.c_str(), type.ptr, &ref, &error
            );
            check_result(ok, error);
            return _VastLogicRef(ref);
        },
        nb::keep_alive<0, 1>(),
        "module"_a,
        "name"_a,
        "type"_a
    );

    m.def(
        "xls_vast_verilog_module_add_logic",
        [](const _VastVerilogModule &mod,
           const std::string &name,
           const _VastDataType &type) -> _VastLogicRef {
            char *error = nullptr;
            xls_vast_logic_ref *ref = nullptr;
            bool ok = xls_vast_verilog_module_add_logic(
                mod.ptr, name.c_str(), type.ptr, &ref, &error
            );
            check_result(ok, error);
            return _VastLogicRef(ref);
        },
        nb::keep_alive<0, 1>(),
        "module"_a,
        "name"_a,
        "type"_a
    );

    // ============================================================
    // VerilogModule — parameters
    // ============================================================
    m.def(
        "xls_vast_verilog_module_add_parameter",
        [](const _VastVerilogModule &mod,
           const std::string &name,
           const _VastExpression &rhs) -> _VastParameterRef {
            return _VastParameterRef(xls_vast_verilog_module_add_parameter(
                mod.ptr, name.c_str(), rhs.ptr
            ));
        },
        nb::keep_alive<0, 1>(),
        "module"_a,
        "name"_a,
        "rhs"_a
    );

    m.def(
        "xls_vast_verilog_module_add_localparam",
        [](const _VastVerilogModule &mod,
           const std::string &name,
           const _VastExpression &rhs) -> _VastLocalparamRef {
            return _VastLocalparamRef(xls_vast_verilog_module_add_localparam(
                mod.ptr, name.c_str(), rhs.ptr
            ));
        },
        nb::keep_alive<0, 1>(),
        "module"_a,
        "name"_a,
        "rhs"_a
    );

    m.def(
        "xls_vast_verilog_module_add_parameter_port",
        [](const _VastVerilogModule &mod,
           const std::string &name,
           const _VastExpression &rhs) -> _VastExpression {
            return _VastExpression(xls_vast_verilog_module_add_parameter_port(
                mod.ptr, name.c_str(), rhs.ptr
            ));
        },
        nb::keep_alive<0, 1>(),
        "module"_a,
        "name"_a,
        "rhs"_a
    );

    m.def(
        "xls_vast_verilog_module_add_typed_parameter_port",
        [](const _VastVerilogModule &mod,
           const std::string &name,
           const _VastDataType &type,
           const _VastExpression &rhs) -> _VastExpression {
            return _VastExpression(
                xls_vast_verilog_module_add_typed_parameter_port(
                    mod.ptr, name.c_str(), type.ptr, rhs.ptr
                )
            );
        },
        nb::keep_alive<0, 1>(),
        "module"_a,
        "name"_a,
        "type"_a,
        "rhs"_a
    );

    m.def(
        "xls_vast_verilog_module_add_parameter_with_def",
        [](const _VastVerilogModule &mod,
           const _VastDef &def,
           const _VastExpression &rhs) -> _VastParameterRef {
            return _VastParameterRef(
                xls_vast_verilog_module_add_parameter_with_def(
                    mod.ptr, def.ptr, rhs.ptr
                )
            );
        },
        nb::keep_alive<0, 1>(),
        "module"_a,
        "_def"_a,
        "rhs"_a
    );

    m.def(
        "xls_vast_verilog_module_add_localparam_with_def",
        [](const _VastVerilogModule &mod,
           const _VastDef &def,
           const _VastExpression &rhs) -> _VastLocalparamRef {
            return _VastLocalparamRef(
                xls_vast_verilog_module_add_localparam_with_def(
                    mod.ptr, def.ptr, rhs.ptr
                )
            );
        },
        nb::keep_alive<0, 1>(),
        "module"_a,
        "_def"_a,
        "rhs"_a
    );

    // ============================================================
    // VerilogModule — members
    // ============================================================
    m.def(
        "xls_vast_verilog_module_add_member_instantiation",
        [](const _VastVerilogModule &mod, const _VastInstantiation &inst) {
            xls_vast_verilog_module_add_member_instantiation(mod.ptr, inst.ptr);
        },
        "module"_a,
        "instantiation"_a
    );

    m.def(
        "xls_vast_verilog_module_add_member_continuous_assignment",
        [](const _VastVerilogModule &mod,
           const _VastContinuousAssignment &assign) {
            xls_vast_verilog_module_add_member_continuous_assignment(
                mod.ptr, assign.ptr
            );
        },
        "module"_a,
        "assignment"_a
    );

    m.def(
        "xls_vast_verilog_module_add_member_comment",
        [](const _VastVerilogModule &mod, const _VastComment &comment) {
            xls_vast_verilog_module_add_member_comment(mod.ptr, comment.ptr);
        },
        "module"_a,
        "comment"_a
    );

    m.def(
        "xls_vast_verilog_module_add_member_blank_line",
        [](const _VastVerilogModule &mod, const _VastBlankLine &blank) {
            xls_vast_verilog_module_add_member_blank_line(mod.ptr, blank.ptr);
        },
        "module"_a,
        "blank_line"_a
    );

    m.def(
        "xls_vast_verilog_module_add_member_inline_statement",
        [](const _VastVerilogModule &mod,
           const _VastInlineVerilogStatement &stmt) {
            xls_vast_verilog_module_add_member_inline_statement(
                mod.ptr, stmt.ptr
            );
        },
        "module"_a,
        "statement"_a
    );

    m.def(
        "xls_vast_verilog_module_add_member_macro_statement",
        [](const _VastVerilogModule &mod, const _VastMacroStatement &stmt) {
            xls_vast_verilog_module_add_member_macro_statement(
                mod.ptr, stmt.ptr
            );
        },
        "module"_a,
        "statement"_a
    );

    // ============================================================
    // VerilogModule — generate loop
    // ============================================================
    m.def(
        "xls_vast_verilog_module_add_generate_loop",
        [](const _VastVerilogModule &mod,
           const std::string &genvar_name,
           const _VastExpression &init,
           const _VastExpression &limit,
           const std::string &label) -> _VastGenerateLoop {
            return _VastGenerateLoop(xls_vast_verilog_module_add_generate_loop(
                mod.ptr, genvar_name.c_str(), init.ptr, limit.ptr, label.c_str()
            ));
        },
        nb::keep_alive<0, 1>(),
        "module"_a,
        "genvar_name"_a,
        "init"_a,
        "limit"_a,
        "label"_a
    );

    // ============================================================
    // VerilogModule — always blocks
    // ============================================================
    m.def(
        "xls_vast_verilog_module_add_always_ff",
        [](const _VastVerilogModule &mod,
           std::vector<_VastExpression *> sensitivity_list) -> _VastAlwaysBase {
            char *error = nullptr;
            xls_vast_always_base *ab = nullptr;
            std::vector<xls_vast_expression *> c_sl;
            for (auto *e : sensitivity_list)
                c_sl.push_back(e->ptr);
            bool ok = xls_vast_verilog_module_add_always_ff(
                mod.ptr, c_sl.data(), c_sl.size(), &ab, &error
            );
            check_result(ok, error);
            return _VastAlwaysBase(ab);
        },
        nb::keep_alive<0, 1>(),
        "module"_a,
        "sensitivity_list"_a
    );

    m.def(
        "xls_vast_verilog_module_add_always_at",
        [](const _VastVerilogModule &mod,
           std::vector<_VastExpression *> sensitivity_list) -> _VastAlwaysBase {
            char *error = nullptr;
            xls_vast_always_base *ab = nullptr;
            std::vector<xls_vast_expression *> c_sl;
            for (auto *e : sensitivity_list)
                c_sl.push_back(e->ptr);
            bool ok = xls_vast_verilog_module_add_always_at(
                mod.ptr, c_sl.data(), c_sl.size(), &ab, &error
            );
            check_result(ok, error);
            return _VastAlwaysBase(ab);
        },
        nb::keep_alive<0, 1>(),
        "module"_a,
        "sensitivity_list"_a
    );

    m.def(
        "xls_vast_verilog_module_add_always_comb",
        [](const _VastVerilogModule &mod) -> _VastAlwaysBase {
            char *error = nullptr;
            xls_vast_always_base *ab = nullptr;
            bool ok =
                xls_vast_verilog_module_add_always_comb(mod.ptr, &ab, &error);
            check_result(ok, error);
            return _VastAlwaysBase(ab);
        },
        nb::keep_alive<0, 1>(),
        "module"_a
    );

    // ============================================================
    // VerilogModule — conditional
    // ============================================================
    m.def(
        "xls_vast_verilog_module_add_conditional",
        [](const _VastVerilogModule &mod,
           const _VastExpression &cond) -> _VastConditional {
            return _VastConditional(
                xls_vast_verilog_module_add_conditional(mod.ptr, cond.ptr)
            );
        },
        nb::keep_alive<0, 1>(),
        "module"_a,
        "cond"_a
    );

    // ============================================================
    // VerilogModule — name & ports
    // ============================================================
    m.def(
        "xls_vast_verilog_module_get_name",
        [](const _VastVerilogModule &mod) -> std::string {
            return own_c_str(xls_vast_verilog_module_get_name(mod.ptr));
        },
        "module"_a
    );

    m.def(
        "xls_vast_verilog_module_get_ports",
        [](const _VastVerilogModule &mod) -> std::vector<_VastModulePort> {
            size_t count = 0;
            xls_vast_module_port **ports =
                xls_vast_verilog_module_get_ports(mod.ptr, &count);
            std::vector<_VastModulePort> result;
            result.reserve(count);
            for (size_t i = 0; i < count; ++i)
                result.emplace_back(ports[i]);
            xls_vast_verilog_module_free_ports(ports, count);
            return result;
        },
        "module"_a
    );

    m.def(
        "xls_vast_verilog_module_port_get_direction",
        [](const _VastModulePort &port) -> XlsVastModulePortDirection {
            return static_cast<XlsVastModulePortDirection>(
                xls_vast_verilog_module_port_get_direction(port.ptr)
            );
        },
        "port"_a
    );

    m.def(
        "xls_vast_verilog_module_port_get_def",
        [](const _VastModulePort &port) -> _VastDef {
            return _VastDef(xls_vast_verilog_module_port_get_def(port.ptr));
        },
        nb::keep_alive<0, 1>(),
        "port"_a
    );

    // ============================================================
    // Def
    // ============================================================
    m.def(
        "xls_vast_def_get_name",
        [](const _VastDef &def) -> std::string {
            return own_c_str(xls_vast_def_get_name(def.ptr));
        },
        "_def"_a
    );

    m.def(
        "xls_vast_def_get_data_type",
        [](const _VastDef &def) -> _VastDataType {
            return _VastDataType(xls_vast_def_get_data_type(def.ptr));
        },
        nb::keep_alive<0, 1>(),
        "_def"_a
    );

    // ============================================================
    // DataType
    // ============================================================
    m.def(
        "xls_vast_data_type_width_as_int64",
        [](const _VastDataType &type) -> int64_t {
            char *error = nullptr;
            int64_t width;
            bool ok =
                xls_vast_data_type_width_as_int64(type.ptr, &width, &error);
            check_result(ok, error);
            return width;
        },
        "type"_a
    );

    m.def(
        "xls_vast_data_type_flat_bit_count_as_int64",
        [](const _VastDataType &type) -> int64_t {
            char *error = nullptr;
            int64_t count;
            bool ok = xls_vast_data_type_flat_bit_count_as_int64(
                type.ptr, &count, &error
            );
            check_result(ok, error);
            return count;
        },
        "type"_a
    );

    m.def(
        "xls_vast_data_type_width",
        [](const _VastDataType &type) -> nb::object {
            auto *expr = xls_vast_data_type_width(type.ptr);
            if (!expr)
                return nb::none();
            return nb::cast(_VastExpression(expr));
        },
        nb::keep_alive<0, 1>(),
        "type"_a
    );

    m.def(
        "xls_vast_data_type_is_signed",
        [](const _VastDataType &type) -> bool {
            return xls_vast_data_type_is_signed(type.ptr);
        },
        "type"_a
    );

    // ============================================================
    // Expression emit
    // ============================================================
    m.def(
        "xls_vast_expression_emit",
        [](const _VastExpression &expr) -> std::string {
            return own_c_str(xls_vast_expression_emit(expr.ptr));
        },
        "expression"_a
    );

    // ============================================================
    // Cast functions
    // ============================================================
    m.def(
        "xls_vast_literal_as_expression",
        [](const _VastLiteral &v) -> _VastExpression {
            return _VastExpression(xls_vast_literal_as_expression(v.ptr));
        },
        nb::keep_alive<0, 1>(),
        "literal"_a
    );

    m.def(
        "xls_vast_logic_ref_as_expression",
        [](const _VastLogicRef &v) -> _VastExpression {
            return _VastExpression(xls_vast_logic_ref_as_expression(v.ptr));
        },
        nb::keep_alive<0, 1>(),
        "logic_ref"_a
    );

    m.def(
        "xls_vast_slice_as_expression",
        [](const _VastSlice &v) -> _VastExpression {
            return _VastExpression(xls_vast_slice_as_expression(v.ptr));
        },
        nb::keep_alive<0, 1>(),
        "slice"_a
    );

    m.def(
        "xls_vast_concat_as_expression",
        [](const _VastConcat &v) -> _VastExpression {
            return _VastExpression(xls_vast_concat_as_expression(v.ptr));
        },
        nb::keep_alive<0, 1>(),
        "concat"_a
    );

    m.def(
        "xls_vast_index_as_expression",
        [](const _VastIndex &v) -> _VastExpression {
            return _VastExpression(xls_vast_index_as_expression(v.ptr));
        },
        nb::keep_alive<0, 1>(),
        "index"_a
    );

    m.def(
        "xls_vast_parameter_ref_as_expression",
        [](const _VastParameterRef &v) -> _VastExpression {
            return _VastExpression(xls_vast_parameter_ref_as_expression(v.ptr));
        },
        nb::keep_alive<0, 1>(),
        "parameter_ref"_a
    );

    m.def(
        "xls_vast_localparam_ref_as_expression",
        [](const _VastLocalparamRef &v) -> _VastExpression {
            return _VastExpression(
                xls_vast_localparam_ref_as_expression(v.ptr)
            );
        },
        nb::keep_alive<0, 1>(),
        "localparam_ref"_a
    );

    m.def(
        "xls_vast_indexable_expression_as_expression",
        [](const _VastIndexableExpression &v) -> _VastExpression {
            return _VastExpression(
                xls_vast_indexable_expression_as_expression(v.ptr)
            );
        },
        nb::keep_alive<0, 1>(),
        "indexable_expression"_a
    );

    m.def(
        "xls_vast_logic_ref_as_indexable_expression",
        [](const _VastLogicRef &v) -> _VastIndexableExpression {
            return _VastIndexableExpression(
                xls_vast_logic_ref_as_indexable_expression(v.ptr)
            );
        },
        nb::keep_alive<0, 1>(),
        "logic_ref"_a
    );

    m.def(
        "xls_vast_index_as_indexable_expression",
        [](const _VastIndex &v) -> _VastIndexableExpression {
            return _VastIndexableExpression(
                xls_vast_index_as_indexable_expression(v.ptr)
            );
        },
        nb::keep_alive<0, 1>(),
        "index"_a
    );

    m.def(
        "xls_vast_macro_ref_as_expression",
        [](const _VastMacroRef &v) -> _VastExpression {
            return _VastExpression(xls_vast_macro_ref_as_expression(v.ptr));
        },
        nb::keep_alive<0, 1>(),
        "macro_ref"_a
    );

    // ============================================================
    // LogicRef
    // ============================================================
    m.def(
        "xls_vast_logic_ref_get_name",
        [](const _VastLogicRef &lr) -> std::string {
            return own_c_str(xls_vast_logic_ref_get_name(lr.ptr));
        },
        "logic_ref"_a
    );

    // ============================================================
    // AlwaysBase
    // ============================================================
    m.def(
        "xls_vast_always_base_get_statement_block",
        [](const _VastAlwaysBase &ab) -> _VastStatementBlock {
            return _VastStatementBlock(
                xls_vast_always_base_get_statement_block(ab.ptr)
            );
        },
        nb::keep_alive<0, 1>(),
        "always_base"_a
    );

    // ============================================================
    // StatementBlock
    // ============================================================
    m.def(
        "xls_vast_statement_block_add_nonblocking_assignment",
        [](const _VastStatementBlock &block,
           const _VastExpression &lhs,
           const _VastExpression &rhs) -> _VastStatement {
            return _VastStatement(
                xls_vast_statement_block_add_nonblocking_assignment(
                    block.ptr, lhs.ptr, rhs.ptr
                )
            );
        },
        nb::keep_alive<0, 1>(),
        "block"_a,
        "lhs"_a,
        "rhs"_a
    );

    m.def(
        "xls_vast_statement_block_add_blocking_assignment",
        [](const _VastStatementBlock &block,
           const _VastExpression &lhs,
           const _VastExpression &rhs) -> _VastStatement {
            return _VastStatement(
                xls_vast_statement_block_add_blocking_assignment(
                    block.ptr, lhs.ptr, rhs.ptr
                )
            );
        },
        nb::keep_alive<0, 1>(),
        "block"_a,
        "lhs"_a,
        "rhs"_a
    );

    m.def(
        "xls_vast_statement_block_add_continuous_assignment",
        [](const _VastStatementBlock &block,
           const _VastExpression &lhs,
           const _VastExpression &rhs) -> _VastStatement {
            return _VastStatement(
                xls_vast_statement_block_add_continuous_assignment(
                    block.ptr, lhs.ptr, rhs.ptr
                )
            );
        },
        nb::keep_alive<0, 1>(),
        "block"_a,
        "lhs"_a,
        "rhs"_a
    );

    m.def(
        "xls_vast_statement_block_add_comment_text",
        [](const _VastStatementBlock &block,
           const std::string &text) -> _VastStatement {
            return _VastStatement(xls_vast_statement_block_add_comment_text(
                block.ptr, text.c_str()
            ));
        },
        nb::keep_alive<0, 1>(),
        "block"_a,
        "text"_a
    );

    m.def(
        "xls_vast_statement_block_add_blank_line",
        [](const _VastStatementBlock &block) -> _VastStatement {
            return _VastStatement(
                xls_vast_statement_block_add_blank_line(block.ptr)
            );
        },
        nb::keep_alive<0, 1>(),
        "block"_a
    );

    m.def(
        "xls_vast_statement_block_add_inline_text",
        [](const _VastStatementBlock &block,
           const std::string &text) -> _VastStatement {
            return _VastStatement(xls_vast_statement_block_add_inline_text(
                block.ptr, text.c_str()
            ));
        },
        nb::keep_alive<0, 1>(),
        "block"_a,
        "text"_a
    );

    m.def(
        "xls_vast_statement_block_add_conditional",
        [](const _VastStatementBlock &block,
           const _VastExpression &cond) -> _VastConditional {
            return _VastConditional(
                xls_vast_statement_block_add_conditional(block.ptr, cond.ptr)
            );
        },
        nb::keep_alive<0, 1>(),
        "block"_a,
        "cond"_a
    );

    m.def(
        "xls_vast_statement_block_add_case",
        [](const _VastStatementBlock &block,
           const _VastExpression &selector) -> _VastCaseStatement {
            return _VastCaseStatement(
                xls_vast_statement_block_add_case(block.ptr, selector.ptr)
            );
        },
        nb::keep_alive<0, 1>(),
        "block"_a,
        "selector"_a
    );

    // ============================================================
    // Conditional
    // ============================================================
    m.def(
        "xls_vast_conditional_get_then_block",
        [](const _VastConditional &cond) -> _VastStatementBlock {
            return _VastStatementBlock(
                xls_vast_conditional_get_then_block(cond.ptr)
            );
        },
        nb::keep_alive<0, 1>(),
        "conditional"_a
    );

    m.def(
        "xls_vast_conditional_add_else_if",
        [](const _VastConditional &cond,
           const _VastExpression &expr_cond) -> _VastStatementBlock {
            return _VastStatementBlock(
                xls_vast_conditional_add_else_if(cond.ptr, expr_cond.ptr)
            );
        },
        nb::keep_alive<0, 1>(),
        "conditional"_a,
        "cond"_a
    );

    m.def(
        "xls_vast_conditional_add_else",
        [](const _VastConditional &cond) -> _VastStatementBlock {
            return _VastStatementBlock(xls_vast_conditional_add_else(cond.ptr));
        },
        nb::keep_alive<0, 1>(),
        "conditional"_a
    );

    // ============================================================
    // CaseStatement
    // ============================================================
    m.def(
        "xls_vast_case_statement_add_item",
        [](const _VastCaseStatement &cs,
           const _VastExpression &match_expr) -> _VastStatementBlock {
            return _VastStatementBlock(
                xls_vast_case_statement_add_item(cs.ptr, match_expr.ptr)
            );
        },
        nb::keep_alive<0, 1>(),
        "case_statement"_a,
        "match_expr"_a
    );

    m.def(
        "xls_vast_case_statement_add_default",
        [](const _VastCaseStatement &cs) -> _VastStatementBlock {
            return _VastStatementBlock(
                xls_vast_case_statement_add_default(cs.ptr)
            );
        },
        nb::keep_alive<0, 1>(),
        "case_statement"_a
    );

    // ============================================================
    // GenerateLoop
    // ============================================================
    m.def(
        "xls_vast_generate_loop_get_genvar",
        [](const _VastGenerateLoop &loop) -> _VastLogicRef {
            return _VastLogicRef(xls_vast_generate_loop_get_genvar(loop.ptr));
        },
        nb::keep_alive<0, 1>(),
        "loop"_a
    );

    m.def(
        "xls_vast_generate_loop_add_generate_loop",
        [](const _VastGenerateLoop &loop,
           const std::string &genvar_name,
           const _VastExpression &init,
           const _VastExpression &limit,
           const std::string &label) -> _VastGenerateLoop {
            return _VastGenerateLoop(xls_vast_generate_loop_add_generate_loop(
                loop.ptr, genvar_name.c_str(), init.ptr, limit.ptr, label.c_str()
            ));
        },
        nb::keep_alive<0, 1>(),
        "loop"_a,
        "genvar_name"_a,
        "init"_a,
        "limit"_a,
        "label"_a
    );

    m.def(
        "xls_vast_generate_loop_add_blank_line",
        [](const _VastGenerateLoop &loop) {
            xls_vast_generate_loop_add_blank_line(loop.ptr);
        },
        "loop"_a
    );

    m.def(
        "xls_vast_generate_loop_add_comment",
        [](const _VastGenerateLoop &loop, const _VastComment &comment) {
            xls_vast_generate_loop_add_comment(loop.ptr, comment.ptr);
        },
        "loop"_a,
        "comment"_a
    );

    m.def(
        "xls_vast_generate_loop_add_instantiation",
        [](const _VastGenerateLoop &loop, const _VastInstantiation &inst) {
            xls_vast_generate_loop_add_instantiation(loop.ptr, inst.ptr);
        },
        "loop"_a,
        "instantiation"_a
    );

    m.def(
        "xls_vast_generate_loop_add_inline_verilog_statement",
        [](const _VastGenerateLoop &loop,
           const _VastInlineVerilogStatement &stmt) {
            xls_vast_generate_loop_add_inline_verilog_statement(
                loop.ptr, stmt.ptr
            );
        },
        "loop"_a,
        "statement"_a
    );

    m.def(
        "xls_vast_generate_loop_add_always_comb",
        [](const _VastGenerateLoop &loop) -> _VastAlwaysBase {
            char *error = nullptr;
            xls_vast_always_base *ab = nullptr;
            bool ok =
                xls_vast_generate_loop_add_always_comb(loop.ptr, &ab, &error);
            check_result(ok, error);
            return _VastAlwaysBase(ab);
        },
        nb::keep_alive<0, 1>(),
        "loop"_a
    );

    m.def(
        "xls_vast_generate_loop_add_always_ff",
        [](const _VastGenerateLoop &loop,
           std::vector<_VastExpression *> sensitivity_list) -> _VastAlwaysBase {
            char *error = nullptr;
            xls_vast_always_base *ab = nullptr;
            std::vector<xls_vast_expression *> c_sl;
            for (auto *e : sensitivity_list)
                c_sl.push_back(e->ptr);
            bool ok = xls_vast_generate_loop_add_always_ff(
                loop.ptr, c_sl.data(), c_sl.size(), &ab, &error
            );
            check_result(ok, error);
            return _VastAlwaysBase(ab);
        },
        nb::keep_alive<0, 1>(),
        "loop"_a,
        "sensitivity_list"_a
    );

    m.def(
        "xls_vast_generate_loop_add_localparam",
        [](const _VastGenerateLoop &loop,
           const std::string &name,
           const _VastExpression &rhs) -> _VastLocalparamRef {
            return _VastLocalparamRef(xls_vast_generate_loop_add_localparam(
                loop.ptr, name.c_str(), rhs.ptr
            ));
        },
        nb::keep_alive<0, 1>(),
        "loop"_a,
        "name"_a,
        "rhs"_a
    );

    m.def(
        "xls_vast_generate_loop_add_localparam_with_def",
        [](const _VastGenerateLoop &loop,
           const _VastDef &def,
           const _VastExpression &rhs) -> _VastLocalparamRef {
            return _VastLocalparamRef(
                xls_vast_generate_loop_add_localparam_with_def(
                    loop.ptr, def.ptr, rhs.ptr
                )
            );
        },
        nb::keep_alive<0, 1>(),
        "loop"_a,
        "_def"_a,
        "rhs"_a
    );

    m.def(
        "xls_vast_generate_loop_add_continuous_assignment",
        [](const _VastGenerateLoop &loop,
           const _VastExpression &lhs,
           const _VastExpression &rhs) -> _VastStatement {
            return _VastStatement(
                xls_vast_generate_loop_add_continuous_assignment(
                    loop.ptr, lhs.ptr, rhs.ptr
                )
            );
        },
        nb::keep_alive<0, 1>(),
        "loop"_a,
        "lhs"_a,
        "rhs"_a
    );

    m.def(
        "xls_vast_generate_loop_add_macro_statement",
        [](const _VastGenerateLoop &loop,
           const _VastMacroStatement &stmt) -> _VastMacroStatement {
            return _VastMacroStatement(
                xls_vast_generate_loop_add_macro_statement(loop.ptr, stmt.ptr)
            );
        },
        nb::keep_alive<0, 1>(),
        "loop"_a,
        "statement"_a
    );

    m.def(
        "xls_vast_generate_loop_add_conditional",
        [](const _VastGenerateLoop &loop,
           const _VastExpression &cond) -> _VastConditional {
            return _VastConditional(
                xls_vast_generate_loop_add_conditional(loop.ptr, cond.ptr)
            );
        },
        nb::keep_alive<0, 1>(),
        "loop"_a,
        "cond"_a
    );
}
