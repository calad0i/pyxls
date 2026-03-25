"""Pythonic wrapper classes and functions for xls.raw.c_api."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from ._c_api import *

from . import raw
from ._wrap import auto_wrap, maybe_unwrap, maybe_wrap, register_wrapper, wrap_module

# ---------------------------------------------------------------------------
# Enum alias mappings for text proto generation
# ---------------------------------------------------------------------------

GeneratorKind = Literal['pipeline', 'combinational']
_GENERATOR_KIND: dict[str, str] = {
    'pipeline': 'GENERATOR_KIND_PIPELINE',
    'combinational': 'GENERATOR_KIND_COMBINATIONAL',
}

IOKind = Literal['flop', 'skid_buffer', 'zero_latency_buffer']
_IO_KIND: dict[str, str] = {
    'flop': 'IO_KIND_FLOP',
    'skid_buffer': 'IO_KIND_SKID_BUFFER',
    'zero_latency_buffer': 'IO_KIND_ZERO_LATENCY_BUFFER',
}

RegisterMergeStrategy = Literal['dont_merge', 'identity_only']
_REGISTER_MERGE_STRATEGY: dict[str, str] = {
    'dont_merge': 'STRATEGY_DONT_MERGE',
    'identity_only': 'STRATEGY_IDENTITY_ONLY',
}

SchedulingStrategy = Literal['sdc', 'asap', 'min_cut', 'random']
_SCHEDULING_STRATEGY: dict[str, str] = {
    'sdc': 'SCHEDULER_TYPE_SDC',
    'asap': 'SCHEDULER_TYPE_ASAP',
    'min_cut': 'SCHEDULER_TYPE_MIN_CUT',
    'random': 'SCHEDULER_TYPE_RANDOM',
}

# Map field names to their enum alias dicts
_ENUM_FIELDS: dict[str, dict[str, str]] = {
    'generator': _GENERATOR_KIND,
    'flop_inputs_kind': _IO_KIND,
    'flop_outputs_kind': _IO_KIND,
    'register_merge_strategy': _REGISTER_MERGE_STRATEGY,
    'scheduling_strategy': _SCHEDULING_STRATEGY,
}


def _build_textproto(fields: dict[str, object]) -> str:
    """Build a textproto string from a dict of field name → value.

    - ``None`` values are skipped (proto default).
    - Enum fields are mapped via ``_ENUM_FIELDS``.
    - ``bool`` -> ``true``/``false``.
    - ``list`` -> repeated field entries.
    - ``str`` values are quoted.
    """
    parts: list[str] = []
    for name, value in fields.items():
        if value is None:
            continue
        enum_map = _ENUM_FIELDS.get(name)
        if enum_map is not None:
            mapped = enum_map.get(value)  # type: ignore[arg-type]
            if mapped is None:
                raise ValueError(f'Invalid value {value!r} for {name}. Choose from: {list(enum_map)}')
            parts.append(f'{name}: {mapped}')
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    parts.append(f'{name}: "{item}"')
                else:
                    parts.append(f'{name}: {item}')
        elif isinstance(value, bool):
            parts.append(f'{name}: {"true" if value else "false"}')
        elif isinstance(value, str):
            parts.append(f'{name}: "{value}"')
        elif isinstance(value, (int, float)):
            parts.append(f'{name}: {value}')
        else:
            raise TypeError(f'Unsupported type {type(value).__name__} for field {name}')
    return ', '.join(parts)


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
        *,
        with_delay_model: bool = False,
        # raw textproto
        scheduling_options_textproto: str | None = None,
        codegen_flags_textproto: str | None = None,
        # CodegenFlagsProto fields
        generator: GeneratorKind | None = 'combinational',
        top: str | None = None,
        module_name: str | None = None,
        input_valid_signal: str | None = None,
        output_valid_signal: str | None = None,
        manual_load_enable_signal: str | None = None,
        flop_inputs: bool | None = None,
        flop_outputs: bool | None = None,
        flop_inputs_kind: IOKind | None = None,
        flop_outputs_kind: IOKind | None = None,
        flop_single_value_channels: bool | None = None,
        add_idle_output: bool | None = None,
        output_port_name: str | None = None,
        reset: str | None = None,
        reset_active_low: bool | None = None,
        reset_asynchronous: bool | None = None,
        reset_data_path: bool | None = None,
        use_system_verilog: bool | None = None,
        separate_lines: bool | None = None,
        max_inline_depth: int | None = None,
        gate_format: str | None = None,
        assert_format: str | None = None,
        smulp_format: str | None = None,
        umulp_format: str | None = None,
        streaming_channel_data_suffix: str | None = None,
        streaming_channel_valid_suffix: str | None = None,
        streaming_channel_ready_suffix: str | None = None,
        ram_configurations: list[str] | None = None,
        gate_recvs: bool | None = None,
        array_index_bounds_checking: bool | None = None,
        register_merge_strategy: RegisterMergeStrategy | None = None,
        max_trace_verbosity: int | None = None,
        emit_sv_types: bool | None = None,
        simulation_macro_name: str | None = None,
        assertion_macro_names: list[str] | None = None,
        add_invariant_assertions: bool | None = None,
        ir_dump_path: str | None = None,
        # SchedulingOptionsFlagsProto fields
        pipeline_stages: int | None = None,
        clock_period_ps: int | None = None,
        delay_model: str | None = None,
        clock_margin_percent: int | None = None,
        period_relaxation_percent: int | None = None,
        worst_case_throughput: int | None = None,
        additional_input_delay_ps: int | None = None,
        additional_output_delay_ps: int | None = None,
        ffi_fallback_delay_ps: int | None = None,
        io_constraints: list[str] | None = None,
        receives_first_sends_last: bool | None = None,
        mutual_exclusion_z3_rlimit: int | None = None,
        default_next_value_z3_rlimit: int | None = None,
        use_fdo: bool | None = None,
        fdo_iteration_number: int | None = None,
        fdo_delay_driven_path_number: int | None = None,
        fdo_fanout_driven_path_number: int | None = None,
        fdo_refinement_stochastic_ratio: float | None = None,
        fdo_path_evaluate_strategy: str | None = None,
        fdo_synthesizer_name: str | None = None,
        fdo_yosys_path: str | None = None,
        fdo_sta_path: str | None = None,
        fdo_synthesis_libraries: str | None = None,
        fdo_default_driver_cell: str | None = None,
        fdo_default_load: str | None = None,
        minimize_clock_on_failure: bool | None = None,
        multi_proc: bool | None = None,
        minimize_worst_case_throughput: bool | None = None,
        recover_after_minimizing_clock: bool | None = None,
        opt_level: int | None = None,
        scheduling_strategy: SchedulingStrategy | None = None,
        merge_on_mutual_exclusion: bool | None = None,
    ) -> ScheduleAndCodegenResult:
        """Schedule and generate Verilog from this package.

        All proto fields default to ``None`` (use proto default). Pass keyword
        arguments for the fields you want to set.  For advanced/uncommon
        fields not exposed here, use ``scheduling_options_textproto`` or
        ``codegen_flags_textproto`` which accept raw textproto strings and
        override all individual kwargs for their respective proto.

        Args:
            with_delay_model: Whether to use a delay model.
            scheduling_options_textproto: Raw ``SchedulingOptionsFlagsProto``
                textproto string. When set, overrides all scheduling kwargs.
            codegen_flags_textproto: Raw ``CodegenFlagsProto`` textproto
                string. When set, overrides all codegen kwargs.

        Codegen flags (``CodegenFlagsProto``):
            generator: Generator kind. ``'pipeline'`` or ``'combinational'``
                (default).
            top: Name of the top-level function/proc to codegen.
            module_name: Override the Verilog module name.
            input_valid_signal: Name of the input valid signal (pipeline only).
            output_valid_signal: Name of the output valid signal (pipeline
                only).
            manual_load_enable_signal: Name of the manual load-enable signal.
            flop_inputs: Whether to flop input ports.
            flop_outputs: Whether to flop output ports.
            flop_inputs_kind: Kind of input flop. ``'flop'``,
                ``'skid_buffer'``, or ``'zero_latency_buffer'``.
            flop_outputs_kind: Kind of output flop. ``'flop'``,
                ``'skid_buffer'``, or ``'zero_latency_buffer'``.
            flop_single_value_channels: Whether to flop single-value channels.
            add_idle_output: Whether to add an idle output port.
            output_port_name: Name of the combinational output port.
            reset: Name of the reset signal (e.g. ``'rst'``).
            reset_active_low: Whether reset is active-low.
            reset_asynchronous: Whether reset is asynchronous.
            reset_data_path: Whether to reset the data path registers.
            use_system_verilog: Emit SystemVerilog instead of plain Verilog.
            separate_lines: Put each expression on a separate line.
            max_inline_depth: Maximum depth of inlined expressions.
            gate_format: Format string for gate operations. Placeholders:
                ``{condition}``/``{input0}`` (gate condition),
                ``{input}``/``{input1}`` (data input), ``{output}`` (result),
                ``{width}`` (bit width).
                Example: ``'my_gate {output} [{width}-1:0] = {condition} & {input}'``.
            assert_format: Format string for assertions. Placeholders:
                ``{message}``, ``{condition}``, ``{label}`` (assert label),
                ``{clk}`` (clock signal), ``{rst}`` (reset signal).
                Example: ``'MY_ASSERT({condition}, {message})'``.
            smulp_format: Format string for signed partial-multiply modules.
                Placeholders: ``{input0}``, ``{input1}``,
                ``{input0_width}``, ``{input1_width}``, ``{output}``,
                ``{output_width}``. Used for instantiating smulp IP cores.
            umulp_format: Format string for unsigned partial-multiply modules.
                Same placeholders as ``smulp_format``.
            streaming_channel_data_suffix: Suffix appended to channel names
                for data ports (default ``""``).
            streaming_channel_valid_suffix: Suffix appended to channel names
                for valid signals (default ``"_vld"``).
            streaming_channel_ready_suffix: Suffix appended to channel names
                for ready signals (default ``"_rdy"``).
            ram_configurations: External RAM integration configs. Format for
                1RW: ``'name:1RW:req_channel:resp_channel:wr_comp_channel[:latency]'``.
                Format for 1R1W:
                ``'name:1R1W:rd_req:rd_resp:wr_req:wr_comp[:latency]'``.
                Latency defaults to 1.
            gate_recvs: Whether to gate receive operations.
            array_index_bounds_checking: Whether to add bounds checking for
                array indexing.
            register_merge_strategy: Strategy for merging registers.
                ``'dont_merge'`` or ``'identity_only'``.
            max_trace_verbosity: Maximum verbosity level for trace statements.
            emit_sv_types: Emit annotated SystemVerilog types for arguments.
            simulation_macro_name: Verilog macro name guarding
                simulation-only constructs (e.g. ``$display``). Default
                ``"SIMULATION"``. Prefix with ``'!'`` to use ``ifndef``
                instead of ``ifdef``.
            assertion_macro_names: Verilog macro names guarding assertions
                with ``ifdef``. Default ``["ASSERT_ON"]``. Prefix an entry
                with ``'!'`` to use ``ifndef`` instead.
            add_invariant_assertions: Whether to emit runtime invariant
                assertions (e.g. one-hot selector checks). Default true.
            ir_dump_path: Path to dump intermediate IR during block
                conversion (debugging).

        Scheduling options (``SchedulingOptionsFlagsProto``):
            pipeline_stages: Number of pipeline stages.
            clock_period_ps: Target clock period in picoseconds.
            delay_model: Delay model name (e.g. ``'unit'``, or a registered
                model from the delay estimator registry).
            clock_margin_percent: Percentage of clock period to reserve as
                margin.
            period_relaxation_percent: Percentage by which the clock period
                may be relaxed.
            worst_case_throughput: Worst-case throughput target (in cycles per
                output).
            additional_input_delay_ps: Extra input delay in picoseconds.
            additional_output_delay_ps: Extra output delay in picoseconds.
            ffi_fallback_delay_ps: Fallback delay for FFI nodes in
                picoseconds.
            io_constraints: I/O ordering constraints. Format:
                ``'chan_a:send:chan_b:recv:min_latency:max_latency'``.
                Use ``'none'`` for unbounded min/max.
                Example: ``['foo:send:bar:recv:1:3']``.
            receives_first_sends_last: Force receives into the first stage
                and sends into the last stage.
            mutual_exclusion_z3_rlimit: Z3 resource limit for mutual
                exclusion analysis.
            default_next_value_z3_rlimit: Z3 resource limit for
                default-next-value analysis.
            use_fdo: Enable feedback-directed optimization.
            fdo_iteration_number: Number of FDO iterations.
            fdo_delay_driven_path_number: Number of delay-driven paths for
                FDO.
            fdo_fanout_driven_path_number: Number of fanout-driven paths for
                FDO.
            fdo_refinement_stochastic_ratio: Stochastic ratio for FDO
                refinement (0.0 to 1.0).
            fdo_path_evaluate_strategy: FDO path evaluation strategy.
                ``'path'``, ``'cone'``, or ``'window'`` (default).
            fdo_synthesizer_name: Synthesis backend for FDO. Currently only
                ``'yosys'`` (default) is supported.
            fdo_yosys_path: Path to the yosys binary for FDO.
            fdo_sta_path: Path to the OpenSTA binary for FDO.
            fdo_synthesis_libraries: Synthesis and STA library files for FDO
                (e.g. ``.lib`` files).
            fdo_default_driver_cell: Cell assumed to drive primary inputs
                in FDO (e.g. ``'BUF_X4'``).
            fdo_default_load: Cell assumed to be driven by primary outputs
                in FDO (e.g. ``'BUF_X4'``).
            minimize_clock_on_failure: Try to minimize clock period when
                scheduling fails.
            multi_proc: Enable multi-proc scheduling.
            minimize_worst_case_throughput: Minimize worst-case throughput.
            recover_after_minimizing_clock: Recover the original clock period
                after minimization.
            opt_level: Optimization level for scheduling.
            scheduling_strategy: Scheduling algorithm. ``'sdc'`` (default),
                ``'asap'``, ``'min_cut'``, or ``'random'``.
            merge_on_mutual_exclusion: Merge mutually exclusive operations.
        """

        if codegen_flags_textproto is None:
            codegen_flags_textproto = _build_textproto(
                {
                    'generator': generator,
                    'top': top,
                    'module_name': module_name,
                    'input_valid_signal': input_valid_signal,
                    'output_valid_signal': output_valid_signal,
                    'manual_load_enable_signal': manual_load_enable_signal,
                    'flop_inputs': flop_inputs,
                    'flop_outputs': flop_outputs,
                    'flop_inputs_kind': flop_inputs_kind,
                    'flop_outputs_kind': flop_outputs_kind,
                    'flop_single_value_channels': flop_single_value_channels,
                    'add_idle_output': add_idle_output,
                    'output_port_name': output_port_name,
                    'reset': reset,
                    'reset_active_low': reset_active_low,
                    'reset_asynchronous': reset_asynchronous,
                    'reset_data_path': reset_data_path,
                    'use_system_verilog': use_system_verilog,
                    'separate_lines': separate_lines,
                    'max_inline_depth': max_inline_depth,
                    'gate_format': gate_format,
                    'assert_format': assert_format,
                    'smulp_format': smulp_format,
                    'umulp_format': umulp_format,
                    'streaming_channel_data_suffix': streaming_channel_data_suffix,
                    'streaming_channel_valid_suffix': streaming_channel_valid_suffix,
                    'streaming_channel_ready_suffix': streaming_channel_ready_suffix,
                    'ram_configurations': ram_configurations,
                    'gate_recvs': gate_recvs,
                    'array_index_bounds_checking': array_index_bounds_checking,
                    'register_merge_strategy': register_merge_strategy,
                    'max_trace_verbosity': max_trace_verbosity,
                    'emit_sv_types': emit_sv_types,
                    'simulation_macro_name': simulation_macro_name,
                    'assertion_macro_names': assertion_macro_names,
                    'add_invariant_assertions': add_invariant_assertions,
                    'ir_dump_path': ir_dump_path,
                }
            )

        if scheduling_options_textproto is None:
            scheduling_options_textproto = _build_textproto(
                {
                    'pipeline_stages': pipeline_stages,
                    'clock_period_ps': clock_period_ps,
                    'delay_model': delay_model,
                    'clock_margin_percent': clock_margin_percent,
                    'period_relaxation_percent': period_relaxation_percent,
                    'worst_case_throughput': worst_case_throughput,
                    'additional_input_delay_ps': additional_input_delay_ps,
                    'additional_output_delay_ps': additional_output_delay_ps,
                    'ffi_fallback_delay_ps': ffi_fallback_delay_ps,
                    'io_constraints': io_constraints,
                    'receives_first_sends_last': receives_first_sends_last,
                    'mutual_exclusion_z3_rlimit': mutual_exclusion_z3_rlimit,
                    'default_next_value_z3_rlimit': default_next_value_z3_rlimit,
                    'use_fdo': use_fdo,
                    'fdo_iteration_number': fdo_iteration_number,
                    'fdo_delay_driven_path_number': fdo_delay_driven_path_number,
                    'fdo_fanout_driven_path_number': fdo_fanout_driven_path_number,
                    'fdo_refinement_stochastic_ratio': fdo_refinement_stochastic_ratio,
                    'fdo_path_evaluate_strategy': fdo_path_evaluate_strategy,
                    'fdo_synthesizer_name': fdo_synthesizer_name,
                    'fdo_yosys_path': fdo_yosys_path,
                    'fdo_sta_path': fdo_sta_path,
                    'fdo_synthesis_libraries': fdo_synthesis_libraries,
                    'fdo_default_driver_cell': fdo_default_driver_cell,
                    'fdo_default_load': fdo_default_load,
                    'minimize_clock_on_failure': minimize_clock_on_failure,
                    'multi_proc': multi_proc,
                    'minimize_worst_case_throughput': minimize_worst_case_throughput,
                    'recover_after_minimizing_clock': recover_after_minimizing_clock,
                    'opt_level': opt_level,
                    'scheduling_strategy': scheduling_strategy,
                    'merge_on_mutual_exclusion': merge_on_mutual_exclusion,
                }
            )

        result = raw.c_api.xls_schedule_and_codegen_package(
            self._raw,
            scheduling_options_textproto,
            codegen_flags_textproto,
            with_delay_model,
        )
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
#

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

    def jit_fn_predict(
        fn_jit: FunctionJit, input: NDArray[np.int64], bit_count: int, in_word_count: int, out_word_count: int
    ) -> NDArray[np.int64]:
        """Run a JIT-compiled function on a numpy integer array and report the output in the same format. Both input and output must be in 1D arrays of numbers (2D array of bits).

        Parameters:
        ==================
        fn_jit: A JIT-compiled function (FunctionJit) to run on the input array. The function should accept and return values both in array format compatible with the input and output specifications.

        input: A numpy array of int64 of size (N * in_word_count) containing the input data to be processed by the JIT function. The shape is disregarded and will always be interpreted as (N, in_word_count) in the row-major order.

        bit_count: The number of bits of each number in the input array.

        in_word_count: The number of words (groups of bits/number of elements) for each input.

        out_word_count: The number of words (groups of bits/number of elements) for each output.
        """
        ...
else:
    value_from_array = auto_wrap(raw.value_from_array)
    values_from_array = auto_wrap(raw.values_from_array)
    value_to_array = auto_wrap(raw.value_to_array)
    jit_fn_predict = auto_wrap(raw.jit_fn_predict)

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
