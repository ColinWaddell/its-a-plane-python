import urllib.request
import json

from animator import Animator
from setup import colours, fonts, frames
from config import TEMPERATURE_LOCATION

from rgbmatrix import graphics

# Weather API
WEATHER_API_URL = "https://taps-aff.co.uk/api/"


def grab_temperature(location):
    current_temp = None

    try:
        request = urllib.request.Request(WEATHER_API_URL + location)
        raw_data = urllib.request.urlopen(request).read()
        content = json.loads(raw_data.decode("utf-8"))
        current_temp = content["temp_c"]

    except:
        pass

    return current_temp


# Scene Setup
TEMPERATURE_REFRESH_SECONDS = 60
TEMPERATURE_FONT = fonts.small
TEMPERATURE_FONT_HEIGHT = 6
TEMPERATURE_POSITION = (44, TEMPERATURE_FONT_HEIGHT + 1)
TEMPERATURE_COLOUR = colours.ORANGE
TEMPERATURE_MIN = 0
TEMPERATURE_MIN_COLOUR = colours.BLUE_LIGHT
TEMPERATURE_MAX = 25
TEMPERATURE_MAX_COLOUR = colours.ORANGE


class TemperatureScene(object):

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
    def temperature(self, count):

        if len(self._data):
            # Ensure redraw when there's new data
            return

        if not (count % TEMPERATURE_REFRESH_SECONDS):
            self.current_temperature = grab_temperature(TEMPERATURE_LOCATION)

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

            if self.current_temperature > 25:
                ratio = 1
            elif self.current_temperature > 0:
                ratio = (self.current_temperature - TEMPERATURE_MIN) / TEMPERATURE_MAX
            else:
                ratio = 0

            temp_colour = self.colour_gradient(
                colours.BLUE, colours.ORANGE, ratio
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
