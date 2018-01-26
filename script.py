import RPi.GPIO as GPIO
import time
import sys
import os

from classes.car import Car
from classes.car_state import CarState

print("""
   __              __                ___  _          _ 
  / /  ___ ___ _  / /  ___  ________/ _ \(_)______  (_)
 / /__/ _ `/  ' \/ _ \/ _ \/ __/___/ ___/ /___/ _ \/ / 
/____/\_,_/_/_/_/_.__/\___/_/     /_/  /_/   /_//_/_/  


By Team Lambor-Pi-ni          
""")

# Set GPIO Mode
GPIO.setmode(GPIO.BCM)

web_app = "bot.joeyderuiter.me"

# Create car instance
car = Car(GPIO, web_app)

try:
    while (car.sensor.state != CarState.DONE):
        wait = car.update()
        time.sleep(wait)

    GPIO.cleanup()
    time.sleep(2.5)
    os.execv(sys.executable, ['python'] + sys.argv) # Restart the program

except KeyboardInterrupt:
    GPIO.cleanup()

