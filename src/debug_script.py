from bt_client import BTClient
from wifi_client import WifiClient
from rfsg_client import RfsgClient

ip_addr = "169.254.54.113"
rf_port = 1
bt = None
wifi = None
rfsg = None
try:
    bt = BTClient(ip_addr, rf_port)
    wifi = WifiClient(ip_addr, rf_port)
    rfsg = RfsgClient(ip_addr, rf_port)
    bt.open()
    bt.reset()
    wifi.open()
    wifi.reset()
    rfsg.open()
    rfsg.reset()
    print(f"bluetooth state is {bt.get_measurement_state()}")
    print(f"wifi state is {wifi.get_measurement_state()}")
    print(f"rfsg is {rfsg.is_generating()}")
    print(f"rfsg waveforms {rfsg.get_waveforms_folder()}")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if bt is not None:
        bt.disconnect()
    if wifi is not None:
        wifi.disconnect()
    if rfsg is not None:
        rfsg.disconnect()
