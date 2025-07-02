# 2 models Incidient, Resource Status
from pydantic import BaseModel
from typing import Optional

class Incident(BaseModel):
    id : int
    location : str
    severity : str
    descripton : Optional[str] = None

class ResourceStatus(BaseModel):
    id : int
    resource_type : str
    available : bool
    quantity : int
