#!/usr/bin/python
"""
    Description:
        This module implements code for the UAV window.
"""

import tkinter as tk
from tkinter import LEFT, TOP
import multiprocessing

from src.py.client.uav_client import UAVClient


class UAVWindow:
    """
    Description:
        UAV window.
        Shows attributes related to the UAV.
    """

    def __init__(self, demo):
        """
        Description:
            Initialize the UAV window.
        """
        self.root = tk.Toplevel()
        self.root.title("UAV Operations")

        self.root.iconbitmap(".\\images\\defenzellc_logo.ico")

        self.canvas = tk.Canvas(self.root, height=700, width=700, bg="#263D42")
        self.canvas.pack()

        self.frame = tk.Frame(self.root, bg="white")
        self.frame.place(relwidth=0.8, relheight=0.6, relx=0.1, rely=0.1)

        self.field_image = tk.PhotoImage(file='.\\images\\field_560x420.png')

        self.field_label = tk.Label(self.frame, image=self.field_image)
        self.field_label.pack(side=tk.BOTTOM)

        self.frame_label = tk.Label(self.frame, text="UAV Video Feed",
                            padx=10, pady=5, fg="white", bg="#263D42")
        self.frame_label.pack(side=TOP)

        self.uav_status_string = "UAV Status: Disconnected"
        self.uav_status = self.create_label(self.uav_status_string)
        self.uav_status_connected = False

        self.hit_status_string = "Hit Status:    "
        self.hit_status = self.create_label(self.hit_status_string)

        self.iff_setting_status_string = "IFF Setting:    "
        self.iff_setting_status = self.create_label(self.iff_setting_status_string)

        self.emergency_stop = tk.Button(self.root, text="Emergency Stop", command=self.emergency_stop_init(),
                                padx=10, pady=5, fg="red", bg="#263D42")
        self.emergency_stop.pack(side=LEFT)

        self.root.resizable(False, False)

        # Create the UAV client ourselves, if demo on same computer
        self.demo = demo
        self.send_and_receive_thread = None
        if self.demo:
            # Create the UAV client
            self.uav_client = UAVClient(demo)

            # Create the network thread
            self.send_and_receive_thread = multiprocessing.Process(target=self.uav_client.run_send_and_receive)

            # Run the UAV client
            self.send_and_receive_thread.start()

            # Create end thread condition
            self.root.wm_protocol('WM_DELETE_WINDOW', self.end_window)

    def create_label(self, text):
        """
        Description:
            Create a tkinter label.
        :param text:
            Text in label.
        """
        label = tk.Label(self.root, text=text, padx=10,
                        pady=5, fg="white", bg="#263D42")
        label.pack(side=LEFT)
        return label

    def emergency_stop_init(self):
        """
        Description:
            Emergency stop init.
        """
        #self.uav_status.configure(text="UAV Status: On", fg="red")
        self.hit_status.configure(text="Hit Status: Yes", fg="orange")

    def show_window(self):
        """
        Description:
            Show the window by starting its main loop.
        """
        self.root.mainloop()

    def end_window(self):
        """
        Description:
            Close the tkinter window, end program.
        """
        if self.send_and_receive_thread is not None:
            while self.send_and_receive_thread.is_alive():
                self.send_and_receive_thread.terminate()
        self.root.destroy()

    def disconnect_uav_client_demo(self):
        """
        Description:
            Disconnect UAV client, for demo purposes.
        """
        while self.send_and_receive_thread.is_alive():
            print("UAV_WINDOW DEMO: Disconnected UAV Client", flush=True)
            self.send_and_receive_thread.terminate()

