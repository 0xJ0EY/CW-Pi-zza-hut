from .audio import Audio
from .button import Button
from .sensor import Sensor
from .light import Light
from .wheel_controller import WheelController
from .navigator import Navigator

from .light_state import LightState
from .crossroad_rotation import CrossroadRotation

class Car:

    GPIO        = None

    audio       = None
    button      = None
    sensor      = None
    lights      = None
    navigator   = None
    wheel_controller = None

    # Conditional
    has_started = False

    # Play starting sound & music
    def start(self):
        self.audio.play_intro(self.navigator.get_state())
        self.audio.play_music()
        self.has_started = True
        return

    # Check
    def update(self):

        # Check if either the button is enabled or there is an chosen end point (WebApp)
        run = self.button.check() or self.sensor.chosen_rotation != CrossroadRotation.NONE

        if (run):
            # If the script hasnt run yet, start it
            if (not self.has_started): self.start()

            direction = self.sensor.get_direction()

            self.lights.update(direction)
            self.wheel_controller.move(direction)
            self.wheel_controller.regulate_speed(direction)

            #  Reset stop
            self.has_stopped = False

        else:
            # If not running
            self.sensor.chosen_rotation = self.navigator.update()

            self.wheel_controller.current_speed = self.wheel_controller.start_speed
            self.lights.set_lights(LightState.DISCO)
            self.audio.stop_music()

            # Reset start
            self.has_started = False

        # Return new speed, for timing event
        return self.wheel_controller.current_speed

    # Stop audio, play audio and send reset api request
    def end(self):
        self.audio.stop_music()
        self.audio.play_outro(self.navigator.get_state())
        self.lights.set_lights(LightState.DISCO)
        self.navigator.reset_state()

        return

    def __init__(self, GPIO, server_ip):
        self.GPIO = GPIO

        self.audio          = Audio()
        self.button         = Button(self.GPIO, 26)
        self.sensor         = Sensor(self.GPIO, self, 14, 15, 18)
        self.lights         = Light(self.GPIO, 13, 19, None)

        self.navigator = Navigator(server_ip)

        self.wheel_controller = WheelController(self.GPIO, [27, 22, 10, 9], [2, 3, 4, 17])

        return