print("__main__ started")

import esp32
import lib.urequests as requests
import ubinascii
import json
import time
import utime

LOGIN_URL = "http://192.168.43.74:5000/api/user/login"
POST_URL = "http://192.168.43.74:5000/api/device/esp32/data"
REFRESH_INTERVAL = 5 #second

def read_sensor() -> dict:
    return dict(val=esp32.hall_sensor())

def _post(post_data: dict, token: str) -> bool:
    auth = f"Bearer {token}"
    headers = {"Authorization":auth, "Content-Type":"application/json"}
    t = utime.mktime(time.localtime())
    t += 8 * 3600
    Y, m, d, H, M, S, *_ = utime.localtime(t)
    time_now = f"{d}/{m}/{Y},{H}:{M}:{S}"
    data = dict(data=post_data, time_collected=time_now) 
    res = requests.post(POST_URL, data=json.dumps(data), headers=headers)
    return True

def _login(username: str, passwd: str) -> str:
    auth = f"{username}:{passwd}"
    encoded_auth = ubinascii.b2a_base64(auth.encode()).decode()
    auth = f"Basic {encoded_auth}"
    headers = dict(Authorization=auth)
    res = requests.get(LOGIN_URL,headers=headers )
    return res.json()["token"]


def main():
    token = _login("jamestansx", "1234")
    while True:
        _post(read_sensor(), token)
        time.sleep(REFRESH_INTERVAL)

main()
