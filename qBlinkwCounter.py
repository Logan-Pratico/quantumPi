import RPi.GPIO as GPIO
import time
import quantumrandom
import threading
import os

SDI = 24
RCLK = 23
SRCLK = 18

placePin = (10,22,27,17)
number = (0xc0, 0xf9, 0xa4, 0xb0, 0x99, 0x92, 0x82, 0xf8, 0x80, 0x90)

counter = 0
timer1 = 0

def clearDisplay():
	for i in range(8):
		GPIO.output(SDI,1)
		GPIO.output(SRCLK, GPIO.HIGH)
		GPIO.output(SRCLK, GPIO.LOW)
	GPIO.output(RCLK, GPIO.HIGH)
	GPIO.output(RCLK, GPIO.LOW)

def hc595_shift(data):
	for i in range(8):
		GPIO.output(SDI, 0x80 & (data << i))
		GPIO.output(SRCLK, GPIO.HIGH)
		GPIO.output(SRCLK, GPIO.LOW)
	GPIO.output(RCLK, GPIO.HIGH)
	GPIO.output(RCLK, GPIO.LOW)

def pickDigit(digit):
	for i in placePin:
		GPIO.output(i, GPIO.LOW)
	GPIO.output(placePin[digit], GPIO.HIGH)

LedPin = 20
LedPinGreen = 21
def setup():
	#Set the GPIO modes to BCM Numbering
	GPIO.setmode(GPIO.BCM)
	#Set LedPin's mode to output, and initial level to High(3.3v)
	GPIO.setup(LedPin,GPIO.OUT, initial=GPIO.HIGH)
	GPIO.setup(LedPinGreen, GPIO.OUT, initial=GPIO.HIGH)

	GPIO.setmode(GPIO.BCM) 
	GPIO.setup(SDI, GPIO.OUT) 
	GPIO.setup(RCLK, GPIO.OUT)
	GPIO.setup(SRCLK, GPIO.OUT) 
	for i in placePin:
		GPIO.setup(i, GPIO.OUT)
	global timer1
	
#Define a main function for main process
	


def main():
#		time.sleep(20)
#	try:
		file = open("numbers.txt", "r")
		#print(file.read())
		num = int(float(file.read()))
		file.close()
#		print(num)
		num = num * 2
		file = open("numbers.txt", "w")
		file.write('%d' % num)
		file.close()

		x = int(quantumrandom.randint(0,2))
#		print(x)
		if(x == 0):

			print('Red ')
		#Turn on LED
			GPIO.output(LedPin, GPIO.LOW)
			time.sleep(2)
			GPIO.output(LedPin, GPIO.HIGH)
		else:
			GPIO.output(LedPinGreen, GPIO.LOW)
			print('Green')
			time.sleep(2)
			GPIO.output(LedPinGreen, GPIO.HIGH)
		
		#lighting up counter
		timeout = time.time() + 15
		while(True):	
			clearDisplay()
			pickDigit(0)
			hc595_shift(number[num % 10])
	
			clearDisplay()
			pickDigit(1)
			hc595_shift(number[num % 100//10])

			clearDisplay()
			pickDigit(2)
			hc595_shift(number[num % 1000//100])

			clearDisplay()
			pickDigit(3)
			hc595_shift(number[num % 10000 // 1000])

			if time.time() > timeout:
				break
		
		



		print('LED OFF....')
		time.sleep(0.5)
		destroy()
#	except:
#		print("Too lazy to figure out the error")
def destroy():
	#turn off LED
	GPIO.output(LedPin, GPIO.HIGH)
	GPIO.output(LedPinGreen, GPIO.HIGH)
	#Release resource
	GPIO.cleanup()

#if run this script directly, do:
if __name__ == '__main__':
	setup()
	try:
		main()
	except KeyboardInterrupt:
		destroy()
