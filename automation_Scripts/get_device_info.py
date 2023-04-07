import mysql.connector
from jnpr.junos import Device

def connect_to_devices(devices):
    """
    Connect to a list of Juniper devices and return a list of connected devices.
    """
    connected_devices = []
    for device in devices:
        try:
            dev = Device(host=device['hostname'], user=device['username'], password=device['password'])
            dev.open()
            connected_devices.append(dev)
        except Exception as e:
            print(f"Error connecting to {device['hostname']}: {e}")
    return connected_devices

def get_device_serial(dev):
    """
    Get the serial number of a Juniper device.
    """
    return dev.facts['serialnumber']

def write_to_database(serials):
    """
    Write the serial numbers to a MySQL database.
    """
    db = mysql.connector.connect(host="localhost", user="username", password="password", database="mydatabase")
    cursor = db.cursor()
    for serial in serials:
        sql = "INSERT INTO devices (serial_number) VALUES (%s)"
        val = (serial,)
        cursor.execute(sql, val)
    db.commit()

if __name__ == "__main__":
    # List of Juniper devices to connect to
    devices = [
        {'hostname': 'device1.example.com', 'username': 'user1', 'password': 'password1'},
        {'hostname': 'device2.example.com', 'username': 'user2', 'password': 'password2'},
        {'hostname': 'device3.example.com', 'username': 'user3', 'password': 'password3'}
    ]

    # Connect to the devices
    connected_devices = connect_to_devices(devices)

    # Get the serial numbers of the devices
    serials = [get_device_serial(dev) for dev in connected_devices]

    # Write the serial numbers to the database
    write_to_database(serials)
