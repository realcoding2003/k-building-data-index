from src.data_collector_building import collect_and_save_building_data
from src.common.state import SIGUNGU_CD, BJDONG_CD, BUN, JI


def print_building_structure(building_data):
    print("\n건물 구조도:")
    print("=" * 40)

    for floor, rooms in sorted(building_data.items(), key=lambda x: int(x[0]), reverse=True):
        print(f"{floor}층:")
        print("|")
        for room, details in sorted(rooms.items()):
            area = details.get('area', 'N/A')
            if area != 'N/A':
                area = f"{float(area):.2f}"  # 소수점 두 자리까지 표시
            room_number = room.rstrip('호')  # '호'를 제거
            print(f"|-- {room_number}호 (면적: {area}㎡)")
        print("|")

    print("=" * 40)


def main():
    print("건물 데이터 수집 프로그램")
    print("------------------------")

    print(f"시군구 코드: {SIGUNGU_CD}")
    print(f"법정동 코드: {BJDONG_CD}")
    print(f"번지: {BUN}")
    print(f"지: {JI}")

    result = collect_and_save_building_data(SIGUNGU_CD, BJDONG_CD, BUN, JI)

    if result:
        print("\n건물 데이터 수집 완료")
        print(f"총 {len(result)} 개의 층이 있습니다.")

        total_rooms = sum(len(rooms) for rooms in result.values())
        print(f"총 {total_rooms}개의 호실이 있습니다.")

        for floor, rooms in result.items():
            print(f"{floor}층: {len(rooms)}개의 호")

        print_building_structure(result)

        print("\n상세 정보는 저장된 JSON 파일을 확인하세요.")
    else:
        print("건물 데이터 수집에 실패했습니다.")


if __name__ == "__main__":
    main()
