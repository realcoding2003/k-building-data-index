from src.data_collector_building import collect_building_data
from src.common import log_scripts as log
from src.common.state import STOP_EVENT
import threading
import time


def monitor_input():
    print("엔터키를 누르면 프로그램이 종료됩니다.")
    while not STOP_EVENT.is_set():
        if input().strip() == "":
            print("프로그램을 종료중입니다.")
            STOP_EVENT.set()
            break
        time.sleep(0.1)


def main():
    input_thread = threading.Thread(target=monitor_input)
    input_thread.start()

    try:
        collect_building_data()
    except Exception as e:
        log.error(f"Error in main execution: {e}")
    finally:
        STOP_EVENT.set()
        input_thread.join()


if __name__ == "__main__":
    main()
