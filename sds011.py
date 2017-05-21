#!/usr/bin/env python
# coding: latin-1
# Autor:   Ingmar Stapel
# Datum:   20170521
# Version:   1.0
# Homepage:   https://www.byteyourlife.com/
# I used this program to log the gps coordinates and the 
# particulate matter values in a single CSV file

import serial, time, struct
import os
from gps import *
import time
import csv

# The path to store the csv file
fname = '/home/pi/feinstaub/feinstaub.csv'

# Start des gpsd Daemon für den NMEA Stream
os.system("sudo gpsd -b /dev/ttyACM0 -F /var/run/gpsd.sock -G")

time.sleep(5)

# Connect a serial connection to the particulate matter sensor
ser = serial.Serial("/dev/ttyUSB0", baudrate=9600, stopbits=1, parity="N", timeout=2)

# Create the session to read the NMEA GPS values to get the lat and lon coordinated.
session = gps(mode=WATCH_ENABLE)

ser.flushInput()

# if debug is True nothing will be stored in the csv file. You will
# see instead the values in the terminal window.
dbug = False

byte, lastbyte = "\x00", "\x00"

while True:
	lastbyte = byte
	byte = ser.read(size=1)

	# We got a valid packet header
	if lastbyte == "\xAA" and byte == "\xC0":
		sentence = ser.read(size=8) # Read 8 more bytes
		# Decode the packet - big endian, 2 shorts for pm2.5 and pm10, 2 reserved bytes, checksum, message tail
		readings = struct.unpack('<hhxxcc',sentence) 

		pm_25 = readings[0]/10.0
		pm_10 = readings[1]/10.0

		session.next()
		
		# Only log values if GPS coordinates are available.
		if -90 <= session.fix.latitude <= 90 and session.fix.latitude != 0:
			if dbug:
				print '-------------------------------------------'
				print 'Es wurden keine GPS Informationen empfangen'
				print 'Wurde der gpsd Daemon schon gestartet?'
				print "PM 2.5:",pm_25,"μg/m^3  PM 10:",pm_10,"μg/m^3"
				print '-------------------------------------------'
		# If coordinates are received successfully the values are stored.
		else:
			if dbug:
				print '------------------ GPS Informationen --------------'
				print 'Breitengrad:  ' , session.fix.latitude
				print 'Laengengrad:  ' , session.fix.longitude
				print 'Zeit utc:     ' , session.utc, \
				session.fix.time
				print "PM 2.5:",pm_25,"μg/m^3  PM 10:",pm_10,"μg/m^3"
				print '----------------------------------------------------'
			else:
				if os.path.isfile(fname):
					with open(fname,'a') as file:
						if session.fix.latitude == 0.0:
							line = ""+str(pm_25)+";"+str(pm_10)
						else:
							line = ""+str(pm_25)+";"+str(pm_10)+";"+str(session.fix.latitude)+";"+str(session.fix.longitude)+";"+str(session.utc)
						file.write(line)
						file.write('\n')
						file.close()
