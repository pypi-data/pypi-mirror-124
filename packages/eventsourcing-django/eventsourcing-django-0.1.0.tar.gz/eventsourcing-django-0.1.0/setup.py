# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eventsourcing_django', 'eventsourcing_django.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.0.0,<4.0.0', 'eventsourcing[crypto]>=9.1.0,<10.0.0']

setup_kwargs = {
    'name': 'eventsourcing-django',
    'version': '0.1.0',
    'description': 'Python package for eventsourcing with Django.',
    'long_description': '# Event Sourcing in Python with Django\n\nThis package is a Django app that supports using the Python\n[eventsourcing](https://github.com/johnbywater/eventsourcing) library\nwith the [Django ORM](https://www.djangoproject.com/).\n\n## Installation\n\nUse pip to install the [stable distribution](https://pypi.org/project/eventsourcing_django/)\nfrom the Python Package Index. Please note, it is recommended to\ninstall Python packages into a Python virtual environment.\n\n    $ pip install eventsourcing_django\n\n\n## Synopsis\n\nTo use Django with your Python eventsourcing application, use the topic `eventsourcing_django.factory:Factory` as the `INFRASTRUCTURE_FACTORY`\nenvironment variable.\n\nFirst define a domain model and application, in the usual way. You may set the\n`INFRASTRUCTURE_FACTORY` environment variable on the application class, so it\ncan always use the Django ORM for storing events.\n\n```python\nfrom eventsourcing.application import Application\nfrom eventsourcing.domain import Aggregate, event\n\n\nclass World(Aggregate):\n    def __init__(self):\n        self.history = []\n\n    @event("SomethingHappened")\n    def make_it_so(self, what):\n        self.history.append(what)\n\n\nclass Worlds(Application):\n    env = {\n        "INFRASTRUCTURE_FACTORY": "eventsourcing_django.factory:Factory",\n        "IS_SNAPSHOTTING_ENABLED": "yes",\n    }\n    snapshotting_intervals = {\n        World: 5,\n    }\n\n    def create_world(self):\n        world = World()\n        self.save(world)\n        return world.id\n\n    def make_it_so(self, world_id, what):\n        world = self.repository.get(world_id)\n        world.make_it_so(what)\n        self.save(world)\n\n    def get_world_history(self, world_id):\n        world = self.repository.get(world_id)\n        return world.history\n```\n\nSetup Django, in the usual way.\n\n```python\nimport os\n\nimport django\nfrom django.core.management import call_command\n\n\n# Set DJANGO_SETTINGS_MODULE.\nos.environ.update({\n    "DJANGO_SETTINGS_MODULE": "tests.djangoproject.settings",\n})\n\n# Setup Django.\ndjango.setup()\n\n# Setup the database.\ncall_command(\'migrate\', \'eventsourcing_django\')\n```\n\nThe application\'s environment can use other environment variables\nsupported by the library, for example to enable application-level\ncompression and encryption of stored events, set `COMPRESSOR_TOPIC`\nand `CIPHER_KEY`.\n\n```python\nfrom eventsourcing.cipher import AESCipher\n\n\n# Generate a cipher key (keep this safe).\ncipher_key = AESCipher.create_key(num_bytes=32)\n\n# Set environment variables.\nos.environ.update({\n    "COMPRESSOR_TOPIC": "zlib",\n    "CIPHER_KEY": cipher_key,\n})\n```\n\nConstruct and use the application. You may wish to do this\nwithin your Django project. The application can be created\non a signal when the project is ready (use the ready() method\nof the AppConfig class in your Django app\'s apps.py module).\nThe application command and query methods may be called\nfrom Django view and form classes.\n\n```python\n# Construct the application.\napp = Worlds()\n\n# Call application command methods.\nworld_id = app.create_world()\napp.make_it_so(world_id, "dinosaurs")\napp.make_it_so(world_id, "trucks")\napp.make_it_so(world_id, "internet")\napp.make_it_so(world_id, "covid")\n\n# Call application query methods.\nhistory = app.get_world_history(world_id)\nassert history == ["dinosaurs", "trucks", "internet", "covid"]\n```\n\nWe can see the automatic snapshotting is working, by looking\nin the snapshots store.\n\n```python\nsnapshots = list(app.snapshots.get(world_id))\nassert len(snapshots) == 1\n```\n\nWe can see the application is using the Django infrastructure,\nand that compression and encryption are enabled, by checking the\nattributes of the application object.\n\n```python\nfrom eventsourcing_django.factory import Factory\nfrom eventsourcing_django.recorders import DjangoAggregateRecorder\nfrom eventsourcing_django.recorders import DjangoApplicationRecorder\nfrom eventsourcing_django.models import StoredEventRecord\nfrom eventsourcing_django.models import SnapshotRecord\nimport zlib\n\nassert isinstance(app.factory, Factory)\nassert isinstance(app.events.recorder, DjangoApplicationRecorder)\nassert isinstance(app.snapshots.recorder, DjangoAggregateRecorder)\nassert issubclass(app.events.recorder.model, StoredEventRecord)\nassert issubclass(app.snapshots.recorder.model, SnapshotRecord)\nassert isinstance(app.mapper.cipher, AESCipher)\nassert app.mapper.compressor == zlib\n```\n\nFor more information, please refer to the Python\n[eventsourcing](https://github.com/johnbywater/eventsourcing) library\nand the [Django](https://www.djangoproject.com/) project.\n',
    'author': 'John Bywater',
    'author_email': 'john.bywater@appropriatesoftware.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://eventsourcing.readthedocs.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
