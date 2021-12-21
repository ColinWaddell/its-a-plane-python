import os
from rgbmatrix import graphics

# Fonts
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
font_extrasmall = graphics.Font()
font_small = graphics.Font()
font_regular = graphics.Font()
font_large = graphics.Font()
font_large_bold = graphics.Font()
font_extrasmall.LoadFont(f"{DIR_PATH}/../fonts/4x6.bdf")
font_small.LoadFont(f"{DIR_PATH}/../fonts/5x8.bdf")
font_regular.LoadFont(f"{DIR_PATH}/../fonts/6x12.bdf")
font_large.LoadFont(f"{DIR_PATH}/../fonts/8x13.bdf")
font_large_bold.LoadFont(f"{DIR_PATH}/../fonts/8x13B.bdf")
