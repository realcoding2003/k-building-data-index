# 대한민국 전국 건물 데이터 수집 시스템

이 프로젝트는 data.go.kr의 건축물대장 표제부 API를 활용하여 대한민국 전국의 건물 데이터를 수집하고 처리하는 멀티스레드 시스템입니다. 대용량 데이터를 효율적으로 처리하며, 중단된 지점부터 재시작할 수 있는 기능을 제공합니다.

## 목차

- [기능](#기능)
- [프로젝트 구조](#프로젝트-구조)
- [설치](#설치)
- [사용법](#사용법)
- [데이터 구조](#데이터-구조)
- [환경 설정](#환경-설정)
- [기여](#기여)
- [라이선스](#라이선스)

## 기능

- **멀티스레드 처리**: 여러 스레드를 사용하여 데이터를 병렬적으로 처리합니다.
- **중단점 복구**: 프로그램 중단 시 이전에 처리한 지점부터 재시작할 수 있습니다.
- **에러 처리 및 로깅**: 포괄적인 로깅 시스템으로 프로그램 실행 중 발생하는 모든 이벤트를 기록합니다.
- **진행 상황 추적**: `tqdm` 라이브러리를 사용하여 실시간 진행률을 표시합니다.
- **데이터 필터링**: 주용도코드가 '02'로 시작하는 다세대 주택 데이터만 수집합니다.
- **유연한 환경 설정**: .env 파일을 통해 쉽게 환경 변수를 설정할 수 있습니다.

## 프로젝트 구조

```
project/
│
├── src/
│   ├── common/
│   │   ├── __init__.py
│   │   ├── logging_setup.py
│   │   ├── state.py
│   │   └── utils.py
│   └── data_collector_bunji.py
│
├── config/
│   └── address_code.json
│
├── scripts/
│   ├── main.py
│   ├── collect_all_data.py
│   └── print_stat.py
│
├── tests/
│   ├── __init__.py
│   ├── test_data_collector.py
│   └── test_utils.py
│
├── requirements.txt
├── sample.env
└── README.md
```

- `src/`: 소스 코드 디렉토리
  - `common/`: 공통 유틸리티 및 설정 파일
    - `__init__.py`: 패키지 초기화 파일
    - `logging_setup.py`: 로깅 설정
    - `state.py`: 전역 상태 변수 관리
    - `utils.py`: 유틸리티 함수
  - `data_collector_bunji.py`: 데이터 수집 및 처리 로직
- `config/`: 설정 파일 디렉토리
  - `address_code.json`: 주소 코드 매핑 파일
- `scripts/`: 프로젝트 실행 파일
  - `main.py`: 단일 지역 데이터 수집 테스트 스크립트
  - `collect_all_data.py`: 전체 데이터 수집 스크립트
  - `print_stat.py`: 수집 통계 출력 스크립트
- `tests/`: 단위 테스트 디렉토리
  - `__init__.py`: 테스트 패키지 초기화 파일
  - `test_data_collector.py`: 데이터 수집기 테스트
  - `test_utils.py`: 유틸리티 함수 테스트
- `requirements.txt`: 프로젝트 의존성 목록
- `sample.env`: 환경 변수 샘플 파일
- `README.md`: 프로젝트 설명 문서

## 설치

1. 레포지토리 클론:
    ```sh
    git clone https://github.com/realcoding2003/k-building-data-index.git
    cd k-building-data-index
    ```

2. 가상 환경 생성 및 활성화:
    ```sh
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

3. 필요한 패키지 설치:
    ```sh
    pip install -r requirements.txt
    ```

4. .env 파일 설정 (자세한 내용은 [환경 설정](#환경-설정) 참조)

5. address_code.json 파일 확인

## 사용법

### 단일 지역 테스트

```sh
python main.py
```

### 전체 데이터 수집

```sh
python collect_all_data.py
```

### 수집 통계 출력

```sh
python print_stat.py
```

## 데이터 구조

수집된 데이터는 다음과 같은 JSON 형식으로 저장됩니다:

```json
{
    "시군구코드-법정동코드-번지-호": {
        "주소": "일반 주소",
        "도로명주소": "도로명을 포함한 주소",
        "건물명": "건물의 이름",
        "주용도코드": "건물의 주용도 코드",
        "주용도코드명": "건물의 주용도 이름 (예: 공동주택)",
        "보조용도": "건물의 보조 용도"
    }
}
```

## 환경 설정

1. 프로젝트 루트 디렉토리에 있는 `sample.env` 파일을 `.env`로 복사합니다:

   ```sh
   cp sample.env .env
   ```

2. 새로 생성된 `.env` 파일을 텍스트 에디터로 열고 필요한 값들을 수정합니다:

   ```
   SERVICE_KEY=your_service_key
   BASE_URL=http://apis.data.go.kr/1613000/BldRgstService_v2/getBrTitleInfo
   MAX_THREADS=10
   SIGUNGU=44210
   BJDONG=10400
   ```

   각 변수의 의미:
   - `SERVICE_KEY`: API 서비스 키 (data.go.kr에서 발급)
   - `BASE_URL`: API 기본 URL
   - `MAX_THREADS`: 최대 스레드 수 (기본값: 10)
   - `SIGUNGU`: 시군구 코드
   - `BJDONG`: 법정동 코드

3. `SERVICE_KEY`에는 반드시 data.go.kr에서 발급받은 실제 서비스 키를 입력해야 합니다.

4. 필요에 따라 `MAX_THREADS`, `SIGUNGU`, `BJDONG` 값을 조정할 수 있습니다.

주의: `.env` 파일에는 민감한 정보가 포함될 수 있으므로, 이 파일을 버전 관리 시스템에 커밋하지 않도록 주의하세요. `.gitignore` 파일에 `.env`가 포함되어 있는지 확인하십시오.

## 기여

1. 프로젝트를 포크합니다.
2. 새 기능 브랜치를 생성합니다 (`git checkout -b feature/amazing-feature`).
3. 변경 사항을 커밋합니다 (`git commit -m 'Add some amazing feature'`).
4. 브랜치에 푸시합니다 (`git push origin feature/amazing-feature`).
5. Pull Request를 생성합니다.

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.