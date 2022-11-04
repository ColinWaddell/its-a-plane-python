import urllib.request
from functools import lru_cache
import datetime
import time
import json
from rgbmatrix import graphics
from utilities.animator import Animator
from setup import colours, fonts, frames
from config import TEMPERATURE_LOCATION

# Attempt to load config data
try:
    from config import OPENWEATHER_API_KEY

except (ModuleNotFoundError, NameError, ImportError):
    # If there's no config data
    OPENWEATHER_API_KEY = None

try:
    from config import TEMPERATURE_UNITS

except (ModuleNotFoundError, NameError, ImportError):
    # If there's no config data
    TEMPERATURE_UNITS = "metric"

if TEMPERATURE_UNITS != "metric" and TEMPERATURE_UNITS != "imperial":
    TEMPERATURE_UNITS = "metric"

# Weather API
WEATHER_API_URL = "https://taps-aff.co.uk/api/"
OPENWEATHER_API_URL = "https://api.openweathermap.org/data/2.5/"

# Cache grabbing weather data

@lru_cache()
def grab_weather(location, ttl_hash=None):
    del ttl_hash # to emphasize we don't use
    
    request = urllib.request.Request(WEATHER_API_URL + location)
    raw_data = urllib.request.urlopen(request).read()
    content = json.loads(raw_data.decode("utf-8"))

    return content

def get_ttl_hash(seconds=60):
    """Return the same value withing `seconds` time period"""
    return round(time.time() / seconds)


def grab_temperature(location, units='metric'):
    current_temp = None

    try:
        weather = grab_weather(location, ttl_hash=get_ttl_hash())
        current_temp = weather["temp_c"]

    except:
        pass

    if units == "imperial":
        current_temp = (current_temp * (9.0 / 5.0)) + 32

    return current_temp

def grab_rainfall(location, hours=7):
    up_coming_rainfall = None

    try:
        weather = grab_weather(location, ttl_hash=get_ttl_hash())

        # We want to parse the data to find the
        # rainfall from now for <hours>
        forecast_today = weather["forecast"][0]["hourly"]
        forecast_tomorrow = weather["forecast"][1]["hourly"]
        hourly_forecast = forecast_today + forecast_tomorrow

        rainfall_per_hour = [
            hour["precip_mm"]
            for hour in hourly_forecast
        ]

        now = datetime.datetime.now()
        current_hour = now.hour
        up_coming_rainfall = rainfall_per_hour[current_hour:current_hour+hours]
        
    except:
        pass
    
    return up_coming_rainfall


def grab_temperature_openweather(location, apikey, units):
    current_temp = None

    try:
        request = urllib.request.Request(
            OPENWEATHER_API_URL
            + "weather?q="
            + location
            + "&appid="
            + apikey
            + "&units="
            + units
        )
        raw_data = urllib.request.urlopen(request).read()
        content = json.loads(raw_data.decode("utf-8"))
        current_temp = content["main"]["temp"]

    except:
        pass

    return current_temp


# Scene Setup
TEMPERATURE_REFRESH_SECONDS = 60
TEMPERATURE_FONT = fonts.small
TEMPERATURE_FONT_HEIGHT = 6
TEMPERATURE_POSITION = (44, TEMPERATURE_FONT_HEIGHT + 1)
TEMPERATURE_MIN_COLOUR = colours.BLUE
TEMPERATURE_MAX_COLOUR = colours.ORANGE

if TEMPERATURE_UNITS == "metric":
    TEMPERATURE_MIN = 0
    TEMPERATURE_MAX = 25
elif TEMPERATURE_UNITS == "imperial":
    TEMPERATURE_MIN = 32
    TEMPERATURE_MAX = 77


class WeatherScene(object):
    def __init__(self):
        super().__init__()
        self._last_temperature = None
        self._last_temperature_str = None

    def colour_gradient(self, colour_A, colour_B, ratio):
        return graphics.Color(
            colour_A.red + ((colour_B.red - colour_A.red) * ratio),
            colour_A.green + ((colour_B.green - colour_A.green) * ratio),
            colour_A.blue + ((colour_B.blue - colour_A.blue) * ratio),
        )

    @Animator.KeyFrame.add(frames.PER_SECOND * 1)
    def rainfall(self, count):
        pass


    @Animator.KeyFrame.add(frames.PER_SECOND * 1)
    def temperature(self, count):

        if len(self._data):
            # Ensure redraw when there's new data
            return

        if not (count % TEMPERATURE_REFRESH_SECONDS):

            if OPENWEATHER_API_KEY:
                self.current_temperature = grab_temperature_openweather(
                    TEMPERATURE_LOCATION, OPENWEATHER_API_KEY, TEMPERATURE_UNITS
                )
            else:
                self.current_temperature = grab_temperature(TEMPERATURE_LOCATION, TEMPERATURE_UNITS)

        if self._last_temperature_str is not None:
            # Undraw old temperature
            _ = graphics.DrawText(
                self.canvas,
                TEMPERATURE_FONT,
                TEMPERATURE_POSITION[0],
                TEMPERATURE_POSITION[1],
                colours.BLACK,
                self._last_temperature_str,
            )

        if self.current_temperature:
            temp_str = f"{round(self.current_temperature)}°".rjust(4, " ")

            if self.current_temperature > TEMPERATURE_MAX:
                ratio = 1
            elif self.current_temperature > TEMPERATURE_MIN:
                ratio = (self.current_temperature - TEMPERATURE_MIN) / TEMPERATURE_MAX
            else:
                ratio = 0

            temp_colour = self.colour_gradient(
                TEMPERATURE_MIN_COLOUR, TEMPERATURE_MAX_COLOUR, ratio
            )

            # Draw temperature
            _ = graphics.DrawText(
                self.canvas,
                TEMPERATURE_FONT,
                TEMPERATURE_POSITION[0],
                TEMPERATURE_POSITION[1],
                temp_colour,
                temp_str,
            )

            self._last_temperature = self.current_temperature
            self._last_temperature_str = temp_str
