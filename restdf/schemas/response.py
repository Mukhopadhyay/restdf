from pydantic import BaseModel
from typing import Dict, Any, Optional, List, Union
from fastapi import __version__ as fa_version


class _Ep(BaseModel):
    method: str
    route: str
    summary: str


class IndexResponse(BaseModel):
    name: str = "RestDF"
    FastAPI_version: str = fa_version
    endpoints: Optional[List[_Ep]] = None


class Response(BaseModel):
    data: Union[Dict[str, Any], List]
    status: Optional[int] = 200


class ColumnResponse(BaseModel):
    data: List[str]
    status: Optional[int] = 200
