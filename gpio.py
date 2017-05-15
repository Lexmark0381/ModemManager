import RPi.GPIO as GPIO, time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

def on():
	GPIO.output(18, 0)
	return 0

def off():
	GPIO.output(18, 1)
	return 0

def reboot(t):
	try:
		t = int(t)
	except:
		print(t + " is not a valid timeout")
		return -1
	print("GPIO : OFF")
	GPIO.output(18, 1)
	time.sleep(t)
	print("GPIO : ON")
	GPIO.output(18, 0)
	return 0