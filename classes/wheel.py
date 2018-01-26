class Wheel:
    GPIO    = None
    pins    = []
    steps   = []
    index   = 0

    def move(self, backwards = False):
        for i in range(0, len(self.pins)):
            pin = self.pins[i]

            if (self.steps[self.index][i] == 1):
                self.GPIO.output(pin, True)
            else:
                self.GPIO.output(pin, False)

        # If the car is reversing just count down the index
        # I guess it works ¯\_(ツ)_/¯
        self.index += 1 if backwards == False else -1
        self.index = self.index % 7
        return

    # Setup the pins
    def set_pins(self):
        for pin in self.pins:
            self.GPIO.setup(pin, self.GPIO.OUT)
            self.GPIO.output(pin, False)

        return

    # Setup the steps required to move the stepper motor
    def set_steps(self, reverse):
        self.steps = list(range(0, 8))
        self.steps[0] = [1, 0, 0, 0]
        self.steps[1] = [1, 1, 0, 0]
        self.steps[2] = [0, 1, 0, 0]
        self.steps[3] = [0, 1, 1, 0]
        self.steps[4] = [0, 0, 1, 0]
        self.steps[5] = [0, 0, 1, 1]
        self.steps[6] = [0, 0, 0, 1]
        self.steps[7] = [1, 0, 0, 1]

        # Reverse step array if the wheel has to be reversed
        if reverse: self.steps = self.steps[::-1]
        return

    def __init__(self, GPIO, pins, reverse):
        self.GPIO = GPIO
        self.pins = pins
        self.set_pins()
        self.set_steps(reverse)

        return