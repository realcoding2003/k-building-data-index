# src/__init__.py
# This file initializes the src package.
import os
from src.common.state import DATA_FOLDER, DATA_BUNJI_FOLDER, DATA_BUILDING_FOLDER, DATA_BUILDING_POS_FOLDER

# 필요한 폴더 생성
os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(DATA_BUNJI_FOLDER, exist_ok=True)
os.makedirs(DATA_BUILDING_FOLDER, exist_ok=True)
os.makedirs(DATA_BUILDING_POS_FOLDER, exist_ok=True)
