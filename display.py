from datetime import datetime
import time
import sys
import os

from animator import Animator
from overhead import Overhead

from rgbmatrix import graphics
from rgbmatrix import RGBMatrix, RGBMatrixOptions


# Loop setup
FRAME_RATE = 0.1
FRAME_PERIOD = 1 / FRAME_RATE

# Fonts
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
font_extrasmall = graphics.Font()
font_small = graphics.Font()
font_regular = graphics.Font()
font_large = graphics.Font()
font_large_bold = graphics.Font()
font_extrasmall.LoadFont(f"{DIR_PATH}/fonts/4x6.bdf")
font_small.LoadFont(f"{DIR_PATH}/fonts/5x8.bdf")
font_regular.LoadFont(f"{DIR_PATH}/fonts/6x12.bdf")
font_large.LoadFont(f"{DIR_PATH}/fonts/8x13.bdf")
font_large_bold.LoadFont(f"{DIR_PATH}/fonts/8x13B.bdf")

# Colour helpers
COLOUR_BLACK = graphics.Color(0, 0, 0)
COLOUR_WHITE = graphics.Color(255, 255, 255)
COLOUR_GREY = graphics.Color(192, 192, 192)
COLOUR_YELLOW = graphics.Color(255, 255, 0)
COLOUR_BLUE = graphics.Color(55, 14, 237)
COLOUR_BLUE_LIGHT = graphics.Color(110, 182, 255)
COLOUR_BLUE_DARK = graphics.Color(29, 0, 156)
COLOUR_PINK = graphics.Color(200, 0, 200)
COLOUR_PINK_DARK = graphics.Color(112, 0, 145)
COLOUR_PINK_DARKER = graphics.Color(96, 1, 125)
COLOUR_GREEN = graphics.Color(0, 200, 0)
COLOUR_ORANGE = graphics.Color(227, 110, 0)
COLOUR_RED = graphics.Color(255, 255, 255)
COLOUR_RED_LIGHT = graphics.Color(255, 195, 195)

# Element colours
FLIGHT_NUMBER_ALPHA_COLOUR = COLOUR_BLUE
FLIGHT_NUMBER_NUMERIC_COLOUR = COLOUR_BLUE_LIGHT
DIVIDING_BAR_COLOUR = COLOUR_GREEN
DATA_INDEX_COLOUR = COLOUR_GREY
JOURNEY_COLOUR = COLOUR_YELLOW
ARROW_COLOUR = COLOUR_ORANGE
PLANE_DETAILS_COLOUR = COLOUR_PINK
BLINKER_COLOUR = COLOUR_WHITE
CLOCK_COLOUR = COLOUR_BLUE_DARK
DATE_COLOUR = COLOUR_PINK_DARKER
DAY_COLOUR = COLOUR_PINK_DARK

# Element Positions
ARROW_POINT_POSITION = (34, 7)
ARROW_WIDTH = 4
ARROW_HEIGHT = 8

BAR_STARTING_POSITION = (0, 18)
BAR_PADDING = 2

BLINKER_POSITION = (63, 0)
BLINKER_STEPS = 10

DATA_INDEX_POSITION = (52, 21)
DATA_INDEX_TEXT_HEIGHT = 6
DATA_INDEX_FONT = font_extrasmall

CLOCK_FONT = font_regular
CLOCK_POSITION = (1, 8)

DATE_FONT = font_small
DATE_POSITION = (1, 31)

DAY_FONT = font_small
DAY_POSITION = (2, 23)

FLIGHT_NO_POSITION = (1, 21)
FLIGHT_NO_TEXT_HEIGHT = 8  # based on font size
FLIGHT_NO_FONT = font_small

JOURNEY_POSITION = (0, 0)
JOURNEY_HEIGHT = 12
JOURNEY_WIDTH = 64
JOURNEY_SPACING = 16
JOURNEY_FONT = font_large
JOURNEY_FONT_SELECTED = font_large_bold

PLANE_DISTANCE_FROM_TOP = 30
PLANE_TEXT_HEIGHT = 9
PLANE_FONT = font_regular

# Constants
MAX_WIDTH = 64
MAX_HEIGHT = 32
MAX_STATIC_TEXT_LEN = 12


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
        options.show_refresh_rate = 0
        options.gpio_slowdown = 1
        options.disable_hardware_pulsing = True
        options.drop_privileges = True
        self.matrix = RGBMatrix(options=options)

        # Setup canvas
        self.canvas = self.matrix.CreateFrameCanvas()
        self.canvas.Clear()

        # Element positions
        self.plane_position = MAX_WIDTH

        # Data to render
        self._data_index = 0
        self._data_all_looped = False
        self._data = []

        # Clock and date elements
        self._last_time = None
        self._last_day = None
        self._last_date = None

        # Start Looking for planes
        self.overhead = Overhead()
        self.overhead.grab_data()

    def draw_square(self, x0, y0, x1, y1, colour):
        for x in range(x0, x1):
            _ = graphics.DrawLine(self.canvas, x, y0, x, y1, colour)

    @Animator.KeyFrame.add(0)
    def flight_details(self):

        # Guard against no data
        if len(self._data) == 0:
            return

        # Clear the area
        self.draw_square(
            0,
            BAR_STARTING_POSITION[1] - (FLIGHT_NO_TEXT_HEIGHT // 2),
            MAX_WIDTH - 1,
            BAR_STARTING_POSITION[1] + (FLIGHT_NO_TEXT_HEIGHT // 2),
            COLOUR_BLACK,
        )

        # Draw flight number if available
        flight_no_text_length = 0
        if (
            self._data[self._data_index]["callsign"]
            and self._data[self._data_index]["callsign"] != "N/A"
        ):
            flight_no = f'{self._data[self._data_index]["callsign"]}'

            for ch in flight_no:
                ch_length = graphics.DrawText(
                    self.canvas,
                    FLIGHT_NO_FONT,
                    FLIGHT_NO_POSITION[0] + flight_no_text_length,
                    FLIGHT_NO_POSITION[1],
                    FLIGHT_NUMBER_NUMERIC_COLOUR
                    if ch.isnumeric()
                    else FLIGHT_NUMBER_ALPHA_COLOUR,
                    ch,
                )
                flight_no_text_length += ch_length

        # Draw bar
        if len(self._data) > 1:
            # Clear are where N of M might have been
            self.draw_square(
                DATA_INDEX_POSITION[0] - BAR_PADDING,
                BAR_STARTING_POSITION[1] - (FLIGHT_NO_TEXT_HEIGHT // 2),
                MAX_WIDTH,
                BAR_STARTING_POSITION[1] + (FLIGHT_NO_TEXT_HEIGHT // 2),
                COLOUR_BLACK,
            )

            # Dividing bar
            graphics.DrawLine(
                self.canvas,
                flight_no_text_length + BAR_PADDING,
                BAR_STARTING_POSITION[1],
                DATA_INDEX_POSITION[0] - BAR_PADDING - 1,
                BAR_STARTING_POSITION[1],
                DIVIDING_BAR_COLOUR,
            )

            # Draw text
            text_length = graphics.DrawText(
                self.canvas,
                font_extrasmall,
                DATA_INDEX_POSITION[0],
                DATA_INDEX_POSITION[1],
                DATA_INDEX_COLOUR,
                f"{self._data_index + 1}/{len(self._data)}",
            )
        else:
            # Dividing bar
            graphics.DrawLine(
                self.canvas,
                flight_no_text_length + BAR_PADDING if flight_no_text_length else 0,
                BAR_STARTING_POSITION[1],
                MAX_WIDTH,
                BAR_STARTING_POSITION[1],
                DIVIDING_BAR_COLOUR,
            )

    @Animator.KeyFrame.add(0)
    def journey(self):

        # Guard against no data
        if len(self._data) == 0:
            return

        if not (
            self._data[self._data_index]["origin"]
            and self._data[self._data_index]["destination"]
        ):
            return

        origin = self._data[self._data_index]["origin"]
        destination = self._data[self._data_index]["destination"]

        # Draw background
        self.draw_square(
            JOURNEY_POSITION[0],
            JOURNEY_POSITION[1],
            JOURNEY_POSITION[0] + JOURNEY_WIDTH - 1,
            JOURNEY_POSITION[1] + JOURNEY_HEIGHT - 1,
            COLOUR_BLACK,
        )

        # Draw origin
        text_length = graphics.DrawText(
            self.canvas,
            JOURNEY_FONT_SELECTED if origin == "GLA" else JOURNEY_FONT,
            1,
            JOURNEY_HEIGHT,
            JOURNEY_COLOUR,
            origin,
        )

        # Draw destination
        _ = graphics.DrawText(
            self.canvas,
            JOURNEY_FONT_SELECTED if destination == "GLA" else JOURNEY_FONT,
            text_length + JOURNEY_SPACING,
            JOURNEY_HEIGHT,
            JOURNEY_COLOUR,
            destination,
        )

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
            MAX_WIDTH,
            MAX_HEIGHT,
            COLOUR_BLACK,
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
            self.plane_position = MAX_WIDTH
            if len(self._data) > 1:
                self._data_index = (self._data_index + 1) % len(self._data)
                self._data_all_looped = (not self._data_index) or self._data_all_looped
                self.reset_scene()

    @Animator.KeyFrame.add(0)
    def journey_arrow(self):
        # Guard against no data
        if len(self._data) == 0:
            return

        if not (
            self._data[self._data_index]["origin"]
            and self._data[self._data_index]["destination"]
        ):
            return

        # Black area before arrow
        self.draw_square(
            ARROW_POINT_POSITION[0] - ARROW_WIDTH,
            ARROW_POINT_POSITION[1] - (ARROW_HEIGHT // 2),
            ARROW_POINT_POSITION[0],
            ARROW_POINT_POSITION[1] + (ARROW_HEIGHT // 2),
            COLOUR_BLACK,
        )

        # Starting positions for filled in arrow
        x = ARROW_POINT_POSITION[0] - ARROW_WIDTH
        y1 = ARROW_POINT_POSITION[1] - (ARROW_HEIGHT // 2)
        y2 = ARROW_POINT_POSITION[1] + (ARROW_HEIGHT // 2)

        # Tip of arrow
        self.canvas.SetPixel(
            ARROW_POINT_POSITION[0],
            ARROW_POINT_POSITION[1],
            ARROW_COLOUR.red,
            ARROW_COLOUR.green,
            ARROW_COLOUR.blue,
        )

        # Draw using columns
        for col in range(0, ARROW_WIDTH):
            graphics.DrawLine(
                self.canvas,
                x,
                y1,
                x,
                y2,
                ARROW_COLOUR,
            )

            # Calculate next column's data
            x += 1
            y1 += 1
            y2 -= 1

    @Animator.KeyFrame.add(2)
    def loading_pulse(self, count):
        reset_count = True
        if self.overhead.processing:
            # Calculate the brightness scaler and
            # ensure it's within a sensible range
            brightness = (1 - (count / BLINKER_STEPS)) / 2
            brightness = 0 if (brightness < 0 or brightness > 1) else brightness

            self.canvas.SetPixel(
                BLINKER_POSITION[0],
                BLINKER_POSITION[1],
                brightness * BLINKER_COLOUR.red,
                brightness * BLINKER_COLOUR.green,
                brightness * BLINKER_COLOUR.blue,
            )

            # Only count 0 -> (BLINKER_STEPS - 1)
            reset_count = count == (BLINKER_STEPS - 1)
        else:
            # Not processing, blank the square
            self.canvas.SetPixel(BLINKER_POSITION[0], BLINKER_POSITION[1], 0, 0, 0)
        return reset_count

    @Animator.KeyFrame.add(FRAME_PERIOD * 5)
    def check_for_loaded_data(self, count):
        if self.overhead.new_data:
            self._data_index = 0
            self._data_all_looped = False
            self._data = self.overhead.data
            self.reset_scene()

    @Animator.KeyFrame.add(FRAME_PERIOD * 1)
    def clock(self, count):
        # If there's no data to display
        # then draw a clock
        if len(self._data) == 0:
            now = datetime.now()
            current_time = now.strftime("%H %M")

            # Only draw if time needs updated
            if self._last_time != current_time:
                # Undraw last time if different from current
                if not self._last_time is None:
                    _ = graphics.DrawText(
                        self.canvas,
                        CLOCK_FONT,
                        CLOCK_POSITION[0],
                        CLOCK_POSITION[1],
                        COLOUR_BLACK,
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

                # Draw Seperator
                _ = graphics.DrawLine(
                    self.canvas,
                    CLOCK_POSITION[0] + 14,
                    CLOCK_POSITION[1] - 6,
                    CLOCK_POSITION[0] + 14,
                    CLOCK_POSITION[1] - 5,
                    CLOCK_COLOUR,
                )

                _ = graphics.DrawLine(
                    self.canvas,
                    CLOCK_POSITION[0] + 14,
                    CLOCK_POSITION[1] - 3,
                    CLOCK_POSITION[0] + 14,
                    CLOCK_POSITION[1] - 2,
                    CLOCK_COLOUR,
                )

    @Animator.KeyFrame.add(FRAME_PERIOD * 1)
    def date(self, count):
        # If there's no data to display
        # then draw the date
        if len(self._data) == 0:
            now = datetime.now()
            current_date = now.strftime("%-d-%-m-%Y")

            # Only draw if time needs updated
            if self._last_date != current_date:
                # Undraw last time if different from current
                if not self._last_date is None:
                    _ = graphics.DrawText(
                        self.canvas,
                        DATE_FONT,
                        DATE_POSITION[0],
                        DATE_POSITION[1],
                        COLOUR_BLACK,
                        self._last_date,
                    )
                self._last_date = current_date

                # Draw Time
                _ = graphics.DrawText(
                    self.canvas,
                    DATE_FONT,
                    DATE_POSITION[0],
                    DATE_POSITION[1],
                    DATE_COLOUR,
                    current_date,
                )

    @Animator.KeyFrame.add(FRAME_PERIOD * 1)
    def day(self, count):
        # If there's no data to display
        # then draw the date
        if len(self._data) == 0:
            now = datetime.now()
            current_day = now.strftime("%A")

            # Only draw if time needs updated
            if self._last_day != current_day:
                # Undraw last time if different from current
                if not self._last_day is None:
                    _ = graphics.DrawText(
                        self.canvas,
                        DAY_FONT,
                        DAY_POSITION[0],
                        DAY_POSITION[1],
                        COLOUR_BLACK,
                        self._last_day,
                    )
                self._last_day = current_day

                # Draw Time
                _ = graphics.DrawText(
                    self.canvas,
                    DAY_FONT,
                    DAY_POSITION[0],
                    DAY_POSITION[1],
                    DAY_COLOUR,
                    current_day,
                )

    @Animator.KeyFrame.add(1)
    def sync(self, count):
        # Redraw screen every frame
        _ = self.matrix.SwapOnVSync(self.canvas)

    @Animator.KeyFrame.add(FRAME_PERIOD * 20)
    def grab_new_data(self, count):
        # Only grab data if we're not already searching
        # for planes, or if there's new data available
        # which hasn't been displayed.
        #
        # We also need wait until all previously grabbed
        # data has been looped through the display.
        #
        # Last, if our internal store of the data
        # is empty, try and grab data
        if not (self.overhead.processing and self.overhead.new_data) and (
            self._data_all_looped or len(self._data) <= 1
        ):
            self.overhead.grab_data()

    def run(self):
        try:
            # Start loop
            print("Press CTRL-C to stop")
            self.play()

        except KeyboardInterrupt:
            print("Exiting\n")
            sys.exit(0)
