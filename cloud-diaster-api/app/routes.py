#Api Routes
#get post incidents resources with async use model
from app.models import Incident, ResourceStatus
from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter()

incidents = []
resources = []
# memory for now we set up dynamodb later

@router.get("/incidents", response_model=List[Incident]) #Get list of incident objects
async def get_incidents():
    return incidents

@router.post("/incidents", response_model=Incident) #create incident model object
async def create_incident(incident: Incident): #Accepting a new incident object
    incidents.append(incident)
    return incident

@router.get("/resources", response_model=List[ResourceStatus])
async def get_resources():          #using async to let app handle tasks while others are in wait time.
    return resources

@router.post("/resources", response_model=ResourceStatus)
async def create_resource(resource: ResourceStatus):
    resources.append(resource)
    return resource

