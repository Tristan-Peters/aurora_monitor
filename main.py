import numpy as np
import cv2
import scrapy
import requests
import time
import datetime

url = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"

kp_alarm = 3


def json_sort_time(x):
    return x["time_tag"]


def kpi_logger():
    while True:
        response = requests.get(url)

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


def main():
    with open("kp_log.log", 'w') as f:
        f.write(str(datetime.datetime.now()))
        f.write('\n')



if __name__ == "__main__":
    main()
