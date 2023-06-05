/**********************************************************************
* Filename    : I2CLCD1602.c
* Description : Use the LCD display data
* Author      : www.freenove.com
* modification: 2020/07/23
**********************************************************************/
#include <stdlib.h>
#include <stdio.h>
#include <wiringPi.h>
#include <wiringPiI2C.h>
#include <pcf8574.h>
#include "../Freenove_Kit/Code/C_Code/21.1.1_DHT11/DHT.hpp"
#include "../Freenove_Kit/Code/C_Code/10.1.1_Nightlamp/Nightlamp.cpp"
#include <lcd.h>
#include <time.h>
#include "mysql_connection.h"

#include <cppconn/driver.h>
#include <cppconn/exception.h>
#include <cppconn/resultset.h>
#include <cppconn/statement.h>


#define ledPin 0
#define DHT11_Pin  0		//define the pin of sensor
DHT dht;			//create a DHT class object
int chk, counts;		//chk:read the return value of sensor; sumCnt:times of reading sensor

int value =0;
float humidity =0.0;
float temperature =0.0;
ADCDevice *adc;  // Define an ADC Device class object

int pcf8574_address = 0x27;        // PCF8574T:0x27, PCF8574AT:0x3F
#define BASE 64         // BASE any number above 64
//Define the output pins of the PCF8574, which are directly connected to the LCD1602 pin.
#define RS      BASE+0
#define RW      BASE+1
#define EN      BASE+2
#define LED     BASE+3
#define D4      BASE+4
#define D5      BASE+5
#define D6      BASE+6
#define D7      BASE+7

int lcdhd;// used to handle LCD
void printCPUTemperature(){// sub function used to print CPU temperature
    FILE *fp;
    char str_temp[15];
    float CPU_temp;
    // CPU temperature data is stored in this directory.
    fp=fopen("/sys/class/thermal/thermal_zone0/temp","r");
    fgets(str_temp,15,fp);      // read file temp
    CPU_temp = atof(str_temp)/1000.0;   // convert to Celsius degrees
    printf("CPU's temperature : %.2f \n",CPU_temp);
    lcdPosition(lcdhd,0,0);     // set the LCD cursor position to (0,0) 
    lcdPrintf(lcdhd,"T:%.2fC, H:%.2f%",temperature,humidity);// Display CPU temperature on LCD
    fclose(fp);
}
void printDataTime(){//used to print system time 
    time_t rawtime;
    struct tm *timeinfo;
    time(&rawtime);// get system time
    timeinfo = localtime(&rawtime);//convert to local time
    printf("%s \n",asctime(timeinfo));
    lcdPosition(lcdhd,0,1);// set the LCD cursor position to (0,1) 
    lcdPrintf(lcdhd,"%02d:%02d B:%d",timeinfo->tm_hour,timeinfo->tm_min,value); //Display system time on LCD
}
void printOutLight(){
    int raw = adc->analogRead(0);  //read analog value of A0 pin
    softPwmWrite(ledPin,value*100/255);
    float voltage = (float)value / 255.0 * 3.3;  // calculate voltage
    if(raw>30) value = 1;
    else if(raw>20) value = 2;
    else value =3;
    printf("ADC value : %d  ,\tVoltage : %.2fV\n",value,voltage);
}
void printOutTemperature(){
    counts++; //counting number of reading times
    printf("Measurement counts : %d \n", counts);
    for (int i = 0; i < 15; i++){
        chk = dht.readDHT11(DHT11_Pin);	//read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
        if(chk == DHTLIB_OK){
            printf("DHT11,OK! \n");
            break;
        }
        delay(100);
    }
    temperature = dht.temperature;
    humidity = dht.humidity;
    printf("Humidity is %.2f %%, \t Temperature is %.2f *C\n\n",humidity, temperature);
    

}
int detectI2C(int addr){
    int _fd = wiringPiI2CSetup (addr);   
    if (_fd < 0){		
        printf("Error address : 0x%x \n",addr);
        return 0 ;
    } 
    else{	
        if(wiringPiI2CWrite(_fd,0) < 0){
            printf("Not found device in address 0x%x \n",addr);
            return 0;
        }
        else{
            printf("Found device in address 0x%x \n",addr);
            return 1 ;
        }
    }
}
int saveToDatabase(){
	try {
  sql::Driver *driver;
  sql::Connection *con;
  sql::Statement *stmt;
  sql::ResultSet *res;

  /* Create a connection */
  driver = get_driver_instance();
  con = driver->connect("tcp://127.0.0.1:3306", "root", "ROOT");
  /* Connect to the MySQL test database */
  con->setSchema("weather");

  stmt = con->createStatement();
  std::string theStatement;
  theStatement+="insert into weather_updates";
  theStatement+="(temp,hum,bright)";
  theStatement+="values(";
  theStatement+=std::to_string(temperature);
  theStatement+=",";
  theStatement+=std::to_string(humidity);
  theStatement+=",";
  theStatement+=std::to_string(value);
  theStatement+=");";
  std::cout<<theStatement;
  res = stmt->executeQuery(theStatement);
  while (res->next()) {
	  std::cout << "\t... MySQL replies: ";
    /* Access column data by alias or column name */
	  std::cout << res->getString("_message") << std::endl;
	  std::cout << "\t... MySQL says it again: ";
    /* Access column data by numeric offset, 1 is the first column */
	  std::cout << res->getString(1) << std::endl;
  }
  delete res;
  delete stmt;
  delete con;

} catch (sql::SQLException &e) {
	std::cout << "# ERR: SQLException in " << __FILE__;
	std::cout << "(" << __FUNCTION__ << ") on line " 
     << __LINE__ << std::endl;
	std::cout << "# ERR: " << e.what();
	std::cout << " (MySQL error code: " << e.getErrorCode();
	std::cout << ", SQLState: " << e.getSQLState() << " )" << std::endl;
}
}
int main(void){
    int i;
    adc = new ADCDevice();
    printf("Program is starting ...\n");

    //4b is adc
    //27 is display
    pcf8574_address = 0x27;     //set led address
    delete adc;               // Free previously pointed memory for dht
    adc = new ADS7830();      // If detected, create an instance of ADS7830. dht

    wiringPiSetup();    //dht
    pcf8574Setup(BASE,pcf8574_address);//initialize PCF8574
    softPwmCreate(ledPin,0,100);
    for(i=0;i<8;i++){
        pinMode(BASE+i,OUTPUT);     //set PCF8574 port to output mode
    } 
    digitalWrite(LED,HIGH);     //turn on LCD backlight
    digitalWrite(RW,LOW);       //allow writing to LCD
	lcdhd = lcdInit(2,16,4,RS,EN,D4,D5,D6,D7,0,0,0,0);// initialize LCD and return “handle” used to handle LCD
    if(lcdhd == -1){
        printf("lcdInit failed !");
        return 1;
    }
    long lastSave = 0;
    while(1){
        printOutTemperature();
        printOutLight();
        printCPUTemperature();//print CPU temperature
        printDataTime();        // print system time
	saveToDatabase();
        delay(2000);
    }
    return 0;
}


