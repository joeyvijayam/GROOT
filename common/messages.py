#!/usr/bin/python
"""
    Description:
        This module implements messages and other shared network settings.
"""

import datetime
import jsons # type: ignore

SET_IFF_MSG_ID = 1
KILL_MESSAGE_ID = 2
FIRE_WEAPON_ID = 3
UAV_STATUS_ID = 101
GROUND_RADAR_STATUS_ID = 201
NETWORK_PORT_NUMBER = 8000
HEARTBEAT_STATUS_INTERVAL = 1

class Message:
    """
    Description:
        Common for all messages
    """
    def msg(self) -> str:
        """
        Description:
            Return class in JSON format for sending.
        """
        msg_dict = self.__dict__
        now = datetime.datetime.now()
        msg_dict['timestamp'] = '{:02d}/{:02d}/{:02d}-{:02d}:{:02d}:{:02d}'.format(now.year, now.month, now.day, now.hour, now.minute, now.second)
        return jsons.dumps(msg_dict)

class SetIffMessage(Message):
    """
        Description:
           IFF message.
    """

    def __init__(self, is_friend: bool = True):
        """
        Description:
           Create IFF message.
        """
        self.is_friend = is_friend
        self.message_type: int = SET_IFF_MSG_ID

class KillMessage(Message):
    """
    Description:
        Kill message.
    """

    def __init__(self):
        """
        Description:
           Create kill message.
        """
        self.message_type: int = KILL_MESSAGE_ID

class FireWeaponMessage(Message):
    """
    Description:
        Fire message.
    """

    def __init__(self):
        """
        Description:
           Create fire message.
        """
        self.message_type: int = FIRE_WEAPON_ID

class UavStatusMessage(Message):
    """
    Description:
        UAV status message.
    """

    def __init__(self, is_hit: bool = True, is_friend: bool = True):
        """
        Description:
           Create UAV status message.
        """
        self.message_type: int = UAV_STATUS_ID
        self.is_hit = is_hit
        self.is_friend = is_friend

class RadarData:
    """
    Description:
        Radar data.
    """

    def __init__(self, detected_range: float = 0, detected_elevation: float = 0, detected_azimuth: float = 0):
        """
        Description:
            Create a radar data object.
        """
        self.detected_range = detected_range
        self.detected_elevation = detected_elevation
        self.detected_azimuth = detected_azimuth

class GroundRadarStatus(Message):
    """
    Description:
        Radar status message.
    """

    def __init__(self, radar_data: RadarData = RadarData(), weapon_armed: bool = False):
        """
        Description:
            Create a radar status message.
        """
        self.message_type: int = GROUND_RADAR_STATUS_ID
        self.radar_data = radar_data
        self.weapon_armed = weapon_armed
