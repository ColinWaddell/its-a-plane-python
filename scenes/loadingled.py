from utilities.animator import Animator
from setup import frames
import RPi.GPIO as GPIO

# Attempt to load config data
try:
    from config import LOADING_LED_GPIO_PIN

except (ModuleNotFoundError, NameError, ImportError):
    # If there's no config data
    LOADING_LED_GPIO_PIN = 25

BLINKER_STEPS = 4

class LoadingLEDScene(object):
    def __init__(self):
        # Setup GPIO for blinking
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LOADING_LED_GPIO_PIN, GPIO.OUT)
        GPIO.output(LOADING_LED_GPIO_PIN, GPIO.HIGH)

        super().__init__()

    @Animator.KeyFrame.add(4)
    def loading_led(self, count):
        reset_count = True
        if self.overhead.processing:
            GPIO.output(
                LOADING_LED_GPIO_PIN,
                GPIO.HIGH if count % 2 else GPIO.LOW
            )

        else:
            # Not processing, leave LED on
            GPIO.output(LOADING_LED_GPIO_PIN, GPIO.HIGH)
