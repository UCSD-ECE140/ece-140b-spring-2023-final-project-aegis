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
#include "WiFiClientSecure.h"
#include "PubSubClient.h"

class communication{
    // const String ssid = "Aegisv1";
    // const String password = "Aegisv111";
    const String ssid = "AndroidAP_1584";
    const String password = "qqqqqqq1";
    const String mqttServer = "b895eb671f8c4fffab7674f93701e3e5.s2.eu.hivemq.cloud";
    const String mqttUser = "aegisDongle";
    const String mqttPassword = "aegisRoot1";
    const int mqttPort = 8883;

    String messageBuffer = "";
    WiFiClientSecure espClient;

    const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = 0;
const int   daylightOffset_sec = 0;


  public:
  PubSubClient client;
    communication(){
        espClient.setInsecure();
        client = PubSubClient(espClient);
    }

    void setupCommunication(){
        WiFi.begin(ssid.c_str(), password.c_str());
        
        while (WiFi.status() != WL_CONNECTED) {
            delay(500);
        }
        configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
        // client.setServer(mqttServer.c_str(), mqttPort);
        // if (client.connect("Dongle-A73E", "aegisDongle", "aegisRoot1")) {
        //     // client.publish("outTopic","hello world");
        //     // client.subscribe("inTopic");
        //     Serial.println("connected");
        // }
        // else{
        //     Serial.println("failed ");
        //     }
        char* mqttServerAddress = new char[mqttServer.length() + 1];
        char* mqttID = new char[mqttUser.length() + 1];
        char* mqttUser = new char[12 + 1];
        char* mqttPass = new char[mqttPassword.length() + 1];

        strcpy(mqttServerAddress, mqttServer.c_str());
        strcpy(mqttID, "ESP32Client");
        strcpy(mqttUser, "aegisDongle");
        strcpy(mqttPass, "aegisRoot1");
        client.setServer(mqttServerAddress, mqttPort);
        while (!client.connected()) {
            if (client.connect(mqttID, mqttUser, mqttPass)) {

            //      client.subscribe("dongleCommand");
            //     client.setCallback([this](char* topic, byte* message, unsigned int length) {
            
            // for (int i = 0; i < length; i++) {
            //     messageBuffer += (char)message[i];
            // }
            // });
               
            } else {
                delay(5000);
            }
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

    void refresh(){
        client.loop();
    }
};


// #include <arduino.h>

// #include <WiFi.h>
// #include <MQTT.h>
// #include <SPIFFS.h>


// #include <list>
// #include <MQTT_strings.h> 

// #define LANGUAGE "en"
// MQTTLanguage::Texts T;

// MQTTClient      mqtt;

// const int       pin_portalbutton = 35;
// const int       pin_demobutton   = 0;
// const int       pin_backlight    = 4;

// // Configuration via WiFiSettings
// unsigned long   mqtt_interval;
// String          mqtt_Pubtopic;
// String          mqtt_Subtopic;
// String          mqtt_template;
// bool            wifi_enabled;
// bool            mqtt_enabled;
// int             max_failures;


// // ***************** OTA handlers ******************************** OTA handlers ******************************** OTA handlers ***************

// void setup_ota() {
//     ArduinoOTA.setHostname(WiFiSettings.hostname.c_str());
//     ArduinoOTA.setPassword(WiFiSettings.password.c_str());
//     ArduinoOTA.onStart(   []()              { display_big("OTA", TFT_BLUE); });
//     ArduinoOTA.onEnd(     []()              { display_big("OTA done", TFT_GREEN); });
//     ArduinoOTA.onError(   [](ota_error_t e) { display_big("OTA failed", TFT_RED); });
//     ArduinoOTA.onProgress([](unsigned int p, unsigned int t) {
//         String pct { (int) ((float) p / t * 100) };
//         display_big(pct + "%");
//     });
//     ArduinoOTA.begin();
// }

// // ***************** MQTT handlers ******************************** MQTT handlers ******************************** MQTT handlers ***************

// void MQTTretain(const String& topic, const String& message) {
//     Serial.printf("MQTTGo v2 Pub-ing ret. message now... topic: %s payload: %s\n", topic.c_str(), message.c_str());
//     display_topic(topic, message);
//     mqtt.publish(topic, message, true, 0);
// }

// void MQTTpub(const String& topic, const String& message) {
// // Handler for to be published messages
//     Serial.printf("publishing on topic: %s payload: %s\n", topic.c_str(), message.c_str());
//     display_topic(topic, message);
//     mqtt.publish(topic, message, false, 0);  //bool .publish(const char topic[], const char payload[], bool retained, int qos);
// }

// void connect_mqtt() {
//     if (mqtt.connected()) return;  // already/still connected - https://github.com/256dpi/arduino-mqtt

//     static int failures = 0;
//     if (mqtt.connect(WiFiSettings.hostname.c_str())) {
//         failures = 0;
//         mqtt.subscribe(mqtt_Subtopic);

//     } else {
//         failures++;
//         if (failures >= max_failures) panic(T.error_mqtt);
//     }
// }

// void MQTT_messageReceived(String &topic, String &payload) {
// // callback function for incomming (subscribed messages)
//   Serial.println("incoming on topic: " + topic + " payload: " + payload);
//   display_Incoming_topic(topic, payload);
//  }


// // ***********************************************************************************************

// void flush(Stream& s, int limit = 20) {
//     // .available() sometimes stays true (why?), hence the limit

//     s.flush();  // flush output
//     while(s.available() && --limit) s.read();  // flush input
// }


// // ******************* SetUp ************************************** SetUp ************************************* SetUp *******************

// void setup() {
//     Serial.begin(115200);
//     Serial.println("MQTTGo v2 start");

//     display_init();

//     MQTTLanguage::select(T, LANGUAGE);

//     if (!SPIFFS.begin(false)) {
//         display_lines(T.first_run, TFT_MAGENTA);
//         if (!SPIFFS.format()) {
//             display_big(T.error_format, TFT_RED);
//             delay(20*1000);
//         }
//     }

//     pinMode(pin_portalbutton,   INPUT_PULLUP);
//     pinMode(pin_demobutton,     INPUT_PULLUP);
//     pinMode(pin_backlight,      OUTPUT);

//     WiFiSettings.hostname = "HiveMQ-";
//     WiFiSettings.language = LANGUAGE;
//     WiFiSettings.begin();
//     MQTTLanguage::select(T, WiFiSettings.language);

//     Serial.println("MQTTGo v2 Display logo");
//     display_logo();
//     delay(2000);

//     for (auto& str : T.portal_instructions[0]) {
//         str.replace("{ssid}", WiFiSettings.hostname);
//     }

//     wifi_enabled  = WiFiSettings.checkbox("MQTTGo_wifi", true, T.config_wifi);
    
//     WiFiSettings.heading("MQTT");
//     mqtt_enabled  = WiFiSettings.checkbox("HiveMQ_mqtt", true, T.config_mqtt) && wifi_enabled;
//     String server = WiFiSettings.string("mqtt_server", 64, "broker.hivemq.com", T.config_mqtt_server);
//     int port      = WiFiSettings.integer("mqtt_port", 0, 65535, 1883, T.config_mqtt_port);
//     max_failures  = WiFiSettings.integer("HiveMQ_max_failures", 0, 1000, 10, T.config_max_failures);
//     mqtt_Pubtopic = WiFiSettings.string("HiveMQ_mqtt_topic", "HiveMQ/"+WiFiSettings.hostname, T.config_mqtt_topic);
//     mqtt_Subtopic  = WiFiSettings.string("HiveMQ_Submqtt_topic", "HiveMQ/SubTopic", T.config_Submqtt_topic); 
//     mqtt_interval = 1000UL * WiFiSettings.integer("HiveMQ_mqtt_interval", 10, 3600, 30, T.config_mqtt_interval);
//     mqtt_template = WiFiSettings.string("HiveMQ_mqtt_template", "Payload : {}", T.config_mqtt_template);
//     WiFiSettings.info(T.config_template_info);


//     Serial.println("*** Setting overview ***");
//     Serial.print("mqtt_Pubtopic: ");
//     Serial.println(mqtt_Pubtopic);
//     Serial.print("mqtt_Subtopic: ");
//     Serial.println(mqtt_Subtopic);
//     Serial.print("mqtt_template/payload: ");
//     Serial.println(mqtt_template);
//     Serial.print("PlatformIO Unix compile time: ");
//     Serial.println(COMPILE_UNIX_TIME);
//     Serial.println("*** ****** *******  ***");
    

//     WiFiSettings.onConnect = [] {
//         display_big(T.connecting, TFT_BLUE);
//         check_portalbutton();
//         return 50;
//     };
//     WiFiSettings.onFailure = [] {
//         display_big(T.error_wifi, TFT_RED);
//         delay(2000);
//     };
//     static int portal_phase = 0;
//     static unsigned long portal_start;
//     WiFiSettings.onPortal = [] {
//         portal_start = millis();
//     };
//     WiFiSettings.onPortalView = [] {
//         if (portal_phase < 2) portal_phase = 2;
//     };
//     WiFiSettings.onConfigSaved = [] {
//         portal_phase = 3;
//     };
//     WiFiSettings.onPortalWaitLoop = [] {
//         if (WiFi.softAPgetStationNum() == 0) portal_phase = 0;
//         else if (! portal_phase) portal_phase = 1;

//         display_lines(T.portal_instructions[portal_phase], TFT_WHITE, TFT_BLUE);

//         if (portal_phase == 0 && millis() - portal_start > 10*60*1000) {
//             panic(T.error_timeout);
//         }

//         // if (ota_enabled) ArduinoOTA.handle();
//         if (button(pin_portalbutton)) ESP.restart();
//     };

//     if (wifi_enabled) WiFiSettings.connect(false, 15);

//     mqtt_enabled = true;
//     static WiFiClient wificlient;
//     if (mqtt_enabled) {
//         mqtt.begin(server.c_str(), port, wificlient);
//         mqtt.onMessage(MQTT_messageReceived);
//     }
    
//     Serial.println("Ready .... ");
    
//     mqtt.loop();
//     connect_mqtt();
//     MQTTretain(mqtt_Pubtopic, "Initial message from "+WiFiSettings.hostname); 
// }


// // ******************* Loop ************************************** Loop ************************************** Loop *******************

// #define every(t) for (static unsigned long _lasttime; (unsigned long)((unsigned long)millis() - _lasttime) >= (t); _lasttime = millis())

// void loop() {
    
//     every(mqtt_interval) {

//         MQTTretain(mqtt_Pubtopic, WiFiSettings.hostname+ " is alive ");
//         Serial.printf("MQTTGo v2 MQTT %s Still alive messages send\n",WiFiSettings.hostname );
//     }

//     if (mqtt_enabled && button(pin_demobutton)) {
//         mqtt_template.replace("{}", WiFiSettings.hostname);
//         Serial.printf("MQTTGo v2 MQTT enabled and Button press detected, pubbing : %s now..\n",mqtt_template);
//         display_big("Btn press"); // Show keypress on Oled
//         delay(1000);
//         MQTTretain(mqtt_Pubtopic, mqtt_template);  // Pub the MQTT message with retain flag 
//         delay(2000);

//         //   str.replace("{ssid}", WiFiSettings.hostname);
//     }

//     if (button(pin_portalbutton)) { // check if upper btn is pressed and invoke Wifi settings portal
//         WiFiSettings.portal();
//     }
  
// }   //loop