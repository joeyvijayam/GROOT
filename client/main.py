from copy import copy
import tkinter as tk
from tkinter import LEFT, N, RIGHT, TOP, Toplevel, filedialog, Text, mainloop
import os
import AreaOfOperationsWindow
import UAVWindow

root = tk.Tk()


if __name__ == '__main__':
    root.destroy()  # destroys root window, you can add to this later with a button or something
    window = AreaOfOperationsWindow
    window2 = UAVWindow
    root.mainloop()
