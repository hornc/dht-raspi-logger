#!/bin/sh
# to run this every 15mins add the following line to root user's crontab:
# */15 * * * * /home/pi/DHT-RaspPi-logger/cron/wlan-monitor.sh
if ifconfig wlan0 | grep -q "inet addr:" ; then
  echo "WiFi connected, everything is OK!" 
else
  echo "Network connection down! Attempting reconnection."
  ifup --force wlan0
fi
