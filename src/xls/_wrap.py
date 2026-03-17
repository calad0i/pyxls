"""Dynamic wrapping machinery for XLS raw C++ bindings."""

import functools
import types
from typing import Any, TypeVar

# Registry: raw_type -> wrapper_class
_RAW_TO_WRAPPED: dict[type, type] = {}
# Registry: wrapper_class -> raw_type
_WRAPPED_TO_RAW: dict[type, type] = {}

TT = TypeVar('TT', bound=type)


def register_wrapper(raw_type: type):
    """Class decorator that registers a wrapper class for a raw type.

    Usage:
        @register_wrapper(raw.Package)
        class Package:
            ...
    """

    def decorator(cls: TT) -> TT:
        _RAW_TO_WRAPPED[raw_type] = cls
        _WRAPPED_TO_RAW[cls] = raw_type
        return cls

    return decorator


def maybe_wrap(val: Any) -> Any:
    """Convert a raw object to its wrapped counterpart if a mapping exists.

    Returns the value as-is if no mapping is registered.
    """
    if val is None:
        return None
    raw_type = type(val)
    wrapper_cls = _RAW_TO_WRAPPED.get(raw_type)
    if wrapper_cls is not None:
        obj = object.__new__(wrapper_cls)
        obj._raw = val
        return obj
    return val


def maybe_unwrap(val: Any) -> Any:
    """Convert a wrapped object back to its raw counterpart via ._raw attr.

    Returns the value as-is if it has no ._raw attribute.
    """
    return getattr(val, '_raw', val)


def _wrap_sequence(val: Any) -> Any:
    """Wrap a value, handling lists and tuples recursively."""
    if isinstance(val, list):
        return [_wrap_sequence(v) for v in val]
    if isinstance(val, tuple):
        return tuple(_wrap_sequence(v) for v in val)
    return maybe_wrap(val)


def _unwrap_sequence(val: Any) -> Any:
    """Unwrap a value, handling lists and tuples recursively."""
    if isinstance(val, list):
        return [_unwrap_sequence(v) for v in val]
    if isinstance(val, tuple):
        return tuple(_unwrap_sequence(v) for v in val)
    return maybe_unwrap(val)


T = TypeVar('T', bound=types.BuiltinFunctionType | types.FunctionType | types.MethodType)


def auto_wrap(fn: T) -> T:
    """Decorator that unwraps all inputs and wraps all outputs.

    - Arguments that are wrapper objects are unwrapped before calling fn.
    - Lists/tuples of wrapper objects are unwrapped element-wise.
    - Return values that are raw objects are wrapped if a mapping exists.
    - Lists/tuples of raw objects are wrapped element-wise.
    """

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        new_args = tuple(_unwrap_sequence(a) for a in args)
        new_kwargs = {k: _unwrap_sequence(v) for k, v in kwargs.items()}
        result = fn(*new_args, **new_kwargs)
        return _wrap_sequence(result)

    return wrapper  # type: ignore


def wrap_module(raw_module, target_dict: dict) -> None:
    """Bulk-wrap all public functions from a raw module into target_dict.

    For each public name in raw_module:
    - If it's a function/callable (but not a type/class), wrap it with auto_wrap
      and store in target_dict under the same name.
    - Non-callable public names (enums, constants) are also copied as-is.
    """
    for name in dir(raw_module):
        if name.startswith('_'):
            continue
        obj = getattr(raw_module, name)
        if isinstance(obj, types.BuiltinFunctionType) or (callable(obj) and not isinstance(obj, type)):
            target_dict[name] = auto_wrap(obj)
        else:
            # enums, constants, type objects
            target_dict[name] = obj
