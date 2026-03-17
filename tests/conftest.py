"""Shared fixtures for XLS Python bindings tests."""

import pytest

import xls.raw as raw

SAMPLE_IR = """\
package test_pkg

top fn add(x: bits[32], y: bits[32]) -> bits[32] {
  ret add.3: bits[32] = add(x, y, id=3)
}
"""

SAMPLE_DSLX = """\
fn add(x: u32, y: u32) -> u32 {
  x + y
}
"""


@pytest.fixture
def sample_ir():
    """A simple IR package string with an add function."""
    return SAMPLE_IR


@pytest.fixture
def sample_dslx():
    """A simple DSLX source string with an add function."""
    return SAMPLE_DSLX


@pytest.fixture
def package(sample_ir):
    """Parsed IR package."""
    return raw.c_api.xls_parse_ir_package(sample_ir)


@pytest.fixture
def function(package):
    """The 'add' function from the parsed package."""
    return raw.c_api.xls_package_get_function(package, 'add')


@pytest.fixture
def jit(function):
    """A JIT-compiled version of the add function."""
    return raw.c_api.xls_make_function_jit(function)
