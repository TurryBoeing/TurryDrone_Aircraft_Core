#!/usr/bin/python
#--------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
#           bme280.py
#  Read data from a digital pressure sensor.
#
#  Official datasheet available from :
#  https://www.bosch-sensortec.com/bst/products/all_products/bme280
#
# Author : Matt Hawkins
# Date   : 21/01/2018
#
# https://www.raspberrypi-spy.co.uk/
#
#--------------------------------------
from ctypes import c_byte
from ctypes import c_short
from ctypes import c_ubyte
import smbus
import time
import requests
import threading

class BarometricAltitudeSensor:
    DEVICE = 0x76 # Default device I2C address
    QNH = 101392
    bus = smbus.SMBus(1) # Rev 2 Pi, Pi 2 & Pi 3 uses bus 1;Rev 1 Pi uses bus 0

    def getQNH(self):
        #Make web request to get QNH of local airport
        r = requests.get(url = "https://api.checkwx.com/metar/" + "LEVX",
        params={'q': ''},
        headers={'X-API-Key': 'f58af269cdfac55d250f584559'},
        )
        json_response = r.json()
        self.QNH=int(json_response['data'][0].split("Q",1)[1].split(" ",1)[0])*100
        print("Barometric Altimeter got QNH:")
        print(repr(self.QNH))

    def getShort(self,data, index):
        # return two bytes from data as a signed 16-bit value
        return c_short((data[index + 1] << 8) + data[index]).value

    def getUShort(self,data, index):
        # return two bytes from data as an unsigned 16-bit value
        return (data[index + 1] << 8) + data[index]

    def getChar(self,data, index):
        # return one byte from data as a signed char
        result = data[index]
        if result > 127:
            result -= 256
        return result

    def getUChar(self,data, index):
        # return one byte from data as an unsigned char
        result = data[index] & 0xFF
        return result

    def readBMP280ID(self,addr=DEVICE):
        # Chip ID Register Address
        REG_ID     = 0xD0
        (chip_id, chip_version) = self.bus.read_i2c_block_data(addr, REG_ID, 2)
        return (chip_id, chip_version)

    def readBMP280All(self,addr=DEVICE):
        # Register Addresses
        REG_DATA = 0xF7
        REG_CONTROL = 0xF4
        REG_CONFIG  = 0xF5

        # Oversample setting - page 27
        OVERSAMPLE_TEMP = 2
        OVERSAMPLE_PRES = 2
        OVERSAMPLE_HUM = 2
        MODE = 1

        control = OVERSAMPLE_TEMP << 5 | OVERSAMPLE_PRES << 2 | MODE
        self.bus.write_byte_data(addr, REG_CONTROL, control)

        # Read blocks of calibration data from EEPROM
        # See Page 22 data sheet
        cal1 = self.bus.read_i2c_block_data(addr, 0x88, 24)
        cal2 = self.bus.read_i2c_block_data(addr, 0xA1, 1)
        cal3 = self.bus.read_i2c_block_data(addr, 0xE1, 7)

        # Convert byte data to word values
        dig_T1 = self.getUShort(cal1, 0)
        dig_T2 = self.getShort(cal1, 2)
        dig_T3 = self.getShort(cal1, 4)

        dig_P1 = self.getUShort(cal1, 6)
        dig_P2 = self.getShort(cal1, 8)
        dig_P3 = self.getShort(cal1, 10)
        dig_P4 = self.getShort(cal1, 12)
        dig_P5 = self.getShort(cal1, 14)
        dig_P6 = self.getShort(cal1, 16)
        dig_P7 = self.getShort(cal1, 18)
        dig_P8 = self.getShort(cal1, 20)
        dig_P9 = self.getShort(cal1, 22)

        dig_H1 = self.getUChar(cal2, 0)
        dig_H2 = self.getShort(cal3, 0)
        dig_H3 = self.getUChar(cal3, 2)

        dig_H4 = self.getChar(cal3, 3)
        dig_H4 = (dig_H4 << 24) >> 20
        dig_H4 = dig_H4 | (self.getChar(cal3, 4) & 0x0F)

        dig_H5 = self.getChar(cal3, 5)
        dig_H5 = (dig_H5 << 24) >> 20
        dig_H5 = dig_H5 | (self.getUChar(cal3, 4) >> 4 & 0x0F)

        dig_H6 = self.getChar(cal3, 6)

        # Wait in ms (Datasheet Appendix B: Measurement time and current calculation)
        wait_time = 1.25 + (2.3 * OVERSAMPLE_TEMP) + ((2.3 * OVERSAMPLE_PRES) + 0.575) + ((2.3 * OVERSAMPLE_HUM) + 0.575)
        time.sleep(wait_time / 1000)  # Wait the required time  

        # Read temperature/pressure
        data = self.bus.read_i2c_block_data(addr, REG_DATA, 8)
        pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)

        #Refine temperature
        var1 = ((((temp_raw >> 3)-(dig_T1 << 1))) * (dig_T2)) >> 11
        var2 = (((((temp_raw >> 4) - (dig_T1)) * ((temp_raw >> 4) - (dig_T1))) >> 12) * (dig_T3)) >> 14
        t_fine = var1 + var2
        temperature = float(((t_fine * 5) + 128) >> 8);

        # Refine pressure and adjust for temperature
        var1 = t_fine / 2.0 - 64000.0
        var2 = var1 * var1 * dig_P6 / 32768.0
        var2 = var2 + var1 * dig_P5 * 2.0
        var2 = var2 / 4.0 + dig_P4 * 65536.0
        var1 = (dig_P3 * var1 * var1 / 524288.0 + dig_P2 * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * dig_P1
        if var1 == 0:
            pressure = 0
        else:
            pressure = 1048576.0 - pres_raw
            pressure = ((pressure - var2 / 4096.0) * 6250.0) / var1
            var1 = dig_P9 * pressure * pressure / 2147483648.0
            var2 = pressure * dig_P8 / 32768.0
            pressure = pressure + (var1 + var2 + dig_P7) / 16.0

        #Calculate Altitude from barometric pressure and pressure at sea level (QNH?)
        altitude=44330.0 * (1.0 - pow(pressure / self.QNH, (1.0/5.255)))

        return temperature / 100.0, pressure / 100.0, altitude

    def __init__(self,positionData):
        self.posData = positionData
        threading.Thread(target=self.readBaroAltitudeThread,daemon=True).start()

    def readBaroAltitudeThread(self):
        time.sleep(1)
        print("Barometric Altimeter reader called and initialized.")
        self.getQNH()
        while(True):
            temp,press,baroAlt=self.readBMP280All()
            self.posData.setBarometricAltitude(baroAlt)
            time.sleep(0.05)