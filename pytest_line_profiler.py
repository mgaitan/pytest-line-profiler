# -*- coding: utf-8 -*-

import io
import pytest
from importlib import import_module
from line_profiler import LineProfiler


def get_stats(lp: LineProfiler) -> str:
    s = io.StringIO()
    lp.print_stats(stream=s)
    return s.getvalue()


def import_string(dotted_path):
    """
    Import a dotted module path and return the object if is callable
    """
    if not isinstance(dotted_path, str):
        return dotted_path
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
        help='Register a function to profile while executed tests.'
    )

    
def pytest_load_initial_conftests(early_config, parser, args):
    early_config.addinivalue_line(
        "markers",
        "line_profile: Line profile this test.",
    )



def pytest_runtest_call(item):
    instrumented = []
    if item.get_closest_marker("line_profile"):
        instrumented += [import_string(s) for s in item.get_closest_marker("line_profile").args]
    if item.config.getvalue("line_profile"):
        instrumented += [import_string(s) for s in item.config.getvalue("line_profile")]
    
    if instrumented:
        lp = LineProfiler(*instrumented)
        item_runtest = item.runtest
        def runtest():
            lp.runcall(item_runtest)
            item.config._line_profile = getattr(item.config, "_line_profile", {})
            item.config._line_profile[item.nodeid] = get_stats(lp)
        item.runtest = runtest


def pytest_terminal_summary(
    terminalreporter: "TerminalReporter",
    exitstatus: "ExitCode",
    config: "Config",
) -> None:
    reports = getattr(config, "_line_profile", {})
    for k, v in reports.items():
        terminalreporter.write_sep("=", f"Line Profile result for {k}")
        terminalreporter.write(v)


@pytest.fixture
def line_profiler(request):
    lp = LineProfiler()
    yield lp
    request.addfinalizer(lp.print_stats)