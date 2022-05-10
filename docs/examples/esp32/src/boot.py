# This file is executed on every boot (including wake-boot from deepsleep)
from machine import I2C, Pin
import network
import time
import socket
import gc
import esp

esp.osdebug(None)

gc.collect()

ssid = "jamestansx"
passwd = "usingjames"


def setup_connect(ssid, pwd):
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print("Connecting to network...")
        wlan.active(True)
        wlan.connect(ssid, passwd)
        while not wlan.isconnected():
            pass
    print("Netork configuration:\n", wlan.ifconfig())


def sync_time():
    import ntptime
    import time

    try:
        print("Local time before synchronization：%s" % str(time.localtime()))
        # make sure to have internet connection
        ntptime.settime()
        print("Local time after synchronization：%s" % str(time.localtime()))
    except:
        print("Error syncing time")


setup_connect(ssid, passwd)
sync_time()
