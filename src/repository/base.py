"""
Repository 기본 인터페이스
클린 아키텍처의 Repository Pattern 구현
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

# 제네릭 타입 변수
T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """
    Repository 기본 인터페이스

    모든 Repository는 이 인터페이스를 구현해야 함
    CRUD 기본 메서드 정의
    """

    @abstractmethod
    def create(self, entity: T) -> T:
        """
        엔티티 생성

        Args:
            entity: 생성할 엔티티

        Returns:
            T: 생성된 엔티티 (ID 포함)
        """
        pass

    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """
        ID로 엔티티 조회

        Args:
            entity_id: 엔티티 ID

        Returns:
            Optional[T]: 엔티티 또는 None
        """
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """
        모든 엔티티 조회 (페이지네이션)

        Args:
            skip: 건너뛸 개수
            limit: 조회할 최대 개수

        Returns:
            List[T]: 엔티티 리스트
        """
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        """
        엔티티 수정

        Args:
            entity: 수정할 엔티티 (ID 포함)

        Returns:
            T: 수정된 엔티티
        """
        pass

    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        """
        엔티티 삭제 (Soft Delete)

        Args:
            entity_id: 삭제할 엔티티 ID

        Returns:
            bool: 삭제 성공 여부
        """
        pass

    @abstractmethod
    def count(self) -> int:
        """
        전체 엔티티 개수 조회

        Returns:
            int: 엔티티 개수
        """
        pass
