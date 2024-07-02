import os
import json
import redis
from tqdm import tqdm
from datetime import datetime
from src.common import log_scripts as log
from src.common.state import DATA_BUILDING_POS_FOLDER, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD

# Redis 클라이언트 생성
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD
)

# 파이프라인 배치 크기
BATCH_SIZE = 1000

# 현재 날짜를 가져와 Redis 키 생성
current_date = datetime.now().strftime("%Y-%m-%d")
REDIS_KEY = f"building_locations_{current_date}"


def process_building_files(file_list):
    pipeline = redis_client.pipeline(transaction=False)
    count = 0

    for filename in tqdm(file_list, desc="Processing building locations"):
        file_path = os.path.join(DATA_BUILDING_POS_FOLDER, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            key = os.path.splitext(os.path.basename(file_path))[0]
            basic_info = data.get('기본정보', {})

            lat = basic_info.get('위도')
            lon = basic_info.get('경도')

            if lat and lon and key:
                lat = float(lat)
                lon = float(lon)

                # GEO 데이터 등록
                pipeline.geoadd(REDIS_KEY, (lon, lat, key))

                count += 1

                # 배치 크기에 도달하면 파이프라인 실행
                if count % BATCH_SIZE == 0:
                    pipeline.execute()
                    pipeline = redis_client.pipeline(transaction=False)
            else:
                log.warning(f"Skipping file {file_path} due to missing latitude, longitude, or key")
        except Exception as e:
            log.error(f"Error processing file {file_path}: {e}")

    # 남은 명령어 실행
    if count % BATCH_SIZE != 0:
        pipeline.execute()

    log.info(f"Total locations processed: {count}")


def register_building_locations():
    file_list = [f for f in os.listdir(DATA_BUILDING_POS_FOLDER) if f.endswith('.json')]
    process_building_files(file_list)


def main():
    try:
        log.info(f"Starting building location processing for key: {REDIS_KEY}")
        register_building_locations()
        log.info(f"All building location processing completed for key: {REDIS_KEY}")
    except Exception as e:
        log.error(f"An error occurred during processing: {e}")


if __name__ == "__main__":
    main()
