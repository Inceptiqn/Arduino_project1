#include "DHT.h"

DHT dht(2,DHT11);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  auto t = dht.readTemperature();
  Serial.println(t);
}
