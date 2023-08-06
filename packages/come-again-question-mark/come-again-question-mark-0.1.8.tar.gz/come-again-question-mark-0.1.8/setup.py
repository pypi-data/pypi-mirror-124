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
    'version': '0.1.8',
    'description': 'Transcription tool for video or audio to text',
    'long_description': '# Come Again?\nVideo-To-Text tool for MetaProvide. Useful when you want to read what was said in a video (or audio clip)\n\n## Requirements\n- Python3\n- Poetry\n- FFMPEG\n\n## How to use\n1. Clone repo `git clone https://github.com/MetaProvide/ComeAgainQuestionMark.git` or download zip\n2. Run command `cd ComeAgainQuestionMark && poetry install` to install dependencies\n3. Download a model from [here](https://alphacephei.com/vosk/models) and unzip\n4. Run command `poetry run python3 comeAgainQuestionMark -m [PATH-TO-MODEL-FOLDER] -i [PATH-TO-VIDEO-INPUT] -o [PATH-TO-TEXT-OUTPUT]`\n5. Open file `[PATH-TO-TEXT-OUTPUT]` to see your results\n\n## Note\nDifferent model yields different transcritions.\n\n## License\nThis program is licensed under the GPLv3 or later.\n',
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
