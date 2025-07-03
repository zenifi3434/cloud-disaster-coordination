
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

active_connections: list[WebSocket] = []            #List to track who is currently connected


#Connecting clients

async def connect_client(websocket: WebSocket):
    await websocket.accept()                        #Awaiting their connection
    active_connections.append(websocket)            #Add to list of active connections

def disconnect_client(websocket: WebSocket):            #If user disconnects remove from list
    active_connections.remove(websocket)

async def broadcast_msg(message: str):                      #Send message to every connected client
    for connection in active_connections:
        await connection.send_text(message)


@router.websocket("/ws/locations")
async def websocket_locations(websocket: WebSocket):
    await connect_client(websocket)                         #wait for user to connect, and add to list
    try:
        while True:
            data = await websocket.receive_text()            #Wait till we recieve text , then broadcast it
            await broadcast_msg(data)
    except WebSocketDisconnect as e:                            #If we disconnect, remove them from websocket
        print(e)
        disconnect_client(websocket)
