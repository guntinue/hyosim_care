"""
Staff Repository 구현
직원 데이터 액세스 레이어
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import date

from src.domain.models import Staff, StaffRole
from src.repository.base import BaseRepository
from src.config.settings import logger


class StaffRepository(BaseRepository[Staff]):
    """
    Staff Repository 구현체

    직원 데이터에 대한 CRUD 및 비즈니스 쿼리 제공
    """

    def __init__(self, session: Session):
        """
        Args:
            session: SQLAlchemy 세션
        """
        self.session = session

    def create(self, entity: Staff) -> Staff:
        """직원 생성"""
        try:
            self.session.add(entity)
            self.session.flush()
            logger.info(f"직원 생성 성공: {entity.name} (ID: {entity.id}, 역할: {entity.role.value})")
            return entity
        except Exception as e:
            logger.error(f"직원 생성 실패: {e}")
            raise

    def get_by_id(self, entity_id: int) -> Optional[Staff]:
        """ID로 직원 조회"""
        try:
            staff = self.session.query(Staff).filter(Staff.id == entity_id).first()
            if staff:
                logger.debug(f"직원 조회 성공: ID {entity_id}")
            else:
                logger.warning(f"직원을 찾을 수 없음: ID {entity_id}")
            return staff
        except Exception as e:
            logger.error(f"직원 조회 실패: {e}")
            raise

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Staff]:
        """모든 직원 조회 (재직 중인 직원만)"""
        try:
            staffs = (
                self.session.query(Staff)
                .filter(Staff.is_active == True)
                .order_by(Staff.created_at.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            logger.debug(f"직원 목록 조회 성공: {len(staffs)}명")
            return staffs
        except Exception as e:
            logger.error(f"직원 목록 조회 실패: {e}")
            raise

    def update(self, entity: Staff) -> Staff:
        """직원 정보 수정"""
        try:
            merged_entity = self.session.merge(entity)
            self.session.flush()
            logger.info(f"직원 수정 성공: {merged_entity.name} (ID: {merged_entity.id})")
            return merged_entity
        except Exception as e:
            logger.error(f"직원 수정 실패: {e}")
            raise

    def delete(self, entity_id: int) -> bool:
        """직원 삭제 (Soft Delete - 퇴사 처리)"""
        try:
            staff = self.get_by_id(entity_id)
            if staff:
                staff.is_active = False
                self.session.flush()
                logger.info(f"직원 퇴사 처리 성공: ID {entity_id}")
                return True
            else:
                logger.warning(f"삭제할 직원을 찾을 수 없음: ID {entity_id}")
                return False
        except Exception as e:
            logger.error(f"직원 삭제 실패: {e}")
            raise

    def count(self) -> int:
        """재직 중인 직원 수 조회"""
        try:
            count = self.session.query(Staff).filter(Staff.is_active == True).count()
            return count
        except Exception as e:
            logger.error(f"직원 수 조회 실패: {e}")
            raise

    # === 비즈니스 쿼리 메서드 ===

    def find_by_name(self, name: str) -> List[Staff]:
        """이름으로 직원 검색 (부분 일치)"""
        try:
            staffs = (
                self.session.query(Staff)
                .filter(Staff.is_active == True)
                .filter(Staff.name.like(f"%{name}%"))
                .all()
            )
            logger.debug(f"이름 검색 결과: {len(staffs)}명 (검색어: {name})")
            return staffs
        except Exception as e:
            logger.error(f"이름 검색 실패: {e}")
            raise

    def find_by_phone(self, phone: str) -> Optional[Staff]:
        """전화번호로 직원 조회"""
        try:
            staff = (
                self.session.query(Staff)
                .filter(Staff.is_active == True)
                .filter(Staff.phone == phone)
                .first()
            )
            return staff
        except Exception as e:
            logger.error(f"전화번호 검색 실패: {e}")
            raise

    def find_by_role(self, role: StaffRole) -> List[Staff]:
        """역할별 직원 조회"""
        try:
            staffs = (
                self.session.query(Staff)
                .filter(Staff.is_active == True)
                .filter(Staff.role == role)
                .all()
            )
            logger.debug(f"{role.value} 직원: {len(staffs)}명")
            return staffs
        except Exception as e:
            logger.error(f"역할별 조회 실패: {e}")
            raise

    def find_by_email(self, email: str) -> Optional[Staff]:
        """이메일로 직원 조회"""
        try:
            staff = (
                self.session.query(Staff)
                .filter(Staff.is_active == True)
                .filter(Staff.email == email)
                .first()
            )
            return staff
        except Exception as e:
            logger.error(f"이메일 검색 실패: {e}")
            raise

    def find_by_license_number(self, license_number: str) -> Optional[Staff]:
        """자격증 번호로 직원 조회"""
        try:
            staff = (
                self.session.query(Staff)
                .filter(Staff.is_active == True)
                .filter(Staff.license_number == license_number)
                .first()
            )
            return staff
        except Exception as e:
            logger.error(f"자격증 번호 검색 실패: {e}")
            raise

    def find_care_workers(self) -> List[Staff]:
        """요양보호사 목록 조회 (자주 사용되는 쿼리)"""
        return self.find_by_role(StaffRole.CARE_WORKER)

    def find_social_workers(self) -> List[Staff]:
        """사회복지사 목록 조회"""
        return self.find_by_role(StaffRole.SOCIAL_WORKER)

    def find_by_hire_date_range(self, start_date: date, end_date: date) -> List[Staff]:
        """입사일 범위로 직원 조회"""
        try:
            staffs = (
                self.session.query(Staff)
                .filter(Staff.is_active == True)
                .filter(Staff.hire_date.between(start_date, end_date))
                .all()
            )
            return staffs
        except Exception as e:
            logger.error(f"입사일 범위 조회 실패: {e}")
            raise
