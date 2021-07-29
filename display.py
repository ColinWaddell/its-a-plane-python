import time
import sys
import os

from animator import Animator

from rgbmatrix import graphics
from rgbmatrix import RGBMatrix, RGBMatrixOptions

DEFAULT_INDENT_STATIC_TEXT = 4


class Display(Animator):
    def __init__(self):
        super().__init__(0.1)

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
        self.data = {"error": "", "journey": "GLA▶EDI", "plane": "01269"}

    def draw_square(self, x0, y0, x1, y1, colour):
        for x in range(x0, x1):
            _ = graphics.DrawLine(self.canvas, x, y0, x, y1, colour)

    @Animator.KeyFrame.add(1)
    def journey(self, count):

        MAX_STATIC_TEXT_LEN = 8
        MAX_TEXT_WIDTH = 48

        # Draw background
        if len(self.data["journey"]) > MAX_STATIC_TEXT_LEN:
            self.draw_square(0, 0, 49, 14, graphics.Color(0, 0, 0))

        # Draw text
        text_length = graphics.DrawText(
            self.canvas,
            self.font_regular,
            self.journey_position,
            12,
            graphics.Color(255, 255, 0),
            self.data["journey"],
        )

        # If it should be scrolling, update
        if len(self.data["journey"]) > MAX_STATIC_TEXT_LEN:
            self.journey_position -= 1
            if self.journey_position + text_length < 0:
                self.journey_position = MAX_TEXT_WIDTH
        else:
            self.journey_position = DEFAULT_INDENT_STATIC_TEXT

    @Animator.KeyFrame.add(1)
    def plane(self, count):

        MAX_STATIC_TEXT_LEN = 8
        MAX_TEXT_WIDTH = 48

        # Draw background
        if len(self.data["plane"]) > MAX_STATIC_TEXT_LEN:
            self.draw_square(0, 18, 48, 32, graphics.Color(0, 0, 0))

        # Draw text
        text_length = graphics.DrawText(
            self.canvas,
            self.font_regular,
            self.plane_position,
            29,
            graphics.Color(255, 255, 0),
            self.data["plane"],
        )

        # If it should be scrolling, update
        if len(self.data["plane"]) > MAX_STATIC_TEXT_LEN:
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

    def run(self):
        try:
            # Start loop
            print("Press CTRL-C to stop")
            self.play()

        except KeyboardInterrupt:
            print("Exiting\n")
            sys.exit(0)
