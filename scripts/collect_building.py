import json
import os
import threading

from tqdm import tqdm

from src.common import start_input_monitor
from src.common.state import STOP_EVENT, MAX_THREADS, DATA_BUNJI_FOLDER, DATA_BUILDING_FOLDER
from src.data_collector_building import collect_and_save_building_data

# 세마포어 생성
semaphore = threading.Semaphore(MAX_THREADS)
processing_completed = threading.Event()


def is_apartment(building_data):
    bld_nm = str(building_data.get("건물명", ""))
    etc_purps = str(building_data.get("보조용도", ""))
    main_purps_cd_nm = str(building_data.get("주용도코드명", ""))

    return (
            "아파트" in bld_nm
            or "더샵" in bld_nm
            or "힐스테이트" in bld_nm
            or "아파트" in etc_purps
            or "아파트" in main_purps_cd_nm
    )


def collect_building_codes():
    building_codes = []

    for file_name in os.listdir(DATA_BUNJI_FOLDER):
        if file_name.endswith('.json'):
            file_path = os.path.join(DATA_BUNJI_FOLDER, file_name)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for key, value in data.items():
                if not is_apartment(value):
                    sigungu_cd, bjdong_cd, bun, ji = key.split('-')
                    building_codes.append((sigungu_cd, bjdong_cd, bun, ji))

    return building_codes


def process_building(building_code, pbar):
    try:
        sigungu_cd, bjdong_cd, bun, ji = building_code
        collect_and_save_building_data(sigungu_cd, bjdong_cd, bun, ji)
    finally:
        pbar.update(1)
        # 세마포어 해제
        semaphore.release()


def collect_all_buildings():
    if not os.path.exists(DATA_BUILDING_FOLDER):
        os.makedirs(DATA_BUILDING_FOLDER)

    building_codes = collect_building_codes()

    threads = []

    # tqdm을 사용하여 진행률 표시줄 생성
    with tqdm(total=len(building_codes), desc="Collecting building data", ncols=100) as pbar:
        for building_code in building_codes:
            # 프로그램 종료 중인지 체크
            if STOP_EVENT.is_set():
                break

            sigungu_cd, bjdong_cd, bun, ji = building_code

            # 이미 존재하는 JSON 파일이 있는지 확인
            if os.path.exists(f"{DATA_BUILDING_FOLDER}/{sigungu_cd}-{bjdong_cd}-{bun}-{ji}.json"):
                pbar.update(1)
                continue

            # 세마포어 획득
            semaphore.acquire()

            # 새로운 쓰레드 생성 및 시작
            thread = threading.Thread(target=process_building, args=(building_code, pbar))
            threads.append(thread)
            thread.start()

        # 모든 쓰레드가 종료될 때까지 대기
        for thread in threads:
            thread.join()

    processing_completed.set()


def main():
    input_thread = start_input_monitor(STOP_EVENT, processing_completed)

    try:
        collect_all_buildings()
    finally:
        input_thread.join()
        STOP_EVENT.set()


if __name__ == "__main__":
    main()
