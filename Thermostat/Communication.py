import serial
from time import sleep

"""
A class to handle Serial communication between Python and the MCU
"""
class Communication:
    '''
    Encapsulated class attributes (with default values)
    '''
    __serial_name = ""
    __baud_rate = 115200
    __ser = None

    '''
    Initialize the class instance
    '''
    def __init__(self, serial_name=None, baud_rate=None):
        self.__serial_name = serial_name
        self.__baud_rate = baud_rate
        if(serial_name != None and baud_rate != None):
            self.setup()

    '''
    Setup the Serial connection
    '''
    def setup(self):
        self.__ser = serial.Serial(self.__serial_name, self.__baud_rate)

    '''
    Close Serial connection. Wait 0.5s to allow commands to finish executing.
    '''
    def close(self):
        sleep(0.5)
        self.__ser.close()

    '''
    Send a message to Serial (always terminated by a newline character)
    '''
    def send_message(self, message):
        if(message[-1] != '\n'):
            message = message + '\n'
        self.__ser.write(message.encode('utf-8'))

    '''
    Receive a message from Serial and limit it to num_bytes (default of 50)
    Note:
      At 50Hz sampling and baud rate of 115200, the limit is 288 bytes/sample
      115200 b/s == 14400 B/s == (14400 B/s)/(50 s/sample) = 288 bytes/sample
    '''
    def receive_message(self, num_bytes=50):
        if(self.__ser.in_waiting > 0):
            return self.__ser.readline(num_bytes).decode('utf-8')
        else:
            return None

    '''
    Clear the data buffer in case it is necessary to eliminate junk data
    '''
    def clear(self):
        self.__ser.reset_input_buffer()