// // same communications file as before used by bus side
// //================================Communications================================
// /*
//  * Precompiler directive elegance: 0 == Serial, 1 == Bluetooth
//  */
// #include "BluetoothSerial.h"
// #include "Arduino.h"



// /**
//  * @brief Class for communication
//  * @cite Adapted from ECE16 communication architecture
//  * @details This class is used to communicate with the ESP32 in a bluetooth or serial fashion more communication methods can be added
//  */
// class communication{
//     bool isBT;
//     String name;
//     BluetoothSerial BTSerial;     // instantiate a BT object

//     public:
//     communication(){
//         isBT = false;
//         name = "AegisDongle-A72E";
//     }
//     communication(communication const&) = delete;
//     /**
//      * @brief Set up the communication object
//      * 
//      * @param isBT 
//      * @param name 
//      */
//     void setupCommunication(bool isBT = false, String name = "AegisDongle-A72E"){
//         this->isBT = isBT;
//         if(isBT){
//             this->name = name;
//             BTSerial.begin(name.c_str());
//         }
//         else Serial.begin(115200);
//     }

//     /**
//      * @brief Receive a message from the communication object
//      * 
//      * @return String 
//      */
//     String receiveMessage() {
//         String message = "";
//         if(isBT){
//             if (BTSerial.available() > 0) {
//                 while (true) {
//                     char c = BTSerial.read();
//                     if (c != char(-1)) {
//                         if (c == '\n')
//                             break;
//                         message += c;
//                     }
//                 }
//             }
//         }
//         else{
//             if (Serial.available() > 0) {
//                 while (true) {
//                     char c = Serial.read();
//                     if (c != char(-1)) {
//                         if (c == '\n')
//                             break;
//                         message += c;
//                     }
//                 }
//             }
//         }
//         return message;
//     }

//     /**
//      * @brief Send a message to the communication object
//      * 
//      * @param message 
//      */
//     void sendMessage(String message) {
//         if(isBT){
//             BTSerial.println(message);
//         }
//         else{
//             Serial.println(message);
//         }
//     }
// };



#include "Arduino.h"
#include "WiFi.h"
#include "PubSubClient.h"

class communication{
    const String ssid = "Aegisv1";
    const String password = "Aegisv111";
    const String mqttServer = "b895eb671f8c4fffab7674f93701e3e5.s2.eu.hivemq.cloud";
    const String mqttUser = "aegisDongle";
    const String mqttPassword = "aegisRoot1";
    const int mqttPort = 8883;

    String messageBuffer = "";
    WiFiClient espClient;
    PubSubClient client;

  public:
    communication(){
        client = PubSubClient(espClient);
    }

    void setupCommunication(){
        WiFi.begin(ssid.c_str(), password.c_str());
        
        while (WiFi.status() != WL_CONNECTED) {
            delay(500);
        }
        
        client.setServer(mqttServer.c_str(), mqttPort);
        while (!client.connected()) {
        if (client.connect("ESP32Client", mqttUser.c_str(), mqttPassword.c_str())) {
            client.subscribe("dongleCommand");
            client.setCallback([this](char* topic, byte* message, unsigned int length) {
        
        for (int i = 0; i < length; i++) {
            messageBuffer += (char)message[i];
        }
        });
        } else {
            delay(5000);
        }
        }
    }

    void sendMessage(String topic, String message) {
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
};
