from bt_client import BTClient
from wifi_client import WifiClient

ip_addr = "169.254.54.113"
rf_port = 1
bt = None
wifi = None
try:
    bt = BTClient(ip_addr, rf_port)
    wifi = WifiClient(ip_addr, rf_port)
    bt.open()
    bt.reset()
    wifi.open()
    wifi.reset()
    print(f"bluetooth state is {bt.get_measurement_state()}")
    print(f"wifi state is {wifi.get_measurement_state()}")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if bt is not None:
        bt.disconnect()
    if wifi is not None:
        wifi.disconnect()
