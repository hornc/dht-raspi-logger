#!/usr/bin/python

import subprocess
import re
import sys
import time
import datetime
import gspread
import logging

logging.basicConfig(filename='sensors.log',format='%(asctime)s %(message)s',level=logging.DEBUG)

# Account details for google docs, encoded in a seperate file
f = open('/root/.dhtlogger', 'r')
email, password, spreadsheet = f.read().splitlines()

# polling interval in seconds
poll_interval = 30*60

# DHT11 sensors can be connected to the following GPIO data pins:
sensors = ['22','21','17','15','4','1']
names   = ['Room', 'n/a', 'n/a', 'n/a', 'n/a', 'Cabinet']

# Login with your Google account
try:
  gc = gspread.login(email.decode('base64'), password.decode('base64'))
  logging.info("Successfully Logged into google docs as %s" % email.decode('base64'))
except:
  logging.warning("Unable to log in.  Check your email address/password")
  sys.exit()

# Continuously append data
while(True):
  # clear the array used to store all of the various sensor results at a particular read time
  row = []
  # Open the first worksheet from your spreadsheet using the filename
  try:
    worksheet = gc.open(spreadsheet).sheet1
  except:
    logging.warning("Unable to open the spreadsheet, Skipping this sensor read. Check your filename: %s" % spreadsheet)
    time.sleep(poll_interval)
    continue
  for x in range(len(sensors)):
    # Run the DHT program to get the humidity and temperature readings!
    output = subprocess.check_output(["./Adafruit_DHT", "11", sensors[x]]);
    print "Sensor %d, %s, GPIO pin %s" % (x+1, names[x], sensors[x])
    print output
    matches = re.search("Temp =\s+([0-9.]+)", output)
    if (not matches):
	time.sleep(3)
	continue
    temp = float(matches.group(1))
  
    # search for humidity printout
    matches = re.search("Hum =\s+([0-9.]+)", output)
    if (not matches):
	time.sleep(3)
	continue
    humidity = float(matches.group(1))

    print "Temperature: %.1f C" % temp
    print "Humidity:    %.1f %%" % humidity
    row.extend([temp, humidity])
 
  # Append the data in the spreadsheet, including a timestamp
  try:
    values = [datetime.datetime.now()] + row
    print values
    worksheet.append_row(values)
    print "Wrote a row to %s" % spreadsheet
  except:
    logging.warning("Unable to append data.  Check your connection?")

  # Wait poll_interval seconds before continuing
  time.sleep(poll_interval)
