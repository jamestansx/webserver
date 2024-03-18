import esp32
import json
import lib.urequests as requests
import lib.base64 as base64
import lib.logging as logging
import time
import utime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


LOGIN_URL = "http://192.168.43.74:8080/api/user/login"
POST_URL = "http://192.168.43.74:8080/api/device/esp32/data"
REFRESH_INTERVAL = 5  # second

logger.info("__main__ started")
logger.info(f"Login url: {LOGIN_URL}")
logger.info(f"Post device data url: {POST_URL}")


class AuthLoginError(Exception):
    ...


def read_sensor() -> dict:
    val = esp32.hall_sensor()
    logger.info(f"Hall sensor value: {val}")
    return dict(val=val)


def _post(post_data: dict, token: str) -> bool:
    auth = f"Bearer {token}"
    headers = {"Authorization": auth, "Content-Type": "application/json"}
    t = utime.mktime(time.localtime())
    t += 8 * 3600
    Y, m, d, H, M, S, *_ = utime.localtime(t)
    time_now = f"{d}/{m}/{Y},{H}:{M}:{S}"
    data = dict(data=post_data, time_collected=time_now)
    logger.info(f"Posting data: {data}")
    res = requests.post(POST_URL, data=json.dumps(data), headers=headers)
    if res.status_code == 200:
        logger.info("Posted successfully")
        return True
    else:
        logger.error(f"Posting failed (status code: {res.status_code})")
        return False


def _login(username: str, passwd: str) -> str | None:
    auth = f"{username}:{passwd}"
    logger.info(f"Logging in user:{username}")
    encoded_auth = base64.b64encode(auth.encode()).decode()
    auth = f"Basic {encoded_auth}"
    headers = dict(Authorization=auth)
    res = requests.get(LOGIN_URL, headers=headers)
    if res.status_code == 200:
        return res.json()["token"]
    elif res.status_code == 401:
        return None


def main():
    username = "jamestansx"
    passwd = "1234"
    token = _login(username, passwd)
    if token is None:
        logger.critical(f"User {username} failed to login")
        raise AuthLoginError("Login failed")
    logger.info("Login Success")
    failed_ = 0
    while True:
        if failed_ > 3:
            logger.critical("POST failed too many times")
            failed_ = 0
            break
        if not _post(read_sensor(), token):
            failed_ += 1
        time.sleep(REFRESH_INTERVAL)

main()
