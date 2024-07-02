import redis
from src.common.state import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD

# Redis 클라이언트 생성
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD
)


def delete_building_data():
    # 'building:*' 패턴의 모든 키를 찾습니다.
    cursor = 0
    deleted_count = 0

    while True:
        cursor, keys = redis_client.scan(cursor, match='building:*', count=1000)
        if keys:
            # 찾은 키들을 삭제합니다.
            deleted_count += redis_client.delete(*keys)

        # cursor가 0이면 모든 키를 순회한 것이므로 루프를 종료합니다.
        if cursor == 0:
            break

    print(f"총 {deleted_count}개의 building 관련 데이터가 삭제되었습니다.")


if __name__ == "__main__":
    delete_building_data()
