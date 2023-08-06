# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['come_again_question_mark']

package_data = \
{'': ['*']}

install_requires = \
['progressbar2>=3.53.3,<4.0.0', 'srt>=3.5.0,<4.0.0', 'vosk>=0.3.30,<0.4.0']

setup_kwargs = {
    'name': 'come-again-question-mark',
    'version': '0.1.7',
    'description': 'Transcription tool for video or audio to text',
    'long_description': None,
    'author': 'Henry Bergström',
    'author_email': 'henrybergstrom@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
