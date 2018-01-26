from .crossroad_rotation import CrossroadRotation

import sys
import requests
import json

class Navigator:

    ticks_required      = 1000 # 1000 * ~0.001 = ~1 sec
    ticks_since_last    = 1000

    last_direction  = CrossroadRotation.NONE

    server_ip = '127.0.0.1'

    addresses = {
        None: CrossroadRotation.NONE,
        "apple": CrossroadRotation.FORWARD,
        "science": CrossroadRotation.RIGHT,
        "starbucks": CrossroadRotation.LEFT
    }

    def get_state(self):

        try:
            response = requests.get('http://' + self.server_ip + '/api/route')
            address = json.loads(response.text)

            self.last_direction = self.addresses[address['content']]

        except requests.exceptions.RequestException as e:
            print(e)
            self.last_direction = CrossroadRotation.NONE

        return self.last_direction

    def reset_state(self):
        try:
            requests.get('http://' + self.server_ip + '/api/reset')

        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

        return self.last_direction


    def update(self):
        if (self.last_direction != CrossroadRotation.NONE): return self.last_direction

        if (self.ticks_since_last > self.ticks_required):
            self.last_direction = self.get_state()
            self.ticks_since_last = 0
            return self.last_direction

        self.ticks_since_last += 1
        return self.last_direction

    def __init__(self, server_ip):
        self.server_ip = server_ip
        return