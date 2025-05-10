import time
from voron.voron_controller import VoronController

def test_is_status_idle():
    controller = VoronController()
    query_times = []

    def custom_is_status_idle():
        while True:
            start_query = time.time()
            is_idle = controller.is_status_idle()
            end_query = time.time()
            query_times.append(end_query - start_query)
            if is_idle:
                return True

    start_time = time.time()
    is_idle = custom_is_status_idle()
    end_time = time.time()

    if is_idle:
        print(f"Printer is idle. Total response time: {end_time - start_time:.2f} seconds.")
        print("Query delays (seconds):", query_times)
    else:
        print("Printer is not idle or timeout occurred.")

if __name__ == "__main__":
    test_is_status_idle()
