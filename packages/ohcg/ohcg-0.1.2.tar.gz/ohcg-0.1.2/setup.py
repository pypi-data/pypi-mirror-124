# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ohcg']

package_data = \
{'': ['*'], 'ohcg': ['templates/*']}

install_requires = \
['httpx>=0.19.0,<0.20.0',
 'jinja2>=3.0.1,<4.0.0',
 'pydantic[email]>=1.8.2,<2.0.0',
 'pydash>=5.0.2,<6.0.0',
 'typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['ohcg = ohcg.main:app']}

setup_kwargs = {
    'name': 'ohcg',
    'version': '0.1.2',
    'description': 'OpenAPI3 HTTP client generator',
    'long_description': '# ohcg - OpenAPI3 HTTP client generator\n[![PyPI version shields.io](https://img.shields.io/pypi/v/ohcg.svg)](https://pypi.python.org/pypi/ohcg/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/ohcg.svg)](https://pypi.python.org/pypi/ohcg/)\n[![PyPI license](https://img.shields.io/pypi/l/ohcg.svg)](https://pypi.python.org/pypi/ohcg/)\n\n> **This package was developed for private use with [FastAPI](https://github.com/tiangolo/fastapi) and it doesn\'t cover all OpenAPI specifications.**\n\n### Installation\n```shell\npip install ohcg\n```\nor \n```shell\npoetry add ohcg\n```\n\n### Usage\n```shell\nUsage: ohcg generate [OPTIONS] URL\n\n  Generate client from specified url\n\nArguments:\n  URL  [required]\n\nOptions:\n  -o, --output-dir DIRECTORY      directory for generated models and client\n                                  instance  [required]\n  -a, --auth, --authorization-header TEXT\n  --help                          Show this message and exit.\n\n```\n\n### Example\n```shell\nohcg generate -o my_output_dir https://raw.githubusercontent.com/OAI/OpenAPI-Specification/main/examples/v3.0/petstore.json\n```\n#### my_output_dir/models.py\n```python\nfrom __future__ import annotations\n\nimport typing\n\nfrom .base_model import (\n    _BaseListModel,\n    _BaseModel,\n)\n\n\nclass Pet(_BaseModel):\n    id: int\n    name: str\n    tag: typing.Optional[str]\n\n\nclass Pets(_BaseListModel):\n    pass\n\n\nclass Error(_BaseModel):\n    code: int\n    message: str\n```\n\n#### my_output_dir/client.py\n```python\nfrom json import JSONDecodeError\nfrom typing import Type\n\nimport httpx\n\nfrom .models import *\n\n\nclass Client:\n    """\n    Swagger Petstore @ 1.0.0\n    """\n\n    def __init__(self, base_url: str = None, **kwargs):\n        self.httpx_client = httpx.AsyncClient(base_url=base_url, **kwargs)\n\n    async def make_request(\n            self,\n            method: str,\n            path: str,\n            *,\n            response_model: Type = None,\n            errors_models: dict[int, Type[BaseModel]] = None,\n            **kwargs\n    ):\n        async with self.httpx_client as client:\n            response = await client.request(method, path, **kwargs)\n\n        if response.is_error:\n            if errors_models is None:\n                errors_models = {}\n\n            error_model = errors_models.get(response.status_code)\n\n            if bool(error_model):\n                try:\n                    raise parse_obj_as(error_model, response.json())\n                except (JSONDecodeError, pydantic.ValidationError):\n                    response.raise_for_status()\n        else:\n            # Raise error if request is not succeeded before trying to parse response\n            response.raise_for_status()\n\n        response_json = response.json()\n\n        if bool(response_model):\n            return pydantic.parse_obj_as(response_model, response_json)\n\n        return response_json\n\n    async def get_pets(\n            self,\n            *,\n            limit: int = None,\n    ) -> Pets:\n        """\n        List all pets\n        """\n        return await self.make_request(\n            "get",\n            "/pets",\n            response_model=Pets,\n            params={\n                "limit": limit,\n            },\n        )\n\n    async def post_pets(\n            self,\n    ):\n        """\n        Create a pet\n        """\n        return await self.make_request(\n            "post",\n            "/pets",\n        )\n\n    async def get_pets_pet_id(\n            self,\n            pet_id: str,\n    ) -> Pet:\n        """\n        Info for a specific pet\n        """\n        return await self.make_request(\n            "get",\n            "/pets/{petId}".format(petId=pet_id),\n            response_model=Pet,\n        )\n```\n\n\n#### my_output_dir/base_model.py\n```python\nfrom typing import (\n    Generic,\n    TypeVar,\n)\n\nimport pydantic\n\n\nclass _BaseModel(pydantic.BaseModel):\n    class Config:\n        allow_population_by_field_name = True\n\n\nclass _Error(_BaseModel, Exception):\n    pass\n\n\nListItemType = TypeVar(\'ListItemType\', bound=_BaseModel)\n\n\nclass _BaseListModel(pydantic.BaseModel, Generic[ListItemType]):\n    __root__: list[ListItemType]\n\n    def __iter__(self):\n        return iter(self.__root__)\n\n    def __getitem__(self, item):\n        return self.__root__[item]\n\n```\n\n## Roadmap\n- [x] Basic models and client generator\n- [ ] Any OpenAPI types support for generated models (including allOf, anyOf, etc.)\n- [ ] Cookie and headers parameters support\n- [ ] Auth and security schemas support\n- [ ] Sync version with httpx\n- [ ] Sync version with requests\n- [ ] Async version with aiohttp\n\n## LICENSE\nThis project is licensed under the terms of the MIT license.',
    'author': 'Pylakey',
    'author_email': 'pylakey@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pylakey/ohcg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
