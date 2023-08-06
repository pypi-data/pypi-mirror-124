from __future__ import annotations

from enum import Enum
from functools import cached_property
from typing import (
    Any,
    Optional,
    TypeVar,
    Union,
)

import pydantic
import pydash
from pydantic import EmailStr

MappingKey = TypeVar('MappingKey')
MappingValue = TypeVar('MappingValue')
# https://swagger.io/specification/#runtime-expression
ConstantOrExpression = Union[Any, str]


class SuperStr(str):
    @classmethod
    def __get_validators__(cls) -> Any:
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> Any:
        return cls(v)

    @property
    def snake_case(self) -> str:
        return pydash.snake_case(self)

    @property
    def camel_case(self) -> str:
        return pydash.camel_case(self)


class ContentType(str, Enum):
    APPLICATION_JSON = 'application/json'
    APPLICATION_XML = 'application/xml'
    APPLICATION_FORM = 'application/x-www-form-urlencoded'
    TEXT_PLAIN = 'text/plain'


class BaseModel(pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        use_enum_values = True
        arbitrary_types_allowed = True
        keep_untouched = (cached_property,)
        alias_generator = pydash.camel_case
        allow_population_by_field_name = True
        extra = pydantic.Extra.allow


class ParameterPosition(str, Enum):
    query = 'query'
    header = 'header'
    path = 'path'
    cookie = 'cookie'


class SecuritySchemeType(str, Enum):
    api_key = 'apiKey'
    http = 'http'
    oauth2 = 'oauth2'
    open_id_connect = 'openIdConnect'


class SecuritySchemePosition(str, Enum):
    query = 'query'
    header = 'header'
    cookie = 'cookie'


class License(BaseModel):
    name: str
    url: Optional[str]


class Contact(BaseModel):
    name: Optional[str]
    url: Optional[str]
    email: Optional[EmailStr]


class Info(BaseModel):
    title: str
    description: Optional[str]
    terms_of_service: Optional[str]
    contact: Optional[Contact]
    license: Optional[License]
    version: str


class ExternalDocs(BaseModel):
    url: str
    description: Optional[str]


class Reference(BaseModel):
    ref: Optional[str] = pydantic.Field(None, alias="$ref")


class Parameter(Reference):
    name: SuperStr
    parameter_schema: Optional[Schema] = pydantic.Field(..., alias='schema')
    position: ParameterPosition = pydantic.Field(..., alias='in')
    description: Optional[str]
    required: bool = False
    deprecated: Optional[bool] = False
    allow_empty_value: Optional[bool] = False


class Link(Reference):
    operation_ref: Optional[str]
    operation_id: Optional[SuperStr]
    parameters: dict[SuperStr, ConstantOrExpression]
    request_body: Optional[ConstantOrExpression]
    description: Optional[str]
    server: Optional[Server]


class Header(Parameter):
    name: Optional[SuperStr] = None
    position: Optional[Any] = pydantic.Field(None, alias='in')


Headers = dict[str, Header]
Links = dict[str, Link]


class Response(Reference):
    description: str
    headers: Headers = {}
    content: Content = {}
    links: Links = {}


Responses = dict[Union[str, int], Response]


class Operation(BaseModel):
    callbacks: Callbacks = {}
    deprecated: bool = False
    description: Optional[str]
    external_docs: Optional[ExternalDocs]
    operation_id: Optional[SuperStr]
    parameters: list[Parameter] = []
    request_body: Optional[RequestBody]
    responses: Responses = {}
    security: list[SecurityRequirement] = []
    servers: list[Server] = []
    summary: Optional[str]
    tags: list[str] = []


class Discriminator(BaseModel):
    property_name: SuperStr
    mapping: dict[str, str] = {}


class XMLObject(BaseModel):
    name: Optional[SuperStr]
    namespace: Optional[str]
    prefix: Optional[str]
    attribute: bool = False
    wrapped: bool = False


class Schema(Reference):
    title: Optional[str]
    multiple_of: Optional[float]
    maximum: Optional[Union[int, float]]
    exclusive_maximum: Optional[Union[int, float]]
    minimum: Optional[Union[int, float]]
    exclusive_minimum: Optional[Union[int, float]]
    max_length: Optional[int]
    min_length: Optional[int]
    pattern: Optional[str]
    max_items: Optional[int]
    min_items: Optional[int]
    unique_items: Optional[bool] = False
    max_properties: Optional[int]
    min_properties: Optional[int]
    max_contains: Optional[int]
    min_contains: Optional[int]
    required: list[str] = []
    enum: Optional[list[Union[str, int]]]
    type: Optional[str]
    all_of: Optional[list[Schema]] = []
    one_of: Optional[list[Schema]] = []
    any_of: Optional[list[Schema]] = []
    _not: Optional[Schema] = pydantic.Field(None, alias='not')
    items: Optional[Schema]
    properties: Properties = {}
    additional_properties: Optional[Schema]
    description: Optional[str]
    format: Optional[str]
    default: Any
    nullable: bool = False
    const: bool = False
    deprecated: bool = False
    discriminator: Optional[Discriminator]
    xml: Optional[XMLObject]
    external_docs: Optional[ExternalDocs]
    read_only: bool = None
    write_only: bool = None


class PathItem(BaseModel):
    ref: Optional[str] = pydantic.Field(None, alias="$ref")
    summary: Optional[str]
    description: Optional[str]
    servers: list[Server] = []
    parameters: list[Parameter] = []
    get: Optional[Operation]
    put: Optional[Operation]
    post: Optional[Operation]
    delete: Optional[Operation]
    options: Optional[Operation]
    head: Optional[Operation]
    patch: Optional[Operation]
    trace: Optional[Operation]


class ServerVariable(BaseModel):
    enum: list[SuperStr] = []
    default: SuperStr
    description: Optional[str]


ServerVariables = dict[str, ServerVariable]


class Server(BaseModel):
    url: str
    description: Optional[str]
    variables: Optional[ServerVariables] = {}


class Encoding(BaseModel):
    content_type: str
    headers: Headers
    style: str
    explode: bool = False
    allow_reversed: bool = False


class Example(Reference):
    summary: Optional[str]
    description: Optional[str]
    value: Optional[Any]
    external_value: Optional[str]


class MediaType(BaseModel):
    media_type_schema: Optional[Schema] = pydantic.Field(None, alias='schema')
    example: Optional[Any]
    examples: Examples = {}
    encoding: Encodings = {}


Callback = dict[str, PathItem]
Content = dict[str, MediaType]
Schemas = dict[str, Schema]
Properties = dict[str, Schema]
Parameters = dict[str, Parameter]
Callbacks = dict[str, Callback]
SecurityRequirement = dict[str, list[str]]
Paths = dict[str, PathItem]
OAuthFlowScopes = dict[str, str]
Examples = dict[str, Example]
Encodings = dict[str, Encoding]


class RequestBody(Reference):
    description: Optional[str]
    content: Content = {}
    required: bool = False


class OAuthFlow(BaseModel):
    authorization_url: Optional[str]
    token_url: Optional[str]
    refresh_url: Optional[str]
    scopes: OAuthFlowScopes = {}


class OAuthFlows(BaseModel):
    implicit: Optional[OAuthFlow]
    password: Optional[OAuthFlow]
    client_credentials: Optional[OAuthFlow]
    authorization_code: Optional[OAuthFlow]


class SecurityScheme(Reference):
    type: SecuritySchemeType
    description: Optional[str]
    name: Optional[SuperStr]
    scheme: Optional[SuperStr]
    position: Optional[SecuritySchemePosition] = pydantic.Field(None, alias='in')
    bearer_format: Optional[str]
    flows: Optional[OAuthFlows]


RequestBodies = dict[str, RequestBody]
SecuritySchemes = dict[str, SecurityScheme]


class Components(BaseModel):
    callbacks: Callbacks = {}
    examples: Examples = {}
    headers: Headers = {}
    links: Links = {}
    parameters: Parameters = {}
    request_bodies: RequestBodies = {}
    responses: Responses = {}
    schemas: Schemas = {}
    security_schemes: SecuritySchemes = {}


class Tag(BaseModel):
    description: Optional[str]
    external_docs: Optional[ExternalDocs]
    name: SuperStr


class OpenAPISchema(BaseModel):
    components: Optional[Components]
    external_docs: Optional[ExternalDocs]
    info: Info
    openapi: str
    paths: Paths = {}
    security: list[SecurityRequirement] = [{}]
    servers: Optional[list[Server]]
    tags: list[Tag] = []


Schema.update_forward_refs()
Link.update_forward_refs()
Header.update_forward_refs()
Operation.update_forward_refs()
Response.update_forward_refs()
Parameter.update_forward_refs()
