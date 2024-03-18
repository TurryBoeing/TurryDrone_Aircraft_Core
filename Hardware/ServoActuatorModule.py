#!/usr/bin/python
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
class ServoActuator:
    def __init__(self,servoPin):
        self.pinNumber = servoPin
        servoFactory = PiGPIOFactory()
        self.servoPower = AngularServo(self.pinNumber, min_pulse_width=0.0006, max_pulse_width=0.0023,pin_factory=servoFactory)

    def deflectServo(self,value):
        self.servoPower.angle = (90 - ((value/100)) * 180)
        return

    def toggleBooleanServo(self,value):
        if value:
            self.servoPower.max()
        else:
            self.servoPower.min()