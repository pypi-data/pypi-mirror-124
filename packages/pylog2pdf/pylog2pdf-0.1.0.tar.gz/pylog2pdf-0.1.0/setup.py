# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylog2pdf']

package_data = \
{'': ['*']}

install_requires = \
['PyPDF2>=1.24.0,<2.0.0']

setup_kwargs = {
    'name': 'pylog2pdf',
    'version': '0.1.0',
    'description': 'PDF, a visualisation of your calculation, can have essentials of your code.',
    'long_description': '# PyLog2PDF\n\n[![PyPI](https://img.shields.io/pypi/v/PyLog2PDF.svg?label=PyPI&style=flat-square)](https://pypi.org/pypi/PyLog2PDF/)\n[![Python](https://img.shields.io/pypi/pyversions/PyLog2PDF.svg?label=Python&color=yellow&style=flat-square)](https://pypi.org/pypi/PyLog2PDF/)\n[![Test](https://img.shields.io/github/workflow/status/KaoruNishikawa/PyLog2PDF/Test?logo=github&label=Test&style=flat-square)](https://github.com/KaoruNishikawa/PyLog2PDF/actions)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square)](LICENSE)\n\nPDF, a visualisation of your calculation, can have essentials of your code.\n\n## Features\n\nThis library provides:\n\n- Log of Python classes and/or functions you employed.\n- Interface to save the log to PDF file.\n\n## Installation\n\n```shell\npip install pylog2pdf\n```\n\n## Usage\n\n### Log your classes and/or functions\n\n```Python\n>>> from pylog2pdf import LoggedClass, LoggedFunction\n\n# Define your class or function with decorator\n>>> @LoggedClass\n... class MyNewClass:\n...     pass\n\n>>> @LoggedFunction\n... def my_new_function():\n...     pass\n\n# Or using them as normal functions\n>>> OtherLoggedClass = LoggedClass(OtherClass)\n>>> other_logged_function = LoggedFunction(other_function)\n```\n\nI strongly recommend the use of class inheritance like the following. It\'s quite useful when determining which parameter is employed in calculation.\n\n```Python\n@LoggedClass\nclass Sun:\n\n    distance: u.Quantity\n    radius: u.Quantity\n\n    def some_calculation(self, ...):\n        pass\n\n    def other_calculation(self, ...):\n        pass\n\n\nclass ThisThesis(Sun):\n    distance = 1.5e8 << u.m\n    radius = 696e3 << u.km\n\nclass OtherThesis(Sun):\n    distance = 1 << u.AU\n    radius = 695e3 << u.km\n```\n\nWhen you use `ThisThesis` class, the log will be:\n\n```Python\n>>> pylog2pdf.LOG\n{\'Sun\': \'ThisThesis\'}\n```\n\nOf cource you can manually add anything you want to save:\n\n```Python\n>>> pylog2pdf["ThisParameter"] = 100 << u.K\n```\n\n### Save the log to PDF file\n\nWrite the log to pdf file:\n\n```Python\n>>> pdf_path = "path/to/figure.pdf"\n>>> fig.savefig(pdf_path)  # Create a pdf file first\n>>> pylog2pdf.write_log(pdf_path)\n```\n\nThen you can read the log:\n\n```Python\n>>> pdf_path = "path/to/pdf/you/saved.pdf"\n>>> pylog2pdf.read_log(pdf_path)\n{\'Sun\': \'ThisThesis\'}\n```\n\n---\n\nThis library is using [Semantic Versioning](https://semver.org).\n',
    'author': 'KaoruNishikawa',
    'author_email': 'k.nishikawa@a.phys.nagoya-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/KaoruNishikawa/PyLog2PDF',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
