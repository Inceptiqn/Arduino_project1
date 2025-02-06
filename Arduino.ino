#include "DHT.h"

#define DHTPIN 2
#define DHTTYPE DHT11

#define RELAY 10

#define TEMP_HIGH 21.0

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();

  pinMode(RELAY, OUTPUT);
}

void loop() {
  float temp = dht.readTemperature();

  Serial.println(temp);

  if (temp > TEMP_HIGH) {
    digitalWrite(RELAY, HIGH);
    //Serial.println("LED_RED_ON");
  }
  else {
    digitalWrite(RELAY, LOW);
    //Serial.println("LED_GREEN_ON");
  }

  delay(1000);
}
