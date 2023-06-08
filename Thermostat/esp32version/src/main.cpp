#include "tempSensor.hpp"
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <stdlib.h>

using namespace std;

WiFiClient espClient;
PubSubClient client(espClient);
std::string messageBuffer;
std::string roomForTemp;

String messageSend = "";
tempSensor ts;

String msg= "";
long startMillis;
long currentMillis;
bool pinState = false;
std::string sender;
bool wasOff = false;
bool ac = false;
bool heat = false;
bool fan = false;

String clientId = WiFi.macAddress();
std::string data;
bool disconnected = false;
bool processed = false;
float currentSet = 0.0;
float currentTemp = 0.0;
bool tempControl = false;
std::vector<std::string> senderSplit;
std::vector<std::string> topicSplit;
std::string topicString;
std::vector<std::string> split;

std::vector<std::string> splitString(std::string str, char splitter){
    std::vector<std::string> result;
    std::string current = ""; 
    for(int i = 0; i < str.size(); i++){
        if(str[i] == splitter){
            if(current != ""){
                result.push_back(current);
                current = "";
            } 
            continue;
        }
        current += str[i];
    }
    if(current.size() != 0)
        result.push_back(current);
    return result;
}

void callback(char* topic, uint8_t* data, unsigned int code){
  for(int i = 0; i < code; i++){
    messageBuffer += (char)data[i];
  }
  split = splitString(messageBuffer, ',');

  topicString = topic;

  topicSplit = splitString(topicString, '/');

  senderSplit = splitString(topicSplit[topicSplit.size()-1], '-');
  if(topicSplit[0] == "Aegis") {
    if(topicSplit[1] == "aegisTempSet") {
      roomForTemp = split[0];
      currentSet = std::stof(split[1]);
      // Serial.println("aegisTempSet received");
      // Serial.print(roomForTemp.c_str());
      // Serial.println(currentSet);
    } else if(topicSplit[1] == "aegisDongleSend") {
      // Serial.println("aegisDongleSend received");
      sender = split[0];
      // Serial.println(sender.c_str());
      // Serial.println(roomForTemp.c_str());
      if(sender == roomForTemp) {
        currentTemp = (std::stof(split[1]) * 9/5) + 32;
        // Serial.println(currentTemp);
        // Serial.println("aegisDongleSend received, correct room");
      }
    } else if(topicSplit[1] == "aegisThermostatControl") {
      // Serial.println("aegisThermostatControl received");
      // Serial.println(messageBuffer.c_str());
      if(messageBuffer == "on") {
        // Serial.println("aegisThermostatControl on");
        tempControl = true;
      } else if(messageBuffer == "off") {
        // Serial.println("aegisThermostatControl off");
        tempControl = false;
      }
    }
  }
  messageBuffer = "";
}

void setUpWifi(){
  // Serial.println("Setting up wifi");
  WiFi.begin("AndroidAP_1584","qqqqqqq1");
  while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      // Serial.println("Connecting to WiFi..");
  }
  // Serial.println("Connected to the WiFi network");
  client.setServer("aegishome.ninja", 8003);
  client.setCallback(callback);
  while (!client.connected()) {
      
      // Serial.println("Connecting to MQTT...");
      if (client.connect(clientId.c_str()), "aegisAdmin", "iLoveAegis!") {
      // Serial.println("connected");  
      } else {
      // Serial.print("failed with state ");
      // Serial.print(client.state());
      delay(2000);
      }
  }
  client.publish("Aegis/aegisDongleInit", "Hello from your Aegis Thermostat!");
  client.subscribe("Aegis/aegisDongleSend/#");
  client.subscribe("Aegis/aegisTempSet");
  client.subscribe("Aegis/aegisThermostatControl");
}

void sendMessage(String topic, String message) {
    // Serial.println("Sending message: " + message + " to topic: " + topic);
    client.publish(topic.c_str(), message.c_str());
}

void setup()
{  
  Serial.begin(115200);
  //set up serial communication look at communications.hpp for details
  //set up temperature sensor look at tempSensor.hpp for details
  ts.initTemp();
  //set up digital pin 27 which is used by the relay
  pinMode(27, OUTPUT); //Heating
  pinMode(26, OUTPUT); //Cooling
  pinMode(25, OUTPUT); //Fan
  //set it to low
  digitalWrite(27, pinState=false);
  digitalWrite(26, pinState=false);
  digitalWrite(25, pinState=false);
  setUpWifi();
}

void loop()
{
  String dhtdata = ts.getTemperature(); //Returns Temperature, Humidity
  if (WiFi.status() != WL_CONNECTED) {
    currentTemp = dhtdata.toInt();
  }
  if(tempControl) {
    if((currentTemp - currentSet) > 1) {
      if(!ac) {
        digitalWrite(27, pinState=false);
        digitalWrite(26, pinState=true);
        digitalWrite(25, pinState=true);
        sendMessage("Aegis/aegisThermostatInfo", "Turning the AC ON!");
        // Serial.println("Turning the AC ON!");
        ac = true;
        heat = false;
      }
      wasOff = false;
    } else if ((currentTemp - currentSet) <= -1) {
      if(!heat) {
        digitalWrite(27, pinState=true);
        digitalWrite(26, pinState=false);
        digitalWrite(25, pinState=true);
        sendMessage("Aegis/aegisThermostatInfo", "Turning the HEAT ON!");
        // Serial.println("Turning the HEAT ON!");
        ac = false;
        heat = true;
      }
      wasOff = false;
    } else {
      if(!wasOff) {
        digitalWrite(27, pinState=false);
        digitalWrite(26, pinState=false);
        digitalWrite(25, pinState=false);
        sendMessage("Aegis/aegisThermostatInfo", "Turning everything OFF");
        // Serial.println("Turning everything OFF");
        wasOff = true;
      }
    }
  } else {
    if(!wasOff) {
      digitalWrite(27, pinState=false);
      digitalWrite(26, pinState=false);
      digitalWrite(25, pinState=false);
      sendMessage("Aegis/aegisThermostatInfo", "Turning everything OFF");
      // Serial.println("Turning everything OFF");
      wasOff = true;
    }
  }
  client.loop();
}