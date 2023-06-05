#include "currentSensor.hpp"
#include "communications.hpp"
#include "tempSensor.hpp"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

// Declare any global variables or objects
CurrentSensor currentSensor;
Communication communication;
TempSensor tempSensor;

// Task function
void taskFunction(void *parameter) {
  while (1) {
    // Main program logic
    float current = currentSensor.readCurrent();
    float temperature = tempSensor.readTemperature();

    communication.sendData(current, temperature);

    // Use FreeRTOS vTaskDelay() instead of delay()
    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}

void app_main() {
    // Initialize hardware and libraries
  currentSensor.begin();
  communication.begin();
  tempSensor.begin();

  // Create a FreeRTOS task
  xTaskCreate(taskFunction, "mainTask", 4096, NULL, 1, NULL);

  while(1){};
}