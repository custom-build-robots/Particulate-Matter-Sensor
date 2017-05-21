#!/usr/bin/python
# -*- coding: UTF-8 -*-

import serial, time, struct
import httplib, urllib
import os
from gps import *
import time
import csv
import datetime
from random import randint

# micro-sd card paths for the kml files
fname25 = '/home/pi/feinstaub/feinstaub_25_'+datetime.datetime.now().strftime ("%Y%m%d")+'.kml'
fname10 = '/home/pi/feinstaub/feinstaub_10_'+datetime.datetime.now().strftime ("%Y%m%d")+'.kml'

fname25_line = '/home/pi/feinstaub/feinstaub_25_line_'+datetime.datetime.now().strftime ("%Y%m%d")+'.kml'
fname10_line = '/home/pi/feinstaub/feinstaub_10_line_'+datetime.datetime.now().strftime ("%Y%m%d")+'.kml'

# not used any more
# fname_csv_25 = '/home/pi/feinstaub/feinstaub_25_csv_'+datetime.datetime.now().strftime ("%Y%m%d")+'.csv'
# fname_csv_10 = '/home/pi/feinstaub/feinstaub_10_csv_'+datetime.datetime.now().strftime ("%Y%m%d")+'.csv'

# USB device
# actual not working because of a problem with the usb drive
# fname = '/home/pi/usb/feinstaub_'+datetime.datetime.now().strftime ("%Y%m%d")+'.kml'
# os.system("sudo mount /dev/sdb1 /home/pi/usb -o umask=000")

# start the GPSd daemon
# optional if the crontab is not used to start the process
#os.system("sudo gpsd -b /dev/ttyACM0 -F /var/run/gpsd.sock -G >> /home/pi/feinstaub/gpsd.log 2>&1 &")

time.sleep(2)

byte, lastbyte = "\x00", "\x00"

lat_old = "initial"
lon_old = "initial"
pm_old_25 = 0
pm_old_10 = 0

color = "#00000000"

def write_log(msg):
	message = msg
	fname = "/home/pi/feinstaub/feinstaub.log"
	with open(fname,'a+') as file:
		file.write(str(message))
		file.write("\n")
		file.close()			
						
def write_kml(value_pm, value_lat, value_lon, value_time, value_fname, type):	
	pm = value_pm
	lat = value_lat
	lon = value_lon
	time = value_time
	fname = value_fname
	
	try:
		if os.path.exists(fname):
			with open(fname,'a+') as file:
				file.write("   <Placemark>\n")
				file.write("       <name>"+type+": "+ pm +"</name>\n")
				file.write("       <description> Time: " + time + "</description>\n")
				file.write("       <Point>\n")
				file.write("           <coordinates>" + lon + "," + lat + ",0</coordinates>\n")
				file.write("       </Point>\n")
				file.write("   </Placemark>\n")	
				file.close()	

		else:
			with open(fname,'a+') as file:
				file.write("<?xml version='1.0' encoding='UTF-8'?>\n")
				file.write("<kml xmlns='http://earth.google.com/kml/2.1'>\n")
				file.write("<Document>\n")
				file.write("   <name> feinstaub_" + type + "_" + datetime.datetime.now().strftime ("%Y%m%d") + ".kml </name>\n")
				file.write('\n')
				file.close()
	except Exception, e:
		write_log(str(e))

def color_selection(value):
	# red
	color = "#64009614"	
	if 50 <= value <= 2000:
		color = "#641400F0"
	# orange
	elif 25 <= value <= 49:
		color = "#641478FF"
	# green
	elif 0 <= value < 25:
		color = "#64009614"		
		
	return color

def write_kml_line(value_pm, value_pm_old, value_lon_old, value_lat_old, value_lat, value_lon, value_time, value_fname, type, value_color):
	pm = value_pm
	pm_old = value_pm_old
	lat_old = value_lat_old
	lon_old = value_lon_old
	lat = value_lat
	lon = value_lon
	time = value_time
	fname = value_fname
	color = value_color 
	try:
		if os.path.exists(fname):
			with open(fname,'a+') as file:
				file.write("   <Placemark>\n")
				file.write("       <LineString>\n")
				file.write("           <altitudeMode>relativeToGround</altitudeMode>\n")
				file.write("           <coordinates>" + lon + "," + lat + "," + pm + "\n           "+ lon_old+ ","+ lat_old+ "," + pm_old + "</coordinates>\n")
				file.write("       </LineString>\n")
				file.write("       <Style>\n")
				file.write("           <LineStyle>\n")
				file.write("               <color>" + color + "</color>\n")
				file.write("               <width>8</width>\n")
				file.write("           </LineStyle>\n")
				file.write("       </Style>\n")
				file.write("   </Placemark>\n")	
				file.close()	

		else:
			with open(fname,'a+') as file:
				file.write("<?xml version='1.0' encoding='UTF-8'?>\n")
				file.write("<kml xmlns='http://earth.google.com/kml/2.1'>\n")
				file.write("<Document>\n")
				file.write("   <name> feinstaub_"+type+"_" + datetime.datetime.now().strftime ("%Y%m%d") + ".kml </name>\n")
				file.write('\n')
				file.close()	
	except Exception, e:
		write_log(e)

# Try to read the Feinstaub Sensor vlues
try:
	ser = serial.Serial("/dev/ttyUSB0", baudrate=9600, stopbits=1, parity="N", timeout=2)
except Exception, e:
	write_log(e)

# create the session for the gps daemon.
session = gps(mode=WATCH_ENABLE)

try:
	ser.flushInput()
except Exception, e:
	write_log(e)
	
while True:
	time.sleep(1)
	lastbyte = byte
	try:
		byte = ser.read(size=1)
	except Exception, e:
		write_log(e)
		
	#color_25 = "#64009614"
	#color_10 = "#64009614"

	# We got a valid packet header
	if lastbyte == "\xAA" and byte == "\xC0":
		try:
			sentence = ser.read(size=8) # Read 8 more bytes
			# Decode the packet - big endian, 2 shorts for pm2.5 and pm10, 2 reserved bytes, checksum, message tail
			readings = struct.unpack('<hhxxcc',sentence) 
		except Exception, e:
			write_log(e)
		pm_25 = readings[0]/10.0
		pm_10 = readings[1]/10.0
	
		# get next GPS coordinates
		try:
			session.next()
		except Exception, e:
			write_log(e)
			

		# only if a fix gps solution is available start recording the data
		if -90 <= session.fix.latitude <= 90 and session.fix.latitude != 0:
			if lat_old == "initial":
				lat_old = session.fix.latitude

			if lon_old == "initial":	
				lon_old = session.fix.longitude
			
			write_kml(str(pm_25), str(session.fix.latitude), str(session.fix.longitude), str(session.utc), fname25, "25")
			write_kml(str(pm_10), str(session.fix.latitude), str(session.fix.longitude), str(session.utc), fname10, "10")
			
			color_25 = color_selection(pm_25)
			color_10 = color_selection(pm_10)
			
			time.sleep(1)
			
			write_kml_line(str(pm_25), str(pm_old_25), str(lon_old), str(lat_old), str(session.fix.latitude), str(session.fix.longitude), str(session.utc), fname25_line, "25", color_25)
			write_kml_line(str(pm_10), str(pm_old_10), str(lon_old), str(lat_old), str(session.fix.latitude), str(session.fix.longitude), str(session.utc), fname10_line, "10", color_10)

			lat_old = session.fix.latitude
			lon_old = session.fix.longitude
			
			pm_old_25 = pm_25
			pm_old_10 = pm_10
