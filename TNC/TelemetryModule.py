#!/usr/bin/python
from audioop import error
import time
import json
import base64
import socket

class Telemetry:

    def __init__(self,data):
        self.flightData = data

    def sendTelemetryThread(self):
        print("+++++++++++++++++++")
        print("-------------------")
        print("___________________")
        tlmSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #tlmSocket.setblocking(0)
        try:
            tlmSocket.bind(('0.0.0.0', 13119))
        except socket.error as msg:
            print("Problem binding socket. Error : " + str(msg[0]) + " Message " + msg[1])
            return
        tlmSocket.listen(2)
        print("Telemetry socket: listening, waiting for connection")
        conn, addr = tlmSocket.accept()
        print("Telemetry socket: Client connected")
        while(True):
            #F"Pitch {self.imuSensor.attData.getPitch()}"
            #F"Roll {self.imuSensor.attData.getBank()}"
            #F"Heading {self.imuSensor.attData.getHeading()}"
            #print("+++++++++++++++++++")
            #print(repr(self.flightData.getAttData().getPitch()))
            #print(repr(self.flightData.getAttData().getBank()))
            #print(repr(self.flightData.getAttData().getHeading()))
            #print("-------------------")
            #print(repr(self.flightData.getPosData().getLatitude()))
            #print(repr(self.flightData.getPosData().getLongitude()))
            #print(repr(self.flightData.getPosData().getBarometricAltitude()))
            #print(repr(self.flightData.getPosData().getSpeed()))
            #print("___________________")
            jsonTelemetryString = self.flightData.toJSON()
            base64TelemetryString = base64.b64encode(bytes(jsonTelemetryString,"utf-8"))
            #print(base64TelemetryString)
            conn.send(base64TelemetryString)
            conn.send(b"\r\n")
            time.sleep(0.5)
            #tlmSocket.close()