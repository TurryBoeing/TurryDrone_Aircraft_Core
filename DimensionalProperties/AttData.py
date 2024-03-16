#!/usr/bin/python

class AttitudeData:
    pitch = 0.0000000000000000
    bank = 0.0000000000000000
    heading = 0.0000000000000000

    def setPitch(self,value):
        self.pitch = value
    def getPitch(self):
        return self.pitch

    def setBank(self,value):
        self.bank = value
    def getBank(self):
        return self.bank

    def setHeading(self,value):
        self.heading = value
    def getHeading(self):
        return self.heading
