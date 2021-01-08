# Covid-Vaccination-Counter-Dual-Display

ESP32 Dev Kit v1 with two OLED screens displaying Covid Vaccination Statistics retreived from a public API

![](Images/Set%20Up.png)

##Why?
I am trying to learn new things and there is no better way to learn new things than by doing it. What I wanted to do was create a little clock that would display some Covid related statistics, specifically the number vaccines that have been distributed and the number of people that have been vaccinated.

## How?

### Hardware Setup

1. ESP32 Dev Kit v1
2. .96" OLED Display
3. TP4056A Li-Ion Battery Charging Module
4. 82K Ohm and 28K ohm resistors
5. Micro Switch
6. A Li-Ion Battery

I will provide a fritzing diagram for the setup. Note that in order for the displays to work you have to change the address of the second display. On the displays I used you can do that by moving the "IIC Adress Select" SMD Resistor.

![](Images/OLED%20Screen.png)

### Software Setup

The base setup for your device is the same as I have described before [here](https://github.com/cashoefman/ESP32-BME680-uPy). Once you have your board configured with MicroPython upload the following files from the Git Repo
```
main.py
ssd1306.py
gfx.py
config.py
```
And you are set!
#### config.py
The Git Repo has a file called `example.config.py` just rename that file to `config.py` and update it with your Wifi SSID and Password.

Depending on the ESP 32 board you use and how you wire it you can also update the PINS for any onboard or remote LED and the PIN for the ADC reading the voltage of the battery.
#### ssd1306.py
This is the driver for the OLED screens
#### gfx.py
This is a library that I used to draw the battery indicator and the timer at the bottom of each OLED screen.
#### main.py
This is your main "application". Refer to the file itself for fairly detailed comments on what each line does.
