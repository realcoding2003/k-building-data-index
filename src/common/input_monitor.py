import sys
import select
import time
import threading


class InputMonitor:
    def __init__(self, stop_event, processing_completed_event):
        self.stop_event = stop_event
        self.processing_completed_event = processing_completed_event

    @staticmethod
    def input_available():
        return select.select([sys.stdin, ], [], [], 0.0)[0]

    def monitor_input(self):
        print("엔터키를 누르면 프로그램이 종료됩니다. (처리 완료 시 자동 종료)")
        while not self.processing_completed_event.is_set():
            if self.stop_event.is_set():
                break
            if self.input_available():
                user_input = input()
                if user_input.strip() == "":
                    print("프로그램을 종료중입니다.\n")
                    self.stop_event.set()
                    break
            time.sleep(0.1)  # 0.1초마다 확인

        if self.processing_completed_event.is_set():
            print("모든 처리가 완료되었습니다. 프로그램을 종료합니다.")


def start_input_monitor(stop_event, processing_completed_event):
    monitor = InputMonitor(stop_event, processing_completed_event)
    input_thread = threading.Thread(target=monitor.monitor_input)
    input_thread.start()
    return input_thread
