from .car_state import CarState
from .car_movement import CarMovement
from .crossroad_rotation import CrossroadRotation
from .light_state import LightState

import time

class Sensor:
    car = None
    GPIO = None

    last_direction  = CarMovement.FORWARD
    last_turn       = None

    state           = CarState.STARTING

    pin_left_sensor     = None
    pin_middle_sensor   = None
    pin_right_sensor    = None

    chosen_rotation     = CrossroadRotation.NONE

    crossed_threeway    = False

    threeway_count      = 0
    threeway_threshold  = 300
    threeway_middle     = 575

    same_direction_count        = 0
    same_direction_threshold    = 500

    search_steps        = 500

    def get_direction(self):
        middle  = self.GPIO.input(self.pin_middle_sensor) == 0
        left    = self.GPIO.input(self.pin_left_sensor) == 0
        right   = self.GPIO.input(self.pin_right_sensor) == 0
        all     = middle and left and right
        none    = (not middle and not left and not right)

        direction = self.last_direction


        # Check if have reached the threshold to cherck for a crossroad / end
        if (self.threeway_count > self.threeway_threshold):

            if (self.check_for_crossing()):
                # Rotate the crossing
                self.rotate_crossing(self.chosen_rotation)

            else:
                # Not a crossing and we dont have a hard corner, so our last option is end it
                if (self.same_direction_count < self.same_direction_threshold):
                    self.car.end()
                    self.state = CarState.DONE

            self.threeway_count = 0
            self.crossed_threeway = False

            return


        # Ride forward when crossed a threeway for checking
        if (self.crossed_threeway == True):
            self.threeway_count += 1
            return CarMovement.FORWARD

        # Read out the sensors and give back the direction enumeration
        if (all):
            direction = self.last_direction
            self.crossed_threeway = True

        elif (none and direction == CarMovement.LEFT):
            direction = CarMovement.HARD_LEFT

        elif (none and direction == CarMovement.RIGHT):
            direction = CarMovement.HARD_RIGHT

        elif (middle and right):
            direction = CarMovement.HARD_RIGHT

        elif (middle and left):
            direction = CarMovement.HARD_LEFT

        elif (middle):
            direction = CarMovement.FORWARD

        elif (left):
            direction = CarMovement.LEFT

        elif (right):
            direction = CarMovement.RIGHT

        self.set_last_direction(direction)
        self.state = CarState.MOVING

        return direction

    # Hard rotate for the crossing
    def rotate_crossing(self, direction):

        forward_steps = 200
        sideways_steps = 1700

        # Play crossroad audio
        self.car.audio.play_crossroad_intro()

        # Ride to the middle of the crossroad
        for i in range(0, self.threeway_middle):
            self.car.wheel_controller.move_forward()
            time.sleep(0.001)

        # Choose direction
        if direction == CrossroadRotation.FORWARD or direction == CrossroadRotation.NONE:
            print("Crossroad: Forward")
            for i in range(0, forward_steps):

                # Play audio of the direction
                if (i == forward_steps - 1): self.car.audio.play_crossroad_outro(direction)

                self.car.wheel_controller.move_forward()
                # Set lights
                self.car.lights.set_lights(LightState.ON)
                time.sleep(0.001)

        elif direction == CrossroadRotation.LEFT:
            print("Crossroad: Left")
            for i in range(0, sideways_steps):

                # Play audio of the direction
                if (i == forward_steps - 1): self.car.audio.play_crossroad_outro(direction)

                self.car.wheel_controller.move_hard_left()
                # Set lights
                self.car.lights.set_lights(LightState.BLINK_LEFT)
                time.sleep(0.001)


        elif direction == CrossroadRotation.RIGHT:
            print("Crossroad: Right")
            for i in range(0, sideways_steps):

                # Play audio of the direction
                if (i == forward_steps - 1): self.car.audio.play_crossroad_outro(direction)

                self.car.wheel_controller.move_hard_right()
                # Set lights
                self.car.lights.set_lights(LightState.BLINK_RIGHT)
                time.sleep(0.001)

        return


    def check_for_crossing(self):
        # Search of the opposite of the last chosen direction
        rotate_left = self.last_turn == CarMovement.RIGHT
        used_steps  = 0
        found       = False

        # Look at the opsite side of the last selected direction
        for step in range(0, self.search_steps):

            # Move car
            self.car.wheel_controller.wheel_left.move(True if rotate_left else False)
            self.car.wheel_controller.wheel_right.move(False if rotate_left else True)
            self.car.lights.set_lights(LightState.BLINK_LEFT if rotate_left else LightState.BLINK_RIGHT)

            used_steps += 1

            if (self.GPIO.input(self.pin_middle_sensor) == 0):
                found = True
                break

            time.sleep(0.001)

        # If not found, check the other side to be sure
        if (found == False):
            rotate_left = not rotate_left

            for step in range(0, self.search_steps * 2):
                # Move car
                self.car.wheel_controller.wheel_left.move(True if rotate_left else False)
                self.car.wheel_controller.wheel_right.move(False if rotate_left else True)
                self.car.lights.set_lights(LightState.BLINK_LEFT if rotate_left else LightState.BLINK_RIGHT)

                if (self.GPIO.input(self.pin_middle_sensor) == 0):
                    found = True
                    break

                time.sleep(0.001)


        print(used_steps)

        # Move car back
        for step in range(0, used_steps):
            # Rotate wheels
            self.car.wheel_controller.wheel_left.move(False if rotate_left else True)
            self.car.wheel_controller.wheel_right.move(True if rotate_left else False)

            self.car.lights.set_lights(LightState.BLINK_RIGHT if rotate_left else LightState.BLINK_LEFT)

            time.sleep(0.001)

        return found

    def set_last_direction(self, direction):
        if (direction == CarMovement.HARD_LEFT or direction == CarMovement.LEFT):
            direction = CarMovement.LEFT
            self.last_turn = direction

        if (direction == CarMovement.HARD_RIGHT or direction == CarMovement.RIGHT):
            direction = CarMovement.RIGHT
            self.last_turn = direction

        if (direction != self.last_direction):
            self.same_direction_count = 0
        else:
            # Don't count forward movement
            # otherwise it would see the straight part at the end point as a corner
            if (direction != CarMovement.FORWARD):
                self.same_direction_count += 1

        self.last_direction = direction

    def set_pins(self):
        # Setup left sensor
        self.GPIO.setup(self.pin_left_sensor, self.GPIO.IN)

        # Setup middle sensor
        self.GPIO.setup(self.pin_middle_sensor, self.GPIO.IN)

        # Setup right sensor
        self.GPIO.setup(self.pin_right_sensor, self.GPIO.IN)

        return


    def __init__(self, GPIO, car, lSensor , mSensor, rSensor):
        self.GPIO = GPIO
        self.car = car
        self.pin_left_sensor    = lSensor
        self.pin_middle_sensor  = mSensor
        self.pin_right_sensor   = rSensor

        self.set_pins()
        return