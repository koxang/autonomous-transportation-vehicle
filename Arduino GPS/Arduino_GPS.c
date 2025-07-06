#include <SoftwareSerial.h>
#include <TinyGPS++.h>

SoftwareSerial gpsSerial(8, 9); // GPS modülü için RX, TX pinleri
TinyGPSPlus gps;

void setup() {
  gpsSerial.begin(9600);
  Serial.begin(9600);
  Serial.println("GPS başlatılıyor...");
}

void loop() {
  while (gpsSerial.available()) {
    int data = gpsSerial.read();
    if (gps.encode(data)) {
      if (gps.location.isValid()) {
        float latitude = gps.location.lat();
        float longitude = gps.location.lng();

        // Android uygulamaya gönderilecek veri
        Serial.print("Latitude: ");
        Serial.print(latitude, 6);
        Serial.print(" | Longitude: ");
        Serial.println(longitude, 6);

        delay(1000); // 1 saniyede bir konum güncelle
      }
    }
  }
}