# Covid-Vaccination-Counter-Dual-Display

ESP32 Dev Kit v1 with two OLED screens displaying Covid Vaccination Statistics retreived from a public API

![](Images/Set%20Up.png)

##Why?
I am trying to learn new things and there is no better way to learn new things than by doing it. What I wanted to do was create a little clock that would display some Covid related statistics, specifically the number vaccines that have been distributed and the number of people that have been vaccinated.

## How?
I am going to use a basic ESP32 based Dev Kit with two OLED screens and battery power it. It will connect to a Public API to retrieve the COVID vaccination statistics and display it on the screen.

When I started this project there was no public API available with the COVID Vaccination statistics so for this purpose of this project I manually retrieve the data from the CDC website and add it to a JSON Rest Server that I will connect to from the ESP32. For more information on how to set that up you can check this out my article on [How to setup a JSON REST API Server on Heroku](https://cashoefman.com/how-to-setup-a-json-rest-api-server-on-heroku) or take a look at my Github Repo, [How to setup a local and remote JSON REST API Server in ten-ish easy steps](https://github.com/cashoefman/my-api-server).

For now you could just use [my JSON Server](https://my-json-server.typicode.com/cashoefman/api-server/counts) for it but I am not sure how long that will keep working. 
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

[Kyle Redelinghuys](https://twitter.com/ksredelinghuys)) at the [Covid 19 API](https://covid19api.com) said he will be adding COVID Vaccination Statistic data to his API, once he does that, I will add information on how to use that API. But for now you can use my JSON Server. For this you will also have to update the API_URL to: `https://my-json-server.typicode.com/cashoefman/api-server/counts`.
#### ssd1306.py
This is the driver for the OLED screens
#### gfx.py
This is a library that I used to draw the battery indicator and the timer at the bottom of each OLED screen.
#### main.py
This is your main "application". Refer to the file itself for fairly detailed comments on what each line does.
