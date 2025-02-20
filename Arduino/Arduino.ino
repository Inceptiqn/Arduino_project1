#include "DHT.h"
#define DHTPIN 2
#define DHTTYPE DHT11

#define RELAY 10
#define TEMP_HIGH 24.0

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();

  pinMode(RELAY, OUTPUT);
}

void loop() {
  float temp = dht.readTemperature();
  float humidity = dht.readHumidity();

  Serial.print(temp);
  Serial.print(",");
  Serial.println(humidity);

  if (temp > TEMP_HIGH) {
    digitalWrite(RELAY, HIGH);
  } else {
    digitalWrite(RELAY, LOW);
  }

  delay(1000);
}
