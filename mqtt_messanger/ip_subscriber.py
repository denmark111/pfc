# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import sys
import os
import socket
import fcntl
import struct
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configure import pfc_conf
from datetime import datetime
class ip_subscriber:
	client = None
	subscribe_topic = 'ezfarm/pfc/ip_notifier'
	ip_log_file_path = '/var/www/html/og/log/pfc_ips.log'
	def __init__(self):
		self.client = mqtt.Client()
		self.client.on_connect = self.on_connect
		self.client.on_message = self.on_message

	def on_connect(self, client, userdata, flags, rc):
		print("Broker Connect Status : " + str(rc))
		client.subscribe(self.subscribe_topic)

	def on_message(self,client,userdata, msg):
		print("Topic : ", msg.topic + " / Message : " + str(msg.payload) + " ____Received on " + str(datetime.now()))
		ip_addr_msg = msg.payload
		f=open(self.ip_log_file,'a')
		f.write(ip_addr_msg +"/"+str(datetime.now()) + "\r\n")
		f.close()

	def client_looping(self):
		self.client.connect(pfc_conf.PFC_BROKER_HOST,pfc_conf.PFC_BROKER_PORT,pfc_conf.PFC_BROKER_KEEPALIVE)
		self.client.loop_forever()

if __name__ == '__main__':
	subscriber = ip_subscriber()
	subscriber.client_looping()