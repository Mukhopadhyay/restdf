from typing import List, Dict, Any
from pydantic import BaseModel

class OpenAPITemplate(BaseModel):
    summary: str
    description: str
    tags: List[str]
    consumes: List[str]
    produces: List[str]
    parameters: Dict[str, str]
    responses: Dict[str, str]

class SchemaObject(BaseModel):
    type: str
    example: Dict[str, Any]

class Response200(BaseModel):
    description: str
    schema: SchemaObject.__dict__

