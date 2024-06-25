import os
import json
from collections import Counter


def read_data_files(data_folder):
    """Reads all JSON files in the specified data folder."""
    data = []
    for filename in os.listdir(data_folder):
        if filename.endswith('.json'):
            filepath = os.path.join(data_folder, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                file_data = json.load(file)
                data.extend(file_data.values())
    return data


def calculate_statistics(data):
    """Calculates and returns statistics from the data."""
    num_records = len(data)
    if num_records == 0:
        return None

    # 통계 계산: 주용도, 지역(시도)
    main_usage_counter = Counter(item['주용도코드명'] for item in data if '주용도코드명' in item)
    region_counter = Counter(item['주소'].split()[0] for item in data if '주소' in item)

    statistics = {
        'total_records': num_records,
        'main_usage_counts': dict(main_usage_counter),
        'region_counts': dict(region_counter),
    }

    return statistics


def print_statistics(statistics):
    """Prints the calculated statistics."""
    if not statistics:
        print("No data to display statistics.")
        return

    print(f"Total Records: {statistics['total_records']}\n")

    print("Main Usage Counts:")
    for usage, count in statistics['main_usage_counts'].items():
        print(f"  {usage}: {count}")

    print("\nRegion Counts:")
    for region, count in statistics['region_counts'].items():
        print(f"  {region}: {count}")


def main():
    data_folder = 'data'
    data = read_data_files(data_folder)
    statistics = calculate_statistics(data)
    print_statistics(statistics)


if __name__ == '__main__':
    main()
