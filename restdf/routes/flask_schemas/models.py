from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


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
    description: str = "RestDF Description"
    version: str = "1.0.0"
    title: str = "RestDF"
    termsOfService: str = "https://github.com/Mukhopadhyay/restdf/blob/master/LICENSE"
    contact: Dict[str, str] = field(default_factory=dict)
    license: Dict[str, str] = field(default_factory=dict)


@dataclass
class Tag:
    name: str
    description: str


@dataclass
class SwaggerEndpoint:
    parameters: Optional[List[Dict[str, Any]]]
    tags: List[str] = field(default_factory=list)
    summary: str = "Summary"
    description: str = "Description"
    produces: List[str] = field(default_factory=list)
    consumes: List[str] = field(default_factory=list)
    responses: Dict[str, Any] = field(default_factory=dict)
