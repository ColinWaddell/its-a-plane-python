from datetime import datetime

from animator import Animator
from constants import framerate, colours, fonts

DAY_COLOUR = colours.COLOUR_PINK_DARK


DAY_FONT = fonts.fonts_small
DAY_POSITION = (2, 23)


class DayScene:
    @Animator.KeyFrame.add(framerate.FRAMES_PER_SECOND * 1)
    def day(self, count):
        if len(self._data):
            # Ensure redraw when there's new data
            self._last_day = None

        else:
            # If there's no data to display
            # then draw the day
            now = datetime.now()
            current_day = now.strftime("%A")

            # Only draw if time needs updated
            if self._last_day != current_day:
                # Undraw last day if different from current
                if not self._last_day is None:
                    _ = graphics.DrawText(
                        self.canvas,
                        DAY_FONT,
                        DAY_POSITION[0],
                        DAY_POSITION[1],
                        colours.COLOUR_BLACK,
                        self._last_day,
                    )
                self._last_day = current_day

                # Draw day
                _ = graphics.DrawText(
                    self.canvas,
                    DAY_FONT,
                    DAY_POSITION[0],
                    DAY_POSITION[1],
                    DAY_COLOUR,
                    current_day,
                )
