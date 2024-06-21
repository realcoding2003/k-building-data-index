import os
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from data_processor import process_data
from tqdm import tqdm

# 최대 동시 실행 쓰레드 개수
MAX_THREADS = 10


def thread_function(sigungu_cd, bjdong_cd):
    """쓰레드에서 실행할 함수"""
    processed_data = process_data(sigungu_cd, bjdong_cd)

    # 처리한 파일에 대한 내용 출력
    if processed_data:
        log_message = f"Processed {len(processed_data)} records for {sigungu_cd}-{bjdong_cd}"

    # tqdm.write(log_message, end='\r')  # 로그 메시지 출력
    return True


def main():
    # 필요한 폴더 생성
    os.makedirs("data", exist_ok=True)

    # JSON 파일에서 모든 시군구 코드와 법정동 코드 읽기
    with open("config/addr_code.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    tasks = []

    # 모든 시군구 코드와 법정동 코드에 대해 쓰레드 생성 및 실행
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        with tqdm(total=len(data), desc="데이터 수집중") as pbar:
            for key, value in data.items():
                sigungu_cd = value[:5]
                bjdong_cd = value[5:]

                if bjdong_cd == "00000":
                    pbar.update(1)
                    continue

                tasks.append(executor.submit(thread_function, sigungu_cd, bjdong_cd))

            for future in as_completed(tasks):
                future.result()  # get the result to raise exceptions if any
                pbar.update(1)


if __name__ == "__main__":
    main()
