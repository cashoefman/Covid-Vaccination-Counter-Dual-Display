# Copyright 2020 Cas Hoefman
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Basic Setup
#
# Import setting from config file 
import config
# Get a device ID, I am not really using that for anything in this example but some APIs like things like that
#
import machine
device_id = ('{:02x}{:02x}{:02x}{:02x}'.format(machine.unique_id()[0], machine.unique_id()[1], machine.unique_id()[2], machine.unique_id()[3]))
#
# Start Display
import ssd1306
from machine import Pin
#pin16 = machine.Pin(16, machine.Pin.OUT) # NOTE: On an Heltec Wifi Kit 32 you have to set pin 16 to high to turn on the screen
#pin16.value(1)
#
# And Configure the screen
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
oled1 = ssd1306.SSD1306_I2C(128, 64, i2c, addr=60) # 128,64 defines the screen width and height of the first oled
oled2 = ssd1306.SSD1306_I2C(128, 64, i2c, addr=61) # 128,64 defines the screen width and height of the second oled
#
# Setup a graphic drawing on both OLED displays, We'll use that later to draw on the screens
import gfx
graphics1 = gfx.GFX(128, 64, oled1.pixel)
graphics2 = gfx.GFX(128, 64, oled2.pixel)
#
# Let's put some stuff on the screen as we get started
oled1.fill(0)
oled1.text('COVID VAC COUNT', 0, 0)
oled1.text('ID: ' + device_id, 0, 20)
oled1.text('By: Cas Hoefman', 0, 30)
oled1.text('Micropython 1.13', 0, 40)      
oled1.show()
#
# And on the second screen
oled2.fill(0)
oled2.text('Starting...', 0, 0)
oled2.show()
#
# Check the battery and show the battery status on the second screen
adc_pin = machine.Pin(config.device_config['adc_pin_battery'])
adc = machine.ADC(adc_pin)
adc.atten(adc.ATTN_11DB)
val = adc.read()
volt = round(val * (3.3 / 4095),2)
percentage = round((val * (3.3 / 4095)) / 3.3 * 100)
print(val, 'V')
print(percentage, '%')
oled2.text('Battery: ' + str(volt) + 'V', 0, 30)
oled2.text(str(round(val)) + '      ' + str(percentage) + '%', 0, 40)
oled2.show()
#
# Set Built-in LED pin
led_pin = machine.Pin(config.device_config['led_pin'], Pin.OUT)
led_pin.value(0)
#
# Get Wifi Set Up, this should become a function to call later in the loop so you can check on if the Wifi Connection is still up
# Next time!
import ntptime
import network
import time
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect(config.wifi_config['ssid'], config.wifi_config['password'])
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(1)
        pass
#
# Printing IP data to serial and adding some info to OLED1 and OLED2
print('network config:', wlan.ifconfig())
oled1.text('Wifi Connected', 0, 10)
oled1.show()
oled2.text('SSID: ', 0, 10)
oled2.text(((config.wifi_config['ssid'])[0:14]), 0, 20)
oled2.show()
led_pin.value(1)
#
# Now that we are connected set the time
from machine import RTC
import ntptime
import utime
ntptime.host = config.api_config['time_server']
try:
    ntptime.settime()
except:
    print(".", end="")
    time.sleep(1)
    pass
tm = utime.localtime()
tm = tm[0:3] + (0,) + tm[3:6] + (0,)
machine.RTC().datetime(tm)
timestamp = '{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}.000Z'.format(tm[0], tm[1], tm[2], tm[3], tm[4], tm[5])
print(timestamp)
timenow = '{:02d}:{:02d}:{:02d}'.format(tm[3], tm[4], tm[5]) 
oled1.text('Time: ' + timenow, 0, 50)    
oled1.show()
time.sleep(5) # Waiting a few seconds just for the fun of it
#
# Set the Time, not really using this anywhere but who knows if I want to display the time at some point somewhere
tm = utime.localtime()
timestamp = '{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}.000Z'.format(tm[0], tm[1], tm[2], tm[3], tm[4], tm[5])  
timenow = '{:02d}:{:02d}:{:02d}'.format(tm[3], tm[4], tm[5])  
datenow = '{:02d}-{:02d}-{:04d}'.format(tm[1], tm[2], tm[0])
#
# GET Latest CDC Data from the test API, probably should check here for a Wifi status but oh well...
while True:
    # Employing a bit of a "hack" to get the ID of the record with the latest entry with counts from the API
    # There must be a better way to do this but I don't want to get all the records at once.
    # Not pretty but it works
    import urequests as requests
    getid = requests.get(url=config.api_config['api_url'] + '?_sort=id&_order=desc&_limit=1')
    parsedid = getid.json() # Turns the response into a json object
    getid.close() # Docs say to close this when done.
    parsedid = (parsedid[0]) # Gets the first (and only) element from the list and that becomes a dict
    id = parsedid["id"] # We get the id from the dict
    #
    # Now we go get the latest record and a older record before that with the counts from the API
    response = requests.get(config.api_config['api_url'] + '/' + str(id))
    response_older = requests.get(config.api_config['api_url'] + '/' + str(id-config.app_config['data_older'])) #Value from config -5 will get data from 5 days ago, -7 will get data from a week ago, presuming the data is updated every day
    print ('Got API data')
    #
    # Let's parse the values we need
    parsed = response.json()
    response.close()
    parsed_older = response_older.json()
    response_older.close()
    administered = (parsed['Total_Doses_Administered'])
    distributed = (parsed['Total_Doses_Distributed'])
    dateLastUpdated = (parsed['DataLastUpdated'])
    #
    # Let's get the latest battery status percentage
    val = adc.read()
    percentage = round((val * (3.3 / 4095)) / 3.3 * 100)
    #
    # Let's Update the OLED Display and display that data 
    oled1.fill(0)
    oled1.text('VACCINATIONS', 17, 0)
    oled1.text('CDC REPORTED', 18, 10)
    oled1.text('Distributed', 21, 20)
    oled1.text(str(round(distributed)), 31, 30)
    oled1.text('Administered', 18, 43)
    oled1.text(str(round(administered)), 35, 53)
    #
    # And we'll use the graphic library to draw line with the battery status on screen 1 at the bottom
    graphics1.line(1, 63, 127, 63, 0) # remove the pixels on the last line
    graphics1.line(0, 62, 0, 63, 1)
    graphics1.line(31, 62, 31, 63, 1)
    graphics1.line(63, 62, 63, 63, 1)
    graphics1.line(94, 62, 94, 63, 1)
    graphics1.line(127, 62, 127, 63, 1)
    batline = (round(percentage / 100 * 128))
    graphics1.line(1, 63, batline, 63, 1)
    oled1.show()
    #
    # Turn the Led Off so we know the API Call is completed
    led_pin.value(0)
    #
    # set the time between API Calls in "about" seconds based on the API Interval setting from the config file
    waiting = config.api_config['api_interval'] 
    for i in range(waiting):
        #
        # Now we are going to calculate the average vaccinations that are being done and the average vaccines being distributed per second
        # We take the values from the last two records, compare those to come up with  values
        administered_older = (parsed_older['Total_Doses_Administered'])
        distributed_older = (parsed_older['Total_Doses_Distributed'])
        dateLastUpdated_older = (parsed_older['DataLastUpdated'])
        timedelta = dateLastUpdated - dateLastUpdated_older
        administered_delta = (administered - administered_older) / timedelta
        distributed_delta = (distributed - distributed_older) / timedelta
        tmoffset = time.time() + 946684800 # Gotta fix for the fact that Micropython clock doesn't start in 1970
        secondssince = tmoffset - dateLastUpdated
        administered_increase = administered_delta * secondssince
        distributed_increase = distributed_delta * secondssince
        administered_calculated = administered + administered_increase
        distributed_calculated = distributed + administered_increase
        #
        # Print some values so I can see it works in serial
        print(str(round(administered_calculated)))
        print(str(round(distributed_calculated)))
        #
        # Update the OLED Display again  
        oled2.fill(0)
        oled2.text('VACCINATIONS', 17, 0)
        oled2.text('FORECASTED', 24, 10)
        oled2.text('Distributed', 21, 20)
        oled2.text(str(round(distributed_calculated)), 31, 30)
        oled2.text('Administered', 18, 43)
        oled2.text(str(round(administered_calculated)), 35, 53)
        #
        # Draw a line with the time until the next API Call 
        graphics2.line(1, 63, 127, 63, 0) # remove the pixels on the last line
        graphics2.line(0, 62, 0, 63, 1)
        graphics2.line(31, 62, 31, 63, 1)
        graphics2.line(63, 62, 63, 63, 1)
        graphics2.line(94, 62, 94, 63, 1)
        graphics2.line(127, 62, 127, 63, 1)
        timeline = (round((128 / waiting) * (waiting-i))) #calculate how long the line should be 128 px / waiting period * remaining # of seconds
        graphics2.line(1, 63, timeline, 63, 1)
        oled2.show()
        #
        # Wait one second before finishing this loop
        time.sleep(1)
    #
    # After doing that for about 30 seconds we go back and get the latest data from the API and do it all again.
    # Set the LED to on so we know the API Call started
    led_pin.value(1) 
