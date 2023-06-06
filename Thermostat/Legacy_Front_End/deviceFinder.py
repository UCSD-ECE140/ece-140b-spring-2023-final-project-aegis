import bluetooth

def find_device(target_name):
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    for addr, name in nearby_devices:
        if target_name.lower() == name.lower():
            return addr
    return None

target_device_name = "AegisDongle-A73E"
target_device_address = find_device(target_device_name)

if target_device_address is not None:
    print(f"Found {target_device_name} with address {target_device_address}")
else:
    print(f"{target_device_name} not found. Please check if the device is powered on and discoverable.")
