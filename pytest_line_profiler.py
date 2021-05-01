# -*- coding: utf-8 -*-

import pytest
from importlib import import_module
from line_profiler import LineProfiler


def import_string(dotted_path):
    """
    Import a dotted module path and return the object if is callable
    """
    try:
        module_path, callable_name = dotted_path.rsplit('.', 1)
        module = import_module(module_path)
        callable_object = getattr(module, callable_name)
        assert callable(callable_object)
        return callable_object
    except (ModuleNotFoundError, ValueError, AttributeError, AssertionError):
        raise pytest.UsageError(f"{dotted_path} not found or is not callable")


def pytest_addoption(parser):
    group = parser.getgroup('line-profile')
    group.addoption(
        '--line-profile',
        action='store',
        nargs="*",
        help='Set the value for the fixture "bar".'
    )

    
def pytest_load_initial_conftests(early_config, parser, args):
    early_config.addinivalue_line(
        "markers",
        "line_profile: Line profile this test.",
    )



def pytest_runtest_call(item):
    instrumented = []
    import ipdb; ipdb.set_trace()
    if item.get_closest_marker("line_profile"):
        instrumented += item.get_closest_marker("line_profile").args
    if item.config.getvalue("line_profile"):
        instrumented += [import_string(s) for s in item.config.getvalue("line_profile")]
    
    if instrumented:
        lp = LineProfiler(*instrumented)
        lp.runcall(item.runtest)
        item.addfinalizer(lp.print_stats)
    else:
        item.runtest()


@pytest.fixture
def line_profiler(request,):
    # return request.config.option.dest_foo

    lp = LineProfiler()
    yield lp
    request.addfinalizer(lp.print_stats)