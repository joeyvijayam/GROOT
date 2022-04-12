#!/usr/bin/python

import asyncio
import socket
import websockets
import json
from common.messages import RadarData, UavStatusMessage, GroundRadarStatus, GROUND_RADAR_STATUS_ID, UAV_STATUS_ID

IP_ADDR = socket.gethostbyname(socket.gethostname())

# Handle all messages
async def handler(websocket):

    message = await websocket.recv()
    message = json.loads(message)
    message_type = message['message_type']

    if message_type == GROUND_RADAR_STATUS_ID:
        # TODO: populate GUI w/ data
        pass

        # Temporary: print to console
        print(message)

    elif message_type == UAV_STATUS_ID:
         # TODO: populate GUI w/ data
        pass

        # Temporary: print to console
        print(message)

if __name__ == '__main__':
    # Create the websocket server
    start_server = websockets.serve(handler, f"{IP_ADDR}", 8000)

    # Run the server
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

    # TODO: have GUI send commands to subsystems on button clicks
