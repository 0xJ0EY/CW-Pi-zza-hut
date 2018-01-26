from .crossroad_rotation import CrossroadRotation
import pygame
import time

class Audio:

    pygame = None

    channel_0 = None # music channel
    channel_1 = None # Audio channel

    addresses = {
        CrossroadRotation.NONE: "none",
        CrossroadRotation.FORWARD: "apple",
        CrossroadRotation.LEFT: "starbucks",
        CrossroadRotation.RIGHT: "science"
    }

    # Play music on the music channel
    def play_music(self):
        music = self.pygame.mixer.Sound("music/music.wav")

        self.channel_0.set_volume(0.5)
        self.channel_0.play(music)
        return

    # Stop all audio playing on the music channel
    def stop_music(self):
        self.channel_0.stop()

    # Play the intro, and wait for starting up
    def play_intro(self, location):
        music = self.pygame.mixer.Sound("music/intro.wav")

        self.channel_1.set_volume(1)
        self.channel_1.play(music)

        # Start driving when sound is starting finished
        time.sleep(2.5)

        # Play intro
        music = self.pygame.mixer.Sound("music/going_to.wav")
        self.channel_1.play(music)

        time.sleep(1)

        self.channel_1.play(self.get_location(location))

        return

    # Play the outro, and wait for it to be finished
    def play_outro(self, location):

        # Play outro
        music = self.pygame.mixer.Sound("music/arrived_at.wav")
        self.channel_1.play(music)
        time.sleep(1)

        self.channel_1.play(self.get_location(location))
        time.sleep(1)

        music = self.pygame.mixer.Sound("music/outro.wav")
        self.channel_1.set_volume(1)
        self.channel_1.play(music)

        time.sleep(2.5)

        return

    # Play audio on crossroad (Has to wait for first part to be finished)
    def play_crossroad(self, location):
        music = self.pygame.mixer.Sound("music/crossroad_to.wav")
        self.channel_1.play(music)
        time.sleep(1)

        self.channel_1.play(self.get_location(location))
        time.sleep(1)


        return


    # Get location based on selected rotation
    def get_location(self, location):

        address = self.addresses[location]

        if (address == "apple"):
            return self.pygame.mixer.Sound("music/apple_store.wav")

        elif (address == "science"):
            return self.pygame.mixer.Sound("music/science_center.wav")

        elif (address == "starbucks"):
            return self.pygame.mixer.Sound("music/starbucks.wav")

        return self.pygame.mixer.Sound("music/do_you_know_the_wae.wav")


    def __init__(self):

        pygame.init()
        pygame.mixer.init()

        # Setup channels
        self.channel_0 = pygame.mixer.Channel(0)
        self.channel_1 = pygame.mixer.Channel(1)

        self.pygame = pygame
        return