# PyLog2PDF

[![PyPI](https://img.shields.io/pypi/v/PyLog2PDF.svg?label=PyPI&style=flat-square)](https://pypi.org/pypi/PyLog2PDF/)
[![Python](https://img.shields.io/pypi/pyversions/PyLog2PDF.svg?label=Python&color=yellow&style=flat-square)](https://pypi.org/pypi/PyLog2PDF/)
[![Test](https://img.shields.io/github/workflow/status/KaoruNishikawa/PyLog2PDF/Test?logo=github&label=Test&style=flat-square)](https://github.com/KaoruNishikawa/PyLog2PDF/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square)](LICENSE)

PDF, a visualisation of your calculation, can have essentials of your code.

## Features

This library provides:

- Log of Python classes and/or functions you employed.
- Interface to save the log to PDF file.

## Installation

```shell
pip install pylog2pdf
```

## Usage

### Log your classes and/or functions

```Python
>>> from pylog2pdf import LoggedClass, LoggedFunction

# Define your class or function with decorator
>>> @LoggedClass
... class MyNewClass:
...     pass

>>> @LoggedFunction
... def my_new_function():
...     pass

# Or using them as normal functions
>>> OtherLoggedClass = LoggedClass(OtherClass)
>>> other_logged_function = LoggedFunction(other_function)
```

I strongly recommend the use of class inheritance like the following. It's quite useful when determining which parameter is employed in calculation.

```Python
@LoggedClass
class Sun:

    distance: u.Quantity
    radius: u.Quantity

    def some_calculation(self, ...):
        pass

    def other_calculation(self, ...):
        pass


class ThisThesis(Sun):
    distance = 1.5e8 << u.m
    radius = 696e3 << u.km

class OtherThesis(Sun):
    distance = 1 << u.AU
    radius = 695e3 << u.km
```

When you use `ThisThesis` class, the log will be:

```Python
>>> pylog2pdf.LOG
{'Sun': 'ThisThesis'}
```

Of cource you can manually add anything you want to save:

```Python
>>> pylog2pdf["ThisParameter"] = 100 << u.K
```

### Save the log to PDF file

Write the log to pdf file:

```Python
>>> pdf_path = "path/to/figure.pdf"
>>> fig.savefig(pdf_path)  # Create a pdf file first
>>> pylog2pdf.write_log(pdf_path)
```

Then you can read the log:

```Python
>>> pdf_path = "path/to/pdf/you/saved.pdf"
>>> pylog2pdf.read_log(pdf_path)
{'Sun': 'ThisThesis'}
```

---

This library is using [Semantic Versioning](https://semver.org).
