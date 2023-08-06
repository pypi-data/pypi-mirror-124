# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests', 'typesafe_parmap']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'typesafe-parmap',
    'version': '0.1.0',
    'description': 'Run functions in parallel safely with typesafe parmap!.',
    'long_description': '# typesafe_parmap\n\n\n[![pypi](https://img.shields.io/pypi/v/typesafe_parmap.svg)](https://pypi.org/project/typesafe_parmap/)\n[![python](https://img.shields.io/pypi/pyversions/typesafe_parmap.svg)](https://pypi.org/project/typesafe_parmap/)\n[![Build Status](https://github.com/thejaminator/typesafe_parmap/actions/workflows/dev.yml/badge.svg)](https://github.com/thejaminator/typesafe_parmap/actions/workflows/dev.yml)\n\n\n\nRun functions in parallel safely with typesafe parmap!\n\n\n* GitHub: <https://github.com/thejaminator/typesafe_parmap>\n* PyPI: <https://pypi.org/project/typesafe_parmap/>\n\n\n## Features\n\nEasy run different functions in parallel!\n```\nimport time\nfrom concurrent.futures import ThreadPoolExecutor\nfrom typesafe_parmap.parmap import par_map_2\n\ntp = ThreadPoolExecutor(5)\n\ndef long_running_int(param: int) -> int:\n    time.sleep(5)  # long IO task here\n    return 123\n\ndef long_running_str(param: str) -> str:\n    time.sleep(5)  # long IO task here\n    return "hello world"\n\nint_result, str_result = par_map_2(\n                        lambda: long_running_int(5),\n                        lambda: long_running_str("test"),\n                        executor=tp)\nassert int_result == 123, str_result == "hello world"  # should finish in 5 seconds\n```\n\nFunction return types are inferred correctly by mypy / pycharm!\n\n```\nreveal_type(int_result) # mypy infers int\nreveal_type(str_result) # mypy infers str\n```\n',
    'author': 'James Chua',
    'author_email': 'chuajamessh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thejaminator/typesafe_parmap',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
