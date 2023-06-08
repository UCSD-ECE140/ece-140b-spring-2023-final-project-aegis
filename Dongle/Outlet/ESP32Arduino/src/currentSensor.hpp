#include "EmonLib.h"                   // Include Emon Library

class currentSensor{
    int pin;
    double calibration;
    EnergyMonitor emon1;
    public:
        /**
         * @brief Construct a new current Sensor object
         * 
         * @param pin default is 33
         * @param calibration default is 0.5 at 66 ohm burden resistor
         */
        currentSensor(int pin=33, double calibration=0.7){
            this->pin = pin;
            this->calibration = calibration;
        }
        /**
         * @brief Set up the current sensor
         * 
         */
        void setupCurrentSensor(){
            emon1.current(pin, calibration);             // Current: input pin, calibration.
        }
        /**
         * @brief Get the Irms object
         * 
         * @return double 
         */
        double getIrms(){
            return emon1.calcIrms(1480);
        }
};