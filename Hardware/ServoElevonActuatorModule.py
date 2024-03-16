#!/usr/bin/python
from gpiozero import AngularServo
class ServoElevonActuator:

    def __init__(self,elevatorPin,aileronPin):
        self.pinForElevator = elevatorPin
        self.pinForAileron = aileronPin
        self.servoPowerElevonElevator = AngularServo(self.pinForElevator, min_pulse_width=0.0006, max_pulse_width=0.0023)
        self.servoPowerElevonAileron = AngularServo(self.pinForAileron, min_pulse_width=0.0006, max_pulse_width=0.0023)

    def deflectElevons(self,aileronRatio,elevatorRatio):
        elevatorOutput=str(aileronRatio-elevatorRatio)
        aileronOutput=str(aileronRatio+elevatorRatio)

        elevatorPctg=((2-(1-float(elevatorOutput)))*100)/2
        aileronPctg=((2-(1-float(aileronOutput)))*100)/2

        elevatorAngle = (90 - ((elevatorPctg/100)) * 180)
        aileronAngle = (90 - ((aileronPctg/100)) * 180)
        if elevatorAngle <= 90 and elevatorAngle >= -90:
            self.servoPowerElevonElevator.angle = elevatorAngle
        if aileronAngle <= 90 and aileronAngle >= -90:
            self.servoPowerElevonAileron.angle = aileronAngle