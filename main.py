import threading
import numpy as np
import cv2
import scrapy
import requests
import time
import datetime
from playsound import playsound

kpi_url = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
kp_alarm = 1

forecast_url = "https://services.swpc.noaa.gov/images/animations/ovation/north/latest.jpg"

forecast_scrape = "https://auroraforecast.is/"


def json_sort_time(x):
    return x["time_tag"]


def kpi_logger():
    while True:
        response = requests.get(kpi_url)

        if response.status_code == 200:
            data = sorted(response.json(), key=json_sort_time, reverse=True)
            kp = max(data[0]['estimated_kp'], data[0]["kp_index"])
            if kp >= kp_alarm:
                with open("kp_log.log", 'a') as f:
                    f.write(str(data[0]))
                    f.write('\n')
        else:
            with open("kp_log.log", 'a') as f:
                f.write(f"Error: {response.status_code}")
                f.write('\n')

        time.sleep(30)


def forecast():
    while True:
        response = requests.get(forecast_url, stream=True)

        if response.status_code == 200:
            response_raw = response.raw
            image = np.asarray(bytearray(response_raw.read()), dtype=np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            focus = image[550:600, 310:350]


def alarm(duration=1):
    t_start = time.time() + duration
    while time.time() < t_start:
        t1 = threading.Thread(target=playsound, args=('./res/mixkit-morning-clock-alarm-1003.wav',))
        t1.daemon = True
        t1.start()
        t1.join()


def main():
    with open("kp_log.log", 'w') as f:
        f.write(str(datetime.datetime.now()))
        f.write('\n')




if __name__ == "__main__":
    main()
