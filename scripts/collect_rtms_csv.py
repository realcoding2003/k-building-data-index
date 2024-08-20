import os
import json
import csv
import io
from collections import defaultdict

from src.common import log_scripts as log
from src.common.state import DATA_BUILDING_RTMS_FOLDER, DATA_FOLDER


def filter_csv_from_file(file_path):
    with open(file_path, "r", encoding="cp949") as file:
        lines = file.readlines()

    start_idx = next(
        (i for i, line in enumerate(lines) if line.strip().startswith('"시군구","번지"')),
        None,
    )

    if start_idx is None:
        return "", "", "", "", "", ""

    contract_date_line = next((line for line in lines if "계약일자" in line), "")
    sido_line = next((line for line in lines if "시도 :" in line), "")
    sigungu_line = next((line for line in lines if "시군구 :" in line), "")
    transaction_type_line = next((line for line in lines if "실거래구분 :" in line), "")

    if "계약일자 :" in contract_date_line:
        dates = [date.strip() for date in contract_date_line.split(":")[1].split("~")]
        start_date = "{}-{}-{}".format(dates[0][:4], dates[0][4:6], dates[0][6:])
        end_date = "{}-{}-{}".format(dates[1][:4], dates[1][4:6], dates[1][6:])
    else:
        start_date, end_date = "", ""

    sido = sido_line.split(":")[1].strip().replace('"', "") if "시도 :" in sido_line else ""
    sigungu = sigungu_line.split(":")[1].strip().replace('"', "") if "시군구 :" in sigungu_line else ""
    building_type = transaction_type_line.split(":")[1].strip().replace('"',
                                                                        "") if "실거래구분 :" in transaction_type_line else ""

    return start_date, end_date, sido, sigungu, building_type, "".join(lines[start_idx + 1:])


def process_csv_file(file_path, address_codes):
    try:
        start_date, end_date, sido, sigungu, building_type, csv_string = filter_csv_from_file(file_path)

        data = defaultdict(lambda: defaultdict(list))
        reader = csv.reader(io.StringIO(csv_string))

        for row in reader:
            addr_code = next((code for code, addr in address_codes.items() if addr == row[0]), None)
            if not addr_code:
                log.warning(f"Address code not found for {row[0]}")
                continue

            if len(addr_code) != 10:
                addr_code = addr_code + "00"

            sigungu_code = addr_code[:5]
            dong_code = addr_code[5:]
            jibun = row[1].split('-')
            bon_bun = row[2].zfill(4)  # 본번을 4자리로 만듦
            bu_bun = row[3].zfill(4)  # 부번을 4자리로 만듦

            key = (sigungu_code, dong_code, bon_bun, bu_bun)
            year = row[7][:4] if "전월세" in building_type else row[6][:4]

            if "전월세" in building_type:
                deal_data = {
                    "계약일": f"{row[7][:4]}-{row[7][4:6]}-{row[8].zfill(2)}",
                    "계약기간": row[14],
                    "갱신요구권사용": "",
                    "보증금": row[9].replace(",", ""),
                    "월세": row[10].replace(",", ""),
                    "전용면적": row[6],
                    "종전계약보증금": "",
                    "종전계약월세": "",
                    "층": row[11]
                }
            else:  # 매매
                deal_data = {
                    "계약일": f"{row[6][:4]}-{row[6][4:6]}-{row[7].zfill(2)}",
                    "계약기간": "",
                    "갱신요구권사용": "",
                    "보증금": "0",
                    "월세": "0",
                    "전용면적": row[5],
                    "종전계약보증금": "",
                    "종전계약월세": "",
                    "층": row[9],
                    "매매가": row[8].replace(",", "")
                }

            data[key][year].append(deal_data)

        return data

    except Exception as e:
        log.error(f"Error processing file {file_path}: {e}")
        return None


def save_data(data, output_folder):
    for (sigungu_code, dong_code, bon_bun, bu_bun), years_data in data.items():
        # 폴더 경로 생성
        folder_path = os.path.join(output_folder, f"{sigungu_code}-{dong_code}-{bon_bun}-{bu_bun}")
        os.makedirs(folder_path, exist_ok=True)

        for year, deals in years_data.items():
            filename = f"{year}.json"
            filepath = os.path.join(folder_path, filename)

            # 기존 파일이 있다면 데이터를 병합
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                existing_data.extend(deals)
                deals = existing_data

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(deals, f, ensure_ascii=False, indent=2)

        log.info(f"Data saved for {sigungu_code}-{dong_code}-{bon_bun}-{bu_bun}")


def main():
    # 주소 코드 로드
    with open("config/address_code.json", "r", encoding="utf-8") as f:
        address_codes = json.load(f)

    # 처리할 CSV 파일 경로 설정 (테스트용 단일 파일)
    csv_file_path = os.path.join(DATA_FOLDER, "rtms", "부산광역시", "연립다세대_전월세", "연립다세대(전월세)_실거래가_2023.csv")

    # CSV 파일 처리
    data = process_csv_file(csv_file_path, address_codes)

    if data:
        # 데이터 저장
        save_data(data, DATA_BUILDING_RTMS_FOLDER)
        log.info(f"Data processing completed. Processed {len(data)} buildings.")
    else:
        log.error("No data processed.")


if __name__ == "__main__":
    main()
