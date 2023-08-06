# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hydratokengen']

package_data = \
{'': ['*']}

install_requires = \
['ory-hydra-client>=1.10.6,<2.0.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'hydratokengen',
    'version': '0.1.0',
    'description': '',
    'long_description': '# HydraTokenGen\n\nORY Hydra JWT generator.\n\n## Install\n\n```sh\npip install hydratokengen\n```\n\n## Usage\n\n```py\nfrom hydratokengen import CachedTokenGen, HydraTokenGen\n\nhydra_token_gen = CachedTokenGen(HydraTokenGen(\n    hydra_public_url="http://localhost:4444",\n    hydra_admin_url="http://localhost:4445",\n    client_id="636986d6-f505-486a-839c-57bb6a881aca",\n    client_secret="CLIENTSECRET",\n    redirect_uri="http://localhost/callback",\n))\n\ntoken = hydra_token_gen.generate(\n    subject="1234",\n    access_token={"claim1": "value1"},\n    id_token={"claim2": "value2"},\n)\n```\n\n## Development\n\n### Format code\n\n```sh\npoetry run black hydratokengen tests\n```\n\n### Testing\n\nStart Hydra:\n\n```sh\ndocker-compose up -d\n```\n\nInstall dependencies:\n\n```sh\npoetry install\n```\n\nRun tests\n\n```sh\npoetry run pytest\n```\n\nHTML coverage report:\n\n```sh\npoetry run pytest --cov=hydratokengen --cov-report=html\n\nopen htmlcov/index.html\n```\n\n### Publish a new version\n\nBump the version number in `hydratokengen/__init__.py` and run:\n\n```sh\npoetry publish\n```\n',
    'author': 'Luka Zakrajšek',
    'author_email': 'luka@bancek.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/reciprocity/hydratokengen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
