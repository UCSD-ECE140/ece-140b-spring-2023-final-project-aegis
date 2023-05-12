#include "DHTesp.h" // Click here to get the library: http://librarymanager/All#DHTesp
#include "communications.hpp" // Click here to get the library:


class tempSensor{
    DHTesp dht;
    /** Pin number for DHT11 data pin */
    int dhtPin;
    communication& com;

    public:
    /**
     * @brief Construct a new temp Sensor object
     * 
     * @param dhtPin 
     */
    tempSensor(communication& aCom, int dhtPin = 14): com(aCom){
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
        com.sendMessage("DHT11 setup done");
        return true;
    }

    /**
     * getTemperature
     * Reads temperature from DHT11 sensor
     * @return bool
     *    true if temperature could be aquired
     *    false if aquisition failed
    */
    bool printTemperature() {
        // Reading temperature for humidity takes about 250 milliseconds!
        // Sensor readings may also be up to 2 seconds 'old' (it's a very slow sensor)
        TempAndHumidity newValues = dht.getTempAndHumidity();

        if (dht.getStatus() != 0) {
            com.sendMessage("DHT11 error status: " + String(dht.getStatusString()));
            return false;
        }
        com.sendMessage(" T:" + String(newValues.temperature) + " H:" + String(newValues.humidity));
        return true;
    }
};