import os  # OS 모듈을 가져와서 디렉토리 관련 작업을 수행합니다.
from data_processor import process_data  # data_processor 모듈에서 process_data 함수를 가져옵니다.
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 최대 동시 실행개수(환경 변수 읽기)
SIGUNGU_CD = os.getenv('SIGUNGU')
BJDONG_CD = os.getenv('BJDONG')


def main(sigungu_cd, bjdong_cd):
    """
    메인 함수로, 데이터 수집을 위한 디렉토리를 생성하고
    지정된 시군구 코드와 법정동 코드를 사용하여 데이터를 처리합니다.
    """
    # 필요한 폴더 생성
    os.makedirs("data", exist_ok=True)

    # 지정된 시군구 코드와 법정동 코드를 사용하여 데이터를 처리합니다.
    processed_data = process_data(sigungu_cd, bjdong_cd)

    # 처리한 파일에 대한 내용 출력
    if processed_data:
        # 데이터를 처리한 경우, 처리된 레코드 수와 시군구-법정동 코드를 출력합니다.
        print(processed_data)
        print(f"Processed {len(processed_data)} records for {sigungu_cd}-{bjdong_cd}")
    else:
        # 데이터가 처리되지 않은 경우, 처리되지 않았음을 출력합니다.
        print(f"No records processed for {sigungu_cd}-{bjdong_cd}")


if __name__ == "__main__":
    # 이 스크립트가 직접 실행된 경우에만 main() 함수를 호출합니다.
    main(SIGUNGU_CD, BJDONG_CD)
