"""
효심케어 시스템 설정 모듈
Local-First 원칙에 따라 모든 경로는 로컬 기반으로 설정됨
"""
import os
import logging
from pathlib import Path
from typing import Final

# 프로젝트 루트 디렉토리
BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent.parent

# 데이터 디렉토리 (SQLite DB 저장 위치)
DATA_DIR: Final[Path] = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# 로그 디렉토리
LOGS_DIR: Final[Path] = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# 데이터베이스 설정
DB_NAME: Final[str] = "hyosim_care.db"
DB_PATH: Final[Path] = DATA_DIR / DB_NAME

# 데이터베이스 암호화 키 (실제 배포 시에는 환경변수나 별도 키 관리 시스템 사용)
# 보안: 이 값은 반드시 .env 파일이나 안전한 키 저장소로 관리해야 함
DB_ENCRYPTION_KEY: Final[str] = os.getenv(
    "DB_ENCRYPTION_KEY",
    "hyosim_care_default_key_CHANGE_THIS_IN_PRODUCTION"
)

# 로그 설정
LOG_FILE: Final[Path] = LOGS_DIR / "hyosim_care.log"
LOG_LEVEL: Final[int] = logging.INFO
LOG_FORMAT: Final[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"

# 애플리케이션 설정
APP_NAME: Final[str] = "효심케어 관리 시스템"
APP_VERSION: Final[str] = "0.1.0"

# 서비스 타입
class ServiceType:
    """서비스 유형 상수"""
    HOME_CARE: Final[str] = "home_care"  # 방문요양
    DAY_CARE: Final[str] = "day_care"    # 데이케어 (주간보호센터)


def setup_logging() -> logging.Logger:
    """
    로깅 시스템 초기화

    Returns:
        logging.Logger: 설정된 로거 인스턴스
    """
    # 로거 생성
    logger = logging.getLogger("hyosim_care")
    logger.setLevel(LOG_LEVEL)

    # 이미 핸들러가 설정되어 있으면 중복 설정 방지
    if logger.handlers:
        return logger

    # 파일 핸들러 설정
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )
    file_handler.setLevel(LOG_LEVEL)
    file_formatter = logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT)
    file_handler.setFormatter(file_formatter)

    # 콘솔 핸들러 설정
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    console_formatter = logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT)
    console_handler.setFormatter(console_formatter)

    # 핸들러 추가
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info(f"{APP_NAME} v{APP_VERSION} 로깅 시스템 초기화 완료")
    logger.info(f"데이터베이스 경로: {DB_PATH}")
    logger.info(f"로그 파일 경로: {LOG_FILE}")

    return logger


# 전역 로거 인스턴스
logger = setup_logging()
