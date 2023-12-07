import threading
import asyncio
import websockets

connected_clients = set()

async def register_client(websocket, path):
    print("A client just connected")
    connected_clients.add(websocket)
    try:
        await asyncio.wait([ws.send("Welcome!") for ws in connected_clients])
        async for message in websocket:
            await asyncio.wait([ws.send(f"Echo: {message}") for ws in connected_clients])
    finally:
        connected_clients.remove(websocket)

async def serve_forever_in_background(server):
    await server.wait_closed()

def server_thread_start():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    start_server = websockets.serve(register_client, "localhost", 8765)

    loop.run_until_complete(start_server)
    loop.run_forever()

# This runs the server in a separate thread
def run_in_thread():
    thread = threading.Thread(target=server_thread_start)
    thread.start()

def send_message(message):
    loop = asyncio.get_event_loop()
    coros = [ws.send(message) for ws in connected_clients]
    asyncio.run_coroutine_threadsafe(asyncio.wait(coros), loop)