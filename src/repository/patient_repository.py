"""
Patient Repository 구현
고객(환자) 데이터 액세스 레이어
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import date

from src.domain.models import Patient, ServiceType
from src.repository.base import BaseRepository
from src.config.settings import logger


class PatientRepository(BaseRepository[Patient]):
    """
    Patient Repository 구현체

    고객(환자) 데이터에 대한 CRUD 및 비즈니스 쿼리 제공
    """

    def __init__(self, session: Session):
        """
        Args:
            session: SQLAlchemy 세션
        """
        self.session = session

    def create(self, entity: Patient) -> Patient:
        """고객 생성"""
        try:
            self.session.add(entity)
            self.session.flush()  # ID 생성을 위해 flush
            logger.info(f"고객 생성 성공: {entity.name} (ID: {entity.id})")
            return entity
        except Exception as e:
            logger.error(f"고객 생성 실패: {e}")
            raise

    def get_by_id(self, entity_id: int) -> Optional[Patient]:
        """ID로 고객 조회"""
        try:
            patient = self.session.query(Patient).filter(Patient.id == entity_id).first()
            if patient:
                logger.debug(f"고객 조회 성공: ID {entity_id}")
            else:
                logger.warning(f"고객을 찾을 수 없음: ID {entity_id}")
            return patient
        except Exception as e:
            logger.error(f"고객 조회 실패: {e}")
            raise

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Patient]:
        """모든 고객 조회 (활성 고객만)"""
        try:
            patients = (
                self.session.query(Patient)
                .filter(Patient.is_active == True)
                .order_by(Patient.created_at.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            logger.debug(f"고객 목록 조회 성공: {len(patients)}명")
            return patients
        except Exception as e:
            logger.error(f"고객 목록 조회 실패: {e}")
            raise

    def update(self, entity: Patient) -> Patient:
        """고객 정보 수정"""
        try:
            # merge를 사용하여 detached 객체도 처리 가능
            merged_entity = self.session.merge(entity)
            self.session.flush()
            logger.info(f"고객 수정 성공: {merged_entity.name} (ID: {merged_entity.id})")
            return merged_entity
        except Exception as e:
            logger.error(f"고객 수정 실패: {e}")
            raise

    def delete(self, entity_id: int) -> bool:
        """고객 삭제 (Soft Delete)"""
        try:
            patient = self.get_by_id(entity_id)
            if patient:
                patient.is_active = False
                self.session.flush()
                logger.info(f"고객 비활성화 성공: ID {entity_id}")
                return True
            else:
                logger.warning(f"삭제할 고객을 찾을 수 없음: ID {entity_id}")
                return False
        except Exception as e:
            logger.error(f"고객 삭제 실패: {e}")
            raise

    def count(self) -> int:
        """활성 고객 수 조회"""
        try:
            count = self.session.query(Patient).filter(Patient.is_active == True).count()
            return count
        except Exception as e:
            logger.error(f"고객 수 조회 실패: {e}")
            raise

    # === 비즈니스 쿼리 메서드 ===

    def find_by_name(self, name: str) -> List[Patient]:
        """이름으로 고객 검색 (부분 일치)"""
        try:
            patients = (
                self.session.query(Patient)
                .filter(Patient.is_active == True)
                .filter(Patient.name.like(f"%{name}%"))
                .all()
            )
            logger.debug(f"이름 검색 결과: {len(patients)}명 (검색어: {name})")
            return patients
        except Exception as e:
            logger.error(f"이름 검색 실패: {e}")
            raise

    def find_by_phone(self, phone: str) -> Optional[Patient]:
        """전화번호로 고객 조회 (정확한 일치)"""
        try:
            patient = (
                self.session.query(Patient)
                .filter(Patient.is_active == True)
                .filter(Patient.phone == phone)
                .first()
            )
            return patient
        except Exception as e:
            logger.error(f"전화번호 검색 실패: {e}")
            raise

    def find_by_service_type(self, service_type: ServiceType) -> List[Patient]:
        """서비스 유형별 고객 조회"""
        try:
            patients = (
                self.session.query(Patient)
                .filter(Patient.is_active == True)
                .filter(Patient.service_type == service_type)
                .all()
            )
            logger.debug(f"{service_type.value} 고객: {len(patients)}명")
            return patients
        except Exception as e:
            logger.error(f"서비스 유형별 조회 실패: {e}")
            raise

    def find_by_care_grade(self, care_grade: str) -> List[Patient]:
        """등급별 고객 조회"""
        try:
            patients = (
                self.session.query(Patient)
                .filter(Patient.is_active == True)
                .filter(Patient.care_grade == care_grade)
                .all()
            )
            return patients
        except Exception as e:
            logger.error(f"등급별 조회 실패: {e}")
            raise

    def find_by_birth_date_range(self, start_date: date, end_date: date) -> List[Patient]:
        """생년월일 범위로 고객 조회"""
        try:
            patients = (
                self.session.query(Patient)
                .filter(Patient.is_active == True)
                .filter(Patient.birth_date.between(start_date, end_date))
                .all()
            )
            return patients
        except Exception as e:
            logger.error(f"생년월일 범위 조회 실패: {e}")
            raise
