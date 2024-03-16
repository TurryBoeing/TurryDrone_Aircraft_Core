#!/usr/bin/python

class MiscelaneousData:
    sats = 0
    battery = 0
    flightmode = 1

    def setSats(self,value):
        self.sats = value
    def getSats(self):
        return self.sats

    def setBattery(self,value):
        self.battery = value
    def getBattery(self):
        return self.battery

    def setFlightMode(self,value):
        #1 is RC
        #2 is Internet
        #3 is Autopilot (Throttle is controlled via RC if range allows, else via Internet)
        #3 is Autopilot (Yaw (for AP disconnection if drone is an airplane) is controlled via RC if range allows, else via Internet)
        self.flightmode = value
    def getFlightMode(self):
        return self.flightmode
