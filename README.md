# pytest-line-profiler

[![PyPI version][]][1] [![Python versions][]][1] [![See Build Status on Travis CI][]][2]

line-by-line profiling for code executed by pytest, using [line-profiler](https://github.com/pyutils/line_profiler).

## Why?

Line profiler is a wonderful tool to easily identify bottlenecks inside specific functions of your code, and quantify the improvements after a refactor. 

Using it is straightforward but required to instrument the functions you want to profile with a "virtual" `@profile` decorator
and then execute "a trigger script" (code that calls the decorated functions somehow) via `kernprof.py` which works as a python wrapper that understands the decorator, register the functions to be profiled, and print the stats when the script finishes.   

Altought it does its job, is a bit invasive: you need to have an special "instrumented" version of your code, 
and execute it in a way that potentially clashes with the way you do normally (for instance, through a shortcut command from your editor, a test runner, another script, etc.)   

Moreover, frequently in real case scenarios, "a trigger script" isn't just a simple function call. 
You need to prepare input data, connect to external resources, etc.  And that's exactly what a test can do, right?    

## Installation 

You can install "pytest-line-profiler" via [pip][] from [PyPI][]:

```
$ pip install pytest-line-profiler
```

## Usage


Mark your test passing the functions you wants to profile as positional arguments, 
like `@pytest.mark.line_profile.with_args(function1, function2, [...])`

If your test exercises any of those functions, you'll get the profile result as a report.  

For example:

```python
import pytest

def f(i):
    return i * 10

def g(n=10):
    return sum(f(i) for i in range(10))


@pytest.mark.line_profile.with_args(f, g)
def test_as_mark():
    assert g() == 450

```


After that test is executed, you'll get the stats from the line profiler instance. 

```
============ Line Profile result for tests/test_line_profiler.py::test_as_mark ============
Timer unit: 1e-06 s

Total time: 4e-06 s
File: /home/tin/lab/pytest-line-profiler/tests/test_line_profiler.py
Function: f at line 4

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     4                                           def f(i):
     5        10          4.0      0.4    100.0      return i * 10

Total time: 3e-05 s
File: /home/tin/lab/pytest-line-profiler/tests/test_line_profiler.py
Function: g at line 7

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     7                                           def g(n=10):
     8         1         30.0     30.0    100.0      return sum(f(i) for i in range(10))
```


Alternatively, you can run any test passing the function/s to profile from the command line

```
$ pytest --line-profile path.to.function_to_be profiled [...] 
```


## Contributing

Contributions are very welcome. Tests can be run with [pytest][], please
ensure the coverage at least stays the same before you submit a pull
request.

## License

Distributed under the terms of the [MIT][] license,
"pytest-line-profiler" is free and open source software

## Issues

If you encounter any problems, please [file an issue][] along with a
detailed description.

  [PyPI version]: https://img.shields.io/pypi/v/pytest-line-profiler.svg
  [1]: https://pypi.org/project/pytest-line-profiler
  [Python versions]: https://img.shields.io/pypi/pyversions/pytest-line-profiler.svg
  [See Build Status on Travis CI]: https://travis-ci.com/mgaitan/pytest-line-profiler.svg?branch=main
  [2]: https://travis-ci.org/mgaitan/pytest-line-profiler
  [pip]: https://pypi.org/project/pip/
  [PyPI]: https://pypi.org/project
  [pytest]: https://github.com/pytest-dev/pytest
  [MIT]: http://opensource.org/licenses/MIT
  [file an issue]: https://github.com/mgaitan/pytest-line-profiler/issues
