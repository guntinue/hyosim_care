"""
Service 레이어 기본 클래스

클린 아키텍처의 Use Case 레이어
비즈니스 로직 및 유스케이스를 구현하는 레이어
"""
from typing import TypeVar, Generic
from abc import ABC

from src.config.database import DatabaseManager
from src.config.settings import logger

# 제네릭 타입 변수
T = TypeVar('T')


class BaseService(ABC, Generic[T]):
    """
    Service 기본 클래스

    모든 Service는 이 클래스를 상속받아 구현
    DatabaseManager를 통한 세션 관리 제공
    """

    def __init__(self, db_manager: DatabaseManager):
        """
        Args:
            db_manager: 데이터베이스 매니저 인스턴스
        """
        self.db_manager = db_manager
        self.logger = logger

    def get_session(self):
        """
        현재 세션 가져오기

        Returns:
            Session: SQLAlchemy 세션
        """
        return self.db_manager.get_session()

    def session_scope(self):
        """
        세션 컨텍스트 매니저

        자동 커밋/롤백 처리

        Example:
            with self.session_scope() as session:
                # 비즈니스 로직
                pass

        Returns:
            ContextManager: 세션 컨텍스트 매니저
        """
        return self.db_manager.session_scope()
