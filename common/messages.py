#!/usr/bin/python

import json
import time

SET_IFF_MSG_ID = 1
KILL_MESSAGE_ID = 2
FIRE_WEAPON_ID = 3
UAV_STATUS_ID = 101
GROUND_RADAR_STATUS_ID = 201

class Message:
    """
    Description:
        Common for all messages
    """
    def msg(self) -> str:
        """
        Description: Return class in JSON format for sending.
        """
        msg_dict = self.__dict__
        msg_dict['timestamp'] = time.time()
        return json.dumps(msg_dict)

class SetIffMessage(Message):
    def __init__(self, is_friend: bool = True):
        self.is_friend = is_friend
        self.message_type: int = SET_IFF_MSG_ID

class KillMessage(Message):
    def __init__(self):
        self.message_type: int = KILL_MESSAGE_ID

class FireWeaponMessage(Message):
    def __init__(self):
        self.message_type: int = FIRE_WEAPON_ID

class UavStatusMessage(Message):
    def __init__(self, is_hit: bool = True, is_friend: bool = True):
        self.message_type: int = UAV_STATUS_ID
        self.is_hit = is_hit
        self.is_friend = is_friend

class RadarData:
    def __init__(self, range: float = 0, elevation: float = 0, azimuth: float = 0):
        self.range = range
        self.elevation = elevation
        self.azimuth = azimuth

class GroundRadarStatus(Message):
    def __init__(self, radar_data: RadarData, weapon_armed: bool = False):
        self.message_type: int = GROUND_RADAR_STATUS_ID
        self.radar_data = radar_data
        self.weapon_armed = weapon_armed
