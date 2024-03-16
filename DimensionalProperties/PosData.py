#!/usr/bin/python

class PositionData:
    latitude = 0.0000000000000000
    longitude = 0.0000000000000000
    speed = 0.0000000000000000
    altitude = 0.0000000000000000
    barometricAltitude = 0.0000000000000000
    altitudeUnit = "M"

    def setLatitude(self,value):
        self.latitude = value
    def getLatitude(self):
        return self.latitude

    def setLongitude(self,value):
        self.longitude = value
    def getLongitude(self):
        return self.longitude

    def setSpeed(self,value):
        self.speed = value
    def getSpeed(self):
        return self.speed

    def setAltitude(self,value):
        self.altitude = value
    def getAltitude(self):
        return self.altitude

    def setBarometricAltitude(self,value):
        self.barometricAltitude = value
    def getBarometricAltitude(self):
        return self.barometricAltitude

    def setAltitudeUnit(self,value):
        self.altitudeUnit = value
    def getAltitudeUnit(self):
        return self.altitudeUnit