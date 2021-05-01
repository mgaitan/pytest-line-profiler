# -*- coding: utf-8 -*-
import pytest
from math import sin 

def f(i):
    return i * 10

def g():
    return sum(f(i) for i in range(10))




@pytest.mark.line_profile.with_args(f, g)
def test_as_mark():
    g()


"""
def test_via_command_line():
    sin(1)
"""