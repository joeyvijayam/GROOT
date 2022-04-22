#!/usr/bin/python
"""
    Description:
        This module implements code for the Area of Operations window.
"""

import tkinter as tk
import multiprocessing
import time
from common.messages import UAV_STATUS_ID

from server.c2_server import C2Server


class AreaOfOperationsWindow:
    """
        Description:
            Area of operations window.
            Shows C2-related data.
    """

    def __init__(self, server_queue, gui_queue, uav_window, should_log):
        """
        Description:
            Initialize the area of operations window.
        """
        self.root = tk.Toplevel()
        self.root.title("Area of Operations")

        self.root.iconbitmap(".\\images\\defenzellc_logo.ico")

        self.canvas = tk.Canvas(self.root, height=700, width=700, bg="#263D42")
        self.canvas.pack()

        self.frame = tk.Frame(self.root, bg="white")
        self.frame.place(relwidth=0.8, relheight=0.6, relx=0.1, rely=0.1)


        self.engagement_zones_image = tk.PhotoImage(file='.\\images\\engagement_zones_560x420.png')

        self.engagement_zones_label = tk.Label(self.frame, image=self.engagement_zones_image)
        self.engagement_zones_label.pack(side=tk.BOTTOM)

        self.frame_label = tk.Label(self.frame, text="Area of Operations",
                            padx=10, pady=5, fg="white", bg="#263D42")
        self.frame_label.pack(side=tk.TOP)

        self.telemetry_frame = tk.Frame(self.root, bg="white")
        self.telemetry_frame.place(relwidth=0.8, relheight=0.18, relx=0.1, rely=0.75)

        self.telemetry_frame_label = tk.Label(self.telemetry_frame, text="Telemetry Data",
                            padx=10, pady=5, fg="white", bg="#263D42")
        self.telemetry_frame_label.pack(side=tk.TOP)
        self.telemetry_label = tk.Label(
            self.telemetry_frame, compound = tk.LEFT,
            background='white',
            text="")
        self.telemetry_label.pack(side=tk.TOP, anchor=tk.NW)

        self.radar_status_string = "Radar Status:    "
        self.radar_status = self.create_label(self.radar_status_string)

        self.weapon_status_string = "Weapon Status:    "
        self.weapon_status = self.create_label(self.weapon_status_string)

        self.iff_indent_string = "IFF Indent:    "
        self.iff_indent = self.create_label(self.iff_indent_string)

        self.detection_status_string = "Detection Status:    "
        self.detection_status = self.create_label(self.detection_status_string)

        self.target_pos_string = "Target Position:    "
        self.target_pos = self.create_label(self.target_pos_string)

        fire_button = tk.Button(self.root, text="FIRE", command=self.fire_button_init(), padx=10,
                            pady=5, fg="red", bg="#263D42")
        fire_button.pack(side=tk.LEFT)

        self.root.resizable(False, False)

        # Get shared memory queue
        self.server_queue = server_queue
        self.gui_queue = gui_queue

        # Create the C2 server
        self.c2_server = C2Server(self.server_queue, self.gui_queue)

        # Create the network thread
        self.c2_server_thread = multiprocessing.Process(target=self.c2_server.run_server)

        # Run the UAV client
        self.c2_server_thread.start()

        # Create end thread condition, on window close
        self.root.protocol('wm_delete_window', self.end_window)

        # Initiate the shared queue checking
        self.root.after(100, self.monitor_server_queue)

        # Keep reference to the UAV window, so we can update it w/ server queue data
        self.uav_window = uav_window

        # Counter to keep track of whether UAV is connected
        self.uav_connected_time_watchdog = 0
        # 5 seconds of no response, and UAV is disconnected
        self.uav_connected_time_watchdog_limit = 5

        # Whether or not to log to text file
        self.should_log = should_log
        self.log = open("logs\\log_"+str(time.time())+".txt", "w+", encoding='UTF-8') if self.should_log else None

    def resize_image(self, img, new_width, new_height):
        """
        Description:
            Resize a tkinter PhotoImage
        :param img:
            The tkinter photo image to resize
        :param new_width:
            The new width
        :param new_height:
            The new height
        """
        old_width = img.width()
        old_height = img.height()
        new_photo_image = tk.PhotoImage(width=new_width, height=new_height)
        for x_pix in range(new_width):
            for y_pix in range(new_height):
                x_old = int(x_pix*old_width/new_width)
                y_old = int(y_pix*old_height/new_height)
                rgb = '#%02x%02x%02x' % img.get(x_old, y_old)
                new_photo_image.put(rgb, (x_pix, y_pix))
        return new_photo_image

    def create_label(self, text):
        """
        Description:
            Create a tkinter label.
        :param text:
            Text in label.
        """
        label = tk.Label(self.root, text=text, padx=10,
                        pady=5, fg="white", bg="#263D42")
        label.pack(side=tk.LEFT)
        return label

    def fire_button_init(self):
        """
        Description:
            Fire button init.
        """
        self.radar_status.configure(text="Radar Status: On", fg="green")
        self.weapon_status.configure(text="Weapon Status: On", fg="green")
        self.detection_status.configure(text="Detection Status: Yes", fg="green")

    def show_window(self):
        """
        Description:
            Show the window by starting its main loop.
        """
        self.root.mainloop()

    def update_telemetry_data(self, text):
        """
        Desciption:
            Update the telemetry data window.
        """
        self.telemetry_label['text'] += text

    def end_window(self):
        """
        Description:
            Close the tkinter window, end program.
        """
        self.c2_server_thread.terminate()
        self.log.close()

    def monitor_server_queue(self):
        """
        Description:
            Check the server queue for new data.
            Update GUI as needed.
        """
        try:
            # Get message from the queue
            message_queue_item = self.server_queue.get(0)

            # Log to text file, if needed
            if self.should_log:
                self.log.write(str(message_queue_item) + "\n")
            

            # Check for Demo communications
            if str(message_queue_item).split(' ', maxsplit=1)[0] == "demo":
                if message_queue_item.split(' ')[1] == "kill_uav_client":
                    self.uav_window.disconnect_uav_client_demo()
                    self.root.after(100, self.monitor_server_queue)
                return

            # Put message in the telemetry window
            current_telemetry_text = self.telemetry_label.cget('text')
            self.telemetry_label.config(text=f"{current_telemetry_text}{message_queue_item}\n")

            # Selectively update GUI based off message type
            message_type = message_queue_item['message_type']

            if message_type == UAV_STATUS_ID:
                # Update UAV windows connected/disconnected status if needed
                if not self.uav_window.uav_status_connected:
                    self.uav_window.uav_status.config(text="UAV Status: Connected", fg="green")
                    self.uav_window.uav_status_connected = True

            self.uav_connected_time_watchdog = 0
            self.root.after(100, self.monitor_server_queue)
        except Exception:
            self.root.after(100, self.monitor_server_queue)
            self.uav_connected_time_watchdog += .1
            if self.uav_connected_time_watchdog >= self.uav_connected_time_watchdog_limit:
                self.uav_window.uav_status_connected = False
                self.uav_window.uav_status.config(text="UAV Status: Disconnected", fg="red")
