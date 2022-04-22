#!/usr/bin/python
"""
    Description:
        Kill the UAV client
"""

import websockets
import socket
from common.messages import NETWORK_PORT_NUMBER
import asyncio


async def kill_uav_client(ip_addr, port_num):
    async with websockets.connect(f"ws://{ip_addr}:{port_num}/websocket") as ws:
        await ws.send("demo kill_uav_client")

if __name__ == "__main__":
    ip_addr = socket.gethostbyname(socket.gethostname())
    port_num = NETWORK_PORT_NUMBER
    asyncio.run(kill_uav_client(ip_addr, port_num))
