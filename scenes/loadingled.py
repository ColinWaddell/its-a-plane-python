from utilities.animator import Animator
from setup import frames
from time import sleep


# Attempt to load GPIO library. On-boot the GPIO
# module isn't always available, so we retry until
# it loads successfully
gpio_retries = 10
while gpio_retries:
    try:
        import RPi.GPIO as GPIO
        break
    except:
        gpio_retries = gpio_retries - 1
        GPIO = None
        sleep(1)

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
        if GPIO is not None:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(LOADING_LED_GPIO_PIN, GPIO.OUT)
            GPIO.output(LOADING_LED_GPIO_PIN, GPIO.HIGH)

        super().__init__()

    @Animator.KeyFrame.add(4)
    def loading_led(self, count):
        reset_count = True
        if self.overhead.processing:
            if GPIO is not None:
                GPIO.output(
                    LOADING_LED_GPIO_PIN,
                    GPIO.HIGH if count % 2 else GPIO.LOW
                )

        else:
            # Not processing, leave LED on
            if GPIO is not None:
                GPIO.output(LOADING_LED_GPIO_PIN, GPIO.HIGH)