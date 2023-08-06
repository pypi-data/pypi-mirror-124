# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eventsourcing_sqlalchemy']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy-Utils>=0.37.9,<0.38.0',
 'SQLAlchemy>=1.4.26,<2.0.0',
 'eventsourcing[crypto]>=9.1.0,<10.0.0']

setup_kwargs = {
    'name': 'eventsourcing-sqlalchemy',
    'version': '0.1.1',
    'description': 'Python package for eventsourcing with SQLAlchemy.',
    'long_description': '# Event Sourcing in Python with SQLAlchemy\n\nThis package supports using the Python [eventsourcing](https://github.com/johnbywater/eventsourcing) library with [SQLAlchemy](https://www.sqlalchemy.org/).\n\n\n## Installation\n\nUse pip to install the [stable distribution](https://pypi.org/project/eventsourcing_sqlalchemy/)\nfrom the Python Package Index. Please note, it is recommended to\ninstall Python packages into a Python virtual environment.\n\n    $ pip install eventsourcing_sqlalchemy\n\n\n## Synopsis\n\nTo use SQLAlchemy with your Python eventsourcing application, use the topic `eventsourcing_sqlalchemy.factory:Factory` as the `INFRASTRUCTURE_FACTORY`\nenvironment variable, and set an SQLAlchemy database URL as the value of\nenvironment variable `SQLALCHEMY_URL`.\n\nFirst define a domain model and application, in the usual way.\n\n```python\nfrom eventsourcing.application import Application\nfrom eventsourcing.domain import Aggregate, event\n\n\nclass World(Aggregate):\n    def __init__(self):\n        self.history = []\n\n    @event("SomethingHappened")\n    def make_it_so(self, what):\n        self.history.append(what)\n\n\nclass Worlds(Application):\n    is_snapshotting_enabled = True\n\n    def create_world(self):\n        world = World()\n        self.save(world)\n        return world.id\n\n    def make_it_so(self, world_id, what):\n        world = self.repository.get(world_id)\n        world.make_it_so(what)\n        self.save(world)\n\n    def get_world_history(self, world_id):\n        world = self.repository.get(world_id)\n        return world.history\n```\n\nSet environment variables `INFRASTRUCTURE_FACTORY` and `SQLALCHEMY_URL`.\nSee the [SQLAlchemy documentation](https://docs.sqlalchemy.org/en/14/core/engines.html) for more information about SQLAlchemy Database URLs.\n\n```python\nimport os\n\nos.environ.update({\n    "INFRASTRUCTURE_FACTORY": "eventsourcing_sqlalchemy.factory:Factory",\n    "SQLALCHEMY_URL": "sqlite:///:memory:",\n})\n```\n\nConstruct and use the application.\n\n```python\n# Construct the application.\napp = Worlds()\n\n# Call application command methods.\nworld_id = app.create_world()\napp.make_it_so(world_id, "dinosaurs")\napp.make_it_so(world_id, "trucks")\napp.make_it_so(world_id, "internet")\n\n# Call application query methods.\nhistory = app.get_world_history(world_id)\nassert history == ["dinosaurs", "trucks", "internet"]    \n```\n\nThese settings can be used with others supported by the library,\nfor example to enable application-level compression and encryption\nof stored events, set `COMPRESSOR_TOPIC` and `CIPHER_KEY`.\n\n```python\nfrom eventsourcing.cipher import AESCipher\n\n\n# Generate a cipher key (keep this safe).\ncipher_key = AESCipher.create_key(num_bytes=32)\n\n# Set environment variables.\nos.environ.update({\n    "COMPRESSOR_TOPIC": "zlib",\n    "CIPHER_KEY": cipher_key,\n})\n\n# Construct the application.\napp = Worlds()\n```\n\nWe can see the application is using the SQLAlchemy infrastructure,\nand that compression and encryption are enabled, by checking the\nattributes of the application object.\n\n```python\nfrom eventsourcing_sqlalchemy.datastore import SQLAlchemyDatastore\nfrom eventsourcing_sqlalchemy.factory import Factory\nfrom eventsourcing_sqlalchemy.recorders import SQLAlchemyAggregateRecorder\nfrom eventsourcing_sqlalchemy.recorders import SQLAlchemyApplicationRecorder\nfrom eventsourcing_sqlalchemy.models import StoredEventRecord\nfrom eventsourcing_sqlalchemy.models import SnapshotRecord\nimport zlib\n\nassert isinstance(app.factory, Factory)\nassert isinstance(app.factory.datastore, SQLAlchemyDatastore)\nassert isinstance(app.events.recorder, SQLAlchemyApplicationRecorder)\nassert isinstance(app.snapshots.recorder, SQLAlchemyAggregateRecorder)\nassert issubclass(app.events.recorder.events_record_cls, StoredEventRecord)\nassert issubclass(app.snapshots.recorder.events_record_cls, SnapshotRecord)\nassert isinstance(app.mapper.cipher, AESCipher)\nassert app.mapper.compressor == zlib\n```\n\nFor more information, please refer to the Python\n[eventsourcing](https://github.com/johnbywater/eventsourcing) library\nand the [SQLAlchemy](https://www.sqlalchemy.org/) project.\n',
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
