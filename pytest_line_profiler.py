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
        components = dotted_path.split('.')

        # Identify the longest valid module path
        for i in range(len(components), 0, -1):
            try:
                module = import_module('.'.join(components[:i]))
                break
            except ModuleNotFoundError:
                continue
        else:
            raise ModuleNotFoundError(f"No module matches the given dotted path: {dotted_path}")

        remaining_components = components[i:]

        # Traverse the remaining components to get to the function or method
        callable_object = module
        for comp in remaining_components:
            try:
                callable_object = getattr(callable_object, comp)
            except AttributeError:
                raise AttributeError(f"Component {comp} not found in {callable_object}")

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
