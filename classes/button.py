class Button:

    GPIO = None
    pin = None
    previous_state = None
    enabled = False

    # Check every tick if the button has been changed
    def check(self):
        current_state = not self.GPIO.input(self.pin)

        # State has changed, toggle enabled
        if (current_state == True and self.previous_state != current_state):
            self.enabled = not self.enabled

        self.previous_state = current_state

        return self.enabled

    def set_pin(self):
        self.GPIO.setup(self.pin, self.GPIO.IN, self.GPIO.PUD_UP)

    def __init__(self, GPIO, pin):
        self.GPIO = GPIO
        self.pin = pin
        self.set_pin()

        return