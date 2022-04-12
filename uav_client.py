#!/usr/bin/python

import asyncio
import socket
import websockets
import json
from common.messages import UavStatusMessage, SET_IFF_MSG_ID, KILL_MESSAGE_ID

IP_ADDR = socket.gethostbyname(socket.gethostname()) # Temporary for testing on same laptop
# IP_ADDR = input("Enter the C2 IP address: ") # Enable for tactical ops
HEARBEAT_STATUS_INTERVAL = 1

uav_status = UavStatusMessage() # Current UAV status, for sending to C2

async def send_status(ws):
    """
    Description:
        Send UAV status
    :param ws:
        Websocket for communicating with C2 station
    """
    # Send the status
    await ws.send(uav_status.msg())

    # Delay
    await asyncio.sleep(HEARBEAT_STATUS_INTERVAL)

async def receive_messages(ws):
    """
    Description: 
        Handle receipt of messages
    :param ws:
        Websocket for communicating with C2 station
    """
    try:
        message = await ws.recv()
        message = json.loads(message)
        message_type = message['message_type']

        if message_type == SET_IFF_MSG_ID:
            uav_status.is_friend = message['is_friend']
        elif message_type == KILL_MESSAGE_ID:
            # TODO: stop UAV
            pass
    except:
        pass
    

async def main():
    """
    Description: 
        Process messages, manage setting LED and detecting IR hits
    """
    async with websockets.connect(f"ws://{IP_ADDR}:8000/websocket") as ws:
        await asyncio.gather(send_status(ws), receive_messages(ws))
        # TODO: set led based on iff, detect whether hit, etc.

if __name__ == '__main__':
    while True:
        asyncio.run(main())
