"""
VisitLog Repository 구현
방문 일지 데이터 액세스 레이어
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date, datetime

from src.domain.models import VisitLog
from src.repository.base import BaseRepository
from src.config.settings import logger


class VisitLogRepository(BaseRepository[VisitLog]):
    """
    VisitLog Repository 구현체

    방문 일지 데이터에 대한 CRUD 및 비즈니스 쿼리 제공
    """

    def __init__(self, session: Session):
        """
        Args:
            session: SQLAlchemy 세션
        """
        self.session = session

    def create(self, entity: VisitLog) -> VisitLog:
        """방문 일지 생성"""
        try:
            self.session.add(entity)
            self.session.flush()
            logger.info(
                f"방문 일지 생성 성공: 날짜={entity.visit_date}, "
                f"고객ID={entity.patient_id}, 직원ID={entity.staff_id}"
            )
            return entity
        except Exception as e:
            logger.error(f"방문 일지 생성 실패: {e}")
            raise

    def get_by_id(self, entity_id: int) -> Optional[VisitLog]:
        """ID로 방문 일지 조회"""
        try:
            visit_log = self.session.query(VisitLog).filter(VisitLog.id == entity_id).first()
            if visit_log:
                logger.debug(f"방문 일지 조회 성공: ID {entity_id}")
            else:
                logger.warning(f"방문 일지를 찾을 수 없음: ID {entity_id}")
            return visit_log
        except Exception as e:
            logger.error(f"방문 일지 조회 실패: {e}")
            raise

    def get_all(self, skip: int = 0, limit: int = 100) -> List[VisitLog]:
        """모든 방문 일지 조회 (최신순)"""
        try:
            visit_logs = (
                self.session.query(VisitLog)
                .order_by(VisitLog.visit_date.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            logger.debug(f"방문 일지 목록 조회 성공: {len(visit_logs)}개")
            return visit_logs
        except Exception as e:
            logger.error(f"방문 일지 목록 조회 실패: {e}")
            raise

    def update(self, entity: VisitLog) -> VisitLog:
        """방문 일지 수정"""
        try:
            merged_entity = self.session.merge(entity)
            self.session.flush()
            logger.info(f"방문 일지 수정 성공: ID {merged_entity.id}")
            return merged_entity
        except Exception as e:
            logger.error(f"방문 일지 수정 실패: {e}")
            raise

    def delete(self, entity_id: int) -> bool:
        """방문 일지 삭제 (Hard Delete)"""
        try:
            visit_log = self.get_by_id(entity_id)
            if visit_log:
                self.session.delete(visit_log)
                self.session.flush()
                logger.info(f"방문 일지 삭제 성공: ID {entity_id}")
                return True
            else:
                logger.warning(f"삭제할 방문 일지를 찾을 수 없음: ID {entity_id}")
                return False
        except Exception as e:
            logger.error(f"방문 일지 삭제 실패: {e}")
            raise

    def count(self) -> int:
        """전체 방문 일지 개수 조회"""
        try:
            count = self.session.query(VisitLog).count()
            return count
        except Exception as e:
            logger.error(f"방문 일지 수 조회 실패: {e}")
            raise

    # === 비즈니스 쿼리 메서드 ===

    def find_by_schedule_id(self, schedule_id: int) -> Optional[VisitLog]:
        """일정 ID로 방문 일지 조회 (1:1 관계)"""
        try:
            visit_log = (
                self.session.query(VisitLog)
                .filter(VisitLog.schedule_id == schedule_id)
                .first()
            )
            return visit_log
        except Exception as e:
            logger.error(f"일정별 방문 일지 조회 실패: {e}")
            raise

    def find_by_patient_id(self, patient_id: int) -> List[VisitLog]:
        """특정 고객의 모든 방문 일지 조회"""
        try:
            visit_logs = (
                self.session.query(VisitLog)
                .filter(VisitLog.patient_id == patient_id)
                .order_by(VisitLog.visit_date.desc())
                .all()
            )
            return visit_logs
        except Exception as e:
            logger.error(f"고객별 방문 일지 조회 실패: {e}")
            raise

    def find_by_staff_id(self, staff_id: int) -> List[VisitLog]:
        """특정 직원의 모든 방문 일지 조회"""
        try:
            visit_logs = (
                self.session.query(VisitLog)
                .filter(VisitLog.staff_id == staff_id)
                .order_by(VisitLog.visit_date.desc())
                .all()
            )
            return visit_logs
        except Exception as e:
            logger.error(f"직원별 방문 일지 조회 실패: {e}")
            raise

    def find_by_date(self, target_date: date) -> List[VisitLog]:
        """특정 날짜의 모든 방문 일지 조회"""
        try:
            visit_logs = (
                self.session.query(VisitLog)
                .filter(VisitLog.visit_date == target_date)
                .all()
            )
            logger.debug(f"{target_date} 방문 일지: {len(visit_logs)}개")
            return visit_logs
        except Exception as e:
            logger.error(f"날짜별 방문 일지 조회 실패: {e}")
            raise

    def find_by_date_range(self, start_date: date, end_date: date) -> List[VisitLog]:
        """날짜 범위로 방문 일지 조회"""
        try:
            visit_logs = (
                self.session.query(VisitLog)
                .filter(VisitLog.visit_date.between(start_date, end_date))
                .order_by(VisitLog.visit_date.desc())
                .all()
            )
            return visit_logs
        except Exception as e:
            logger.error(f"날짜 범위 방문 일지 조회 실패: {e}")
            raise

    def find_by_staff_and_date(self, staff_id: int, target_date: date) -> List[VisitLog]:
        """특정 직원의 특정 날짜 방문 일지 조회"""
        try:
            visit_logs = (
                self.session.query(VisitLog)
                .filter(
                    and_(
                        VisitLog.staff_id == staff_id,
                        VisitLog.visit_date == target_date
                    )
                )
                .all()
            )
            return visit_logs
        except Exception as e:
            logger.error(f"직원별 날짜 방문 일지 조회 실패: {e}")
            raise

    def find_by_patient_and_date_range(
        self,
        patient_id: int,
        start_date: date,
        end_date: date
    ) -> List[VisitLog]:
        """특정 고객의 특정 기간 방문 일지 조회"""
        try:
            visit_logs = (
                self.session.query(VisitLog)
                .filter(
                    and_(
                        VisitLog.patient_id == patient_id,
                        VisitLog.visit_date.between(start_date, end_date)
                    )
                )
                .order_by(VisitLog.visit_date.desc())
                .all()
            )
            return visit_logs
        except Exception as e:
            logger.error(f"고객별 기간 방문 일지 조회 실패: {e}")
            raise

    def find_by_staff_and_date_range(
        self,
        staff_id: int,
        start_date: date,
        end_date: date
    ) -> List[VisitLog]:
        """특정 직원의 특정 기간 방문 일지 조회"""
        try:
            visit_logs = (
                self.session.query(VisitLog)
                .filter(
                    and_(
                        VisitLog.staff_id == staff_id,
                        VisitLog.visit_date.between(start_date, end_date)
                    )
                )
                .order_by(VisitLog.visit_date.desc())
                .all()
            )
            return visit_logs
        except Exception as e:
            logger.error(f"직원별 기간 방문 일지 조회 실패: {e}")
            raise

    def find_incomplete_logs(self) -> List[VisitLog]:
        """미작성 방문 일지 조회 (출퇴근 시간이나 내용이 없는 것)"""
        try:
            visit_logs = (
                self.session.query(VisitLog)
                .filter(
                    or_(
                        VisitLog.check_in_time.is_(None),
                        VisitLog.check_out_time.is_(None),
                        VisitLog.service_content.is_(None)
                    )
                )
                .order_by(VisitLog.visit_date.desc())
                .all()
            )
            return visit_logs
        except Exception as e:
            logger.error(f"미작성 방문 일지 조회 실패: {e}")
            raise

    def count_by_patient(self, patient_id: int) -> int:
        """특정 고객의 총 방문 횟수"""
        try:
            count = (
                self.session.query(VisitLog)
                .filter(VisitLog.patient_id == patient_id)
                .count()
            )
            return count
        except Exception as e:
            logger.error(f"고객별 방문 횟수 조회 실패: {e}")
            raise

    def count_by_staff(self, staff_id: int) -> int:
        """특정 직원의 총 방문 횟수"""
        try:
            count = (
                self.session.query(VisitLog)
                .filter(VisitLog.staff_id == staff_id)
                .count()
            )
            return count
        except Exception as e:
            logger.error(f"직원별 방문 횟수 조회 실패: {e}")
            raise
