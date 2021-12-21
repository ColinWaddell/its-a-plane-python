from rgbmatrix import graphics

from animator import Animator
from setup import colours, fonts, screen

# Setup
PLANE_DETAILS_COLOUR = colours.COLOUR_PINK
PLANE_DISTANCE_FROM_TOP = 30
PLANE_TEXT_HEIGHT = 9
PLANE_FONT = fonts.font_regular


class PlaneDetailsScene:
    def __init__(self):
        # Element positions
        self.plane_position = screen.WIDTH
        self._data_all_looped = False

    @Animator.KeyFrame.add(1)
    def plane_details(self, count):

        # Guard against no data
        if len(self._data) == 0:
            return

        plane = f'{self._data[self._data_index]["plane"]}'

        # Draw background
        self.draw_square(
            0,
            PLANE_DISTANCE_FROM_TOP - PLANE_TEXT_HEIGHT,
            screen.WIDTH,
            screen.HEIGHT,
            colours.COLOUR_BLACK,
        )

        # Draw text
        text_length = graphics.DrawText(
            self.canvas,
            PLANE_FONT,
            self.plane_position,
            PLANE_DISTANCE_FROM_TOP,
            PLANE_DETAILS_COLOUR,
            plane,
        )

        # Handle scrolling
        self.plane_position -= 1
        if self.plane_position + text_length < 0:
            self.plane_position = screen.WIDTH
            if len(self._data) > 1:
                self._data_index = (self._data_index + 1) % len(self._data)
                self._data_all_looped = (not self._data_index) or self._data_all_looped
                self.reset_scene()

    @Animator.KeyFrame.add(0)
    def reset_scrolling(self):
        self.plane_position = screen.WIDTH
