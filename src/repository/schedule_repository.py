"""
Schedule Repository 구현
일정 데이터 액세스 레이어
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import date, time, datetime

from src.domain.models import Schedule, ServiceType
from src.repository.base import BaseRepository
from src.config.settings import logger


class ScheduleRepository(BaseRepository[Schedule]):
    """
    Schedule Repository 구현체

    일정 데이터에 대한 CRUD 및 비즈니스 쿼리 제공
    중복 일정 검증 등 핵심 비즈니스 로직 포함
    """

    def __init__(self, session: Session):
        """
        Args:
            session: SQLAlchemy 세션
        """
        self.session = session

    def create(self, entity: Schedule) -> Schedule:
        """일정 생성"""
        try:
            self.session.add(entity)
            self.session.flush()
            logger.info(
                f"일정 생성 성공: 날짜={entity.schedule_date}, "
                f"고객ID={entity.patient_id}, 직원ID={entity.staff_id}"
            )
            return entity
        except Exception as e:
            logger.error(f"일정 생성 실패: {e}")
            raise

    def get_by_id(self, entity_id: int) -> Optional[Schedule]:
        """ID로 일정 조회"""
        try:
            schedule = self.session.query(Schedule).filter(Schedule.id == entity_id).first()
            if schedule:
                logger.debug(f"일정 조회 성공: ID {entity_id}")
            else:
                logger.warning(f"일정을 찾을 수 없음: ID {entity_id}")
            return schedule
        except Exception as e:
            logger.error(f"일정 조회 실패: {e}")
            raise

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Schedule]:
        """모든 일정 조회 (최신순)"""
        try:
            schedules = (
                self.session.query(Schedule)
                .order_by(Schedule.schedule_date.desc(), Schedule.start_time.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            logger.debug(f"일정 목록 조회 성공: {len(schedules)}개")
            return schedules
        except Exception as e:
            logger.error(f"일정 목록 조회 실패: {e}")
            raise

    def update(self, entity: Schedule) -> Schedule:
        """일정 수정"""
        try:
            merged_entity = self.session.merge(entity)
            self.session.flush()
            logger.info(f"일정 수정 성공: ID {merged_entity.id}")
            return merged_entity
        except Exception as e:
            logger.error(f"일정 수정 실패: {e}")
            raise

    def delete(self, entity_id: int) -> bool:
        """일정 삭제 (Hard Delete - 일정은 물리적 삭제)"""
        try:
            schedule = self.get_by_id(entity_id)
            if schedule:
                self.session.delete(schedule)
                self.session.flush()
                logger.info(f"일정 삭제 성공: ID {entity_id}")
                return True
            else:
                logger.warning(f"삭제할 일정을 찾을 수 없음: ID {entity_id}")
                return False
        except Exception as e:
            logger.error(f"일정 삭제 실패: {e}")
            raise

    def count(self) -> int:
        """전체 일정 개수 조회"""
        try:
            count = self.session.query(Schedule).count()
            return count
        except Exception as e:
            logger.error(f"일정 수 조회 실패: {e}")
            raise

    # === 비즈니스 쿼리 메서드 ===

    def find_by_patient_id(self, patient_id: int) -> List[Schedule]:
        """특정 고객의 모든 일정 조회"""
        try:
            schedules = (
                self.session.query(Schedule)
                .filter(Schedule.patient_id == patient_id)
                .order_by(Schedule.schedule_date.desc())
                .all()
            )
            return schedules
        except Exception as e:
            logger.error(f"고객별 일정 조회 실패: {e}")
            raise

    def find_by_staff_id(self, staff_id: int) -> List[Schedule]:
        """특정 직원의 모든 일정 조회"""
        try:
            schedules = (
                self.session.query(Schedule)
                .filter(Schedule.staff_id == staff_id)
                .order_by(Schedule.schedule_date.desc())
                .all()
            )
            return schedules
        except Exception as e:
            logger.error(f"직원별 일정 조회 실패: {e}")
            raise

    def find_by_date(self, target_date: date) -> List[Schedule]:
        """특정 날짜의 모든 일정 조회"""
        try:
            schedules = (
                self.session.query(Schedule)
                .filter(Schedule.schedule_date == target_date)
                .order_by(Schedule.start_time)
                .all()
            )
            logger.debug(f"{target_date} 일정: {len(schedules)}개")
            return schedules
        except Exception as e:
            logger.error(f"날짜별 일정 조회 실패: {e}")
            raise

    def find_by_date_range(self, start_date: date, end_date: date) -> List[Schedule]:
        """날짜 범위로 일정 조회"""
        try:
            schedules = (
                self.session.query(Schedule)
                .filter(Schedule.schedule_date.between(start_date, end_date))
                .order_by(Schedule.schedule_date, Schedule.start_time)
                .all()
            )
            return schedules
        except Exception as e:
            logger.error(f"날짜 범위 일정 조회 실패: {e}")
            raise

    def find_by_staff_and_date(self, staff_id: int, target_date: date) -> List[Schedule]:
        """특정 직원의 특정 날짜 일정 조회"""
        try:
            schedules = (
                self.session.query(Schedule)
                .filter(
                    and_(
                        Schedule.staff_id == staff_id,
                        Schedule.schedule_date == target_date
                    )
                )
                .order_by(Schedule.start_time)
                .all()
            )
            return schedules
        except Exception as e:
            logger.error(f"직원별 날짜 일정 조회 실패: {e}")
            raise

    def find_by_patient_and_date(self, patient_id: int, target_date: date) -> List[Schedule]:
        """특정 고객의 특정 날짜 일정 조회"""
        try:
            schedules = (
                self.session.query(Schedule)
                .filter(
                    and_(
                        Schedule.patient_id == patient_id,
                        Schedule.schedule_date == target_date
                    )
                )
                .order_by(Schedule.start_time)
                .all()
            )
            return schedules
        except Exception as e:
            logger.error(f"고객별 날짜 일정 조회 실패: {e}")
            raise

    def find_incomplete_schedules(self) -> List[Schedule]:
        """미완료 일정 조회"""
        try:
            schedules = (
                self.session.query(Schedule)
                .filter(Schedule.is_completed == False)
                .order_by(Schedule.schedule_date, Schedule.start_time)
                .all()
            )
            return schedules
        except Exception as e:
            logger.error(f"미완료 일정 조회 실패: {e}")
            raise

    def find_completed_schedules(self) -> List[Schedule]:
        """완료된 일정 조회"""
        try:
            schedules = (
                self.session.query(Schedule)
                .filter(Schedule.is_completed == True)
                .order_by(Schedule.schedule_date.desc())
                .all()
            )
            return schedules
        except Exception as e:
            logger.error(f"완료 일정 조회 실패: {e}")
            raise

    def find_by_service_type(self, service_type: ServiceType) -> List[Schedule]:
        """서비스 유형별 일정 조회"""
        try:
            schedules = (
                self.session.query(Schedule)
                .filter(Schedule.service_type == service_type)
                .order_by(Schedule.schedule_date.desc())
                .all()
            )
            return schedules
        except Exception as e:
            logger.error(f"서비스 유형별 일정 조회 실패: {e}")
            raise

    def check_staff_time_conflict(
        self,
        staff_id: int,
        schedule_date: date,
        start_time: time,
        end_time: time,
        exclude_schedule_id: Optional[int] = None
    ) -> bool:
        """
        직원 일정 시간 충돌 검사

        중요: 같은 날짜에 같은 직원이 겹치는 시간대에 다른 일정이 있는지 확인

        Args:
            staff_id: 직원 ID
            schedule_date: 일정 날짜
            start_time: 시작 시간
            end_time: 종료 시간
            exclude_schedule_id: 수정 시 제외할 일정 ID (자기 자신 제외)

        Returns:
            bool: 충돌 있음(True), 충돌 없음(False)
        """
        try:
            query = self.session.query(Schedule).filter(
                and_(
                    Schedule.staff_id == staff_id,
                    Schedule.schedule_date == schedule_date,
                    or_(
                        # 새 일정의 시작 시간이 기존 일정 시간대 안에 있음
                        and_(
                            Schedule.start_time <= start_time,
                            Schedule.end_time > start_time
                        ),
                        # 새 일정의 종료 시간이 기존 일정 시간대 안에 있음
                        and_(
                            Schedule.start_time < end_time,
                            Schedule.end_time >= end_time
                        ),
                        # 새 일정이 기존 일정을 완전히 포함
                        and_(
                            Schedule.start_time >= start_time,
                            Schedule.end_time <= end_time
                        )
                    )
                )
            )

            # 수정 시 자기 자신 제외
            if exclude_schedule_id:
                query = query.filter(Schedule.id != exclude_schedule_id)

            conflicting_schedule = query.first()

            if conflicting_schedule:
                logger.warning(
                    f"직원 일정 충돌 감지: 직원ID={staff_id}, "
                    f"날짜={schedule_date}, 시간={start_time}-{end_time}"
                )
                return True

            return False

        except Exception as e:
            logger.error(f"일정 충돌 검사 실패: {e}")
            raise

    def check_patient_time_conflict(
        self,
        patient_id: int,
        schedule_date: date,
        start_time: time,
        end_time: time,
        exclude_schedule_id: Optional[int] = None
    ) -> bool:
        """
        고객 일정 시간 충돌 검사

        같은 날짜에 같은 고객이 겹치는 시간대에 다른 일정이 있는지 확인

        Args:
            patient_id: 고객 ID
            schedule_date: 일정 날짜
            start_time: 시작 시간
            end_time: 종료 시간
            exclude_schedule_id: 수정 시 제외할 일정 ID

        Returns:
            bool: 충돌 있음(True), 충돌 없음(False)
        """
        try:
            query = self.session.query(Schedule).filter(
                and_(
                    Schedule.patient_id == patient_id,
                    Schedule.schedule_date == schedule_date,
                    or_(
                        and_(
                            Schedule.start_time <= start_time,
                            Schedule.end_time > start_time
                        ),
                        and_(
                            Schedule.start_time < end_time,
                            Schedule.end_time >= end_time
                        ),
                        and_(
                            Schedule.start_time >= start_time,
                            Schedule.end_time <= end_time
                        )
                    )
                )
            )

            if exclude_schedule_id:
                query = query.filter(Schedule.id != exclude_schedule_id)

            conflicting_schedule = query.first()

            if conflicting_schedule:
                logger.warning(
                    f"고객 일정 충돌 감지: 고객ID={patient_id}, "
                    f"날짜={schedule_date}, 시간={start_time}-{end_time}"
                )
                return True

            return False

        except Exception as e:
            logger.error(f"일정 충돌 검사 실패: {e}")
            raise
