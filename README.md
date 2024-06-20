# 전국 데이터 수집 프로젝트

이 프로젝트는 전국의 시군구와 법정동 데이터를 수집하여 JSON 파일로 저장하는 스크립트를 제공합니다. 데이터는 공공 API를 통해 수집되며, 각 지역별로 JSON 파일이 생성됩니다.

## 기능

- 시군구와 법정동 데이터를 공공 API를 통해 수집
- 수집된 데이터를 JSON 파일로 저장
- 멀티쓰레드를 이용하여 동시에 여러 지역의 데이터를 수집
- 이미 처리된 데이터는 재처리하지 않음

## 파일 구조

```
project/
│
├── data/                     # 수집된 데이터가 저장되는 디렉토리
│   ├── <sigunguCd>-<bjdongCd>.json  # 각 지역별 데이터 파일
│
├── config/
│   ├── addr_code2.json       # 시군구와 법정동 코드가 포함된 설정 파일
│
├── .env                      # 환경 변수 파일 (API 키 등)
├── data_processor.py         # 데이터 수집 및 처리 모듈
├── collect_all_data.py       # 전국 데이터를 수집하는 스크립트
├── README.md                 # 프로젝트 설명 파일
│
```

## 설치 방법

1. 이 저장소를 클론합니다.
   ```bash
   git clone https://github.com/your-repository-url
   cd your-repository
   ```

2. 필요한 Python 패키지를 설치합니다.
   ```bash
   pip install -r requirements.txt
   ```

3. `.env` 파일을 생성하고, 필요한 환경 변수를 설정합니다.
   ```env
   SERVICE_KEY=YOUR_SERVICE_KEY
   BASE_URL=http://apis.data.go.kr/1613000/BldRgstService_v2/getBrTitleInfo
   NUM_OF_ROWS=100
   TYPE=json
   ```

4. `config/addr_code2.json` 파일을 생성하고, 시군구와 법정동 코드를 입력합니다.
   ```json
   {
     "서울특별시 종로구 사직동": "1111010300",
     ...
   }
   ```

## 사용 방법

1. 데이터를 수집하려면 `collect_all_data.py` 스크립트를 실행합니다.
   ```bash
   python collect_all_data.py
   ```

2. 스크립트가 실행되면 `data` 디렉토리에 각 지역별로 JSON 파일이 생성됩니다. 이미 수집된 데이터가 있으면 해당 지역은 스킵됩니다.

## 스크립트 설명

### `data_processor.py`

이 모듈은 데이터를 수집하고 JSON 파일로 저장하는 함수들을 포함합니다.

- `process_data(sigungu_cd, bjdong_cd)`: 지정된 시군구 코드와 법정동 코드에 대해 데이터를 수집하고 JSON 파일로 저장합니다.

### `collect_all_data.py`

이 스크립트는 `data_processor.py` 모듈을 사용하여 전국의 데이터를 수집합니다.

- 멀티쓰레드를 이용하여 동시에 여러 지역의 데이터를 수집합니다.
- 이미 처리된 JSON 파일이 존재하면 해당 지역은 스킵됩니다.

### 환경 변수 설정

API 키와 기타 설정 값은 `.env` 파일에 저장됩니다. 예시:

```env
SERVICE_KEY=YOUR_SERVICE_KEY
BASE_URL=http://apis.data.go.kr/1613000/BldRgstService_v2/getBrTitleInfo
NUM_OF_ROWS=100
TYPE=json
```

### 실행 예제

1. `.env` 파일 설정
2. `config/addr_code2.json` 파일 설정
3. `python collect_all_data.py` 명령어로 실행

## 기여

기여를 환영합니다! 버그 제보, 기능 추가 요청, 풀 리퀘스트는 언제든지 환영합니다.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 LICENSE 파일을 참고하세요.