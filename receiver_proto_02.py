#!/usr/bin/env python

#
# Example using Dynamic Payloads
# 
#  This is an example of how to use payloads of a varying (dynamic) size.
# 

from __future__ import print_function
import time, sys
from RF24 import *
import numpy as np



########### USER CONFIGURATION ###########
radio = RF24(RPI_BPLUS_GPIO_J8_22, RPI_BPLUS_GPIO_J8_24, BCM2835_SPI_SPEED_8MHZ)

##########################################
print('Initiating Setup...')
pipes = [0xF0F0F0F0D2]
print("1")
radio.begin()
print("2")
#radio.setPayloadSize(2)
radio.setDataRate(NRF24.BR_1MBPS)       # 1 MB/s data rate
radio.setPALevel(NRF24.PA_HIGH)         # Power Level (range): [MAX, HIGH, LOW, MIN]
radio.enableDynamicPayloads()
radio.setRetries(5,15)
radio.openReadingPipe(1,pipes[0])
print("Setup complete.\n")
radio.printDetails()

radio.startListening()
print("\nListening...\n")


# forever loop
while True:
    # if there is data ready
    if radio.available():
        while radio.available():
                len = radio.getDynamicPayloadSize()
                accData = radio.read(len)

                # Spew it
                print('Got payload size={} value="{}"'.format(len, accData.decode('utf-8')))

    # in no data
    else:
        print("Waiting... Radio.available={}".format(radio.available()))
        time.sleep(0.5)

