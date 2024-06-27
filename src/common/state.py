import threading
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# 전역 상태 변수들
STOP_EVENT = threading.Event()

# 환경 변수
SERVICE_KEY = os.getenv('SERVICE_KEY')
BASE_URL = os.getenv('BASE_URL')
MAX_THREADS = int(os.getenv('MAX_THREADS', 10))  # 기본값 10
NUM_OF_ROWS = int(os.getenv('NUM_OF_ROWS', 100))  # 기본값 100
TYPE = os.getenv('TYPE', 'json')  # 기본값 'json'
