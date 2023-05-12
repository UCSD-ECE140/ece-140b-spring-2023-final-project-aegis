import bluetooth

# Replace 'XX:XX:XX:XX:XX:XX' with the MAC address of your ESP32 device.
bt_addr = "B8:D6:1A:0E:54:82"
port = 1  # Replace with the desired port number.

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bt_addr, port))

try:
    while True:
        # Read data from the Bluetooth device.
        data = sock.recv(1024)
        print("Received:", data)

        # Write data to the Bluetooth device.
        sock.send(b"data to send\n")

finally:
    sock.close()