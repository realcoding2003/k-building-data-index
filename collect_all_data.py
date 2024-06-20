import os
import json
import threading
from data_processor import process_data

# 최대 동시 실행 쓰레드 개수
MAX_THREADS = 10

# 세마포어 생성
semaphore = threading.Semaphore(MAX_THREADS)


def thread_function(sigungu_cd, bjdong_cd):
    """
    쓰레드에서 실행할 함수
    """
    with semaphore:
        # 처리완료 파일이 있으면 스킵
        if os.path.exists(f"data/bunji/complete/{sigungu_cd}-{bjdong_cd}.txt"):
            print(f"{sigungu_cd}-{bjdong_cd} 지역 데이터는 이미 처리되었습니다.")
            return

        processed_data = process_data(sigungu_cd, bjdong_cd)

        # 처리한 파일에 대한 내용 출력
        if processed_data:
            print(f"Processed {len(processed_data)} records for {sigungu_cd}-{bjdong_cd}")
        else:
            print(f"No records processed for {sigungu_cd}-{bjdong_cd}")


def main():
    # 필요한 폴더 생성
    os.makedirs("data/bunji", exist_ok=True)
    os.makedirs("data/bunji/complete", exist_ok=True)

    # JSON 파일에서 모든 시군구 코드와 법정동 코드 읽기
    with open("config/addr_code2.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    threads = []

    # 모든 시군구 코드와 법정동 코드에 대해 쓰레드 생성 및 실행
    for key, value in data.items():
        sigungu_cd = value[:5]
        bjdong_cd = value[5:]
        thread = threading.Thread(target=thread_function, args=(sigungu_cd, bjdong_cd))
        threads.append(thread)
        thread.start()

    # 모든 쓰레드가 종료될 때까지 대기
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
