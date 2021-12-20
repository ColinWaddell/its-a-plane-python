from datetime import datetime

from animator import Animator
from constants import framerate, colours, fonts

from rgbmatrix import graphics

CLOCK_FONT = fonts.font_regular
CLOCK_POSITION = (1, 8)
CLOCK_COLOUR = colours.COLOUR_BLUE_DARK


class ClockScene:
    @Animator.KeyFrame.add(framerate.FRAMES_PER_SECOND * 1)
    def clock(self, count):
        if len(self._data):
            # Ensure redraw when there's new data
            self._last_time = None

        else:
            # If there's no data to display
            # then draw a clock
            now = datetime.now()
            current_time = now.strftime("%H:%M")

            # Only draw if time needs updated
            if self._last_time != current_time:
                # Undraw last time if different from current
                if not self._last_time is None:
                    _ = graphics.DrawText(
                        self.canvas,
                        CLOCK_FONT,
                        CLOCK_POSITION[0],
                        CLOCK_POSITION[1],
                        colours.COLOUR_BLACK,
                        self._last_time,
                    )
                self._last_time = current_time

                # Draw Time
                _ = graphics.DrawText(
                    self.canvas,
                    CLOCK_FONT,
                    CLOCK_POSITION[0],
                    CLOCK_POSITION[1],
                    CLOCK_COLOUR,
                    current_time,
                )
