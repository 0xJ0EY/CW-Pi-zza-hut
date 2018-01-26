from .wheel import Wheel

from .car_movement import CarMovement

class WheelController:

    wheel_left  = None
    wheel_right = None

    # Speed
    previous_direction = None
    current_speed = 0.001
    start_speed = 0.001
    max_speed = 0.00075

    decrement_speed = 0.0000015

    # Move based on direction
    def move(self, direction):
        if direction == CarMovement.FORWARD:
            self.move_forward()

        elif direction == CarMovement.BACKWARD:
            self.move_backward()

        elif direction == CarMovement.LEFT:
            self.move_left()

        elif direction == CarMovement.RIGHT:
            self.move_right()

        elif direction == CarMovement.HARD_LEFT:
            self.move_hard_left()

        elif direction == CarMovement.HARD_RIGHT:
            self.move_hard_right()
        return

    def move_forward(self):
        self.wheel_left.move()
        self.wheel_right.move()
        return

    def move_backward(self):
        self.wheel_left.move(True)
        self.wheel_right.move(True)
        return

    def move_left(self):
        self.wheel_right.move()
        return

    def move_hard_left(self):
        self.wheel_left.move(True)
        self.wheel_right.move()
        return

    def move_right(self):
        self.wheel_left.move()
        return

    def move_hard_right(self):
        self.wheel_left.move()
        self.wheel_right.move(True)
        return

    def regulate_speed(self, direction):
        # Direction has changed, so return to slow speed
        if (direction != self.previous_direction):
            speed_gained = self.start_speed - self.current_speed
            self.current_speed = self.start_speed + (speed_gained / 2)

        # Ramp up the POWER-R-R
        if (self.current_speed > self.max_speed):
            self.current_speed -= self.decrement_speed

        self.previous_direction = direction
        return

    def __init__(self, GPIO, pinsLeftWheel, pinsRightWheel):
        self.wheel_left     = Wheel(GPIO, pinsLeftWheel, False)
        self.wheel_right    = Wheel(GPIO, pinsRightWheel, True)
        return

