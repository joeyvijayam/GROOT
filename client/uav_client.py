#!/usr/bin/python
"""
    Description:
        This module implements code for the UAV client's websocket connection and messaging.
"""

import sys
import asyncio
import socket
import json
import websockets

from common.messages import UavStatusMessage, SET_IFF_MSG_ID, KILL_MESSAGE_ID, NETWORK_PORT_NUMBER

class UAVClient:
    """
    Description:
        UAV client.
        Connects to C2 server. Sends status to it, and receives commands from it.
    """
    def __init__(self, demo):
        # TODO: Temporary for testing on same laptop, replace w/ input
        if demo:
            self.ip_addr = socket.gethostbyname(socket.gethostname())
        else:
            print("Enter C2 station ip address: ", flush=True)
            self.ip_addr = input()

        # Netork port number
        self.port_num = NETWORK_PORT_NUMBER

        # Use a 1/second status interval. Defines how frequently we send status to the C2 station.
        self.heartbeat_status_interval = 1

        # Create the UAV status message
        self.uav_status = UavStatusMessage()

    async def send_status(self, uav_websocket):
        """
        Description:
            Send UAV status
        :param uav_websocket:
            Websocket for communicating with C2 station
        """
        # Send the status
        await uav_websocket.send(self.uav_status.msg())

        # Delay
        await asyncio.sleep(self.heartbeat_status_interval)


    async def receive_messages(self, uav_websocket):
        """
        Description:
            Handle receipt of messages
        :param uav_websocket:
            Websocket for communicating with C2 station
        """
        try:
            message = await uav_websocket.recv()
            message = json.loads(message)
            message_type = message['message_type']

            if message_type == SET_IFF_MSG_ID:
                self.uav_status.is_friend = message['is_friend']
            elif message_type == KILL_MESSAGE_ID:
                # TODO: stop UAV
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
        async with websockets.connect(f"ws://{self.ip_addr}:{self.port_num}/websocket") as uav_websocket:
            await asyncio.gather(self.send_status(uav_websocket), self.receive_messages(uav_websocket))
            # TODO: set led based on iff, detect whether hit, etc.

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
    uav_client = UAVClient(demo=False)

    # Run the send and receive
    uav_client.run_send_and_receive()
    
