import tkinter as tk
from tkinter import LEFT, N, RIGHT, TOP, filedialog, Text
import os

root = tk.Tk()
root.title("UAV Operations")

canvas = tk.Canvas(root, height=700, width=700, bg="#263D42")
canvas.pack()

frame = tk.Frame(root, bg="white")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

frameLabel = tk.Label(frame, text="UAV Video Feed",
                      padx=10, pady=5, fg="white", bg="#263D42")
frameLabel.pack(side=TOP)


def createLabel(text):
    label = tk.Label(root, text=text, padx=10,
                     pady=5, fg="white", bg="#263D42")
    label.pack(side=LEFT)
    return label


uavStatusString = "UAV Status:    "
uavStatus = createLabel(uavStatusString)

batteryStatusString = "Battery %:    "
batteryStatus = createLabel(batteryStatusString)

emergencyStop = tk.Button(root, text="Emergency Stop", command=lambda: emergencyStopCommand(),
                          padx=10, pady=5, fg="red", bg="#263D42")
emergencyStop.pack(side=LEFT)

hitStatusString = "Hit Status:    "
hitStatus = createLabel(hitStatusString)

iffSettingStatusString = "IFF Setting:    "
iffSettingStatus = createLabel(iffSettingStatusString)


def emergencyStopCommand():
    uavStatus.configure(text="UAV Status: On", fg="green")
    batteryStatus.configure(text="Battery: 80%", fg="green")
    hitStatus.configure(text="Hit Status: Yes", fg="orange")
