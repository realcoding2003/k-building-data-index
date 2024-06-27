import json

from src.common import call_api, log_data_processor as log
from src.common.state import SERVICE_KEY, BASE_URL, NUM_OF_ROWS, TYPE, STOP_EVENT


def process_data(sigungu_cd, bjdong_cd):
    """
    주어진 시군구 코드와 법정동 코드에 대한 데이터를 처리하는 함수

    :param sigungu_cd: 시군구 코드
    :param bjdong_cd: 법정동 코드
    :return: 처리된 데이터 딕셔너리 또는 오류 발생 시 None
    """
    # API 호출을 위한 기본 URL 설정
    base_url = (
        f"{BASE_URL}?serviceKey={SERVICE_KEY}"
        f"&sigunguCd=[sigunguCd]&bjdongCd=[bjdongCd]&numOfRows={NUM_OF_ROWS}&pageNo=[pageNo]&_type={TYPE}"
    )

    # 수집된 원시 데이터를 저장할 딕셔너리 초기화
    raw_data = {}
    page_no = 1  # 시작 페이지 번호

    try:
        # stop_event가 설정되지 않았거나, 설정되었더라도 이벤트가 발생하지 않을 때까지 반복
        while not STOP_EVENT.is_set():
            # 현재 페이지 번호, 시군구 코드, 법정동 코드로 URL 업데이트
            url = (
                base_url.replace("[sigunguCd]", sigungu_cd)
                .replace("[bjdongCd]", bjdong_cd)
                .replace("[pageNo]", str(page_no))
            )

            # API 호출 및 응답 데이터 받기
            response_data = call_api(url)

            # 응답에 항목이 없으면 (페이지 초과) 반복 종료
            if response_data["response"]["body"]["items"] == "":
                break

            # 응답에 항목이 있는 경우 처리
            items = response_data["response"]["body"]["items"]
            if items != "":
                # items["item"]이 딕셔너리인 경우(단일 항목) 리스트로 변환
                if isinstance(items["item"], dict):
                    items["item"] = [items["item"]]

                # 각 항목 처리
                for item in items["item"]:
                    main_purps_cd = str(item["mainPurpsCd"]).strip()
                    # 주용도코드가 '02'로 시작하는 경우만 처리 (다세대 주택)
                    if main_purps_cd.startswith("02"):
                        # 데이터 저장을 위한 고유 키 생성
                        insert_key = (
                            f"{sigungu_cd}-{bjdong_cd}-{item['bun']}-{item['ji']}"
                        )

                        # 건물명이 있거나, 기존에 저장된 데이터가 없는 경우에만 저장
                        bld_nm = str(item["bldNm"]).strip()
                        insert_data = (
                            True if bld_nm != "" else insert_key not in raw_data
                        )

                        if insert_data:
                            # 필요한 데이터만 추출하여 저장
                            raw_data[insert_key] = {
                                "주소": item["platPlc"].strip(),
                                "도로명주소": item["newPlatPlc"].strip(),
                                "건물명": bld_nm,
                                "주용도코드": main_purps_cd,
                                "주용도코드명": item["mainPurpsCdNm"],
                                "보조용도": str(item["etcPurps"]).strip(),
                            }

            # 다음 페이지로 이동
            page_no += 1

        # 수집된 데이터가 있으면 JSON 파일로 저장
        if raw_data:
            with open(f"data/{sigungu_cd}-{bjdong_cd}.json", "w", encoding="utf-8") as f:
                json.dump(raw_data, f, ensure_ascii=False, indent=4)

        return raw_data

    except Exception as e:
        # 예외 발생 시 로그 기록
        log.error(f"process_data(): [{sigungu_cd}-{bjdong_cd}]: {e}")
        return None
