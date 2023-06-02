#include "currentSensor.hpp"
#include "tempSensor.hpp"
#include "circle.hpp"
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <thread>
#include <mutex>
#include <condition_variable>

using namespace std;
WiFiClient espClient;
PubSubClient client(espClient);
String messageBuffer = "";
circular_buffer<String, 30> cbuf;

String messageSend = "";
currentSensor cs;
tempSensor ts;
String clientId = "ESP32Client-Unique-bed-77632231234431";
String topic = "aegisDongleSend/" + clientId;

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

void wifi_thread() {
  while (true) {
    Serial.println("Just in");
    std::unique_lock lk(m);
    Serial.println("Just in it");
    cv.wait(lk, []{return WiFi.status() != WL_CONNECTED;});
    Serial.println("Just in about");
    setUpWifi();
    Serial.println("Just in dubs");
  }
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
  //set up temperature sensor look at tempSensor.hpp for details
  ts.initTemp();
  //set up current sensor look at currentSensor.hpp for details
  cs.setupCurrentSensor();
  //set up digital pin 27 which is used by the relay
  pinMode(27, OUTPUT);
  //set it to high turn on the relay
  digitalWrite(27, pinState=false);
  startMillis = millis(); 
  setUpWifi();
  // worker = new thread(wifi_thread);
  // cv.notify_all();
}

void loop()
{
  currentMillis = millis();
  long newtime = currentMillis - startMillis;
  double Irms = cs.getIrms();  // Calculate Irms only
  String dhtdata = ts.getTemperature(); //Returns Temperature, Humidity
  messageSend = clientId + "," + dhtdata + "," + String(Irms) + ';';
  if (WiFi.status() == WL_CONNECTED) {
    while(!cbuf.empty()) {
      sendMessage(topic, cbuf.get().value());
    }
    cbuf.reset();
    sendMessage(topic, messageSend); //Sends Temperature,Humidity,Irms over bluetooth 
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