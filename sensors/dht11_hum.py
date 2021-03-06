import serial
import time
import sys
import os
import termios
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pfc_connection_arduino import pfc_connection_arduino

class dht11_hum:
	SERIAL = None
	def __init__(self):
		self.connect()
	def connect(self):
		cont_ad = pfc_connection_arduino()
		port = cont_ad.get_USB_PORT()
		f = open(port)
		attrs = termios.tcgetattr(f)
		attrs[2] = attrs[2] & ~termios.HUPCL
		termios.tcsetattr(f, termios.TCSAFLUSH, attrs)
		f.close()
		self.SERIAL = serial.Serial(port, cont_ad.get_BAUD_RATE(),timeout=60)

	def getValue(self):
		self.SERIAL.write("get_hum")
		time.sleep(0.5)
		value = self.SERIAL.readline()
		return value
if __name__ == '__main__':
	dht11_hum = dht11_hum()
	order = sys.argv[1]

	if order == 'get':
		v = dht11_hum.getValue().strip()
		print(v+ "," + str(datetime.now()))
