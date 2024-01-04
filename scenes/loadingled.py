from utilities.animator import Animator
from setup import frames

# Attempt to load config data
try:
    from config import LOADING_LED_GPIO_PIN

except (ModuleNotFoundError, NameError, ImportError):
    # If there's no config data
    LOADING_LED_GPIO_PIN = 25

BLINKER_STEPS = 4
GPIO = None

class LoadingLEDScene(object):
    def __init__(self):
        self.gpio_setup_complete = False
        self.gpio_setup()

        super().__init__()
    
    def gpio_setup(self):
        if not self.gpio_setup_complete:
            try:
                import RPi.GPIO as GPIO
                # Setup GPIO for blinking
                GPIO.setwarnings(False)
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(LOADING_LED_GPIO_PIN, GPIO.OUT)
                GPIO.output(LOADING_LED_GPIO_PIN, GPIO.HIGH)
                self.gpio_setup_complete = True

            except:
                self.gpio_setup_complete = False

    @Animator.KeyFrame.add(4)
    def loading_led(self, count):
        if self.gpio_setup_complete:
            reset_count = True
            if self.overhead.processing:
                GPIO.output(
                    LOADING_LED_GPIO_PIN,
                    GPIO.HIGH if count % 2 else GPIO.LOW
                )

            else:
                # Not processing, leave LED on
                GPIO.output(LOADING_LED_GPIO_PIN, GPIO.HIGH)
        else:
            self.gpio_setup()
