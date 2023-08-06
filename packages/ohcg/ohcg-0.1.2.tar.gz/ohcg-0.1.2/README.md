# ohcg - OpenAPI3 HTTP client generator
[![PyPI version shields.io](https://img.shields.io/pypi/v/ohcg.svg)](https://pypi.python.org/pypi/ohcg/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/ohcg.svg)](https://pypi.python.org/pypi/ohcg/)
[![PyPI license](https://img.shields.io/pypi/l/ohcg.svg)](https://pypi.python.org/pypi/ohcg/)

> **This package was developed for private use with [FastAPI](https://github.com/tiangolo/fastapi) and it doesn't cover all OpenAPI specifications.**

### Installation
```shell
pip install ohcg
```
or 
```shell
poetry add ohcg
```

### Usage
```shell
Usage: ohcg generate [OPTIONS] URL

  Generate client from specified url

Arguments:
  URL  [required]

Options:
  -o, --output-dir DIRECTORY      directory for generated models and client
                                  instance  [required]
  -a, --auth, --authorization-header TEXT
  --help                          Show this message and exit.

```

### Example
```shell
ohcg generate -o my_output_dir https://raw.githubusercontent.com/OAI/OpenAPI-Specification/main/examples/v3.0/petstore.json
```
#### my_output_dir/models.py
```python
from __future__ import annotations

import typing

from .base_model import (
    _BaseListModel,
    _BaseModel,
)


class Pet(_BaseModel):
    id: int
    name: str
    tag: typing.Optional[str]


class Pets(_BaseListModel):
    pass


class Error(_BaseModel):
    code: int
    message: str
```

#### my_output_dir/client.py
```python
from json import JSONDecodeError
from typing import Type

import httpx

from .models import *


class Client:
    """
    Swagger Petstore @ 1.0.0
    """

    def __init__(self, base_url: str = None, **kwargs):
        self.httpx_client = httpx.AsyncClient(base_url=base_url, **kwargs)

    async def make_request(
            self,
            method: str,
            path: str,
            *,
            response_model: Type = None,
            errors_models: dict[int, Type[BaseModel]] = None,
            **kwargs
    ):
        async with self.httpx_client as client:
            response = await client.request(method, path, **kwargs)

        if response.is_error:
            if errors_models is None:
                errors_models = {}

            error_model = errors_models.get(response.status_code)

            if bool(error_model):
                try:
                    raise parse_obj_as(error_model, response.json())
                except (JSONDecodeError, pydantic.ValidationError):
                    response.raise_for_status()
        else:
            # Raise error if request is not succeeded before trying to parse response
            response.raise_for_status()

        response_json = response.json()

        if bool(response_model):
            return pydantic.parse_obj_as(response_model, response_json)

        return response_json

    async def get_pets(
            self,
            *,
            limit: int = None,
    ) -> Pets:
        """
        List all pets
        """
        return await self.make_request(
            "get",
            "/pets",
            response_model=Pets,
            params={
                "limit": limit,
            },
        )

    async def post_pets(
            self,
    ):
        """
        Create a pet
        """
        return await self.make_request(
            "post",
            "/pets",
        )

    async def get_pets_pet_id(
            self,
            pet_id: str,
    ) -> Pet:
        """
        Info for a specific pet
        """
        return await self.make_request(
            "get",
            "/pets/{petId}".format(petId=pet_id),
            response_model=Pet,
        )
```


#### my_output_dir/base_model.py
```python
from typing import (
    Generic,
    TypeVar,
)

import pydantic


class _BaseModel(pydantic.BaseModel):
    class Config:
        allow_population_by_field_name = True


class _Error(_BaseModel, Exception):
    pass


ListItemType = TypeVar('ListItemType', bound=_BaseModel)


class _BaseListModel(pydantic.BaseModel, Generic[ListItemType]):
    __root__: list[ListItemType]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]

```

## Roadmap
- [x] Basic models and client generator
- [ ] Any OpenAPI types support for generated models (including allOf, anyOf, etc.)
- [ ] Cookie and headers parameters support
- [ ] Auth and security schemas support
- [ ] Sync version with httpx
- [ ] Sync version with requests
- [ ] Async version with aiohttp

## LICENSE
This project is licensed under the terms of the MIT license.