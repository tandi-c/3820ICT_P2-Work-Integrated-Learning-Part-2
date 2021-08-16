"""DATA.py: Description..."""

__author__      = "Barack Obama"
__copyright__   = "Copyright 2021, Planet Earth"

# Global Data
video_file = ""
pointsDict = {}

def resetDict():
    global pointsDict
    pointsDict = {
        "Head": [(0,0)],
        "Chest": [(0,0)],
        "M_Hip": [(0,0)],
        "L_Shoulder": [(0,0)],
        "R_Shoulder": [(0,0)],
        "L_Elbow": [(0,0)],
        "R_Elbow": [(0,0)],
        "L_Wrist": [(0,0)],
        "R_Wrist": [(0,0)],
        "L_Hip": [(0,0)],
        "R_Hip": [(0,0)],
        "L_Knee": [(0,0)],
        "R_Knee": [(0,0)],
        "L_Ankle": [(0,0)],
        "R_Ankle": [(0,0)],
        "Distance": [0]
    }
    return 