#!/usr/bin/python
import threading
import time

from DimensionalProperties import FltData
from Hardware import IMUSensorModule
from Hardware import GPSSensorModule
from Hardware import BarometricAltimeterSensorModule

from TNC import TelemetryModule
from TNC import ControlModule

print("##############################")
print("####TURRYDRONE 2.0 ALPHA 6####")
print("########CORE PROGRAM##########")
print("##FEATURES ENABLED: TLM THREAD")
print("##                  GPS READ  ")
print("##                  IMU READ  ")
print("##             BARO ALT READ  ")
print("##    RC SERVO MOVE (PiGPIO)  ")
print("##############################")

time.sleep(1)

flightData = FltData.FlightData()

IMU = IMUSensorModule.IMUSensor(flightData.getAttData())
GPS = GPSSensorModule.GPSSensor(flightData.getPosData(),flightData.getExtraData())
BaroAltimeter = BarometricAltimeterSensorModule.BarometricAltitudeSensor(flightData.getPosData())

telemetryController = TelemetryModule.Telemetry(flightData)
threading.Thread(target=telemetryController.sendTelemetryThread).start()

droneController = ControlModule.Control(flightData)
threading.Thread(target=droneController.processDroneControl).start()