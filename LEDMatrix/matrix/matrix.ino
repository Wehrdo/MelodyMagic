#include <Adafruit_GFX.h>
#include <Adafruit_NeoMatrix.h>
#include <Adafruit_NeoPixel.h>

#include "Exploder.hpp"
#include "Twinkler.hpp"

#define PIN 5


Adafruit_NeoMatrix matrix = Adafruit_NeoMatrix(32, 8, PIN,
  NEO_MATRIX_TOP     + NEO_MATRIX_LEFT +
  NEO_MATRIX_COLUMNS + NEO_MATRIX_ZIGZAG,
  NEO_GRB            + NEO_KHZ800);

Exploder exploder(2000, 32, 8);
Twinkler twinkler(250, 32, 8);

const int MSG_SIZE = 7;
uint8_t msg[MSG_SIZE];
uint8_t msgLen = 0, msgStart, msgEnd;

bool pin = false;

void setup() {
  Serial.begin(115200);

  pinMode(2, OUTPUT);
  digitalWrite(2, pin);
  
  matrix.begin();
  //matrix.setBrightness(40);
}

unsigned long long nextTime = 0;
const unsigned long long UPDATE_RATE = 20;

bool newMsg = false;
uint8_t type, note;

uint8_t getMsgByte(int i) {
  i = (i + msgStart) % MSG_SIZE;

  return msg[i];
}

void loop() {
  if(Serial.available()) {
    uint8_t b = Serial.read();

    if(msgLen == MSG_SIZE && b == 0) {
      pin = !pin;
      digitalWrite(2, pin);

      Serial.println("[Info] Received hit");
      
      newMsg = true;
      type = getMsgByte(0);
      note = getMsgByte(3);
      //hue = 212 * getMsgByte(3) / 6;

      msgStart = msgEnd = msgLen = 0;
    }
    else {
      msg[msgEnd] = b;
  
      msgEnd = (msgEnd + 1) % MSG_SIZE;
      if(msgLen >= MSG_SIZE) {
        msgStart = (msgStart + 1) % MSG_SIZE;
      }
      else {
        msgLen++;
      }
    }
  }

  auto curTime = millis();
  if(curTime >= nextTime) {
    if(newMsg && type < 2) {
      uint8_t hue = 212 * note / 6;
      exploder.tick(type, hue);
      newMsg = false;
    }
    else {
      exploder.tick();
    }
    if(newMsg && type == 2) {
      uint8_t hue = 212 * note / 7;
      twinkler.addTwinkle(hue);
      newMsg = false;
    }
    
    exploder.render(matrix);
    twinkler.render(matrix);
    matrix.show();

    newMsg = false;
    nextTime = curTime + UPDATE_RATE;
  }
}
