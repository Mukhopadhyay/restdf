from typing import List, Dict, Any
from pydantic import BaseModel, Field
from ..routes.flask_schemas.api_metadata import flask_api_metadata


class PathParameters(BaseModel):
    name: str = 'column_name'
    in_: str = Field('path', alias='in')
    type_: str = Field('string', alias='type')
    enum: List[str]
    required: str = 'true'
    default: str = ''


class OpenAPITemplate(BaseModel):
    summary: str
    description: str
    tags: List[str]
    consumes: List[str]
    produces: List[str] = 'application/json'
    responses: Dict[str, Any]


def get_path_params(column_names: List[str]) -> Dict[str, Any]:
    path_params = PathParameters(enum=column_names)
    return dict(path_params)


def get_swagger_schema(ep_name: str, column_names) -> Dict[str, Any]:
    schema = dict(OpenAPITemplate(**flask_api_metadata[ep_name]))
    schema.update({'parameters': get_path_params(column_names)})
    return schema
