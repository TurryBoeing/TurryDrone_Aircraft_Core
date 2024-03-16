#!/usr/bin/python

import json

from . import AttData
from . import PosData
from . import MiscData

class FlightData:

    def __init__(self):
        self.attData = AttData.AttitudeData()
        self.posData = PosData.PositionData()
        self.extraData = MiscData.MiscelaneousData()

    def getAttData(self):
        return self.attData

    def getPosData(self):
        return self.posData

    def getExtraData(self):
        return self.extraData

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
