import os  # OS 모듈을 가져와서 디렉토리 관련 작업을 수행합니다.
from data_processor import process_data  # data_processor 모듈에서 process_data 함수를 가져옵니다.


def main(sigungu_cd, bjdong_cd):
    """
    메인 함수로, 데이터 수집을 위한 디렉토리를 생성하고
    지정된 시군구 코드와 법정동 코드를 사용하여 데이터를 처리합니다.
    """
    # 필요한 폴더 생성
    os.makedirs("data/bunji", exist_ok=True)  # "data/bunji" 폴더를 생성합니다. 이미 존재하면 무시합니다.
    os.makedirs("data/bunji/complete", exist_ok=True)  # "data/bunji/complete" 폴더를 생성합니다. 이미 존재하면 무시합니다.

    # 지정된 시군구 코드와 법정동 코드를 사용하여 데이터를 처리합니다.
    processed_data = process_data(sigungu_cd, bjdong_cd)

    # 처리한 파일에 대한 내용 출력
    if processed_data:
        # 데이터를 처리한 경우, 처리된 레코드 수와 시군구-법정동 코드를 출력합니다.
        print(f"Processed {len(processed_data)} records for {sigungu_cd}-{bjdong_cd}")
    else:
        # 데이터가 처리되지 않은 경우, 처리되지 않았음을 출력합니다.
        print(f"No records processed for {sigungu_cd}-{bjdong_cd}")


if __name__ == "__main__":
    # 시군구 코드와 법정동 코드 설정
    _sigungu_cd = "11110"  # 예시로 서울특별시 종로구의 시군구 코드입니다.
    _bjdong_cd = "10300"   # 예시로 사직동의 법정동 코드입니다.

    # 이 스크립트가 직접 실행된 경우에만 main() 함수를 호출합니다.
    main(_sigungu_cd, _bjdong_cd)
