import RPi.GPIO as GPIO
from NRF24 import NRF24
import time
import spidev
import numpy as np

GPIO.setmode(GPIO.BCM)
pipes = [[0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0,17)                       # CE0 pin = GPIO 17
radio.setPayloadSize(16)
radio.setChannel(0x4c)                  # hex?
radio.setDataRate(NRF24.BR_2MBPS)       # 2 MB/s data rate
radio.setPALevel(NRF24.PA_HIGH)         # Power Level (range): [MAX, HIGH, LOW, MIN]
radio.setAutoAck(True)                  # 
radio.enableAckPayload()                # 
radio.enableDynamicPayloads()           # enable dynamic payload size

radio.openReadingPipe(1, pipes[0])
radio.printDetails()

radio.startListening()

while True:
    ackPL = [1]
    while not radio.available(0):
        time.sleep(1/100)

    receivedMessage = []
    radio.read(receivedMessage, radio.getDynamicPayloadSize())
    print("Received: {}".format(receivedMessage))

