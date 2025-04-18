# RBG Matrix Flight Tracker

[Blog article about this project](https://blog.colinwaddell.com/flight-tracker/)

[![Finished flight tracker showing a flight](https://blog.colinwaddell.com/user/pages/01.articles/02.flight-tracker/screen-flight-thumb.jpg)](https://blog.colinwaddell.com/user/pages/01.articles/02.flight-tracker/screen-flight-thumb.jpg)

# Setup

## Installation
1. Assemble the RGB matrix, Pi, and Bonnet as described in [this Adafruit guide](https://learn.adafruit.com/adafruit-rgb-matrix-bonnet-for-raspberry-pi/overview). 
2. When complete, install the LED-matrix (rgbmatrix) python library, again as described in the [Adafruit installation guide](https://learn.adafruit.com/adafruit-rgb-matrix-bonnet-for-raspberry-pi/driving-matrices).
3. It is assumed the [solder bridge is added to the HAT](https://learn.adafruit.com/assets/57727) in order to use the Pi's soundcard to drive the device's PWM
4. Clone this repository (`git clone https://github.com/ColinWaddell/its-a-plane-python`). 
5. Install the FlightRadarAPI dependency (`sudo pip3 install FlightRadarAPI`). Note - running with `sudo` is required as `rgbmatrix` [must be run as as root](https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/bindings/python#using-the-library) for best performance.
6. Go to the its-a-plane-python repo folder `cd its-a-plane-python` (or wherever you cloned it to). 
7. Add a config.py file as described below. 
8. Run `sudo python3 its-a-plane.py`.


## Configuration
In the root of the repo create a files `config.py` with the settings for your display.
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


## Usage
If you are running a headless Pi that you are managing over `ssh`, you'll find that you have to remain connected for the display to keep running. A simple solution is to run the its-a-plane.py script in a `tmux` or `screen` session. For instance:
1. ssh to the Pi.
2. `sudo apt-get install tmux`
3. Once installed, start a new session by running the command `tmux`.
4. Run `sudo python3 /path/to/its-a-plane.py`. 
5. Detach from the tmux session by pressing Ctrl+B and then pressing D. 
6. `logout` to exit the Pi. Note that you'll need to re-enter or kill the tmux session to modify/stop the display. 

A more permanent solution if you'd like the software to run automatically on boot is to add it to your `/etc/rc.local`
1. ssh to the Pi.
2. Edit `/etc/rc.local` - for example `sudo nano -w /etc/rc.local`
3. Add a line pointing to the location this software is installed. In the following example some logging is provided for debugging purposes:
```
/usr/bin/python3 /home/pi/its-a-plane-python/its-a-plane.py > /home/pi/plane.log 2>&1 &
```

## Optional

### Loading LED
An LED can be wired to a GPIO on the Raspberry Pi which can then blinks when data is being loaded.

To enabled this add the following to your `config.py`. Adjust `LOADING_LED_GPIO_PIN` to suit your setup.

```
LOADING_LED_ENABLED = True
LOADING_LED_GPIO_PIN = 25
```

If you are using `rc.local` to load this software on boot and you see the error `RuntimeError: No access to /dev/mem.  Try running as root!` then you need to update your `rc.local` to launch the application using `sudo`

```
sudo /usr/bin/python3 /home/pi/its-a-plane-python/its-a-plane.py > /home/pi/plane.log 2>&1 &
```

### Rainfall chart
If weather data is being pulled from my server (as opposed to using `OPENWEATHER_API_KEY`) then you can
display a chart of rainfall by adding the following to your `config.py`:

```
RAINFALL_ENABLED = True
```

# License Update:
As of April 2025, Fridge Flight Tracker is released under the GNU General Public License v3.0

You’re welcome to use, modify, and share the code—just keep it under the same license and include
proper attribution (retain my copyright and license notice). See LICENSE for details.

I had to add this license folks have started selling these online as their own with zero attribution.
Open-source projects like this are our CVs: they show peers and potential employers what we can do.
Passing off someone else’s work as your own robs us of our chance to promote ourselves.
