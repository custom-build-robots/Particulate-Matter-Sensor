# Mobile Particulate Matter Sensor (MPMS)
This is my  python program for the mobile particulate matter sensor. 
You need a SDS011 particulate matter sensor and a USB GPS receiver.
I installed everything on a Raspberry Pi ZERO W.
![me and the mobile version of the Particulate Matter Sensor](https://www.byteyourlife.com/wp-content/uploads/2017/05/Ingmar_Stapel_mobiler_Feinstaub_Sensor_SDS011_klein.jpg)
## Component List
- SDS011 particualte matter sensor
- USB GPS receiver
## Python program sds011.py
This program logs the GPS coordinates and particulate matter values in a CSV file.
## Python program sds011_2.py
This program logs the GPS coordinates and particulate matter values in different KML files.
### Google Earth KML files with lines
Please add at the end of each KML file the closing for Document </Document> and kml </kml>.
- PM2.5 KLM file with a line (red orange green) and the altitude shows how high the messured values are.
- PM10 KLM file with a line (red orange green) and the altitude shows how high the messured values are.
### Google Earth KML files with point
Please add at the end of each KML file the closing for Document </Document> and kml </kml>.
- PM2.5 KLM file with and the messured values.
- PM2.5 KLM file with and the messured values.
# HowTo Guide
Teh detailed HowTo is available on my blog:
https://www.byteyourlife.com/haushaltsgeraete/feinstaub-sensor-sds011-mobile-variante-mit-datenaufzeichnung-und-gps-logging/7253
