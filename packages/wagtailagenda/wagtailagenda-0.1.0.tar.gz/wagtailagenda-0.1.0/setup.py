# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wagtailagenda', 'wagtailagenda.migrations']

package_data = \
{'': ['*'],
 'wagtailagenda': ['templates/wagtailagenda/activity.html',
                   'templates/wagtailagenda/activity.html',
                   'templates/wagtailagenda/agenda.html',
                   'templates/wagtailagenda/agenda.html']}

install_requires = \
['ics>=0.7,<0.8', 'wagtail>=2.14.1,<3.0.0', 'wagtailperson>=0.13.2,<0.14.0']

setup_kwargs = {
    'name': 'wagtailagenda',
    'version': '0.1.0',
    'description': 'An aganda app for Wagtail',
    'long_description': '# Wagtail Agenda #\n\nAn aganda app for Wagtail.\n\nThis app is designed to be used in 2 cases:\n* The agenda of an organisation, like a club or an association, with\n  an archive for past activities\n* The programme of an convention, with no archive and all activities\n  can be seen on the agenda independently of the actual hour and date\n\nWith this app, you can:\n* Have one or more aganda\n* One or more activities by agenda\n* Each agenda can have an archive: If enabled, past activities can\n  only be seen on the archive\n* Each activity have a location\n* Each location can have description, address, floor, the list of\n  nearby public transport stops and images\n* Each aganda provide an ICS online agenda\n\n\n## Status ##\n\nThe dev of this app just started.\n\nTodo: Everything.\n\n\n## Install on your Wagtail website ##\n\nTBD\n\n\n## Install for dev ##\n\nTBD\n\n\n## Licence ##\n\nAGPLv3\n\n\n## Author ##\n\nSébastien Gendre <seb@k-7.ch>\n',
    'author': 'Sébastien Gendre',
    'author_email': 'seb@k-7.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://framagit.org/SebGen/wagtail-agenda',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
