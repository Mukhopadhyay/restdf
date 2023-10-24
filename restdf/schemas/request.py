from pydantic import BaseModel
from typing import Optional, List


class _CommonRequestAttrs(BaseModel):
    columns: Optional[List[str]] = None
    index: Optional[bool] = False
