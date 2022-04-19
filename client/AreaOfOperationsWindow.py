import tkinter as tk
from tkinter import LEFT, N, RIGHT, TOP, filedialog, Text
import os

root = tk.Tk()
root.title("Area of Operations")

canvas = tk.Canvas(root, height=700, width=700, bg="#263D42")
canvas.pack()

frame = tk.Frame(root, bg="white")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)


def createLabel(text):
    label = tk.Label(root, text=text, padx=10,
                     pady=5, fg="white", bg="#263D42")
    label.pack(side=LEFT)
    return label


frameLabel = tk.Label(frame, text="Area of Operations",
                      padx=10, pady=5, fg="white", bg="#263D42")
frameLabel.pack(side=TOP)

radarStatusString = "Radar Status:    "
radarStatus = createLabel(radarStatusString)

weaponStatusString = "Weapon Status:    "
weaponStatus = createLabel(weaponStatusString)

iffIndentString = "IFF Indent:    "
iffIndent = createLabel(iffIndentString)

detectionStatusString = "Detection Status:    "
detectionStatus = createLabel(detectionStatusString)

targetPosString = "Target Position:    "
targetPos = createLabel(targetPosString)

fireButton = tk.Button(root, text="FIRE", command=lambda: fireButtonCommand(), padx=10,
                       pady=5, fg="red", bg="#263D42")
fireButton.pack(side=LEFT)


def fireButtonCommand():
    radarStatus.configure(text="Radar Status: On", fg="green")
    weaponStatus.configure(text="Weapon Status: On", fg="green")
    detectionStatus.configure(text="Detection Status: Yes", fg="green")
