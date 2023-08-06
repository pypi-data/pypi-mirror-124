# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['notion_gcal_sync', 'notion_gcal_sync.clients', 'notion_gcal_sync.events']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'google-api-python-client==2.23.0',
 'google-auth-oauthlib==0.4.6',
 'notion-client==0.7.0',
 'pandas==1.3.3',
 'pyyaml==5.4.1']

entry_points = \
{'console_scripts': ['notion-gcal-sync = notion_gcal_sync.__main__:main']}

setup_kwargs = {
    'name': 'notion-gcal-sync',
    'version': '1.0.3',
    'description': 'Bidirectional synchronize calendar events within notion and google calendar',
    'long_description': '[![CI](https://github.com/Ravio1i/notion-gcal-sync/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Ravio1i/notion-gcal-sync/actions/workflows/ci.yml)\n[![PyPI version](https://badge.fury.io/py/notion-gcal-sync.svg)](https://badge.fury.io/py/notion-gcal-sync)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n# Notion-GCal-Sync\n\nNotion-GCal-Sync is a python application to bidirectional synchronize calendar events within notion and google calendar.\n\n## Getting started\n\nFollow [these instructions](https://github.com/Ravio1i/notion-gcal-sync/blob/main/docs/setup.md).\n\n## Usage\n\n**IMPORTANT:** Make sure you followed the [setup](https://github.com/Ravio1i/notion-gcal-sync/blob/main/docs/setup.md) and\nconfigured the `config.yml` with your notion token and page for Notion API and gathered and setup\ncredentials `client_secret.json` for Google Calendar API.\n\nFrom pip and running directly\n\n```bash\nnotion-gcal-sync\n```\n\nWith docker (Not the mounting of `client_secret.json` and `config.yml`)\n\n```yaml\ndocker run --net=host -it \\\n    -v $(pwd)/config.yml:/app/notion_gcal_sync/config.yml \\\n    -v $(pwd)/client_credentials.json:/app/notion_gcal_sync/client_credentials.json \\\n    notion-gcal-sync\n```\n\nOn first run or when token is old you will be asked to authorize the application. Follow the link and authorize with your\naccount. After authorization the application will continue.\n\n```bash\n$ notion-gcal-sync\n...\nPlease visit this URL to authorize this application:\nhttps://accounts.google.com/o/oauth2/auth?response_type=code&client_id=***\n```\n\n## Notes\n\nBE AWARE OF THE FOLLOWING:\n\n* This sync will update your source links in gcal. Links to mail etc. will get overwritten with a link to the notion page. The\n  original links will be put on top of the description\n* This sync will update all your invites from other calendars not specified to your default calendar. There is a button on gcal\n  to restore back\n* Goals defined from calendar apps are skipped.\n* Recurrent original events are skipped. Recurrent occurrences of events are created one by one in notion. Changing in notion\n  will change only an occurrence in GCal.\n\n## Notes\n\nWith around ~2500 events in gcal the sync:\n\n* to get all events took ~1min\n',
    'author': 'Luka Kroeger',
    'author_email': 'luka.kroeger@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Ravio1i/notion-gcal-sync',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4',
}


setup(**setup_kwargs)
