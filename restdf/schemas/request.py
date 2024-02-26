from pydantic import BaseModel
from typing import List, Optional, Any, Union


class DataRequest(BaseModel):
    num: Optional[int] = 5
    columns: List[str] = []


class ConditionalData(DataRequest):
    value: Any
    as_string: Optional[bool] = False


class SamplePayload(DataRequest):
    frac: Optional[float] = None
    replace: Optional[bool] = False
    weights: Optional[Union[str, list]] = None
    random_state: Optional[int] = None
    axis: Optional[int] = None
    ignore_index: Optional[bool] = False


class MultiConditionalData(DataRequest):
    values: List[Any]
    as_string: Optional[bool] = False


class FindStringData(DataRequest):
    pattern: str
    case: Optional[bool] = False
    flags: Optional[Any] = 0
    na: Optional[bool] = True
    regex: Optional[bool] = False
