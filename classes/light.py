from .car_movement import CarMovement
from .light_state import LightState

class Light:

    GPIO = None

    left_lights     = None
    right_lights    = None
    other_lights    = None

    status = {
        'left': 0,
        'right': 0,
        'other': 0
    }

    blinker_index   = 0
    blink_ticks     = 200
    blinker_on      = True

    # Set lights every tick based on direction
    def update(self, direction):

        state = LightState.ON

        if (direction == CarMovement.LEFT or direction == CarMovement.HARD_LEFT):
            state = LightState.BLINK_LEFT

        elif (direction == CarMovement.RIGHT or direction == CarMovement.HARD_RIGHT):
            state = LightState.BLINK_RIGHT

        self.set_lights(state)
        return

    def set_lights(self, state):
        if (state == LightState.ON):
            self.set_left_lights(self.GPIO.HIGH)
            self.set_right_lights(self.GPIO.HIGH)
            self.set_other_lights(self.GPIO.HIGH)

        elif (state == LightState.BLINK_LEFT):
            self.set_left_lights(self.GPIO.HIGH if self.blinker_on else self.GPIO.LOW)
            self.set_right_lights(self.GPIO.HIGH)
            self.set_other_lights(self.GPIO.HIGH)

        elif (state == LightState.BLINK_RIGHT):
            self.set_left_lights(self.GPIO.HIGH)
            self.set_right_lights(self.GPIO.HIGH if self.blinker_on else self.GPIO.LOW)
            self.set_other_lights(self.GPIO.HIGH)

        elif (state == LightState.OFF):
            self.set_left_lights(self.GPIO.LOW)
            self.set_right_lights(self.GPIO.LOW)
            self.set_other_lights(self.GPIO.LOW)

        elif (state == LightState.DISCO):
            self.set_left_lights(self.GPIO.HIGH if not self.blinker_on else self.GPIO.LOW)
            self.set_right_lights(self.GPIO.HIGH if self.blinker_on else self.GPIO.LOW)
            self.set_other_lights(self.GPIO.HIGH)

        self.blinker_index += 1

        if (self.blinker_index == 10):
            self.blinker_on = not self.blinker_on

        self.blinker_index = self.blinker_index % self.blink_ticks

        return

    def set_left_lights(self, value):
        if (self.left_lights is not None and self.status['left'] != value):
            self.GPIO.output(self.left_lights, value)
            self.status['left'] = value


    def set_right_lights(self, value):
        if (self.right_lights is not None and self.status['right'] != value):
            self.GPIO.output(self.right_lights, value)
            self.status['right'] = value

    def set_other_lights(self, value):
        if (self.other_lights is not None and self.status['other'] != value):
            self.GPIO.output(self.other_lights, value)
            self.status['other'] = value


    def set_pins(self):
        # Setup left lights
        if (self.left_lights is not None):
            self.GPIO.setup(self.left_lights, self.GPIO.OUT)
            self.GPIO.output(self.left_lights, self.GPIO.LOW)

        # Setup right lights
        if (self.right_lights is not None):
            self.GPIO.setup(self.right_lights, self.GPIO.OUT)
            self.GPIO.output(self.right_lights, self.GPIO.LOW)

        # Setup other lights
        if (self.other_lights is not None):
            self.GPIO.setup(self.other_lights, self.GPIO.OUT)
            self.GPIO.output(self.other_lights, self.GPIO.LOW)


    def __init__(self, GPIO, lLights, rLights, oLights):
        self.GPIO = GPIO
        self.left_lights    = lLights
        self.right_lights   = rLights
        self.other_lights   = oLights
        self.set_pins()


