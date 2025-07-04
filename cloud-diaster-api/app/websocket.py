from typing import List,Dict,Union
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
from app.routes import rescue_teams, incidents
router = APIRouter()

active_connections: list[WebSocket] = []


#Connecting clients

class Connect:
    def __init__(self):
        self.active_connections: List[WebSocket] = []


    async def connect_client(self,websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect_client(self,websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast_msg(self,message: dict):
        data = json.dumps(message)
        for connection in self.active_connections:
            await connection.send_text(data)



manager = Connect()

@router.websocket("/ws/locations")
async def websocket_locations(websocket: WebSocket):
    await manager.connect_client(websocket)
    try:
        while True:
            data_str = await websocket.receive_text()
            data = json.loads(data_str)

            entity_type = data.get("type")
            entity_id = data.get("id")
            lat = data.get("latitude")
            lon = data.get("longitude")

            if not entity_type or entity_id is None or lat is None or lon is None:
                await websocket.send_text(json.dumps({"error": "Missing required fields"}))
                continue

            if entity_type == "incident":
                if entity_id in incidents:
                    incident = incidents[entity_id]
                    incident.latitude = lat
                    incident.longitude = lon
                    incidents[entity_id] = incident
                else:
                    # Incident not found — send error back, don't create new
                    await websocket.send_text(json.dumps({
                        "error": f"Incident with ID {entity_id} has not been assigned"
                    }))
                    continue

            elif entity_type == "rescue_team":
                if entity_id in rescue_teams:
                    team = rescue_teams[entity_id]
                    team.latitude = lat
                    team.longitude = lon
                    rescue_teams[entity_id] = team
                else:
                    # Rescue team not found — send error back, don't create new
                    await websocket.send_text(json.dumps({
                        "error": f"Rescue team with ID {entity_id} has not been assigned"
                    }))
                    continue

            else:
                await websocket.send_text(json.dumps({"error": "Unknown type"}))
                continue

            broadcast_msg = {
                "type": entity_type,
                "id": entity_id,
                "latitude": lat,
                "longitude": lon
            }
            await manager.broadcast_msg(broadcast_msg)

    except WebSocketDisconnect:
        manager.disconnect_client(websocket)