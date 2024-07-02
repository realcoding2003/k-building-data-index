import threading
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# 전역 상태 변수들
STOP_EVENT = threading.Event()

# 환경 변수
SERVICE_KEY = os.getenv('SERVICE_KEY')
MAX_THREADS = int(os.getenv('MAX_THREADS', 10))  # 기본값 10
NUM_OF_ROWS = int(os.getenv('NUM_OF_ROWS', 100))  # 기본값 100
SIGUNGU_CD = os.getenv('SIGUNGU')   # 시군구 코드
BJDONG_CD = os.getenv('BJDONG')     # 법정동 코드
BUN = os.getenv('BUN')              # 번
JI = os.getenv('JI')                # 지
TYPE = os.getenv('TYPE', 'json')    # 기본값 'json'

# Kakao API 관련 설정
KAKAO_API_URL = "https://dapi.kakao.com/v2/local/search/address.json"
KAKAO_API_KEY = os.getenv('KAKAO_API_KEY')
KAKAO_HEADERS = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}

# 표제부:  https://apis.data.go.kr/1613000/BldRgstService_v2/getBrTitleInfo
# 전유공용면적: https://apis.data.go.kr/1613000/BldRgstService_v2/getBrExposPubuseAreaInfo
BASE_URL_TITLE = "https://apis.data.go.kr/1613000/BldRgstService_v2/getBrTitleInfo"
BASE_URL_AREA = "https://apis.data.go.kr/1613000/BldRgstService_v2/getBrExposPubuseAreaInfo"

# DATA 디렉토리 구조
DATA_FOLDER = os.getenv('DATA_FOLDER', 'data')

# 다른 폴더들을 DATA_FOLDER를 기준으로 자동 설정
DATA_BUNJI_FOLDER = os.path.join(DATA_FOLDER, 'bunji')
DATA_BUILDING_FOLDER = os.path.join(DATA_FOLDER, 'building')
DATA_BUILDING_NO_DATA_FOLDER = os.path.join(DATA_BUILDING_FOLDER, 'no-data')
DATA_BUILDING_MERGED_FOLDER = os.path.join(DATA_FOLDER, 'building-merged')
DATA_BUILDING_POS_FOLDER = os.path.join(DATA_FOLDER, 'building-pos')

# LOG 디렉토리 구조
LOG_FOLDER = os.getenv('LOG_FOLDER', 'logs')
LOG_FOLDER_FORMAT = os.getenv('LOG_FOLDER_FORMAT', '%Y-%m-%d')
