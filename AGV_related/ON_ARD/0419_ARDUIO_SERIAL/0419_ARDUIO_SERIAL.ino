#include <Adafruit_SSD1306.h>
#include <Wire.h>
#include <string.h>

// to python 명령어 저장 cmd
int cmd;
int input_plc=4;

void setup() {
  Serial.begin(115200);
  // put your setup code here, to run once:
  pinMode(input_plc, INPUT);

  while (! Serial) {
    delay(1);
  }
  //Serial.println(1);
}

void loop() {
  
  if(digitalRead(input_plc) == HIGH){
    Serial.println(int(1));
    delay(1000);
  }

}
