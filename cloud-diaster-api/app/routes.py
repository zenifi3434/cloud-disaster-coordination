
from fastapi import APIRouter, HTTPException
from typing import List
import math

from app.models import (
    Incident, RescueTeam, Shelter, SupplyStock,
    UpdateIncident, UpdateRescueTeam, UpdateShelter, UpdateSupplyStock
)

router = APIRouter()
                            #update doesnt work
incidents = {}
rescue_teams = {}
shelters = {}
supply_stocks = {}
# For now, in-memory storage; will migrate to DynamoDB later

def distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371  # Earth radius in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c



# --- Incident Endpoints ---

@router.get("/all-incidents", response_model=List[Incident])
async def get_all_incidents():
    return list(incidents.values())

@router.get("/get-incident-id/{id}", response_model=Incident)
async def get_incident_by_id(id: int):
    if id not in incidents:
        raise HTTPException(status_code=404, detail=f"Incident with id {id} not found")
    return incidents[id]

@router.post("/create-incidents", response_model=Incident)
async def create_incident(incident: Incident):
    if incident.id in incidents:
        raise HTTPException(status_code=400, detail=f"Incident already assigned to id {incident.id}")
    incidents[incident.id] = incident
    return incident

@router.delete("/delete-incident/{id}")
async def delete_incident(id: int):
    if id not in incidents:
        raise HTTPException(status_code=404, detail="No incident has been assigned with this ID")
    incidents.pop(id)
    return {"message": f"Incident with ID {id} deleted successfully"}

@router.put("/update-incident-id/{id}", response_model=Incident)
async def update_incident(id: int, incident_update: UpdateIncident):
    if id not in incidents:
        raise HTTPException(status_code=404, detail=f"No incident assigned with ID {id}")

    existing_incident = incidents[id]

    # Update only provided fields
    if incident_update.title is not None:
        existing_incident.title = incident_update.title
    if incident_update.location is not None:
        existing_incident.location = incident_update.location
    if incident_update.severity is not None:
        existing_incident.severity = incident_update.severity
    if incident_update.description is not None:
        existing_incident.description = incident_update.description
    if incident_update.latitude is not None:
        existing_incident.latitude = incident_update.latitude
    if incident_update.longitude is not None:
        existing_incident.longitude = incident_update.longitude
    if incident_update.status is not None:
        existing_incident.status = incident_update.status
    if incident_update.reported_at is not None:
        existing_incident.reported_at = incident_update.reported_at

    incidents[id] = existing_incident
    return existing_incident


@router.get("/locations/incidents")
async def get_all_incident_locations():
    # Return list of dicts with id + location info
    return [{"id": inc.id, "latitude": inc.latitude, "longitude": inc.longitude} for inc in incidents.values()]

@router.get("/locations/incidents/{id}")
async def get_incident_location_by_id(id: int):
    if id not in incidents:
        raise HTTPException(status_code=404, detail="Incident not found")
    inc = incidents[id]
    return {"id": inc.id, "latitude": inc.latitude, "longitude": inc.longitude}



# --- RescueTeam Endpoints ---

@router.get("/all-rescue-teams", response_model=List[RescueTeam])
async def get_all_rescue_teams():
    return list(rescue_teams.values())

@router.get("/get-rescue-team-id/{id}", response_model=RescueTeam)
async def get_rescue_team_by_id(id: int):
    if id not in rescue_teams:
        raise HTTPException(status_code=404, detail=f"Rescue team with id {id} not found")
    return rescue_teams[id]

@router.post("/create-rescue-teams", response_model=RescueTeam)
async def create_rescue_team(team: RescueTeam):
    if team.id in rescue_teams:
        raise HTTPException(status_code=400, detail=f"Rescue team already assigned to id {team.id}")
    rescue_teams[team.id] = team
    return team

@router.delete("/delete-rescue-team/{id}")
async def delete_rescue_team(id: int):
    if id not in rescue_teams:
        raise HTTPException(status_code=404, detail="No rescue team assigned with this ID")
    rescue_teams.pop(id)
    return {"message": f"Rescue team with ID {id} deleted successfully"}

@router.put("/update-rescue-team-id/{id}", response_model=RescueTeam)
async def update_rescue_team(id: int, team_update: UpdateRescueTeam):
    if id not in rescue_teams:
        raise HTTPException(status_code=404, detail=f"No rescue team assigned with ID {id}")

    existing_team = rescue_teams[id]

    if team_update.name is not None:
        existing_team.name = team_update.name
    if team_update.resource_type is not None:
        existing_team.resource_type = team_update.resource_type
    if team_update.available is not None:
        existing_team.available = team_update.available
    if team_update.last_updated is not None:
        existing_team.last_updated = team_update.last_updated
    if team_update.location is not None:
        existing_team.location = team_update.location

    rescue_teams[id] = existing_team
    return existing_team



@router.get("/locations/rescue_team")
async def get_all_rescue_team_location():
    # Return list of dicts with id + location info
    return [{"id": rescue_team.id, "latitude": rescue_team.latitude, "longitude": rescue_team.longitude} for rescue_team in rescue_teams.values()]

@router.get("/locations/rescue_team/{id}")
async def get_incident_location_by_id(id: int):
    if id not in rescue_teams:
        raise HTTPException(status_code=404, detail="Team not found")
    rescue_team = rescue_teams[id]
    return {"id": rescue_team.id, "latitude": rescue_team.latitude, "longitude": rescue_team.longitude}


@router.get("/nearest-rescue-team/{incident_id}", response_model=RescueTeam)
async def get_nearest_rescue_team(incident_id: int):
    if incident_id not in incidents:
        raise HTTPException(status_code=404, detail=f"Incident with id {incident_id} not found")

    incident = incidents[incident_id]

    if not rescue_teams:
        raise HTTPException(status_code=404, detail="No rescue teams available")

    nearest_team = min(
        rescue_teams.values(),
        key=lambda team: distance(
            incident.latitude,
            incident.longitude,
            team.latitude,
            team.longitude
        ),
        default=None,
    )

    if nearest_team is None:
        raise HTTPException(status_code=404, detail="No rescue teams found")

    return nearest_team





# --- Shelter Endpoints ---

@router.get("/all-shelters", response_model=List[Shelter])
async def get_all_shelters():
    return list(shelters.values())

@router.get("/get-shelter-id/{id}", response_model=Shelter)
async def get_shelter_by_id(id: int):
    if id not in shelters:
        raise HTTPException(status_code=404, detail=f"Shelter with id {id} not found")
    return shelters[id]

@router.post("/create-shelters", response_model=Shelter)
async def create_shelter(shelter: Shelter):
    if shelter.id in shelters:
        raise HTTPException(status_code=400, detail=f"Shelter already assigned to id {shelter.id}")
    shelters[shelter.id] = shelter
    return shelter

@router.delete("/delete-shelter/{id}")
async def delete_shelter(id: int):
    if id not in shelters:
        raise HTTPException(status_code=404, detail="No shelter assigned with this ID")
    shelters.pop(id)
    return {"message": f"Shelter with ID {id} deleted successfully"}

@router.put("/update-shelter-id/{id}", response_model=Shelter)
async def update_shelter(id: int, shelter_update: UpdateShelter):
    if id not in shelters:
        raise HTTPException(status_code=404, detail=f"No shelter assigned with ID {id}")

    existing_shelter = shelters[id]

    if shelter_update.name is not None:
        existing_shelter.name = shelter_update.name
    if shelter_update.location is not None:
        existing_shelter.location = shelter_update.location
    if shelter_update.capacity is not None:
        existing_shelter.capacity = shelter_update.capacity
    if shelter_update.current_occupied is not None:
        existing_shelter.current_occupied = shelter_update.current_occupied
    if shelter_update.status is not None:
        existing_shelter.status = shelter_update.status

    shelters[id] = existing_shelter
    return existing_shelter




@router.get("/locations/shelter")
async def get_all_shelters_location():
    # Return list of dicts with id + location info
    return [{"id": shelter.id, "latitude": shelter.latitude, "longitude": shelter.longitude} for shelter in shelters.values()]

@router.get("/locations/shelter/{id}")
async def get_shelter_location_id(id: int):
    if id not in shelters:
        raise HTTPException(status_code=404, detail="Shelter not found")
    shelter = shelters[id]
    return {"id": shelter.id, "latitude": shelter.latitude, "longitude": shelter.longitude}



@router.get("/nearest-shelter/{incident_id}", response_model=Shelter)
async def get_nearest_shelter(incident_id: int):
    if incident_id not in incidents:
        raise HTTPException(status_code=404, detail=f"Incident with id {incident_id} not found")

    incident = incidents[incident_id]

    if not shelters:
        raise HTTPException(status_code=404, detail="No shelters available")

    nearest_shelter = min(
        shelters.values(),
        key=lambda shelter: distance(
            incident.latitude,
            incident.longitude,
            shelter.latitude,
            shelter.longitude
        ),
        default=None,
    )

    if nearest_shelter is None:
        raise HTTPException(status_code=404, detail="No shelters found")

    return nearest_shelter


# --- SupplyStock Endpoints ---

@router.get("/all-supply-stocks", response_model=List[SupplyStock])
async def get_all_supply_stocks():
    return list(supply_stocks.values())

@router.get("/get-supply-stock-id/{id}", response_model=SupplyStock)
async def get_supply_stock_by_id(id: int):
    if id not in supply_stocks:
        raise HTTPException(status_code=404, detail=f"Supply stock with id {id} not found")
    return supply_stocks[id]

@router.post("/create-supply-stocks", response_model=SupplyStock)
async def create_supply_stock(stock: SupplyStock):
    if stock.id in supply_stocks:
        raise HTTPException(status_code=400, detail=f"Supply stock already assigned to id {stock.id}")
    supply_stocks[stock.id] = stock
    return stock

@router.delete("/delete-supply-stock/{id}")
async def delete_supply_stock(id: int):
    if id not in supply_stocks:
        raise HTTPException(status_code=404, detail="No supply stock assigned with this ID")
    supply_stocks.pop(id)
    return {"message": f"Supply stock with ID {id} deleted successfully"}

@router.put("/update-supply-stock-id/{id}", response_model=SupplyStock)
async def update_supply_stock(id: int, stock_update: UpdateSupplyStock):
    if id not in supply_stocks:
        raise HTTPException(status_code=404, detail=f"No supply stock assigned with ID {id}")

    existing_stock = supply_stocks[id]

    if stock_update.name is not None:
        existing_stock.name = stock_update.name
    if stock_update.quantity is not None:
        existing_stock.quantity = stock_update.quantity
    if stock_update.location is not None:
        existing_stock.location = stock_update.location

    supply_stocks[id] = existing_stock
    return existing_stock


