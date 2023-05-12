// same communications file as before used by bus side
//================================Communications================================
/*
 * Precompiler directive elegance: 0 == Serial, 1 == Bluetooth
 */
#include "BluetoothSerial.h"
#include "Arduino.h"



/**
 * @brief Class for communication
 * @cite Adapted from ECE16 communication architecture
 * @details This class is used to communicate with the ESP32 in a bluetooth or serial fashion more communication methods can be added
 */
class communication{
    bool isBT;
    String name;
    BluetoothSerial BTSerial;     // instantiate a BT object

    public:
    communication(){
        isBT = false;
        name = "AegisDongle-A72E";
    }
    communication(communication const&) = delete;
    /**
     * @brief Set up the communication object
     * 
     * @param isBT 
     * @param name 
     */
    void setupCommunication(bool isBT = false, String name = "AegisDongle-A72E"){
        this->isBT = isBT;
        if(isBT){
            this->name = name;
            BTSerial.begin(name.c_str());
        }
        else Serial.begin(115200);
    }

    /**
     * @brief Receive a message from the communication object
     * 
     * @return String 
     */
    String receiveMessage() {
        String message = "";
        if(isBT){
            if (BTSerial.available() > 0) {
                while (true) {
                    char c = BTSerial.read();
                    if (c != char(-1)) {
                        if (c == '\n')
                            break;
                        message += c;
                    }
                }
            }
        }
        else{
            if (Serial.available() > 0) {
                while (true) {
                    char c = Serial.read();
                    if (c != char(-1)) {
                        if (c == '\n')
                            break;
                        message += c;
                    }
                }
            }
        }
        return message;
    }

    /**
     * @brief Send a message to the communication object
     * 
     * @param message 
     */
    void sendMessage(String message) {
        if(isBT){
            BTSerial.println(message);
        }
        else{
            Serial.println(message);
        }
    }
};