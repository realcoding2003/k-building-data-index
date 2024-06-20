import os
import json
from data_processor import process_data


def main():
    # 필요한 폴더 생성
    os.makedirs("data/bunji", exist_ok=True)
    os.makedirs("data/bunji/complete", exist_ok=True)

    # 시군구 코드와 법정동 코드 설정
    sigungu_cd = "11110"  # 예시 코드
    bjdong_cd = "10300"   # 예시 코드

    # 처리완료 파일이 있으면 스킵
    if os.path.exists(f"data/bunji/complete/{sigungu_cd}-{bjdong_cd}.txt"):
        print(f"{sigungu_cd}-{bjdong_cd} 지역 데이터는 이미 처리되었습니다.")
        return

    process_data(sigungu_cd, bjdong_cd)

    directory_path = "data/bunji"

    # 총 레코드 수
    total_records = 0

    # 디렉토리 내의 모든 파일을 순회
    for filename in os.listdir(directory_path):
        # JSON 파일인 경우
        if filename.endswith(".json"):
            # 파일 경로
            file_path = os.path.join(directory_path, filename)

            # JSON 파일 읽기
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            print(
                f"{filename}: {format(len(data), ',')} records"
                if len(data) > 0
                else f"{filename}: No records"
            )
            # 레코드 수를 총 레코드 수에 더함
            total_records += len(data)

    print(f"총 레코드 수: {format(total_records, ',')}")


if __name__ == "__main__":
    main()
