# Documentation

[Blog article about this project](https://blog.colinwaddell.com/flight-tracker/)

# Setup

## Installation
1. Assemble the RGB matrix, Pi, and Bonnet as described in [this Adafruit guide](https://learn.adafruit.com/adafruit-rgb-matrix-bonnet-for-raspberry-pi/overview). 
2. When complete, install the LED-matrix (rgbmatrix) python library, again as described in the [Adafruit installation guide](https://learn.adafruit.com/adafruit-rgb-matrix-bonnet-for-raspberry-pi/driving-matrices).
3. Clone this repository (`git clone https://github.com/ColinWaddell/its-a-plane-python`). 
4. Install the FlightRadarAPI dependency (`sudo pip install FlightRadarAPI`). Note - running with `sudo` is requred make this python library available to root on the pi. This will overcome what I understand is is a Debian (and Raspbian)-specific behavior of `pip`, where the default installation is `--user` specific. We'll need this later, as `rgbmatrix` [must be run as as root](https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/bindings/python#using-the-library) for best performance.
5. Go to the its-a-plane-python repo folder `cd its-a-plane-python` (or wherever you cloned it to). 
6. Add a config.py file as described below. 
7. Run `sudo python its-a-plane.py`. i


## Configuration

In the root of the repo create a files `config.py` with the settings for your display.
`ZONE_HOME` defines the area within which flights should be tracked. 
`LOCATION_HOME` is the latitude/longitude of your home.
`TEMPERATURE_LOCATION` is the city that will be used to display the temperature. If using Openweather (see next), please type in the city in the form of "City" or "City,Province/State,Country", e.g. "Paris" or "Paris,Ile-de-France,FR".
`OPENWEATHER_API_KEY` If provided, will use the OpenWeather API. You can obtain a free OpenWeather API key by going [here](https://openweathermap.org/price). If not using OpenWeather, just leave as `OPENWEATHER_API_KEY = "" `. 

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
TEMPERATURE_LOCATION = "Glasgow"
OPENWEATHER_API_KEY = "" # Get an API key from https://openweathermap.org/price
```


## Usage
If you are running a headless Pi that you are managing over `ssh`, you'll find that you have to remain connected for the display to keep running. A simple solution is to run the its-a-plane.py script in a `tmux` or `screen` session. For instance:
1. ssh to the Pi.
2. `sudo apt-get install tmux`
3. Once installed, start a new session by running the command `tmux`.
4. Run `sudo python /path/to/its-a-plane.py`. 
5. Detach from the tmux session by pressing Ctrl+B and then pressing D. 
6. `logout` to exit the Pi. Note that you'll need to re-enter or kill the tmux session to modify/stop the display. 
