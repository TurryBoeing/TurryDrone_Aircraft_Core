#!/usr/bin/python
from gpiozero import AngularServo
class ServoActuator:
    def __init__(self,servoPin):
        self.pinNumber = servoPin
        self.servoPower = AngularServo(self.pinNumber, min_pulse_width=0.0006, max_pulse_width=0.0023)

    def deflectServo(self,value):
        self.servoPower.angle = (90 - ((value/100)) * 180)
        return

    def toggleBooleanServo(self,value):
        if value:
            self.servoPower.max()
        else:
            self.servoPower.min()