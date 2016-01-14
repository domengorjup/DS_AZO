/* nRF24L01 analogue accelerometer ADXL335 example: nRF24L01 Transmit Acceleration values
 - CONNECTIONS: nRF24L01 Modules See:
 http://arduino-info.wikispaces.com/Nrf24L01-2.4GHz-HowTo
   1 - GND
   2 - VCC 3.3V !!! NOT 5V
   3 - CE to Arduino pin 9
   4 - CSN to Arduino pin 10
   5 - SCK to Arduino pin 13
   6 - MOSI to Arduino pin 11
   7 - MISO to Arduino pin 12
   8 - UNUSED
   - 
   ADXL335:
   GND to Arduino GND
   VCC to Arduino +5V
   X Pot to Arduino A0
   Y Pot to Arduino A1
   Z Pot to Arduino A2
   

/*-----( Import needed libraries )-----*/
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <stdio.h>

/*-----( Declare Constants and Pin Numbers )-----*/
#define CE_PIN   9
#define CSN_PIN 10
#define XPIN A0
#define YPIN A1
#define ZPIN A2

// NOTE: the "LL" at the end of the constant is "LongLong" type
const uint64_t pipe = 0xE8E8F0F0E1L; // Define the transmit pipe


/*-----( Declare objects )-----*/
RF24 radio(CE_PIN, CSN_PIN); // Create a Radio
/*-----( Declare Variables )-----*/
int acc[4];  // 3 element array holding Acc. readings
int start_time = millis();

void setup()   /****** SETUP: RUNS ONCE ******/
{
  Serial.begin(115200);
  radio.begin();
  //radio.setRetries(15,15);
  radio.setDataRate(RF24_1MBPS);
  //radio.setPayloadSize(2);
  radio.openWritingPipe(pipe);

}//--(end setup )---


void loop()   /****** LOOP: RUNS CONSTANTLY ******/
{
  int tStamp = millis() - start_time;
  
  acc[0] = analogRead(XPIN);
  acc[1] = analogRead(YPIN);
  acc[2] = analogRead(ZPIN);
  acc[3] = tStamp;
  
  radio.write( acc, sizeof(acc) );
  //Serial.print(acc[0]);
  //Serial.print(acc[1]);
  //Serial.println(acc[2]);
  
  //delay(0.1);
  

}//--(end main loop )---

/*-----( Declare User-written Functions )-----*/

//NONE
//*********( THE END )***********
