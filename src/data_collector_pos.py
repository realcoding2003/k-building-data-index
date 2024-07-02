import json
import requests
import os
from src.common import log_data_collector as log
from src.common.state import (
    DATA_BUILDING_MERGED_FOLDER,
    DATA_BUILDING_POS_FOLDER,
    KAKAO_API_URL,
    KAKAO_HEADERS,
    STOP_EVENT
)


class APILimitExceeded(Exception):
    pass


def get_location_info(address):
    """주소를 받아 Kakao API를 통해 위치 정보(위도, 경도)를 반환"""
    params = {"query": address}

    try:
        response = requests.get(KAKAO_API_URL, headers=KAKAO_HEADERS, params=params)

        if response.status_code == 429:
            error_data = response.json()
            if error_data.get("errorType") == "RequestThrottled" and error_data.get(
                    "message") == "API limit has been exceeded.":
                log.warning("API 호출 한도 초과. 프로세스를 중단합니다.")
                STOP_EVENT.set()
                raise APILimitExceeded("일일 API 호출 한도에 도달했습니다.")

        response.raise_for_status()
        json_data = response.json()

        if json_data["documents"]:
            lat = json_data["documents"][0]["y"]  # 위도
            lng = json_data["documents"][0]["x"]  # 경도
            return lat, lng
        else:
            return None, None
    except requests.RequestException as e:
        log.error(f"API 요청 중 오류 발생: {e}")
        if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code == 429:
            STOP_EVENT.set()
            raise APILimitExceeded("일일 API 호출 한도에 도달했습니다.")
        return None, None
    except KeyError as e:
        log.error(f"API 응답 데이터 처리 중 오류 발생: {e}")
        return None, None


def process_file(filename):
    """개별 파일을 처리하고 위치 정보를 추가"""
    input_file_path = os.path.join(DATA_BUILDING_MERGED_FOLDER, filename)
    output_file_path = os.path.join(DATA_BUILDING_POS_FOLDER, filename)

    try:
        with open(input_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        basic_info = data.get("기본정보", {})
        address = basic_info.get("도로명주소", "")
        if address:
            lat, lng = get_location_info(address)
            if lat and lng:
                basic_info["위도"] = lat
                basic_info["경도"] = lng

        with open(output_file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        log.info(f"{filename} 처리 완료")
        return data
    except APILimitExceeded:
        log.warning(f"{filename} 처리 중 API 한도 초과")
        return None
    except Exception as e:
        log.error(f"{filename} 처리 중 오류 발생: {e}")
        return None
