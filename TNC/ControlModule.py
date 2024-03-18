#!/usr/bin/python
import time
import serial

from Hardware import ServoActuatorModule
from Hardware import ServoElevonActuatorModule
class Control:
    def __init__(self,data):
        self.flightData = data
        self.throttle = ServoActuatorModule.ServoActuator(16)
        self.elevon = ServoElevonActuatorModule.ServoElevonActuator(6,5)
        self.lights = ServoActuatorModule.ServoActuator(24)

        self.rcInput  = serial.Serial()
        self.rcInput.baudrate = 115200
        self.rcInput.port = '/dev/ttyUSB0'

    def processDroneControl(self):
        #self.flightControlsMovementDemo()
        while(True):
            if self.flightData.getExtraData().getFlightMode() == 1:
                self.controlViaRCLoop()

    def controlViaRCLoop(self):
        if not self.rcInput.is_open:
            self.rcInput.open()
        self.rcInput.flushInput()

        rcInputValue = self.rcInput.readline().decode('utf-8').strip()

        if rcInputValue.find("drnrc") == -1 or rcInputValue.find("drnrc") > 0:
            print("RC Parser: Invalid command")
        else:
            #Power:
            powerPercentage = float(rcInputValue.split("&")[1].split(";")[0].split("=")[1])
            self.throttle.deflectServo(powerPercentage)

            #Elevons:
            aileronRatio = float(rcInputValue.split("&")[1].split(";")[1].split("=")[1].split(",")[0])
            elevatorRatio = float(rcInputValue.split("&")[1].split(";")[1].split("=")[1].split(",")[1])
            self.elevon.deflectElevons(aileronRatio,elevatorRatio)

            #Flight Mode:
            #self.flightData.getExtraData().setFlightMode(int(rcInputValue.split("&")[1].split(";")[2].split("=")[1]+1))

    def flightControlsMovementDemo(self):
        #while(True):
        print("FLIGHT CONTROLS MOVEMENT DEMO IN PROGRESS (WARNING!! also moves throttle)")
        self.throttle.deflectServo(100-(0))
        time.sleep(2)
        self.lights.toggleBooleanServo(True)
        print("FLIGHT CONTROLS MOVEMENT DEMO: PITCH UP (pull up)")
        self.elevon.deflectElevons(0.0,0.4)
        time.sleep(2)
        print("FLIGHT CONTROLS MOVEMENT DEMO: PITCH DOWN (push down)")
        self.elevon.deflectElevons(0.0,-0.4)
        time.sleep(2)
        print("FLIGHT CONTROLS MOVEMENT DEMO: PITCH CENTER")
        self.elevon.deflectElevons(0.0,0.0)
        time.sleep(2)
        print("FLIGHT CONTROLS MOVEMENT DEMO: ROLL RIGHT")
        self.elevon.deflectElevons(0.4,0.0)
        time.sleep(2)
        print("FLIGHT CONTROLS MOVEMENT DEMO: ROLL LEFT")
        self.elevon.deflectElevons(-0.4,0.0)
        time.sleep(2)
        print("FLIGHT CONTROLS MOVEMENT DEMO: ROLL CENTER")
        self.elevon.deflectElevons(0.0,0.0)
        time.sleep(5)
        print("FLIGHT CONTROLS MOVEMENT DEMO: Throttle 25 percent")
        self.throttle.deflectServo(100-(25))
        time.sleep(5)
        print("FLIGHT CONTROLS MOVEMENT DEMO: Throttle idle")
        self.throttle.deflectServo(100-(0))
        time.sleep(10)
        self.lights.toggleBooleanServo(False)