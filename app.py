from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from service import manager

import webbrowser
 
app = FastAPI()

@app.get("/")
async def get():
    return HTMLResponse(webbrowser.open_new_tab('index.html'))


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)                                                                                                                                                   
    try:
        while True: 
            data = await websocket.receive_text()
            await manager.send_personal_message(f"you wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} say:{data}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} has left the chat")
    