#!/usr/bin/python
"""
    Description:
        This module implements code for the Ground Radar client's websocket connection and messaging.
"""

import sys
import asyncio
import socket
import json
import websockets

from src.py.common.messages import FIRE_WEAPON_ID, GroundRadarStatus, NETWORK_PORT_NUMBER, HEARTBEAT_STATUS_INTERVAL

class RadarClient:
    """
    Description:
        Radar client.
        Connects to C2 server. Sends status to it, and receives commands from it.
    """
    def __init__(self):
        # IP address will always be same as C2 server, since run on same computer
        self.ip_addr = socket.gethostbyname(socket.gethostname())

        # Netork port number
        self.port_num = NETWORK_PORT_NUMBER

        # Use a 1/second status interval. Defines how frequently we send status to the C2 station.
        self.heartbeat_status_interval = HEARTBEAT_STATUS_INTERVAL

        # Create the UAV status message
        self.radar_status = GroundRadarStatus()

    async def send_status(self, radar_websocket):
        """
        Description:
            Send Ground Radar status
        :param radar_websocket:
            Websocket for communicating with C2 station server
        """
        # Send the status
        await radar_websocket.send(self.radar_status.msg())

        # Delay
        await asyncio.sleep(self.heartbeat_status_interval)


    async def receive_messages(self, radar_websocket):
        """
        Description:
            Handle receipt of messages
        :param radar_websocket:
            Websocket for communicating with C2 station
        """
        try:
            message = await radar_websocket.recv()
            message = json.loads(message)
            message_type = message['message_type']

            if message_type == FIRE_WEAPON_ID:
                # TODO: Fire weapon!
                pass

        # pylint: disable=unused-variable,broad-except # We only use exception for debug prints. Safe to suppress pylint warning
        except Exception as receive_exception:
            # print(f"Exception: {receive_exception}", flush=True) # Only use for debug
            pass

    async def send_and_receive(self):
        """
        Description:
            Process messages, manage setting LED and detecting IR hits
        """
        async with websockets.connect(f"ws://{self.ip_addr}:{self.port_num}/websocket") as radar_websocket:
            await asyncio.gather(self.send_status(radar_websocket), self.receive_messages(radar_websocket))
            # TODO: populate hearteat message w/ radar data and weapon status

    def run_send_and_receive(self):
        """
        Description:
            Run the send and receive function
        """
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)

        while True:
            asyncio.run(self.send_and_receive())

    def exit(self):
        """"
        Desciption:
            Exit upon request.
        """
        sys.exit(1)


if __name__ == "__main__":

    # Create the client
    radar_client = RadarClient()

    # Run the send and receive
    radar_client.run_send_and_receive()
