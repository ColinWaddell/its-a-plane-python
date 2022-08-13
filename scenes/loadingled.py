from utilities.animator import Animator
import RPi.GPIO as GPIO

# Attempt to load config data
try:
    from config import LOADING_LED_GPIO_PIN

except (ModuleNotFoundError, NameError, ImportError):
    # If there's no config data
    LOADING_LED_GPIO_PIN = 25

BLINKER_STEPS = 10

class LoadingLEDScene(object):
    def __init__(self):
        # Setup GPIO for blinking
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LOADING_LED_GPIO_PIN, GPIO.OUT)

        # Setup PWM
        self._pwm  = GPIO.PWM(LOADING_LED_GPIO_PIN, 50)
        self._pwm.start(100)

        super().__init__()

    @Animator.KeyFrame.add(2)
    def loading_led(self, count):
        reset_count = True
        if self.overhead.processing:
            # Calculate the brightness scaler and
            # ensure it's within a sensible range
            brightness = (1 - (count / BLINKER_STEPS)) / 2
            brightness = 0 if (brightness < 0 or brightness > 1) else brightness

            # Set LED to brightness
            self._pwm.start(100 * brightness)

            # Only count 0 -> (BLINKER_STEPS - 1)
            reset_count = count == (BLINKER_STEPS - 1)
        else:
            # Not processing, leave LED on
            self._pwm.start(100)

        return reset_count
