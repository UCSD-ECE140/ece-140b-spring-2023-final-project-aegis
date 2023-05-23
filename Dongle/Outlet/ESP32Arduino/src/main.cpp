// EmonLibrary examples openenergymonitor.org, Licence GNU GPL V3

#include "currentSensor.hpp"
#include "tempSensor.hpp"
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>

#include <WiFi.h>
#include "time.h"

const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = 0;
const int   daylightOffset_sec = 0;




currentSensor cs;
communication com;
tempSensor ts(com);


long startMillis;
long currentMillis;
bool pinState = false;

// A function that will be executed by the task
void TaskFunction( void *pvParameters ) {
    for(;;) {
        // task code here
    }
}

void setup()
{  
  //set up serial communication look at communications.hpp for details
  com.setupCommunication();
  //set up temperature sensor look at tempSensor.hpp for details
  ts.initTemp();
  //set up current sensor look at currentSensor.hpp for details
  cs.setupCurrentSensor();
  //set up digital pin 27 which is used by the relay
  pinMode(27, OUTPUT);
  //set it to high turn on the relay
  digitalWrite(27, pinState=false);
  startMillis = millis(); 
  Serial.begin(115200);
}

void loop()
{
  currentMillis = millis();
  long newtime = currentMillis - startMillis;
  double Irms = cs.getIrms();  // Calculate Irms only
  String dhtdata = ts.getTemperature(); //Returns Temperature, Humidity
  com.sendMessage("dongleData", String(newtime) + "," + dhtdata + "," + String(Irms) + ';'); //Sends Temperature,Humidity,Irms over bluetooth 
  //String message = com.receiveMessage();
  // Serial.println("recieved " + message);
  // if(message == String("on")) {
  //   digitalWrite(27, pinState=true);
  // } else if (message==String("off")) {
  //   digitalWrite(27, pinState=false);
  // }
  delay(1000);
  com.refresh();
}