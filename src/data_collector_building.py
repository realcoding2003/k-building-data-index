import os
import json
from src.common import call_api, log_data_collector as log
from src.common.state import SERVICE_KEY, BASE_URL_AREA, NUM_OF_ROWS, TYPE, DATA_BUILDING_FOLDER


def get_area_info(sigungu_cd, bjdong_cd, bun, ji):
    base_url = (
        f"{BASE_URL_AREA}?serviceKey={SERVICE_KEY}"
        f"&sigunguCd={sigungu_cd}&bjdongCd={bjdong_cd}&bun={bun}&ji={ji}"
        f"&numOfRows={NUM_OF_ROWS}&pageNo=[pageNo]&_type={TYPE}"
    )

    raw_data = []
    page_no = 1

    while True:
        url = base_url.replace("[pageNo]", str(page_no))
        response_data = call_api(url)

        if response_data["response"]["body"]["items"] == "":
            break

        items = response_data["response"]["body"]["items"]
        if items != "":
            if isinstance(items["item"], dict):
                items["item"] = [items["item"]]

            for item in items["item"]:
                bld_nm = str(item.get("bldNm", ""))
                etc_purps = str(item.get("etcPurps", ""))
                main_purps_cd_nm = str(item.get("mainPurpsCdNm", ""))

                if (
                        "아파트" in bld_nm
                        or "더샵" in bld_nm
                        or "힐스테이트" in bld_nm
                        or "아파트" in etc_purps
                        or "아파트" in main_purps_cd_nm
                ):
                    print("아파트로 판단되어 데이터를 수집하지 않습니다.")
                    return []

                raw_data.append(item)

        page_no += 1

    return raw_data


def reorganize_rooms_data(rooms):
    result = {}
    for room in rooms:
        if room.get("exposPubuseGbCd") == 2:
            continue

        floor = str(room["flrNoNm"]).replace("층", "")
        room_number = str(room["hoNm"])
        area = room["area"]
        if floor not in result:
            result[floor] = {}
        if room_number not in result[floor]:
            result[floor][room_number] = {}
        result[floor][room_number]["area"] = area

    for floor in result:
        result[floor] = dict(sorted(result[floor].items(), key=lambda x: x[0]))

    result = dict(sorted(result.items(), key=lambda x: x[0]))
    return result


def collect_and_save_building_data(sigungu_cd, bjdong_cd, bun, ji):
    try:
        log.info(f"Collecting data for building: {sigungu_cd}-{bjdong_cd}-{bun}-{ji}")

        raw_data = get_area_info(sigungu_cd, bjdong_cd, bun, ji)

        if not raw_data:
            log.info("No data found for this building.")
            return None

        rooms_data = reorganize_rooms_data(raw_data)

        if not os.path.exists(DATA_BUILDING_FOLDER):
            os.makedirs(DATA_BUILDING_FOLDER)

        output_path = f"{DATA_BUILDING_FOLDER}/{sigungu_cd}-{bjdong_cd}-{bun}-{ji}.json"

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(rooms_data, f, ensure_ascii=False, indent=4)

        log.info(f"Building data saved to: {output_path}")

        return rooms_data

    except Exception as e:
        log.error(f"Error collecting and saving building data: {e}")
        return None
