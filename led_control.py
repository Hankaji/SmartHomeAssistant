from gpiozero import LED
import time

green_LED = LED(21)

green_LED.on()
time.sleep(5)
green_LED.off()
