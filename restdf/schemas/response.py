from pydantic import BaseModel
from typing import List, Dict, Any


class DataResponse(BaseModel):
    data: List[Dict[str, Any]]
    type: str
