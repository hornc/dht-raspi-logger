#!/usr/bin/python

import subprocess
import re
import sys
import time
import datetime
import gspread

# ===========================================================================
# Google Account Details
# ===========================================================================

# Account details for google docs
email       = 'secret'
password    = 'secret'
spreadsheet = 'DHT Logger'

poll_interval = 30*60
# DHT11 sensors can be connected to the following GPIO data pins:
sensors = ['22','21','17','15','4','1']
names   = ['Room', 'n/a', 'n/a', 'n/a', 'n/a', 'Cabinet']

# Login with your Google account
try:
  gc = gspread.login(email, password)
except:
  print "Unable to log in.  Check your email address/password"
  sys.exit()

# Open a worksheet from your spreadsheet using the filename
try:
  worksheet = gc.open(spreadsheet).sheet1
  # Alternatively, open a spreadsheet using the spreadsheet's key
  # worksheet = gc.open_by_key('0BmgG6nO_6dprdS1MN3d3MkdPa142WFRrdnRRUWl1UFE')
except:
  print "Unable to open the spreadsheet.  Check your filename: %s" % spreadsheet
  sys.exit()

# Continuously append data
while(True):
  # Run the DHT program to get the humidity and temperature readings!
  row = []
  for x in range(len(sensors)):
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
  except:
    print "Unable to append data.  Check your connection?"
    sys.exit()

  # Wait poll_interval seconds before continuing
  print "Wrote a row to %s" % spreadsheet
  time.sleep(poll_interval)
