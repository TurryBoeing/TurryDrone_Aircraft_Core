#!/usr/bin/python

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

from time import sleep

class BatteryMeterSensor:
    channel
    def __init__(self,miscelaneousData):
        #TurryDrone model object
        self.miscData = miscelaneousData
        #MCP3008 initialization
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        cs = digitalio.DigitalInOut(board.D5)
        mcp = MCP.MCP3008(spi, cs)
        self.channel = AnalogIn(mcp, MCP.P0)

    def readBatteryMeterThread(self):
        print("Battery Meter Reader called and initialized.")
        while(True):
            self.miscData.setBattery(self.channel.value)
            sleep(1)