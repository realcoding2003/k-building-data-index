import os
import json
import threading
from data_processor import process_data
from tqdm import tqdm
import logging
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 최대 동시 실행 개수(환경 변수 읽기)
MAX_THREADS = int(os.getenv('MAX_THREADS'))
# 쓰레드 종료 이벤트
stop_event = threading.Event()
# 세마포어 설정
semaphore = threading.Semaphore(MAX_THREADS)

# 로그 설정
logging.basicConfig(filename='logs/processing.log', level=logging.INFO,
                    format='[%(asctime)s %(levelname)s] %(message)s')


def thread_function(sigungu_cd, bjdong_cd):
    """쓰레드에서 실행할 함수"""

    # 프로그램 종료중일 경우
    if stop_event.is_set():
        return False

    try:
        # 데이터 처리 함수 호출
        processed_data = process_data(sigungu_cd, bjdong_cd)

        # 처리된 데이터가 있으면 로그 출력
        if processed_data:
            logging.info(f"{sigungu_cd}-{bjdong_cd}: {len(processed_data)}개 레코드 처리완료")

        return True
    except Exception as e:
        # 예외 발생 시 로그 기록
        logging.error(f"예외 발생: {sigungu_cd}-{bjdong_cd}: {e}")
        return False
    finally:
        # 쓰레드 종료 시 세마포어 해제
        semaphore.release()


def monitor_input():
    """키보드 입력을 모니터링하여 엔터 키가 눌리면 stop_event를 설정"""
    input("엔터키를 누르면 프로그램이 종료됩니다.\n")
    print("프로그램을 종료중입니다.\n")
    stop_event.set()


def main():
    global stop_event

    # 필요한 폴더 생성
    os.makedirs("data", exist_ok=True)

    # JSON 파일에서 미리 정의된 모든 시군구 코드와 법정동 코드 읽기
    with open("config/address_code.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # 쓰레드 리스트 초기화
    threads = []

    # 사용자 입력을 모니터링할 쓰레드 생성 및 시작
    input_thread = threading.Thread(target=monitor_input)
    input_thread.start()

    # tqdm을 사용하여 진행률 표시줄 생성
    with tqdm(total=len(data), desc="데이터 수집중", ncols=150) as pbar:
        for key, value in data.items():
            # 프로그램 종료 중인지 체크
            if stop_event.is_set():
                break

            sigungu_cd = key[:5]
            bjdong_cd = key[5:]

            # 상위 코드(시도/구군) 무시 && 이미 존재하는 JSON 파일이 있는지 확인
            if bjdong_cd == "00000" or os.path.exists(f"data/{sigungu_cd}-{bjdong_cd}.json"):
                pbar.update(1)
                continue

            # 세마포어 획득
            semaphore.acquire()

            # 새로운 쓰레드 생성 및 시작
            thread = threading.Thread(target=thread_function, args=(sigungu_cd, bjdong_cd))
            threads.append(thread)
            thread.start()

            # 진행률 업데이트
            pbar.update(1)

        # 모든 쓰레드가 종료될 때까지 대기
        for thread in threads:
            thread.join()

    # 종료키 입력 쓰레드 대기
    input_thread.join()


if __name__ == "__main__":
    main()
