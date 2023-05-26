#include "currentSensor.hpp"
#include "tempSensor.hpp"
#include "circle.hpp"
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <pthread.h>


WiFiClient espClient;
PubSubClient client(espClient);
String messageBuffer = "";
circular_buffer<String, 30> cbuf;

String messageSend = "";
currentSensor cs;
tempSensor ts;

String msg= "";
long startMillis;
long currentMillis;
bool pinState = false;


void callback(char* topic, uint8_t* data, unsigned int code){
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
  Serial.print("Message:");
  for(int i = 0; i < code; i++){
    Serial.print((char)data[i]);
    messageBuffer += (char)data[i];
  }
  if(messageBuffer == String("on")) {
      digitalWrite(27, pinState=true);
  } else if (messageBuffer == String("off")) {
      digitalWrite(27, pinState=false);
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

// void *receive(void *i) {
//   while (1) {
//     String message = receiveMessage();
//     Serial.println("recieved " + message);
//     if(message == String("on")) {
//       digitalWrite(27, pinState=true);
//     } else if (message==String("off")) {
//       digitalWrite(27, pinState=false);
//     }
//     delay(100);
//   }
// }


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
  // pthread_t mainThreadRef;
  // int mainValue;
  // mainValue = pthread_create(&mainThreadRef, NULL, receive, (void*)NULL);
  // if (mainValue) {
  //   Serial.println("Problem setting up the communication thread!");
  // }
}

void loop()
{
  currentMillis = millis();
  long newtime = currentMillis - startMillis;
  double Irms = cs.getIrms();  // Calculate Irms only
  String dhtdata = ts.getTemperature(); //Returns Temperature, Humidity
  messageSend = dhtdata + "," + String(Irms) + ';';
  if (WiFi.status() == WL_CONNECTED) {
    while(!cbuf.empty()) {
      sendMessage("aegisDongleSend", cbuf.get().value());
    }
    cbuf.reset();
    sendMessage("aegisDongleSend", messageSend); //Sends Temperature,Humidity,Irms over bluetooth 
    String message = receiveMessage();
    delay(1000);
  } else {
    setUpWifi();
    cbuf.put(messageSend);
    digitalWrite(27, pinState=true); //Or whatever value makes it so relay stays permanently on if the wifi is disconnected
    delay(1000);
  }
  client.loop();
}