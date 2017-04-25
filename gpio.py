import RPi.GPIO as GPIO, time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
def on():
	GPIO.output(18, 1)
def off():
	GPIO.output(18, 0)
def reboot(t):
	try:
		t = int(t)
	except:
		print(t + " is not a valid timeout")
		return
        GPIO.output(18, 0)
	time.sleep(t)
        GPIO.output(18, 1)

