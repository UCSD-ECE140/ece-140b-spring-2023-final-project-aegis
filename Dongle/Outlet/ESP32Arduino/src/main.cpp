#include "currentSensor.hpp"
#include "tempSensor.hpp"
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>

WiFiClient espClient;
PubSubClient client(espClient);
String messageBuffer = "";
String clientId = "ESP32Client-Unique-bed-77632231234431";

void callback(char* topic, uint8_t* data, unsigned int code){
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
  Serial.print("Message:");
  for(int i = 0; i < code; i++){
    Serial.print((char)data[i]);
    messageBuffer += (char)data[i];
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
      if (client.connect(clientId.c_str())) {
      Serial.println("connected");  
      } else {
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
      }
  }
  client.publish("Aegis/aegisDongleInit","Hello from outlet!");
  client.subscribe("Aegis/aegisDongleReceive");
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
}

void loop()
{
  currentMillis = millis();
  long newtime = currentMillis - startMillis;
  double Irms = cs.getIrms();  // Calculate Irms only
  String dhtdata = ts.getTemperature(); //Returns Temperature, Humidity
  sendMessage("Aegis/aegisDongleSend/" + clientId, dhtdata + "," + String(Irms) + ';'); //Sends Temperature,Humidity,Irms over bluetooth 
  String message = receiveMessage();
  Serial.println("recieved " + message);
  if(message == String("on")) {
    digitalWrite(27, pinState=true);
  } else if (message==String("off")) {
    digitalWrite(27, pinState=false);
  }
  client.loop();
  delay(1000);
}