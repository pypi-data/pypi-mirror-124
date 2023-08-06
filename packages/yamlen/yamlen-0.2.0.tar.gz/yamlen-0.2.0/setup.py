# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yamlen', 'yamlen.tag', 'yamlen.tag.impl']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=6.0,<7.0']

setup_kwargs = {
    'name': 'yamlen',
    'version': '0.2.0',
    'description': 'A PyYAML thin wrapper.',
    'long_description': '# Yamlen - a Thin PyYAML Wrapper\n\n[![CircleCI](https://circleci.com/gh/ymoch/yamlen.svg?style=svg)][Circle CI]\n[![Codecov](https://codecov.io/gh/ymoch/yamlen/branch/main/graph/badge.svg)][Codecov]\n\n## Features\n- Contextual tag construction.\n\n## Examples\n\n### Create a Loader\n```\n>>> from yamlen import Loader\n>>> loader = Loader()\n\n```\n\n\n### Load YAML documents in Streams\n\n```\n>>> from io import StringIO\n\n>>> stream = StringIO("foo")\n>>> loader.load(stream)\n\'foo\'\n\n>>> stream = StringIO("foo\\n---\\nbar")\n>>> list(loader.load_all(stream))\n[\'foo\', \'bar\']\n\n```\n\n### Load YAML Documents in Files.\n\n```\n>>> import os\n>>> from tempfile import TemporaryDirectory\n\n>>> with TemporaryDirectory() as dir_path:\n...     path = os.path.join(dir_path, "example.yml")\n...     with open(path, "w") as f:\n...         _ = f.write("foo")\n...     loader.load_from_path(path)\n\'foo\'\n\n>>> with TemporaryDirectory() as dir_path:\n...     path = os.path.join(dir_path, "example.yml")\n...     with open(path, "w") as f:\n...         _ = f.write("foo\\n---\\nbar")\n...     list(loader.load_all_from_path(path))\n[\'foo\', \'bar\']\n\n```\n\n### Contextual tag construction: include another YAML file.\n\n```\n>>> from yamlen.tag.impl.inclusion import InclusionTag\n>>> loader.add_tag("!include", InclusionTag())\n\n```\n\n```\n>>> with TemporaryDirectory() as dir_path:\n...     foo_path = os.path.join(dir_path, "foo.yml")\n...     bar_path = os.path.join(dir_path, "bar.yml")\n...     with open(foo_path, "w") as f:\n...         _ = f.write(f"!include ./bar.yml")\n...     with open(bar_path, "w") as f:\n...         _ = f.write("bar")\n...     loader.load_from_path(foo_path)\n\'bar\'\n\n```\n\n## License\n\n[![MIT License](https://img.shields.io/badge/License-MIT-brightgreen.svg)][MIT License]\n\nCopyright (c) 2021 Yu Mochizuki\n\n[Circle CI]: https://circleci.com/gh/ymoch/yamlen\n[Codecov]: https://codecov.io/gh/ymoch/yamlen\n[MIT License]: https://opensource.org/licenses/MIT\n',
    'author': 'Yu Mochizuki',
    'author_email': 'ymoch.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ymoch/yamlen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
