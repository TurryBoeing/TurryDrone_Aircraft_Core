#!/usr/bin/python

import serial
import adafruit_bno055
import threading

from time import sleep

class IMUSensor:

    uart = serial.Serial("/dev/ttyUSB1", 115200)
    sensor = adafruit_bno055.BNO055_UART(uart)

    last_val = 0xFFFF
    
    def __init__(self,attitudeData):
        self.attData = attitudeData
        threading.Thread(target=self.readIMUThread,daemon=True).start()

    def readIMUData(self):
        while(True):
            try:
                if not self.sensor.calibrated:
                    print ("IMU not yet calibrated. Calibration status (syst, gyro, accel, mag): {}".format(self.sensor.calibration_status))
                    sleep(1)
                else:
                    self.readIMUAngles()
                    sleep(1.0 / 62.5)
            except RuntimeError:
                sleep(1.0 / 62.5)
        return

    def readIMUAngles(self):
        self.attData.setPitch(self.sensor.euler[2])
        self.attData.setBank(self.sensor.euler[1])
        hdg=(self.sensor.euler[0]-180)
        if hdg < 0:
            hdg=self.sensor.euler[0]+180
        self.attData.setHeading(hdg)
        return

    def readTemperature(self):
        global last_val  # pylint: disable=global-statement
        result = self.sensor.temperature
        if abs(result - last_val) == 128:
            result = self.sensor.temperature
        if abs(result - last_val) == 128:
            return 0b00111111 & result
        last_val = result
        return result

    def getAttitudeData(self):
        return self.attData

    def readIMUThread(self):
        sleep(1)
        print("IMU Reader called and initialized.")
        self.readIMUData()