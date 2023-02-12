#include <Arduino.h>
#include <ESP32QRCodeReader.h>
#include <TimeLib.h>
#include <WiFi.h>
#include "time.h"
#include <Firebase_ESP_Client.h>

// Provide the token generation process info.
#include "addons/TokenHelper.h"
// Provide the RTDB payload printing info and other helper functions.
#include "addons/RTDBHelper.h"

#define API_KEY "AIzaSyDVoPt75RpCkReVnf04O9mO1d94f5p8VeI"
#define DATABASE_URL "https://istudio-70ff0-default-rtdb.firebaseio.com/"

// Define Firebase Data object
FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

unsigned long sendDataPrevMillis = 0;
int intValue;
float floatValue;
bool signupOK = false;

const char *ssid = "DIGI-GGS3";
const char *password = "Furanet1";
const char *ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = 7200;
const int   daylightOffset_sec = 0;

tmElements_t tm;
int Year, Month, Day, Hour, Minute, Second, Milli, Tz;

void displayTime(time_t t) {
  Serial.print(hour(t));
  Serial.print('-');
  Serial.print(day(t));
  Serial.print('-');
  Serial.print(month(t));
  Serial.print('-');
  Serial.println(year(t));
}

bool isTimeEqual(time_t t1, time_t t2) {
  if (
    hour(t1) == hour(t2)
    and day(t1) == day(t2)
    and month(t1) == month(t2)
    and year(t1) == year(t2)
  )
    return true;
  return false;
}

void createElements(const char *str)
{
  sscanf(str, "%d-%d-%dT%d:%d:%d.%dZ", &Year, &Month, &Day, &Hour, &Minute, &Second, &Milli, &Tz);
  tm.Year = CalendarYrToTm(Year);
  tm.Month = Month;
  tm.Day = Day;
  tm.Hour = Hour;
  tm.Minute = Minute;
  tm.Second = Second;
}

void printLocalTime(){
  struct tm timeinfo;
  if(!getLocalTime(&timeinfo)) {
    Serial.println("Failed to obtain time");
    return;
  }
  Serial.println(&timeinfo, "%A, %B %d %Y %H:%M:%S");
  Serial.print("Day of week: ");
  Serial.println(&timeinfo, "%A");
  Serial.print("Month: ");
  Serial.println(&timeinfo, "%B");
  Serial.print("Day of Month: ");
  Serial.println(&timeinfo, "%d");
  Serial.print("Year: ");
  Serial.println(&timeinfo, "%Y");
  Serial.print("Hour: ");
  Serial.println(&timeinfo, "%H");
  Serial.print("Hour (12 hour format): ");
  Serial.println(&timeinfo, "%I");
  Serial.print("Minute: ");
  Serial.println(&timeinfo, "%M");
  Serial.print("Second: ");
  Serial.println(&timeinfo, "%S");

  Serial.println("Time variables");
  char timeHour[3];
  strftime(timeHour,3, "%H", &timeinfo);
  Serial.println(timeHour);
  char timeWeekDay[10];
  strftime(timeWeekDay,10, "%A", &timeinfo);
  Serial.println(timeWeekDay);
  Serial.println();
}

ESP32QRCodeReader reader(CAMERA_MODEL_AI_THINKER);

void onQrCodeTask(void *pvParameters) {
  struct QRCodeData qrCodeData;

  while (true) {
    if (reader.receiveQrCode(&qrCodeData, 100)) {
      Serial.println("Found QRCode");

      if (qrCodeData.valid) {
        // Get qr time
        const char *dateTime = (const char *)qrCodeData.payload;
        createElements(dateTime);
        char qr_time[14];
        strncpy(qr_time, dateTime, 13);
        qr_time[13] = '\0';
        Serial.print("QR time:");
        Serial.println(qr_time);

        // Get current time
        struct tm timeinfo;
        if(!getLocalTime(&timeinfo)){
          Serial.println("Failed to obtain time");
          return;
        }
        char current_time[20];
        time_t stime = mktime(&timeinfo);
        sprintf(current_time, "%02d-%02d-%02dT%02d", year(stime), month(stime), day(stime), hour(stime));
        Serial.print("Current time:");
        Serial.println(current_time);

        // Compare qr time with current time
        if (strcmp(qr_time, current_time) == 0)
          Serial.println("--- ACCESS GRANTED ---");
        else
          Serial.println("--- ACCESS DENIED ---");

      } else {
        Serial.print("Invalid: ");
        Serial.println((const char *)qrCodeData.payload);
      }
    }
    vTaskDelay(100 / portTICK_PERIOD_MS);
  }
}

void setup()
{
  Serial.begin(115200);
  Serial.println();

  // Connect to Wi-Fi
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected.");

  configTime(7200, 0, ntpServer);
  printLocalTime();

  /* Assign the api key (required) */
  config.api_key = API_KEY;

  /* Assign the RTDB URL (required) */
  config.database_url = DATABASE_URL;

  /* Sign up */
  if (Firebase.signUp(&config, &auth, "", "")) {
    Serial.println("Firebase login: ok");
    signupOK = true;
  }
  else {
    Serial.printf("%s\n", config.signer.signupError.message.c_str());
  }

  /* Assign the callback function for the long running token generation task */
  config.token_status_callback = tokenStatusCallback; //see addons/TokenHelper.h

  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);

  reader.setup();

  Serial.println("Setup QRCode Reader");

  reader.beginOnCore(1);

  Serial.println("Begin on Core 1");

  xTaskCreate(onQrCodeTask, "onQrCode", 4 * 1024, NULL, 4, NULL);
}

void loop() {
  delay(100);
}