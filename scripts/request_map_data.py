import redis
from datetime import datetime
from prettytable import PrettyTable
from colorama import init, Fore, Style
from src.common.state import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD

# Redis 클라이언트 생성
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD
)

# 부산시청 좌표 (위도, 경도)
BUSAN_CITY_HALL_LAT = 35.1798159
BUSAN_CITY_HALL_LON = 129.0750222

# 검색 반경 (미터)
RADIUS = 1000

# colorama 초기화
init()


def get_nearby_buildings(lat, lon, radius):
    current_date = datetime.now().strftime("%Y-%m-02")
    redis_key = f"building_locations_{current_date}"

    try:
        nearby_buildings = redis_client.georadius(
            redis_key, lon, lat, radius, unit='m',
            withdist=True, withcoord=True, count=100
        )
        return nearby_buildings
    except Exception as e:
        print(f"{Fore.RED}Error querying Redis: {e}{Style.RESET_ALL}")
        return []


def main():
    print(f"{Fore.CYAN}Querying buildings within {RADIUS}m of Busan City Hall{Style.RESET_ALL}")
    nearby_buildings = get_nearby_buildings(BUSAN_CITY_HALL_LAT, BUSAN_CITY_HALL_LON, RADIUS)

    if nearby_buildings:
        print(f"{Fore.GREEN}Found {len(nearby_buildings)} buildings{Style.RESET_ALL}")

        table = PrettyTable()
        table.field_names = ["No.", "Building Key", "Distance (m)", "Latitude", "Longitude"]

        for i, building in enumerate(nearby_buildings, 1):
            key, distance, coordinates = building
            table.add_row([
                i,
                key.decode('utf-8'),
                f"{distance:.2f}",
                f"{coordinates[1]:.6f}",
                f"{coordinates[0]:.6f}"
            ])

        print(table)
    else:
        print(f"{Fore.YELLOW}No buildings found in the specified radius{Style.RESET_ALL}")


if __name__ == "__main__":
    main()