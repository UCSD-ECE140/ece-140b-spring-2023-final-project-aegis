import bluetooth

bluetooth_address = "70:B8:F6:5B:61:BA"
port = 1

socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
socket.connect((bluetooth_address, port))

try:
    while True:
        data = socket.recv(1024)
        print("Received:", data)

        socket.send(b"data to send\n")

except Exception as e:
    print(e)
    socket.close()
finally:
    socket.close()
