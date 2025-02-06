#include "DHT.h"

#define DHTPIN 2
#define DHTTYPE DHT11

#define LED_RED 4
#define LED_GREEN 3

#define TEMP_HIGH 22.0
#define TEMP_LOW 19.0

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();

  pinMode(LED_RED, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
}

void loop() {
  float temp = dht.readTemperature();

  Serial.println(temp);

  if (temp > TEMP_HIGH) {
    digitalWrite(LED_RED, HIGH);
    digitalWrite(LED_GREEN, LOW);
    //Serial.println("LED_RED_ON");
  }
  else if (temp >= TEMP_LOW && temp <= TEMP_HIGH) {
    digitalWrite(LED_RED, LOW);
    digitalWrite(LED_GREEN, HIGH);
    //Serial.println("LED_GREEN_ON");
  }
  else {
    digitalWrite(LED_RED, LOW);
    digitalWrite(LED_GREEN, LOW);
    //Serial.println("LED_OFF");
  }

  delay(1000);
}
