# Mobile Particulate Matter Sensor (MPMS)
This is my  python program for the mobile particulate matter sensor. 
You need a SDS011 particulate matter sensor and a USB GPS receiver.
I installed everything on a Raspberry Pi ZERO W.
## Component List
- SDS011 particualte matter sensor
- USB GPS receiver
## Python program sds011.py
This program logs the GPS coordinates and particulate matter values in a CSV file.
## Python program sds011_2.py
This program logs the GPS coordinates and particulate matter values in different KML files.
### Google Earth KML files with lines
- PM2.5 KLM file with a line (red orange green) and the altitude shows how high the messured values are.
- PM10 KLM file with a line (red orange green) and the altitude shows how high the messured values are.
### Google Earth KML files with point
- PM2.5 KLM file with and the messured values.
- PM2.5 KLM file with and the messured values.
## Auto start
This is the script "sds_start.sh" to start the python program via the cronttab after each reboot of the Raspberry Pi.
Just add the following line into the crontrab with the command "sudo nano /etc/crontab".
line to add:
- @reboot pi /home/pi/feinstaub/sds_start.sh &
## Known issue
The KML files are not closed correct. Please manual add the following two lines at the end of each KML file. Otherwise Google Earth will raise an error.
</Document>
</kml>
