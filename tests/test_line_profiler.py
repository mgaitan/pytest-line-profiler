# -*- coding: utf-8 -*-

def f(i):
    return i * 10

def g():
    return sum(f(i) for i in range(10))



def test_basic(line_profiler):
    line_profiler(f)
    line_profiler.runctx("g()", globals(), locals())


def test_another(line_profiler):
    line_profiler(g)
    line_profiler.runctx("g()", globals(), locals())
