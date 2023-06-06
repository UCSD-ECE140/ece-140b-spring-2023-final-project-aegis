#include "currentSensor.hpp"
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
std::string messageBuffer = "";
std::string clientId = WiFi.macAddress().c_str();
std::string room = "room";
std::vector<std::string> topicSplit;
std::vector<std::string> messageSplit;
String topic = "Aegis/aegisDongleSend/" + WiFi.macAddress();
String topic1 = "Aegis/aegisDongleReceive/" + WiFi.macAddress();
std::string message = "on";

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
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
  Serial.print("Message:");
  messageBuffer = "";
  for(int i = 0; i < code; i++){
    Serial.print((char)data[i]);
    messageBuffer += (char)data[i];
  }
  Serial.print("\n");
  topicSplit = splitString(topic, '/');
  messageSplit = splitString(messageBuffer, ',');
  if(topicSplit[0] == "Aegis" && topicSplit[1] == "dongleRoomChange") {
    if(messageSplit[0] == clientId) {
      room = messageSplit[1];
    }
  } else if(topicSplit[0] == "Aegis" && topicSplit[1] == "aegisDongleReceive") {
    if(messageBuffer == "off") {
      Serial.println("Turning OFF!");
      message = "off";
    } else {
      Serial.println("Turning ON!");
      message = "on";
    }
  }
}

void setUpWifi(){
  Serial.println("Setting up wifi");
  WiFi.begin("AndroidAP_1584","qqqqqqq1");
  while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
  client.setServer("aegishome.ninja",8003);
  client.setCallback(callback);
  while (!client.connected()) {
      Serial.println("Connecting to MQTT...");
      if (client.connect(clientId.c_str()), "aegisAdmin", "iLoveAegis!") {
      Serial.println("connected");  
      } else {
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
      }
  }

  client.publish(topic.c_str(), "Hello from dongle!");
  client.subscribe(topic1.c_str());
  client.subscribe("Aegis/dongleRoomChange");
}

void sendMessage(String topic, String message) {
    Serial.println("Sending message: " + message + " to topic: " + topic);
    client.publish(topic.c_str(), message.c_str());
}

std::string receiveMessage() {
    if(messageBuffer.length()>0){
        std::string temp = messageBuffer;
        messageBuffer = "";
        return temp;
    }
    return "";
}
currentSensor cs;
tempSensor ts;

long startMillis;
long currentMillis;
bool pinState = false;

void setup()
{  
  Serial.begin(115200);
  //set up serial communication look at communications.hpp for details
  setUpWifi();
  //set up temperature sensor look at tempSensor.hpp for details
  ts.initTemp();
  //set up current sensor look at currentSensor.hpp for details
  cs.setupCurrentSensor();
  //set up digital pin 27 which is used by the relay
  pinMode(27, OUTPUT);
  //set it to high turn on the relay
  digitalWrite(27, pinState=false);
  startMillis = millis(); 
  Serial.println(WiFi.macAddress());
}

void loop()
{
  currentMillis = millis();
  long newtime = currentMillis - startMillis;
  double Irms = cs.getIrms();  // Calculate Irms only
  String dhtdata = ts.getTemperature(); //Returns Temperature, Humidity
  sendMessage(topic, String(room.c_str()) + "," + dhtdata + "," + String(Irms) + ';'); //Sends Temperature,Humidity,Irms over bluetooth 
  // Serial.println(message.c_str());
  if(message == "on") {
    digitalWrite(27, pinState=true);
  } else if (message == "off") {
    digitalWrite(27, pinState=false);
  }
  client.loop();
  delay(1000);
}