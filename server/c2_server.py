#!/usr/bin/python
"""
    Description:
        This module implements code for the C2 server's websocket connection and messaging.
"""

import asyncio
import socket
import json
import websockets


from common.messages import GROUND_RADAR_STATUS_ID, UAV_STATUS_ID, NETWORK_PORT_NUMBER

class C2Server:
    """
    Description:
        C2 server.
        Receives heartbeat message from UAV, and sends commands to it.
    """

    def __init__(self, server_queue, gui_queue):
        """
        Description:
            Initialize the C2 connections.
        """
        self.start_server = None

        # Get C2 server computer IP address.
        self.ip_addr = socket.gethostbyname(socket.gethostname())
        print(f"C2: User, please note for use w/ UAV that IP address is: {self.ip_addr}", flush=True)

        # Netork port number
        self.port_num = NETWORK_PORT_NUMBER

        # Queues for communicating w/ gui
        self.gui_queue = gui_queue
        self.server_queue = server_queue

    # Handle all messages
    async def handler(self, websocket):
        """
        Description:
            Handle receipt of messages.
        """
        message = await websocket.recv()
        if str(message).split(' ', maxsplit=1)[0] == "demo":
            # Share demo message and return
            self.server_queue.put(message)
            return
        message = json.loads(message)
        message_type = message['message_type']

        # Update GUI w/ telemetry data
        # from gui.main import area_of_ops_win
        self.server_queue.put(message)

        # Additional message processing
        if message_type == GROUND_RADAR_STATUS_ID:
            # Temporary: print to console
            #print('C2: ', message, flush=True)
            pass

        elif message_type == UAV_STATUS_ID:
            # Temporary: print to console
            #print('C2: ', message, flush=True)
            pass

    def run_server(self):
        """
        Description:
            Start hosting the server.
        """

        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)

        # Create the websocket server
        self.start_server = websockets.serve(self.handler, f"{self.ip_addr}", self.port_num)

        # Run the websocket server

        event_loop.run_until_complete(self.start_server)
        event_loop.run_forever()
