#!/usr/bin/python

import subprocess
import re
import sys
import time
import datetime
import gspread
import logging

logging.basicConfig(filename='sensors.log',format='%(asctime)s %(message)s',level=logging.DEBUG)
config_file = '/root/.dhtlogger'

# Account details for google docs, encoded in a seperate file
try:
  f = open(config_file, 'r')
  email, password, spreadsheet = f.read().splitlines()
except:
  print "Unable to open %s" % config_file
  print " see README.md for expected format of this file."

# polling interval in seconds
poll_interval = 30*60

# DHT11 sensors can be connected to the following GPIO data pins:
sensors = ['22','27','17','15','4','3']
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
    # skip un-named sensors
    if names[x] == 'n/a': continue
    # Run the DHT program to get the humidity and temperature readings!
    output = subprocess.check_output(["./Adafruit_DHT_Driver/Adafruit_DHT", "11", sensors[x]]);
    print "Sensor %d, %s, GPIO pin %s" % (x+1, names[x], sensors[x])
    print output
    matches = re.search("Temp =\s+([0-9.]+)", output)
    temp = float(matches.group(1)) if matches else '--' 
  
    # search for humidity printout
    matches = re.search("Hum =\s+([0-9.]+)", output)
    humidity = float(matches.group(1)) if matches else '--'

    print "Temperature: %s C" % str(temp)
    print "Humidity:    %s %%" % str(humidity)
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
