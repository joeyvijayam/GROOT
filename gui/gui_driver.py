#!/usr/bin/python
"""
    Description:
        This module implements code for opening the UAV and Area of Ops GUI windows.
"""

import signal
import sys
import multiprocessing
import argparse
import tkinter as tk

from src.py.gui.area_of_operations_window import AreaOfOperationsWindow
from src.py.gui.uav_window import UAVWindow


class GUIDriver:
    """
    Description:
        Start the GUI windows.
    """

    def __init__(self):
        """
        Description:
            Initialize, run the GUI windows.
        """
        self.main_win = tk.Tk()
        self.main_win.withdraw()
        # Handle command-line args
        parser = argparse.ArgumentParser(description='Runs GUIs for UAV and TINYRAD. Also starts C2 server, radar client, and optionally UAV client for demo')
        parser.add_argument('--demo', action='store_true', help="Whether to run in demo mode, w/ client network code on same computer, or not. Default behavior, w/out this arg, is to run on separate computers")
        parser.add_argument('--log', action='store_true', help='Log telemetry data to text file.')
        args = parser.parse_args()

        # Create exit signal handler
        signal.signal(signal.SIGINT, self.signal_handler)

        # Create shared memory queues, for communication b/n GUI windows and server code
        self.server_queue = multiprocessing.Queue()
        self.gui_queue = multiprocessing.Queue()

        # Create GUI windows
        self.uav_win = UAVWindow(args.demo)
        self.area_of_ops_win = AreaOfOperationsWindow(self.server_queue, self.gui_queue, self.uav_win, args.log)

        # Show the GUI windows
        self.uav_win.show_window()
        self.area_of_ops_win.show_window()

    def signal_handler(self, sig, frame):
        """
        Desciption:
            Do things when user quits, if needed.
        """
        print("Ctrl-C pressed")
        self.area_of_ops_win.end_window()
        sys.exit(0)

if __name__ == '__main__':
    gui_driver = GUIDriver()
