from pydantic import BaseModel
from typing import List, Optional, Any


class DataRequest(BaseModel):
    columns: List[str] = []


class ConditionalData(DataRequest):
    value: Any
    as_string: Optional[bool] = False


class HeadPayload(DataRequest):
    num: Optional[int] = 5


class SamplePayload(DataRequest):
    num: Optional[int] = 5


class MultiConditionalData(DataRequest):
    values: List[Any]
    as_string: Optional[bool] = False


class FindStringData(DataRequest):
    pattern: str
    case: Optional[bool] = False
    flags: Optional[Any] = 0
    na: Optional[bool] = True
    regex: Optional[bool] = False
