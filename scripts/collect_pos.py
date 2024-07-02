import os
import threading
from tqdm import tqdm
from src.data_collector_pos import process_file, APILimitExceeded
from src.common import start_input_monitor, log_scripts as log
from src.common.state import STOP_EVENT, MAX_THREADS, DATA_BUILDING_MERGED_FOLDER, DATA_BUILDING_POS_FOLDER

# 세마포어 설정
semaphore = threading.Semaphore(MAX_THREADS)

processing_completed = threading.Event()


def thread_function(filename):
    """스레드에서 실행할 함수"""
    if STOP_EVENT.is_set():
        return False

    try:
        processed_data = process_file(filename)
        if processed_data:
            log.info(f"{filename}: 처리 완료")
        return True
    except APILimitExceeded:
        log.warning("API 호출 한도 초과. 프로세스를 중단합니다.")
        return False
    except Exception as e:
        log.error(f"예외 발생: {filename}: {e}")
        return False
    finally:
        semaphore.release()


def main():
    if not os.path.exists(DATA_BUILDING_POS_FOLDER):
        os.makedirs(DATA_BUILDING_POS_FOLDER)

    files = [f for f in os.listdir(DATA_BUILDING_MERGED_FOLDER) if f.endswith('.json')]
    threads = []

    input_thread = start_input_monitor(STOP_EVENT, processing_completed)

    with tqdm(total=len(files), desc="위치 정보 수집 중", ncols=100) as pbar:
        for filename in files:
            if STOP_EVENT.is_set():
                break

            output_path = os.path.join(DATA_BUILDING_POS_FOLDER, filename)
            if os.path.exists(output_path):
                pbar.update(1)
                continue

            semaphore.acquire()

            thread = threading.Thread(target=thread_function, args=(filename,))
            threads.append(thread)
            thread.start()

            pbar.update(1)

        for thread in threads:
            thread.join()

    processing_completed.set()
    input_thread.join()


if __name__ == "__main__":
    main()
