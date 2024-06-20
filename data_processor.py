import os
import json
import sys
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

    except Exception as e:
        print(f"Error occurred: {e}")
        sys.exit(1)
