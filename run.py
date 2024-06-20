import os
import json
import sys
import threading
from dotenv import load_dotenv

import requests
from requests.exceptions import Timeout

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수 읽기
SERVICE_KEY = os.getenv('SERVICE_KEY')
BASE_URL = os.getenv('BASE_URL')
NUM_OF_ROWS = os.getenv('NUM_OF_ROWS')
TYPE = os.getenv('TYPE')

# 최대 프로세스
MAX_THREAD = 8

# 스레드 동시 실행 제한을 위한 세마포어 설정
semaphore = threading.Semaphore(MAX_THREAD)


def process_data(sigungu_cd, bjdong_cd):
    """
    데이터 처리 함수
    :return:
    """
    base_url = (
        f"{BASE_URL}?serviceKey={SERVICE_KEY}"
        f"&sigunguCd=[sigunguCd]&bjdongCd=[bjdongCd]&numOfRows={NUM_OF_ROWS}&pageNo=[pageNo]&_type={TYPE}"
    )

    raw_data = {}
    semaphore.acquire()  # 세마포어 잠금
    page_no = 1

    try:
        while True:
            url = (
                base_url.replace("[sigunguCd]", sigungu_cd)
                .replace("[bjdongCd]", bjdong_cd)
                .replace("[pageNo]", str(page_no))
            )
            print(f"Processing {sigungu_cd}-{bjdong_cd} {page_no} page")

            response_data = call_api(url)

            # 페이지 넘어갔을 때 처리
            if response_data["response"]["body"]["items"] == "":
                break

            # 연립(다세대) 물건에 대한 법정동 코드 수집
            # 2000, 2002, 2003 = mainPurpsCd
            items = response_data["response"]["body"]["items"]
            if items != "":
                # items["item"]이 사전인지 확인
                if isinstance(items["item"], dict):
                    items["item"] = [items["item"]]

                # item 처리
                for item in items["item"]:
                    main_purps_cd = str(item["mainPurpsCd"]).strip()
                    if main_purps_cd in [
                        "02000",
                        "02002",
                        "02003",
                    ]:
                        # raw_data에 저장
                        # 기존 데이터가 있으면 bldNm이 있는 데이터를 우선으로 함
                        insert_key = (
                            f"{sigungu_cd}-{bjdong_cd}-{item['bun']}-{item['ji']}"
                        )

                        # bldNm이 있는 데이터가 있으면 저장
                        bld_nm = str(item["bldNm"]).strip()
                        print(insert_key, bld_nm)

                        insert_data = (
                            True if bld_nm != "" else insert_key not in raw_data
                        )

                        if insert_data:
                            raw_data[insert_key] = {
                                "주소": item["platPlc"].strip(),
                                "도로명주소": item["newPlatPlc"].strip(),
                                "건물명": bld_nm,
                                "주용도코드": main_purps_cd,
                                "주용도코드명": item["mainPurpsCdNm"],
                                "보조용도": str(item["etcPurps"]).strip(),
                            }
            page_no += 1

        # data를 파일로 저장
        with open(
            f"data/bunji/{sigungu_cd}-{bjdong_cd}.json", "w", encoding="utf-8"
        ) as f:
            json.dump(raw_data, f, ensure_ascii=False, indent=4)

        # 처리완료 여부 저장
        with open(f"data/bunji/complete/{sigungu_cd}-{bjdong_cd}.txt", "w") as f:
            f.write("complete")

    finally:
        semaphore.release()  # 세마포어 해제


def call_api(_url):
    """
    API 호출 함수
    :param _url:
    :return:
    """
    try:
        _response = requests.get(_url, timeout=2)
        return _response.json()
    except Timeout:
        print("Timeout occurred, retrying...")
        return call_api(_url)
    except Exception as e:
        print(f"Error occurred: {e}")
        sys.exit(1)


def main():
    # JSON 파일 읽기
    with open("config/addr_code2.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    threads = []

    # 부산광역시로 시작하는 키 찾기
    # 부산광역시만 처리
    # 부산광역시로 시작하고 00000으로 끝나지 않는 키 찾기
    # 검색 결과를 구군별로 파일에 저장
    for key, value in data.items():
        if key.startswith("부산광역시") and not value.endswith("00000"):
            # 10자리의 숫자를 5자리씩 끊어서 sigunguCd와 bjdongCd 변수에 저장
            sigungu_cd = value[:5]
            bjdong_cd = value[5:]
            # 처리완료 파일이 있으면 스킵
            if os.path.exists(f"data/bunji/complete/{sigungu_cd}-{bjdong_cd}.txt"):
                continue

            thread = threading.Thread(target=process_data, args=(sigungu_cd, bjdong_cd))
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()

    directory_path = "data/bunji"

    # 총 레코드 수
    total_records = 0

    # 디렉토리 내의 모든 파일을 순회
    for filename in os.listdir(directory_path):
        # JSON 파일인 경우
        if filename.endswith(".json"):
            # 파일 경로
            file_path = os.path.join(directory_path, filename)

            # JSON 파일 읽기
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            print(
                f"{filename}: {format(len(data), ',')} records"
                if len(data) > 0
                else f"{filename}: No records"
            )
            # 레코드 수를 총 레코드 수에 더함
            total_records += len(data)

    print(f"총 레코드 수: {format(total_records, ',')}")


if __name__ == "__main__":
    main()
