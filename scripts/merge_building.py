import os
import json
from tqdm import tqdm

from src.common.state import DATA_BUNJI_FOLDER, DATA_BUILDING_FOLDER
from src.common import log_scripts as log

# 새로운 병합된 데이터를 저장할 폴더
DATA_BUILDING_MERGED_FOLDER = 'data/building_merged'


def load_bunji_data():
    bunji_data = {}
    for filename in os.listdir(DATA_BUNJI_FOLDER):
        if filename.endswith('.json'):
            file_path = os.path.join(DATA_BUNJI_FOLDER, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    if data:  # 데이터가 비어있지 않은 경우에만 처리
                        bunji_data.update(data)
                except json.JSONDecodeError:
                    log.error(f"잘못된 JSON 파일 무시됨: {file_path}")
    return bunji_data


def merge_building_data():
    if not os.path.exists(DATA_BUILDING_MERGED_FOLDER):
        os.makedirs(DATA_BUILDING_MERGED_FOLDER)

    bunji_data = load_bunji_data()

    for filename in tqdm(os.listdir(DATA_BUILDING_FOLDER), desc="병합 중"):
        if filename.endswith('.json'):
            file_path = os.path.join(DATA_BUILDING_FOLDER, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                building_data = json.load(f)

            key = filename[:-5]  # .json 확장자 제거
            basic_info = bunji_data.get(key, {})

            merged_data = {
                "기본정보": basic_info,
                "호실정보": building_data
            }

            output_path = os.path.join(DATA_BUILDING_MERGED_FOLDER, filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(merged_data, f, ensure_ascii=False, indent=4)

            log.info(f"병합된 데이터 저장: {output_path}")


def main():
    try:
        merge_building_data()
        log.info("모든 데이터 병합 완료")
    except Exception as e:
        log.error(f"데이터 병합 중 오류 발생: {e}")


if __name__ == "__main__":
    main()
