#!/usr/bin/python

import io
import termios
import pynmea2
import serial
import sys
import time
import threading

class GPSSensor:

    gpsInput = serial.Serial('/dev/ttyS0', 57600)
    nmeaString = ""

    def __init__(self,positionData,miscelaneousData):
        self.posData = positionData
        self.miscData = miscelaneousData
        threading.Thread(target=self.readGPSThread,daemon=True).start()

    def readGPSData(self):
        try:
            if not self.gpsInput.is_open:
                self.gpsInput.open()
            #Purposedly duplicated lines:
            self.gpsInput.flushInput()
            self.gpsInput.flushInput()
            #Purposedly duplicated lines:
            self.parseNmea(self.gpsInput.readline().decode('utf-8').strip())
            self.parseNmea(self.gpsInput.readline().decode('utf-8').strip())
            self.gpsInput.close()
        except:
            self.gpsInput.close()
        return

    def parseNmea(self,nmeaString):
        try:
            parsedNmea = pynmea2.parse(nmeaString)
            #print('------')
            #print(nmeaString)
            #print('++++++')
            if nmeaString.startswith('$GPGGA') :
                latDegreesRaw = parsedNmea.lat
                latDegrees = int(float(latDegreesRaw)/100)
                latSeconds = float(latDegreesRaw) - (latDegrees * 100)
                self.posData.setLatitude(latDegrees+(latSeconds/60))

                lonDegreesRaw = parsedNmea.lon
                lonDegrees = int(float(lonDegreesRaw)/100)
                lonSeconds = float(lonDegreesRaw) - (lonDegrees * 100)
                self.posData.setLongitude((lonDegrees+(lonSeconds/60))*-1)

                #lat = str(parsedNmea.latitude)
                #lon = str(parsedNmea.longitude)
                self.posData.setAltitude(parsedNmea.altitude)
                self.posData.setAltitudeUnit(parsedNmea.altitude_units)
                #if "None" not in alt:
                    #setCurrentAlt(str(parsedNmea.altitude))
                #else:
                    #setCurrentAlt("0")
                self.miscData.setSats(parsedNmea.num_sats)
                #print nmeaString
            if nmeaString.startswith("$GPRMC") :
                latDegreesRaw = parsedNmea.lat
                latDegrees = int(float(latDegreesRaw)/100)
                latSeconds = float(latDegreesRaw) - (latDegrees * 100)
                self.posData.setLatitude(latDegrees+(latSeconds/60))

                lonDegreesRaw = parsedNmea.lon
                lonDegrees = int(float(lonDegreesRaw)/100)
                lonSeconds = float(lonDegreesRaw) - (lonDegrees * 100)
                self.posData.setLongitude((lonDegrees+(lonSeconds/60))*-1)

                self.posData.setSpeed(parsedNmea.spd_over_grnd)
                #setCurrentSpd(str(parsedNmea.spd_over_grnd))
                #setCurrentYaw(str(parsedNmea.true_course))
                #print "HDG " + str(msg.true_course)
                #print nmeaString
            if nmeaString.startswith("$GPGSV") :
                #satsView = parsedNmea.num_sv_in_view
                print(nmeaString)
            #if nmeaString.startswith("$GPGSA") :
            #   parsedNmea = pynmea2.parse(msg)
            #   lat = str(msg.latitude)
            #   lon = str(msg.longitude)
            #   alt = str(msg.altitude) + " "+ msg.altitude_units
            #   if "None" not in alt:
            #       setCurrentAlt(str(msg.altitude))
            #   else:
            #       setCurrentAlt("0")
        except pynmea2.nmea.ParseError:
            print("GPS: Error parseado NMEA")
            print('NMEA String: '+nmeaString)
        except AttributeError:
            print("GPS: Attribute Error")
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
        except ValueError:
            print("GPS: Value Error")
            print('NMEA String: '+nmeaString)

    def readGPSThread(self):
        time.sleep(1)
        print("GPS Reader called and initialized.")
        while(True):
            self.readGPSData()