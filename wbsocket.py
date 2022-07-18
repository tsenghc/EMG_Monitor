import asyncio
import websockets
import numpy as np
import json


async def hello(websocket, path):
    data1 = np.random.randint(4, size=10)

    while True:
        await websocket.send(str(data1))

start_server=websockets.serve(hello, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
