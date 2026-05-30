
from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

router = APIRouter()


@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):

    await websocket.accept()

    print("✅ WebSocket Connected")

    try:

        while True:

            data = await websocket.receive_text()

            print("📩 Message:", data)

            response = f"Nevark AI received: {data}"

            await websocket.send_text(response)

    except WebSocketDisconnect:

        print("❌ WebSocket Disconnected")
