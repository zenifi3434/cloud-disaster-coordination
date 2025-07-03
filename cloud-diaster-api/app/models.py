
from pydantic import BaseModel
from typing import Optional

class Incident(BaseModel):
    id: int
    title: str
    location: str
    severity: int
    description: Optional[str] = None  # fixed typo
    latitude: float
    longitude: float
    status: Optional[str] = None
    reported_at: str

class RescueTeam(BaseModel):
    id: int
    name: str
    resource_type: str
    available: bool
    last_updated: int  # consider using datetime instead of int timestamp?
    location: str
    latitude: float
    longitude: float

class Shelter(BaseModel):
    id: int
    name: str
    location: str
    capacity: int
    current_occupied: int
    status: str
    latitude: float
    longitude: float

class SupplyStock(BaseModel):
    id: int
    name: str
    quantity: int  # added type annotation
    location: str  # added type annotation

class UpdateIncident(BaseModel):
    id: int  # Usually you keep the ID required to identify the record to update
    title: Optional[str] = None
    location: Optional[str] = None
    severity: Optional[int] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    status: Optional[str] = None
    reported_at: Optional[str] = None

class UpdateRescueTeam(BaseModel):
    id: int
    name: Optional[str] = None
    resource_type: Optional[str] = None
    available: Optional[bool] = None
    last_updated: Optional[int] = None
    location: Optional[str] = None

class UpdateShelter(BaseModel):
    id: int
    name: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[int] = None
    current_occupied: Optional[int] = None
    status: Optional[str] = None

class UpdateSupplyStock(BaseModel):
    id: int
    name: Optional[str] = None
    quantity: Optional[int] = None
    location: Optional[str] = None
