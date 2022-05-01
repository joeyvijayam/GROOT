#!/usr/bin/python
"""
    Description:
        Kill the UAV client
"""

import socket
import asyncio
import websockets

from common.messages import NETWORK_PORT_NUMBER


async def kill_uav_client(ip_address, port_num):
    """
    Description:
        Test disconnect of UAV.
    :param ip_address:
        IP address of UAV client.
    :param port_num:
        Port number of UAV client.
    """
    async with websockets.connect(f"ws://{ip_address}:{port_num}/websocket") as websocket: # pylint: disable=no-member # NOTE: pylint can't figure out the connect method
        await websocket.send("demo kill_uav_client")

if __name__ == "__main__":
    ip_addr = socket.gethostbyname(socket.gethostname())
    asyncio.run(kill_uav_client(ip_addr, NETWORK_PORT_NUMBER))
