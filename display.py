import time
import sys
import os
from typing import overload

from animator import Animator
from overhead import Overhead

from rgbmatrix import graphics
from rgbmatrix import RGBMatrix, RGBMatrixOptions

DEFAULT_INDENT_STATIC_TEXT = 4
FRAME_RATE = 0.1
FRAME_PERIOD = 1 / FRAME_RATE


class Display(Animator):
    def __init__(self):
        super().__init__(FRAME_RATE)

        # Setup Display
        options = RGBMatrixOptions()
        options.hardware_mapping = "adafruit-hat-pwm"
        options.rows = 32
        options.cols = 64
        options.chain_length = 1
        options.parallel = 1
        options.row_address_type = 0
        options.multiplexing = 0
        options.pwm_bits = 11
        options.brightness = 100
        options.pwm_lsb_nanoseconds = 130
        options.led_rgb_sequence = "RGB"
        options.pixel_mapper_config = ""
        options.panel_type = ""
        options.show_refresh_rate = 0
        options.gpio_slowdown = 1
        options.disable_hardware_pulsing = True
        options.drop_privileges = True
        self.matrix = RGBMatrix(options=options)

        # Setup canvas
        self.canvas = self.matrix.CreateFrameCanvas()
        self.canvas.Clear()

        # Setup fonts
        self.font_regular = graphics.Font()
        self.font_regular.LoadFont("fonts/6x12.bdf")

        # Element positions
        self.journey_position = DEFAULT_INDENT_STATIC_TEXT
        self.plane_position = DEFAULT_INDENT_STATIC_TEXT

        # Data to render
        self._data = [
            {
                "error": "",
                "plane": "",
                "origin": "",
                "destination": "",
                "vertical_speed": 0,
                "altitude": 0,
            }
        ]

        # Start Looking for planes
        self.overhead = Overhead()
        self.overhead.grab_data()

    def draw_square(self, x0, y0, x1, y1, colour):
        for x in range(x0, x1):
            _ = graphics.DrawLine(self.canvas, x, y0, x, y1, colour)

    @Animator.KeyFrame.add(1)
    def journey(self, count):

        MAX_STATIC_TEXT_LEN = 8
        MAX_TEXT_WIDTH = 48

        journey = f"{self._data[0]['origin']}▶{self._data[0]['destination']}"

        # Draw background
        if len(journey) > MAX_STATIC_TEXT_LEN:
            self.draw_square(0, 0, 49, 14, graphics.Color(0, 0, 0))

        # Draw text
        text_length = graphics.DrawText(
            self.canvas,
            self.font_regular,
            self.journey_position,
            12,
            graphics.Color(255, 255, 0),
            journey,
        )

        # If it should be scrolling, update
        if len(journey) > MAX_STATIC_TEXT_LEN:
            self.journey_position -= 1
            if self.journey_position + text_length < 0:
                self.journey_position = MAX_TEXT_WIDTH
        else:
            self.journey_position = DEFAULT_INDENT_STATIC_TEXT

    @Animator.KeyFrame.add(1)
    def plane(self, count):

        MAX_STATIC_TEXT_LEN = 8
        MAX_TEXT_WIDTH = 48

        plane = self._data[0]["plane"]

        # Draw background
        if len(plane) > MAX_STATIC_TEXT_LEN:
            self.draw_square(0, 18, 48, 32, graphics.Color(0, 0, 0))

        # Draw text
        text_length = graphics.DrawText(
            self.canvas,
            self.font_regular,
            self.plane_position,
            29,
            graphics.Color(255, 255, 0),
            plane,
        )

        # If it should be scrolling, update
        if len(plane) > MAX_STATIC_TEXT_LEN:
            self.plane_position -= 1
            if self.plane_position + text_length < 0:
                self.plane_position = MAX_TEXT_WIDTH
        else:
            self.plane_position = DEFAULT_INDENT_STATIC_TEXT

    @Animator.KeyFrame.add(1)
    def permanant_elements(self, count):
        graphics.DrawLine(self.canvas, 0, 16, 49, 16, graphics.Color(153, 204, 255))
        graphics.DrawLine(self.canvas, 49, 0, 49, 32, graphics.Color(153, 204, 255))

    @Animator.KeyFrame.add(1)
    def sync(self, count):
        _ = self.matrix.SwapOnVSync(self.canvas)

    @Animator.KeyFrame.add(FRAME_PERIOD * 5)
    def load_data(self, count):
        if self.overhead.processing:
            # show processing animation
            print("loading data")
            pass

        if self.overhead.new_data:
            print("new data")
            self._data = self.overhead.data

    @Animator.KeyFrame.add(FRAME_PERIOD * 30)
    def grab_data(self, count):
        self.overhead.grab_data()

    def run(self):
        try:
            # Start loop
            print("Press CTRL-C to stop")
            self.play()

        except KeyboardInterrupt:
            print("Exiting\n")
            sys.exit(0)
