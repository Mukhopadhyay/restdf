from pydantic import BaseModel
from typing import Optional, List


class _CommonRequestAttrs(BaseModel):
    columns: Optional[List[str]] = None
    index: Optional[bool] = False


class DescribeRequest(BaseModel):
    datetime_is_numeric: Optional[bool] = False
    exclude: Optional[List[str]] = ["O"]
    include: Optional[List[str]] = ["int"]
    percentiles: Optional[List[float]] = [0.01, 0.25, 0.75, 0.99]
