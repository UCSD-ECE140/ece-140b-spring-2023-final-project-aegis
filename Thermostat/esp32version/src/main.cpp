#include "currentSensor.hpp"
#include "tempSensor.hpp"
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <stdlib.h>

using namespace std;
WiFiClient espClient;
PubSubClient client(espClient);
std::string messageBuffer = "";

String messageSend = "";
currentSensor cs;
tempSensor ts;

String msg= "";
long startMillis;
long currentMillis;
bool pinState = false;

std::mutex m;
std::condition_variable cv;
std::string data;
std::thread* worker;
bool disconnected = false;
bool processed = false;
int currentset = 0;

void callback(char* topic, uint8_t* data, unsigned int code){
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
  Serial.print("Message:");
  for(int i = 0; i < code; i++){
    Serial.print((char)data[i]);
    messageBuffer += (char)data[i];
  }
  Serial.print("\n");
  if(messageBuffer == String("on")) {
      digitalWrite(27, pinState=true);
  } else if (messageBuffer == String("off")) {
      digitalWrite(27, pinState=false);
  }
  if(topic == std::string("aegisTempSet")) {
    int currentset = std::stoi(messageBuffer);
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
  client.setServer("broker.hivemq.com",1883);
  client.setCallback(callback);
  while (!client.connected()) {
      String clientId = "ESP32Client-Unique-77632231234431";
      Serial.println("Connecting to MQTT...");
      if (client.connect(clientId.c_str())) {
      Serial.println("connected");  
      } else {
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
      }
  }
  client.publish("aegisDongleInit","Hello from ESP32");
  client.subscribe("aegisDongleReceive");
}

void sendMessage(String topic, String message) {
    Serial.println("Sending message: " + message + " to topic: " + topic);
    client.publish(topic.c_str(), message.c_str());
}

String receiveMessage() {
    if(messageBuffer.length()>0){
        String temp = messageBuffer;
        messageBuffer = "";
        return temp;
    }
    return "";
}

void setup()
{  
  Serial.begin(115200);
  //set up serial communication look at communications.hpp for details
  //set up temperature sensor look at tempSensor.hpp for details
  ts.initTemp();
  //set up digital pin 27 which is used by the relay
  pinMode(27, OUTPUT); //Heating
  pinMode(28, OUTPUT); //Cooling
  pinMode(29, OUTPUT); //Fan
  //set it to low
  digitalWrite(27, pinState=false);
  digitalWrite(28, pinState=false);
  digitalWrite(29, pinState=false);

  setUpWifi();
}

void loop()
{
  String dhtdata = ts.getTemperature(); //Returns Temperature, Humidity
  if (WiFi.status() == WL_CONNECTED) {
    while(!cbuf.empty()) {
      sendMessage("aegisDongleSend", cbuf.get().value());
    }
    cbuf.reset();
    sendMessage("aegisDongleSend", messageSend); //Sends Temperature,Humidity,Irms over bluetooth 
    String message = receiveMessage();
    delay(1000);
  } else {
    // cv.notify_all();
    cbuf.put(messageSend);
    Serial.println("Adding to circle");
    digitalWrite(27, pinState=true); //Or whatever value makes it so relay stays permanently on if the wifi is disconnected
    delay(1000);  
  }
  client.loop();
}