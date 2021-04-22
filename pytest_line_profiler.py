# -*- coding: utf-8 -*-

import pytest
from line_profiler import LineProfiler


def pytest_addoption(parser):
    group = parser.getgroup('line-profiler')
    group.addoption(
        '--foo',
        action='store',
        dest='dest_foo',
        default='2021',
        help='Set the value for the fixture "bar".'
    )

    parser.addini('HELLO', 'Dummy pytest.ini setting')


@pytest.fixture
def line_profiler(request,):
    # return request.config.option.dest_foo

    lp = LineProfiler()
    yield lp
    request.addfinalizer(lp.print_stats)