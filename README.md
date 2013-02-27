DHT-RaspPi-logger
=================

Connect multiple DHT11 etc sensors to a Raspberry Pi and log to Google docs

This python script is what I am using to read multiple (currently up to six) DHT11 temperature and humidity sensors via a Raspberry Pi and send the results to a Google docs spreadsheet. It is a minor modification of example code found in the Adafruit tutorial at http://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/overview
which I will customise to fit my needs.

Original Adafruit code at github repo: https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code
>Adafruit's Raspberry-Pi Python Code Library
>
>Here is a growing collection of libraries and example python scripts for controlling a variety of Adafruit electronics with a Raspberry Pi
>
>In progress!
>
>Adafruit invests time and resources providing this open source code, please support Adafruit and open-source hardware by purchasing products from Adafruit!
>
>Written by Limor Fried, Kevin Townsend and Mikey Sklar for Adafruit Industries. BSD license

This script just uses Adafruit\_DHT from the Adafruit\_DHT\_Driver/ directory. I had to recompile the Adafruit binary to get it to work on my R.Pi, which also required the lowlevel BCM2835 C Library from http://www.open.com.au/mikem/bcm2835/index.html

The Google docs writing ability comes from the gspread python library: http://pypi.python.org/packages/source/g/gspread/gspread-0.0.13.tar.gz#md5=d413ad08805f3f0a1e9d5f9bebe5d35b  which is not included here.
```
wget http://pypi.python.org/packages/source/g/gspread/gspread-0.0.13.tar.gz#md5=d413ad08805f3f0a1e9d5f9bebe5d35b
tar -zxvf gspread-0.0.13.tar.gz
cd gspread
sudo python setup.py install
```

To write logged data to a Google Docs spreadsheet you will need to create a config file (default location: /root/.dhtlogger) with the following format:
```
<Base64 encoded Google Docs username@gmail.com>
<Base64 encoded password>
<Plaintext Google Docs spreadsheet name>
```

None of the C code here was written by me, I have just made modifications to the example python script to suit my application and storing it on github so I can easily clone to my Raspberry Pi's. If someone else finds my modifications useful, so much the better!

Thanks Adafruit for the original code and the very clear guide!  
   http://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/overview

C.Horn
