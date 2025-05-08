from moonrakerpy import MoonrakerPrinter
import requests
import time
from config import MOONRAKER_HOST

# Initialize the printer connection
printer = MoonrakerPrinter("http://172.20.10.6")

# List all available printer objects
while True:
    response = requests.get(f"{MOONRAKER_HOST}/printer/objects/query?motion_report")

    if response.status_code != 200:
        print("Error fetching status from Moonraker")
        time.sleep(0.2)

    status = response.json()
    motion_queue = status['result']['status']['motion_report']['live_velocity']
    print(motion_queue)
