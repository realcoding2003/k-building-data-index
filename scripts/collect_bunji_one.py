from src.data_collector_bunji import collect_data
from src.common.state import SIGUNGU_CD, BJDONG_CD


def main(sigungu_cd, bjdong_cd):
    """
    지정된 시군구 코드와 법정동 코드를 사용하여 데이터를 처리합니다.
    테스트를 위한 코드
    """

    # 지정된 시군구 코드와 법정동 코드를 사용하여 데이터를 처리합니다.
    _data = collect_data(sigungu_cd, bjdong_cd)

    # 처리한 파일에 대한 내용 출력
    if _data:
        # 데이터를 처리한 경우, 처리된 레코드 수와 시군구-법정동 코드를 출력합니다.
        print(_data)
        print(f"Processed {len(_data)} records for {sigungu_cd}-{bjdong_cd}")
    else:
        # 데이터가 처리되지 않은 경우, 처리되지 않았음을 출력합니다.
        print(f"No records processed for {sigungu_cd}-{bjdong_cd}")


if __name__ == "__main__":
    # 이 스크립트가 직접 실행된 경우에만 main() 함수를 호출합니다.
    main(SIGUNGU_CD, BJDONG_CD)
