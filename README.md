# GROOT

Project Development for GROOT System.


## Run the GUIs and C2 Server / UAV Client 

1. Create a python venv: python -m venv venv
1. Activate the venv: .\venv\Scripts\activate.bat
1. Install required libs: pip install -r requirements.txt
1. Run the help menu, from the project root directory: python -m gui.gui_driver --help
1. Could run the demo, with logging: python -m gui.gui_driver --demo --log
    1. Then after killing program, observe, in the logs folder, a new log was created with your run



## Still left to do
1. Less time now that I&T activities in AK picking up again
1. Still to do:
    1. Fix pipeline (2 hrs)
    1. Radar client (2-3 hrs)
    1. Link remaining text fields/messages in GUI (2 hrs), and radar graphical overlay map (4.5 hrs)
    1. Demo drivers:
        1. Weapon status, radar status (on/off) (1.5 hrs)
        1. mock change IFF mode (30 mins)
        1. BIG ONE: mock fire/hit sequence (3-4 hrs)
        1. BIG ONE: simulate radar tracking & reporting, draw on gui map (6 hrs)
    
