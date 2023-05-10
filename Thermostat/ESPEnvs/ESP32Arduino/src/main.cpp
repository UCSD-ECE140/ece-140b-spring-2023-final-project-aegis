// EmonLibrary examples openenergymonitor.org, Licence GNU GPL V3

#include "currentSensor.hpp"
#include "tempSensor.hpp"


currentSensor cs;
communication com;
tempSensor ts(com);



void setup()
{  
  //set up serial communication look at communications.hpp for details
  com.setupCommunication(true, "AegisDongle");
  //set up temperature sensor look at tempSensor.hpp for details
  ts.initTemp();
  //set up current sensor look at currentSensor.hpp for details
  cs.setupCurrentSensor();
  //set up digital pin 27 which is used by the relay
  pinMode(27, OUTPUT);
  //set it to high turn on the relay
  digitalWrite(27, HIGH);
}

void loop()
{
  double Irms = cs.getIrms();  // Calculate Irms only
  ts.printTemperature();
  com.sendMessage("Current: " + String(Irms) + "A");
}