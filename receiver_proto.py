import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time, sys
import spidev
import numpy as np

GPIO.setmode(GPIO.BCM)
pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xd2]]

print("Initiating setup...\n")

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(1,22)                       # CE1, GPIO22
radio.setRetries(15,15)
#radio.setPayloadSize(16)
#radio.setChannel(66)                  # hex?
radio.setDataRate(NRF24.BR_1MBPS)       # 2 MB/s data rate
radio.setPALevel(NRF24.PA_HIGH)         # Power Level (range): [MAX, HIGH, LOW, MIN]
#radio.setAutoAck(True)                  # 
#radio.enableAckPayload()                # 
radio.enableDynamicPayloads()           # enable dynamic payload size

radio.openReadingPipe(1, pipes[0])
radio.printDetails()
radio.startListening()

print("Setup complete.")

radio.stopListening()
radio.startListening()
print("Listening...")
try:
    while True:
        time.sleep(0.0001)
        
        while not radio.available():
            time.sleep(1)
            print(radio.available())

        receivedMessage = []
        radio.read(receivedMessage, radio.getDynamicPayloadSize())
        print("Received: {}".format(receivedMessage))
        

except KeyboardInterrupt:
    sys.exit(0)
