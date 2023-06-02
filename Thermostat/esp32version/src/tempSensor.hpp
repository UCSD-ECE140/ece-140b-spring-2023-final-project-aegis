#include "DHTesp.h" // Click here to get the library: http://librarymanager/All#DHTesp


class tempSensor{
    DHTesp dht;
    /** Pin number for DHT11 data pin */
    int dhtPin;


    public:
    /**
     * @brief Construct a new temp Sensor object
     * 
     * @param dhtPin 
     */
    tempSensor(int dhtPin = 14){
        this->dhtPin = dhtPin;
    }
    /**
     * initTemp
     * Setup DHT library
     * Setup task and timer for repeated measurement
     * @return bool
     *    true if task and timer are started
     *    false if task or timer couldn't be started
     */
    bool initTemp() {
        dht.setup(dhtPin, DHTesp::DHT11);
        return true;
    }

    /**
     * getTemperature
     * Reads temperature from DHT11 sensor
     * @return bool
     *    true if temperature could be aquired
     *    false if aquisition failed
    */
    // bool printTemperature() {
    //     // Reading temperature for humidity takes about 250 milliseconds!
    //     // Sensor readings may also be up to 2 seconds 'old' (it's a very slow sensor)
    //     TempAndHumidity newValues = dht.getTempAndHumidity();

    //     if (dht.getStatus() != 0) {
    //         com.sendMessage("DHT11 error status: " + String(dht.getStatusString()));
    //         return false;
    //     }
    //     com.sendMessage(" T:" + String(newValues.temperature) + " H:" + String(newValues.humidity));
    //     return true;
    // }
    
    /** getTemperature
     Reads temperature from DHT11 sensor
     returns comma separated data as a string
    */
    String getTemperature() {
        TempAndHumidity newValues = dht.getTempAndHumidity();
        if (dht.getStatus() != 0) {
            return "DHT11 error status: " + String(dht.getStatusString());
        }
        return String(newValues.temperature) + "," + String(newValues.humidity);
    }

};