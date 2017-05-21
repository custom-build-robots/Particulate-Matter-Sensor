#!/bin/bash
/bin/sleep 10
gpsd -b /dev/ttyACM0 -F /var/run/gpsd.sock -G >> /home/pi/feinstaub/gpsd_daemon.log 2>&1 &
/bin/sleep 10
python /home/pi/feinstaub/sds011_2.py >> /home/pi/feinstaub/python_sds011.log 2>&1 &
