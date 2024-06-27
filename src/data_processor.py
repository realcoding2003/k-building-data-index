import os
import json
from dotenv import load_dotenv
import logging
from src.common.utils import call_api


# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

# 환경 변수를 읽어옵니다.
SERVICE_KEY = os.getenv('SERVICE_KEY')
BASE_URL = os.getenv('BASE_URL')
NUM_OF_ROWS = 100
TYPE = 'json'

# 로깅 설정: 로그 파일 경로와 로그 레벨 및 포맷을 지정합니다.
logging.basicConfig(filename='logs/data_processor.log', level=logging.INFO,
                    format='[%(asctime)s %(levelname)s] %(message)s')


def process_data(sigungu_cd, bjdong_cd, stop_event=None):
    """
    데이터 처리 함수
    :param sigungu_cd: 시군구 코드
    :param bjdong_cd: 법정동 코드
    :param stop_event: 처리를 중단할 이벤트 (기본값: None)
    :return: 처리된 데이터 또는 None
    """
    # 기본 URL을 설정합니다.
    base_url = (
        f"{BASE_URL}?serviceKey={SERVICE_KEY}"
        f"&sigunguCd=[sigunguCd]&bjdongCd=[bjdongCd]&numOfRows={NUM_OF_ROWS}&pageNo=[pageNo]&_type={TYPE}"
    )

    # 원시 데이터를 저장할 딕셔너리 초기화
    raw_data = {}
    page_no = 1

    try:
        # stop_event가 설정되지 않았거나 설정되었더라도 이벤트가 발생하지 않을 때까지 반복합니다.
        while stop_event is None or not stop_event.is_set():
            # URL을 현재 페이지 번호와 시군구 코드 및 법정동 코드로 업데이트합니다.
            url = (
                base_url.replace("[sigunguCd]", sigungu_cd)
                .replace("[bjdongCd]", bjdong_cd)
                .replace("[pageNo]", str(page_no))
            )

            # API 호출
            response_data = call_api(url)

            # 페이지가 초과된 경우 반복을 중단합니다.
            if response_data["response"]["body"]["items"] == "":
                break

            # 다세대 주택 항목의 법정동 코드를 수집합니다 (mainPurpsCd가 02로 시작하는 경우).
            items = response_data["response"]["body"]["items"]
            if items != "":
                # items["item"]이 딕셔너리인 경우 리스트로 변환합니다.
                if isinstance(items["item"], dict):
                    items["item"] = [items["item"]]

                # 항목을 처리합니다.
                for item in items["item"]:
                    main_purps_cd = str(item["mainPurpsCd"]).strip()
                    if main_purps_cd.startswith("02"):
                        # raw_data에 저장할 키를 생성합니다.
                        insert_key = (
                            f"{sigungu_cd}-{bjdong_cd}-{item['bun']}-{item['ji']}"
                        )

                        # 건물명이 있는 경우 데이터를 저장할지 여부를 결정합니다.
                        bld_nm = str(item["bldNm"]).strip()
                        insert_data = (
                            True if bld_nm != "" else insert_key not in raw_data
                        )

                        if insert_data:
                            # 데이터를 raw_data에 저장합니다.
                            raw_data[insert_key] = {
                                "주소": item["platPlc"].strip(),
                                "도로명주소": item["newPlatPlc"].strip(),
                                "건물명": bld_nm,
                                "주용도코드": main_purps_cd,
                                "주용도코드명": item["mainPurpsCdNm"],
                                "보조용도": str(item["etcPurps"]).strip(),
                            }
            page_no += 1

        # raw_data가 비어 있지 않은 경우 데이터를 파일로 저장합니다.
        with open(f"data/{sigungu_cd}-{bjdong_cd}.json", "w", encoding="utf-8") as f:
            json.dump(raw_data, f, ensure_ascii=False, indent=4)

        return raw_data

    except Exception as e:
        # 예외 발생 시 로그를 기록합니다.
        logging.error(f"process_data(): [{sigungu_cd}-{bjdong_cd}]: {e}")
        return None
