import urllib.request
import json

from animator import Animator
from constants import framerate, colours, fonts

from rgbmatrix import graphics


TEMPERATURE_LOCATION = "Glasgow"
TEMPERATURE_REFRESH_SECONDS = 60
TEMPERATURE_FONT = fonts.font_small
TEMPERATURE_FONT_HEIGHT = 6
TEMPERATURE_POSITION = (44, TEMPERATURE_FONT_HEIGHT + 1)
TEMPERATURE_COLOUR = colours.COLOUR_ORANGE
TEMPERATURE_MIN = 0
TEMPERATURE_MIN_COLOUR = colours.COLOUR_BLUE_LIGHT
TEMPERATURE_MAX = 25
TEMPERATURE_MAX_COLOUR = colours.COLOUR_ORANGE


URL = "https://taps-aff.co.uk/api/"
LOCATION = "Glasgow"  # todo: add to config.py


def grab_temperature(location):
    current_temp = None

    try:
        request = urllib.request.Request(URL + location)
        raw_data = urllib.request.urlopen(request).read()
        content = json.loads(raw_data.decode("utf-8"))
        current_temp = content["temp_c"]

    except:
        pass

    return current_temp


class TemperatureScene:

    def colour_gradient(self, colour_A, colour_B, ratio):
        return graphics.Color(
            colour_A.red + ((colour_B.red - colour_A.red) * ratio),
            colour_A.green + ((colour_B.green - colour_A.green) * ratio),
            colour_A.blue + ((colour_B.blue - colour_A.blue) * ratio),
        )

    @Animator.KeyFrame.add(framerate.FRAMES_PER_SECOND * 1)
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
                colours.COLOUR_BLACK,
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
                colours.COLOUR_BLUE, colours.COLOUR_ORANGE, ratio
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
