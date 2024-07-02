import os
import json
from src.data_collector_pos import process_file, APILimitExceeded
from src.common import log_scripts as log
from src.common.state import DATA_BUILDING_MERGED_FOLDER, DATA_BUILDING_POS_FOLDER, STOP_EVENT


def process_single_file(filename):
    """단일 파일을 처리하고 결과를 출력"""
    if not filename.endswith('.json'):
        filename += '.json'

    input_file_path = os.path.join(DATA_BUILDING_MERGED_FOLDER, filename)

    if not os.path.exists(input_file_path):
        print(f"파일을 찾을 수 없습니다: {input_file_path}")
        return

    print(f"처리 중인 파일: {filename}")

    try:
        processed_data = process_file(filename)

        if processed_data:
            print("\n처리 결과:")
            print(json.dumps(processed_data, ensure_ascii=False, indent=2))

            output_file_path = os.path.join(DATA_BUILDING_POS_FOLDER, filename)
            print(f"\n결과가 다음 위치에 저장되었습니다: {output_file_path}")
        else:
            print("파일 처리 중 오류가 발생했습니다.")

    except APILimitExceeded:
        print("API 호출 한도 초과. 프로세스를 중단합니다.")

    except Exception as e:
        print(f"예외 발생: {e}")

    finally:
        if STOP_EVENT.is_set():
            print("API 한도 초과로 인해 프로세스가 중단되었습니다.")


def main():
    if not os.path.exists(DATA_BUILDING_POS_FOLDER):
        os.makedirs(DATA_BUILDING_POS_FOLDER)

    filename = "11110-16800-0004-0112.json"
    process_single_file(filename)


if __name__ == "__main__":
    main()