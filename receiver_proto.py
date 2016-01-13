import RPi.GPIO as GPIO
from NRF24.lib_nrf24 import NRF24
import time, sys
import spidev
import numpy as np

GPIO.setmode(GPIO.BCM)
pipes = [0xF0F0F0F0D2]

print("Initiating setup...")

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0,17)                       # CE0 pin = GPIO 17
#radio.setRetries(15,15)
#radio.setPayloadSize(2)
#radio.setChannel(66)                  # hex?
#radio.setDataRate(NRF24.BR_250KBPS)       # 2 MB/s data rate
#radio.setPALevel(NRF24.PA_HIGH)         # Power Level (range): [MAX, HIGH, LOW, MIN]
#radio.setAutoAck(True)                  # 
#radio.enableAckPayload()                # 
radio.enableDynamicPayloads()           # enable dynamic payload size

radio.openReadingPipe(1, pipes[0])
radio.printDetails()

print("Setup complete.")

radio.startListening()
print("Listening...")
try:
    while True:
        ackPL = [1]
        
        while not radio.available():
            time.sleep(1)
            print(radio.available())

        receivedMessage = []
        radio.read(receivedMessage, radio.getDynamicPayloadSize())
        print("Received: {}".format(receivedMessage))

        #radio.writeAckPayload(1, ackPL, len(ackPL))

except KeyboardInterrupt:
    sys.exit(0)
