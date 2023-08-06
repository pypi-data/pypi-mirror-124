import re
from datetime import (
    date,
    datetime,
    time,
    timedelta,
)
from decimal import Decimal
from ipaddress import (
    IPv4Address,
    IPv4Interface,
    IPv4Network,
    IPv6Address,
    IPv6Interface,
    IPv6Network,
)
from pathlib import Path
from re import Pattern
from typing import (
    Any,
    Optional,
    Union,
)
from uuid import UUID

import httpx
import jinja2
import pydantic
import pydash
from pydantic import UUID4

from . import openapi_models
from .openapi_models import (
    ContentType,
    Info,
    OpenAPISchema,
    ParameterPosition,
    PathItem,
    Schema,
    SuperStr,
)
from .utils import wrap_str

RE_APPLICATION_JSON_PATTERN = re.compile(r'^application/.*json$')

schema_to_field = {
    'true': bool,
    'false': bool,
    'null': None,
    'boolean': bool,
    'integer': int,
    'string': str,
    'array': list,
    'object': dict,
    'number': Decimal
}

field_class_by_format = {
    'integer': {
        'int32': int,
        'int64': int
    },
    'string': {
        'password': str,
        'byte': str,
        'binary': bytes,
        'path': Path,
        'date-time': datetime,
        'date': date,
        'time': time,
        'ipv4network': IPv4Network,
        'ipv6network': IPv6Network,
        'ipv4interface': IPv4Interface,
        'ipv6interface': IPv6Interface,
        'ipv4': IPv4Address,
        'ipv6': IPv6Address,
        'regex': Pattern,
        'uuid': UUID,
        'uuid4': UUID4,
        'email': pydantic.EmailStr,
    },
    'number': {
        'time-delta': timedelta,
        'float': float,
        'double': float
    }
}

braces_regex = re.compile(r'{.*?}')


class BaseModel(pydantic.BaseModel):
    class Config:
        allow_mutation = True


class Attribute(BaseModel):
    name: str
    type: str = None
    default: Optional[Any] = None
    title: Optional[str] = None
    description: Optional[str] = None
    nullable: bool = False
    deprecated: bool = False
    constraints: list[tuple[str, Any]] = []


class Model(BaseModel):
    name: SuperStr
    description: Optional[str]
    attributes: list[Attribute] = []
    # Enum specific
    is_enum: bool = False
    enum_type: str = False
    enum_members: list[tuple[str, Any]] = []
    need_update_forward_refs: bool = False
    is_error: bool = False
    # List specific
    is_list: bool = False
    items_type: Optional[str] = False


class Param(BaseModel):
    name: SuperStr
    type: Optional[str] = None
    description: Optional[str] = None
    required: bool = False
    deprecated: bool = False
    allow_empty_value: bool = False
    default: Optional[Any] = None


class RequestData(BaseModel):
    type: str
    description: Optional[str]
    required: bool = False
    content_type: Union[ContentType, str]


class Response(BaseModel):
    type: Optional[str]
    description: Optional[str]


class Operation(BaseModel):
    name: SuperStr
    path: str
    method: str
    summary: Optional[str] = None
    description: Optional[str] = None
    query_parameters: list[Param] = []
    path_parameters: list[Param] = []
    header_parameters: list[Param] = []
    cookie_parameters: list[Param] = []
    request_data: Optional[RequestData] = None
    response: Optional[Response] = None
    # { int_error_code: model_type_str }
    errors: dict[int, Optional[str]] = {}
    tags: list[str] = []

    @property
    def required_parameters(self):
        return [
            *[p for p in self.path_parameters if p.required and not bool(p.default)],
            *[p for p in self.query_parameters if p.required and not bool(p.default)],
            *[p for p in self.cookie_parameters if p.required and not bool(p.default)],
            *[p for p in self.header_parameters if p.required and not bool(p.default)],
        ]

    @property
    def optional_parameters(self):
        return [
            *[p for p in self.path_parameters if not p.required or bool(p.default)],
            *[p for p in self.query_parameters if not p.required or bool(p.default)],
            *[p for p in self.cookie_parameters if not p.required or bool(p.default)],
            *[p for p in self.header_parameters if not p.required or bool(p.default)],
        ]


class OpenAPIParserResult(BaseModel):
    info: Info
    models: list[Model] = []
    operations: list[Operation] = []


class OpenAPIParser:
    schema: OpenAPISchema
    models: dict[str, Model] = {}
    operations: list[Operation] = []

    def __init__(self, schema_uri: str, *, authorization_header: str = None, use_camel_case_alias: bool = False):
        self.schema_uri = schema_uri
        self.authorization_header = authorization_header or ""
        self.use_camel_case_alias = use_camel_case_alias

    def get_schema_python_type(
            self,
            schema: Schema,
            *,
            referencing_model_name: Optional[str] = None,
    ) -> Optional[str]:
        if bool(schema.ref):
            return self.get_or_create_model_by_ref(
                schema.ref,
                referencing_model_name=referencing_model_name
            ).name
        elif bool(schema.type):
            if bool(schema.format):
                return field_class_by_format.get(schema.type).get(schema.format).__name__
            elif bool(schema.additional_properties):
                additional_properties_type = self.get_schema_python_type(
                    schema.additional_properties,
                    referencing_model_name=referencing_model_name
                )
                return f"dict[str, {additional_properties_type}]"
            elif bool(schema.items):
                items_type = self.get_schema_python_type(
                    schema.items,
                    referencing_model_name=referencing_model_name
                )

                if schema.unique_items:
                    return f"set[{items_type}]"
                else:
                    return f"list[{items_type}]"

            return schema_to_field.get(schema.type).__name__
        elif bool(schema.any_of) or bool(schema.all_of) or bool(schema.one_of):
            list_of = schema.any_of or schema.all_of or schema.one_of or []

            if len(list_of) > 1:
                list_of_types = ", ".join(
                    self.get_schema_python_type(e, referencing_model_name=referencing_model_name)
                    for e in list_of
                )
                return f"typing.Union[{list_of_types}]"

            return self.get_schema_python_type(list_of[0], referencing_model_name=referencing_model_name)

        return None

    def create_model_from_schema(self, schema_name: str) -> Model:
        schema: Schema = self.schema.components.schemas[schema_name]
        model = Model(
            name=schema_name,
            description=schema.description,
        )

        if bool(schema.enum):
            enum_type = self.get_schema_python_type(schema)
            model.is_enum = True
            model.enum_type = self.get_schema_python_type(schema)
            model.enum_members = [
                (
                    pydash.snake_case(e).upper() if enum_type == 'str' else f"VALUE_{i}".upper(),
                    f"\"{e}\"" if enum_type == 'str' else e
                )
                for i, e in enumerate(schema.enum)
            ]
        elif bool(schema.type) and schema.type == 'array' and bool(schema.items):
            model.is_list = True
            model.items_type = self.get_schema_python_type(schema.items)
        elif bool(schema.all_of):
            # TODO:
            pass

        self.models[schema_name] = model
        model.attributes = self.make_model_attributes(schema_name)

        return self.models[schema_name]

    def make_model_attributes(self, schema_name: str) -> list[Attribute]:
        schema: Schema = self.schema.components.schemas[schema_name]

        if not bool(schema.properties):
            return []

        attributes = []

        for prop_name, prop_schema in schema.properties.items():
            prop_constraints = []
            prop_default = prop_schema.default
            prop_nullable = (prop_name not in schema.required) or prop_schema.nullable

            # Prop type hint
            prop_type_hint = self.get_schema_python_type(prop_schema, referencing_model_name=schema_name)

            if prop_nullable and prop_default is None:
                prop_type_hint = f"typing.Optional[{prop_type_hint}]"

            # Prop default
            if isinstance(prop_schema.default, str):
                prop_default = wrap_str(prop_schema.default)
            elif isinstance(prop_schema.default, list):
                prop_default = "[]"
            elif isinstance(prop_schema.default, dict):
                prop_default = "{}"
            elif isinstance(prop_schema.default, bool):
                prop_default = str(prop_schema.default)

            # pydantic.Field constraints
            if self.use_camel_case_alias:
                prop_camel_case_alias = pydash.camel_case(prop_name)

                if prop_name != prop_camel_case_alias:
                    prop_constraints.append(("alias", wrap_str(prop_camel_case_alias)))

            if prop_schema.exclusive_minimum is not None:
                prop_constraints.append(("gt", prop_schema.exclusive_minimum))

            if prop_schema.minimum is not None:
                prop_constraints.append(("ge", prop_schema.minimum))

            if prop_schema.exclusive_maximum is not None:
                prop_constraints.append(("lt", prop_schema.exclusive_maximum))

            if prop_schema.minimum is not None:
                prop_constraints.append(("le", prop_schema.maximum))

            if prop_schema.multiple_of is not None:
                prop_constraints.append(("multiple_of", prop_schema.multiple_of))

            if prop_schema.min_items is not None:
                prop_constraints.append(("min_items", prop_schema.min_items))

            if prop_schema.max_items is not None:
                prop_constraints.append(("max_items", prop_schema.max_items))

            if prop_schema.min_length is not None:
                prop_constraints.append(("min_length", prop_schema.min_length))

            if prop_schema.max_length is not None:
                prop_constraints.append(("max_length", prop_schema.max_length))

            if prop_schema.pattern is not None:
                prop_constraints.append(("regex", wrap_str(prop_schema.pattern, regex=True)))

            attribute = Attribute(
                name=prop_name,
                type=prop_type_hint,
                default=prop_default,
                title=prop_schema.title,
                description=prop_schema.description,
                nullable=prop_nullable,
                deprecated=prop_schema.deprecated,
                constraints=prop_constraints,
            )
            attributes.append(attribute)

        return attributes

    def get_or_create_model_by_ref(self, ref: str, *, referencing_model_name: Optional[str] = None) -> Model:
        model_name = ref.split('/')[-1]
        model = self.models.get(model_name)

        if not bool(model):
            model = self.create_model_from_schema(model_name)
            self.models[referencing_model_name].need_update_forward_refs = True

        return model

    def process_path_item_method(self, path: str, method: str):
        path_item: PathItem = self.schema.paths[path]
        operation_data: openapi_models.Operation = getattr(path_item, method)

        # name = operation_data.operation_id
        suffix = f"{method}_{pydash.snake_case(path)}"
        name = suffix
        # FastAPI workaround for better generated client methods naming
        # name = name.snake_case.replace(f"_{suffix}", '') if bool(name) else suffix

        path_parameters: list[Param] = []
        query_parameters: list[Param] = []
        header_parameters: list[Param] = []
        cookie_parameters: list[Param] = []

        for parameter in [*path_item.parameters, *operation_data.parameters]:
            param = Param(
                name=parameter.name,
                description=parameter.description,
                type=self.get_schema_python_type(parameter.parameter_schema),
                required=parameter.required,
                deprecated=parameter.deprecated,
                allow_empty_value=parameter.allow_empty_value,
                default=parameter.parameter_schema.default if bool(parameter.parameter_schema) else None,
            )

            if parameter.position == ParameterPosition.path:
                path_parameters.append(param)
            elif parameter.position == ParameterPosition.query:
                query_parameters.append(param)
            elif parameter.position == ParameterPosition.header:
                header_parameters.append(param)
            elif parameter.position == ParameterPosition.cookie:
                cookie_parameters.append(param)

        request_data: Optional[RequestData] = None

        if bool(operation_data.request_body):
            for content_type, media_type in operation_data.request_body.content.items():
                if content_type in [ContentType.APPLICATION_JSON, ContentType.APPLICATION_FORM]:
                    request_data = RequestData(
                        type=self.get_schema_python_type(media_type.media_type_schema),
                        required=operation_data.request_body.required,
                        description=operation_data.request_body.description,
                        content_type=content_type
                    )

        response: Optional[Response] = None
        errors: dict[int, Optional[str]] = {}

        if bool(operation_data.responses):
            for r_code, r in operation_data.responses.items():
                try:
                    r_code = int(r_code)
                except ValueError:
                    # TODO: support for default response code
                    continue

                for content_type, media_type in r.content.items():
                    if content_type in [ContentType.APPLICATION_JSON, ContentType.APPLICATION_FORM]:
                        if r_code // 100 == 2:
                            response = Response(
                                type=self.get_schema_python_type(media_type.media_type_schema),
                                description=r.description,
                            )
                        elif 400 <= r_code <= 599:
                            errors[r_code] = self.get_schema_python_type(media_type.media_type_schema)
                            model = self.models.get(errors[r_code])
                            if bool(model):
                                model.is_error = True

        operation = Operation(
            name=name,
            path=path,
            method=method,
            summary=operation_data.summary,
            description=operation_data.description,
            path_parameters=path_parameters,
            query_parameters=query_parameters,
            request_data=request_data,
            response=response,
            tags=operation_data.tags,
            errors=errors
        )

        self.operations.append(operation)

    def create_operation(self, path: str):
        path_item: PathItem = self.schema.paths[path]

        if bool(path_item.get):
            self.process_path_item_method(path, 'get')
        if bool(path_item.put):
            self.process_path_item_method(path, 'put')
        if bool(path_item.post):
            self.process_path_item_method(path, 'post')
        if bool(path_item.delete):
            self.process_path_item_method(path, 'delete')
        if bool(path_item.options):
            self.process_path_item_method(path, 'options')
        if bool(path_item.head):
            self.process_path_item_method(path, 'head')
        if bool(path_item.patch):
            self.process_path_item_method(path, 'patch')
        if bool(path_item.trace):
            self.process_path_item_method(path, 'trace')

    def parse(self) -> OpenAPIParserResult:
        response = httpx.get(
            self.schema_uri,
            headers={
                "Authorization": self.authorization_header
            }
        ).json()
        self.schema = OpenAPISchema.parse_obj(response)

        # Preparing models
        for schema_name in self.schema.components.schemas:
            self.create_model_from_schema(schema_name)

        # Preparing operations
        for path in self.schema.paths:
            self.create_operation(path)

        return OpenAPIParserResult(
            info=self.schema.info,
            models=list(self.models.values()),
            operations=self.operations,
        )


def generate_code(url: str, output_dir: Path, authorization_header: str = None):
    parser = OpenAPIParser(url, authorization_header=authorization_header)
    result = parser.parse()

    output_dir.mkdir(exist_ok=True)
    env = jinja2.Environment(
        loader=jinja2.PackageLoader("ohcg", "templates"),
        autoescape=jinja2.select_autoescape(['jinja2'])
    )
    client_template = env.get_template('client.jinja2')
    base_model_template = env.get_template('base_model.jinja2')
    models_template = env.get_template('models.jinja2')

    with open(f"{output_dir}/client.py", 'w+') as file:
        file.write(client_template.render(result=result))

    with open(f"{output_dir}/base_model.py", 'w+') as file:
        file.write(base_model_template.render(result=result))

    with open(f"{output_dir}/models.py", 'w+') as file:
        file.write(models_template.render(result=result))
