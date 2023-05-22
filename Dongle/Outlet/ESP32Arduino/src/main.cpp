// EmonLibrary examples openenergymonitor.org, Licence GNU GPL V3

#include "currentSensor.hpp"
#include "tempSensor.hpp"
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>


currentSensor cs;
communication com;
tempSensor ts(com);


long startMillis;
long currentMillis;
bool pinState = false;

void setup()
{  
  //set up serial communication look at communications.hpp for details
  com.setupCommunication(true, "AegisDongle-A73E");
  //set up temperature sensor look at tempSensor.hpp for details
  ts.initTemp();
  //set up current sensor look at currentSensor.hpp for details
  cs.setupCurrentSensor();
  //set up digital pin 27 which is used by the relay
  pinMode(27, OUTPUT);
  //set it to high turn on the relay
  digitalWrite(27, pinState=false);
  startMillis = millis(); 
}

void loop()
{
  currentMillis = millis();
  long newtime = currentMillis - startMillis;
  double Irms = cs.getIrms();  // Calculate Irms only
  String dhtdata = ts.getTemperature(); //Returns Temperature, Humidity
  com.sendMessage(String(newtime) + "," + dhtdata + "," + String(Irms) + ';'); //Sends Temperature,Humidity,Irms over bluetooth 
  String message = com.receiveMessage();
  if(message == String("on")) {
    digitalWrite(27, pinState=true);
  } else if (message==String("off")) {
    digitalWrite(27, pinState=false);
  }
  delay(1000);
}