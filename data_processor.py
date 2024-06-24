import os
import json
from dotenv import load_dotenv
import logging
import requests

# Load environment variables from .env file
load_dotenv()

# Read environment variables
SERVICE_KEY = os.getenv('SERVICE_KEY')
BASE_URL = os.getenv('BASE_URL')
NUM_OF_ROWS = 100
TYPE = 'json'

# Set up logging
logging.basicConfig(filename='logs/data_processor.log', level=logging.INFO,
                    format='[%(asctime)s %(levelname)s] %(message)s')


def call_api(_url):
    """
    API call function
    :param _url: URL to call
    :return: JSON response
    """
    try:
        _response = requests.get(_url, timeout=2)
        _response.raise_for_status()
        try:
            return _response.json()
        except json.JSONDecodeError as e:
            logging.error(f"_response.json() : {_url}\n{_response.text}\n{e}\n")
            return call_api(_url)
    except requests.exceptions.Timeout:
        # logging.error(f"Timeout : {_url}\n{e}\n")
        # Timeout 은 너무 자주 일어나는 오류로 다시 시도하는 것으로 해결함
        return call_api(_url)
    except Exception as e:
        logging.error(f"Exception : {_url}\n{_response.text if '_response' in locals() else 'No response'}\n{e}\n")
        return call_api(_url)


def process_data(sigungu_cd, bjdong_cd, stop_event=None):
    """
    Data processing function
    :param sigungu_cd: City/District code
    :param bjdong_cd: Town code
    :param stop_event: Event to stop the processing
    :return: Processed data or None
    """
    base_url = (
        f"{BASE_URL}?serviceKey={SERVICE_KEY}"
        f"&sigunguCd=[sigunguCd]&bjdongCd=[bjdongCd]&numOfRows={NUM_OF_ROWS}&pageNo=[pageNo]&_type={TYPE}"
    )

    raw_data = {}
    page_no = 1

    try:
        while stop_event is None or not stop_event.is_set():
            url = (
                base_url.replace("[sigunguCd]", sigungu_cd)
                .replace("[bjdongCd]", bjdong_cd)
                .replace("[pageNo]", str(page_no))
            )

            response_data = call_api(url)

            # Handle when the page is exceeded
            if response_data["response"]["body"]["items"] == "":
                break

            # Collecting legal dong code for multi-family (row house) items
            # mainPurpsCd starts with 02
            items = response_data["response"]["body"]["items"]
            if items != "":
                # Check if items["item"] is a dictionary
                if isinstance(items["item"], dict):
                    items["item"] = [items["item"]]

                # Process items
                for item in items["item"]:
                    main_purps_cd = str(item["mainPurpsCd"]).strip()
                    if main_purps_cd.startswith("02"):
                        # Save to raw_data
                        # If existing data, prioritize data with bldNm
                        insert_key = (
                            f"{sigungu_cd}-{bjdong_cd}-{item['bun']}-{item['ji']}"
                        )

                        # Save if there is bldNm
                        bld_nm = str(item["bldNm"]).strip()
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

        # Save data to file only if raw_data is not empty
        with open(f"data/{sigungu_cd}-{bjdong_cd}.json", "w", encoding="utf-8") as f:
            json.dump(raw_data, f, ensure_ascii=False, indent=4)

        return raw_data

    except Exception as e:
        logging.error(f"process_data(): [{sigungu_cd}-{bjdong_cd}]: {e}")
        return None
