from dataclasses import dataclass, field
from typing import Dict, Any, List, Union


@dataclass
class SwaggerTemplate:
    swagger: str = "2.0"
    info: Dict[str, Any] = field(default_factory=dict)
    tags: List[Dict[str, str]] = field(default_factory=list)
    schemes: List[str] = field(default_factory=list)
    paths: Dict[str, Any] = field(default_factory=dict)
    definitions: Dict[str, Any] = field(default_factory=dict)


@dataclass
class InfoTemplate:
    description: str = "<b>[Created using <code><a href='//github.com/Mukhopadhyay/restdf' target='_blank'>RestDF</a></code>]</b>"
    version: str = "1.0.0"
    title: str = "RestDF API"
    termsOfService: str = "https://github.com/Mukhopadhyay/restdf/blob/master/LICENSE"
    contact: Dict[str, str] = field(default_factory=dict)
    license: Dict[str, str] = field(default_factory=dict)


@dataclass
class Tag:
    name: str
    description: str


@dataclass
class SwaggerEndpoint:
    parameters: Union[List[Dict[str, Any]], List[Any]]
    tags: List[str] = field(default_factory=list)
    summary: str = "Summary"
    description: str = "Description"
    produces: List[str] = field(default_factory=list)
    consumes: List[str] = field(default_factory=list)
    responses: Dict[str, Any] = field(default_factory=dict)
