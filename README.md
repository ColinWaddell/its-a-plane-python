# RBG Matrix Flight Tracker

[Blog article about this project](https://blog.colinwaddell.com/flight-tracker/)

[![Finished flight tracker showing a flight](https://blog.colinwaddell.com/media/flight-tracker/screen-flight-thumb.jpg)](https://blog.colinwaddell.com/media/flight-tracker/screen-flight.jpg)

# Setup

## Installation

The previous instructions were written against Debian Buster and can be found a this commit. People were starting to find the instructions didn't line up with the latest version of Debian Bookwork. These new instructions are less battle-tested that the previous version so if you run into any problems please raise it as issue.

### Installation Guide

These instructions will assume that running the Flight Tracker on your Raspberry Pi is the only thing you're going to be doing with the device. The other assumptions are going to be:

- You've got your Raspberry Pi setup with Raspbian based on Debian Bookwork 
- The username of the device is `pi`
- If you're not using a screen/keyboard attached to the Pi then you've figured out how to remote edit over SSH

### Installation Locations

For future reference, in this installation process we're going to use the following locations:

| Location                                | Purpose                                                             |
| --------------------------------------- | ------------------------------------------------------------------- |
| `/home/pi/rpi-rgb-led-matrix`           | RGB Matrix Driver                                                   |
| `/home/pi/its-a-plane-python`           | The Flight Tracking software (this repo)                            |
| `/home/pi/its-a-plane-python/env`       | The virtual environment we'll install the necessary python packages |
| `/home/pi/its-a-plane-python/config.py` | Config file for this flight tracking software                       |

### First steps

Before installing anything let's ensure out system is up-to-date:

```
sudo apt-get update
sudo apt-get dist-upgrade
```

This will take a while on a fresh device as it picks up all its updates.

### Install the RGB Screen


1. Assemble the RGB matrix, Pi, and Bonnet as described in [this Adafruit guide](https://learn.adafruit.com/adafruit-rgb-matrix-bonnet-for-raspberry-pi/overview).
2. It is recommended that the [solder bridge is added to the HAT](https://learn.adafruit.com/assets/57727) in order to use the Pi's soundcard to drive the device's PWM 
3. Please [read the official installating instructions](https://learn.adafruit.com/adafruit-rgb-matrix-bonnet-for-raspberry-pi/driving-matrices) for further details before proceding but don't run any commands or install anything yet
4. Use the following commands to install the `rgb-matrix` library. Please note the paths used in these instructions are used later in this guide and must be adhered to for everything to make sense.

```
cd /home/pi
curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/main/rgb-matrix.sh > /tmp/rgb-matrix.sh
sudo bash /tmp/rgb-matrix.sh
```

5. If the installating has worked successfully then there should be some demo applications available to run:

```
cd /home/pi/rpi-rgb-led-matrix/examples-api-use
sudo ./demo --led-rows=32 --led-cols=64 -D0
```

### Install this Flight Tracking software

1. Clone this repository (`git clone https://github.com/ColinWaddell/its-a-plane-python`). 
2. Head into this repository and create a virtual-environment, activate it and install all the dependancies

```
cd /home/pi/its-a-plane-python
python3 -m venv env
source env\bin\activate
pip install -r requirements.txt
```

3. Head into the rgb-matrix library and install the python library into our virtual environment. These commands assume you are still using the same environment that we activated in the above steps. If not rerun the `source` command in the `its-a-plane` directory.

```
cd /home/pi/rpi-rgb-led-matrix/bindings/python
pip install .
```

### Configure the Flight Tracking software for your location

These instructions will show you how to create a config file from the commandline with `nano` but in reality you can do this however you want.

```
cd /home/pi/its-a-plane-python 
nano config.py
```

Here is an example config you can copy into that file:

```
ZONE_HOME = {
    "tl_y": 56.06403, # Top-Left Latitude (deg)
    "tl_x": -4.51589, # Top-Left Longitude (deg)
    "br_y": 55.89088, # Bottom-Right Latitude (deg)
    "br_x": -4.19694 # Bottom-Right Longitude (deg)
}
LOCATION_HOME = [
    55.9074356, # Latitude (deg)
    -4.3331678, # Longitude (deg)
    0.01781 # Altitude (km)
]
WEATHER_LOCATION = "Glasgow"
OPENWEATHER_API_KEY = "" # Get an API key from https://openweathermap.org/price
TEMPERATURE_UNITS = "metric"
MIN_ALTITUDE = 100
BRIGHTNESS = 50
GPIO_SLOWDOWN = 2
JOURNEY_CODE_SELECTED = "GLA"
JOURNEY_BLANK_FILLER = " ? "
HAT_PWM_ENABLED = True
```

To save and exit nano hit `Ctrl-X` followed by `Y`.

In reality you'll want to customise `config.py` for your own purposes.

### Configuration file details 
* `ZONE_HOME` defines the area within which flights should be tracked. 
* `LOCATION_HOME` is the latitude/longitude of your home.
* `WEATHER_LOCATION` is the city that will be used to display the temperature. If using Openweather (see next), please type in the city in the form of "City" or "City,Province/State,Country", e.g. "Paris" or "Paris,Ile-de-France,FR".
* `OPENWEATHER_API_KEY` If provided, will use the OpenWeather API. You can obtain a free OpenWeather API key by going [here](https://openweathermap.org/price) (Optional)
* `TEMPERATURE_UNITS` One of "metric" or "imperial". Defaults to "metric".
* `MIN_ALTITUDE` Will remove planes below a certain altitude (in feet). Depending on the defined ZONE_HOME, can be useful for filtering out planes parked on the tarmac.
* `BRIGHTNESS` 0-100, changes the brightness of the display. 
* `GPIO_SLOWDOWN` 0-4, larger numbers for faster hardware can reduce/eliminate flickering. (e.g., 2 seems to work well on a Pi Zero 2 W, but 0 might be fine for an older Pi Zero). 
* `JOURNEY_CODE_SELECTED` Three-letter airport code of local airport to put in **bold** on the display (Optional).
* `JOURNEY_BLANK_FILLER` Three-letter text to use in place of an unknown airport origin/destination. Defaults to " ? ".
* `HAT_PWM_ENABLED` Drive the PWM using the Pi's soundcard, [assuming the solder bridge has been added to the HAT](https://learn.adafruit.com/assets/57727). Defaults to `True`



### Configuring permissions to avoid running as root

Previous versions of the instructions always pointed out to run everything as root for performance reasons but for security I think this is best avioded. Plus the latest version of the GPIO driver and rgb-matrix have strong opinions about who is in charge when running as root.

To avoid running as root and to grant python permission to set real-time scheduling priorities without needing to run as root:

```
sudo setcap 'cap_sys_nice=eip' /usr/bin/python3.11 
```

### Running the software manually

The software can now be tested by running it from the command-line

```
cd /home/pi/its-a-plane-python 
env/bin/python3 its-a-plane.py
```

### Running the software on start-up

This repo contains an example `.service` file to allow this software to be easily ran on boot. Provided that the same paths have been used in your own installation as these instructions then you shouldn't need to edit this file.

```
sudo cp /home/pi/its-a-plane-python/assets/its-a-plane.service /etc/systemd/system/its-a-plane.service
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable its-a-plane.service
sudo systemctl start its-a-plane.service
```

Any problems, check the status and logs:

```
sudo systemctl status its-a-plane.service
journalctl -u its-a-plane.service -f
```

## Optional

### Loading LED
An LED can be wired to a GPIO on the Raspberry Pi which can then blinks when data is being loaded.

To enabled this add the following to your `config.py`. Adjust `LOADING_LED_GPIO_PIN` to suit your setup.

```
LOADING_LED_ENABLED = True
LOADING_LED_GPIO_PIN = 25
```

### Rainfall chart
If weather data is being pulled from my server (as opposed to using `OPENWEATHER_API_KEY`) then you can
display a chart of rainfall by adding the following to your `config.py`:

```
RAINFALL_ENABLED = True
```