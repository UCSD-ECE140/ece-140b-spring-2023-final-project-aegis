import serial
import time


def setup(serial_name, baud_rate):
    ser = serial.Serial(serial_name, baud_rate)
    return ser

def close(ser):
    ser.close()

def send_message(ser, message):
    if(message[-1] != '\n'):
        message = message + '\n'
    ser.write(message.encode('utf-8'))

def receive_message(ser, num_bytes=50):
    if(ser.in_waiting > 0):
        return ser.readline(num_bytes).decode('utf-8')
    else:
        return None


def main():
    # wired is /dev/cu.usbserial-02761644
    ser = setup("/dev/cu.AegisDongle", 115200)
    while(True):
        time.sleep(3)
        message = receive_message(ser)
        print(message)
    close(ser)


"""
Main entrypoint for the application
"""
if __name__== "__main__":
    main()
