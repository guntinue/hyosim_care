"""
ScheduleService - 일정 관리 비즈니스 로직

일정 생성, 수정, 삭제 및 시간 충돌 검증 등의 유스케이스 구현
"""
from typing import List, Optional
from datetime import date, time

from src.service.base_service import BaseService
from src.domain.models import Schedule, ServiceType
from src.repository import ScheduleRepository, PatientRepository, StaffRepository
from src.config.database import DatabaseManager


class ScheduleService(BaseService[Schedule]):
    """
    일정 관리 서비스

    일정 생성, 수정, 삭제 및 시간 충돌 검증 등의 비즈니스 로직 제공
    """

    def __init__(self, db_manager: DatabaseManager):
        super().__init__(db_manager)

    def create_schedule(
        self,
        patient_id: int,
        staff_id: int,
        schedule_date: date,
        start_time: time,
        end_time: time,
        service_type: ServiceType,
        notes: Optional[str] = None
    ) -> Schedule:
        """
        새로운 일정 생성

        Args:
            patient_id: 고객 ID
            staff_id: 직원 ID
            schedule_date: 방문 날짜
            start_time: 시작 시간
            end_time: 종료 시간
            service_type: 서비스 유형
            notes: 일정 메모

        Returns:
            Schedule: 생성된 일정 엔티티

        Raises:
            ValueError: 시간 충돌, 존재하지 않는 고객/직원, 잘못된 시간 등
        """
        with self.session_scope() as session:
            schedule_repo = ScheduleRepository(session)
            patient_repo = PatientRepository(session)
            staff_repo = StaffRepository(session)

            # 비즈니스 규칙 1: 고객 존재 여부 확인
            patient = patient_repo.get_by_id(patient_id)
            if not patient:
                raise ValueError(f"존재하지 않는 고객입니다: ID {patient_id}")
            if not patient.is_active:
                raise ValueError(f"비활성화된 고객입니다: {patient.name} (ID {patient_id})")

            # 비즈니스 규칙 2: 직원 존재 여부 확인
            staff = staff_repo.get_by_id(staff_id)
            if not staff:
                raise ValueError(f"존재하지 않는 직원입니다: ID {staff_id}")
            if not staff.is_active:
                raise ValueError(f"재직 중이 아닌 직원입니다: {staff.name} (ID {staff_id})")

            # 비즈니스 규칙 3: 시간 유효성 검증
            if start_time >= end_time:
                raise ValueError(f"시작 시간이 종료 시간보다 늦거나 같습니다: {start_time} >= {end_time}")

            # 비즈니스 규칙 4: 직원 일정 시간 충돌 검사 ⭐ 핵심 로직
            if schedule_repo.check_staff_time_conflict(
                staff_id=staff_id,
                schedule_date=schedule_date,
                start_time=start_time,
                end_time=end_time
            ):
                raise ValueError(
                    f"직원의 일정이 충돌합니다: {staff.name} - {schedule_date} {start_time}~{end_time}"
                )

            # 비즈니스 규칙 5: 고객 일정 시간 충돌 검사
            if schedule_repo.check_patient_time_conflict(
                patient_id=patient_id,
                schedule_date=schedule_date,
                start_time=start_time,
                end_time=end_time
            ):
                raise ValueError(
                    f"고객의 일정이 충돌합니다: {patient.name} - {schedule_date} {start_time}~{end_time}"
                )

            # 일정 엔티티 생성
            schedule = Schedule(
                patient_id=patient_id,
                staff_id=staff_id,
                schedule_date=schedule_date,
                start_time=start_time,
                end_time=end_time,
                service_type=service_type,
                notes=notes,
                is_completed=False
            )

            created_schedule = schedule_repo.create(schedule)
            self.logger.info(
                f"일정 생성 완료: ID {created_schedule.id}, "
                f"고객 {patient.name}, 직원 {staff.name}, "
                f"{schedule_date} {start_time}~{end_time}"
            )
            return created_schedule

    def get_schedule_by_id(self, schedule_id: int) -> Optional[Schedule]:
        """
        ID로 일정 조회

        Args:
            schedule_id: 일정 ID

        Returns:
            Optional[Schedule]: 일정 엔티티 또는 None
        """
        with self.session_scope() as session:
            repo = ScheduleRepository(session)
            return repo.get_by_id(schedule_id)

    def get_all_schedules(self, skip: int = 0, limit: int = 100) -> List[Schedule]:
        """
        모든 일정 조회

        Args:
            skip: 건너뛸 개수
            limit: 조회할 최대 개수

        Returns:
            List[Schedule]: 일정 리스트
        """
        with self.session_scope() as session:
            repo = ScheduleRepository(session)
            return repo.get_all(skip=skip, limit=limit)

    def update_schedule(
        self,
        schedule_id: int,
        patient_id: Optional[int] = None,
        staff_id: Optional[int] = None,
        schedule_date: Optional[date] = None,
        start_time: Optional[time] = None,
        end_time: Optional[time] = None,
        service_type: Optional[ServiceType] = None,
        notes: Optional[str] = None,
        is_completed: Optional[bool] = None
    ) -> Schedule:
        """
        일정 수정

        Args:
            schedule_id: 수정할 일정 ID
            patient_id: 고객 ID (선택)
            staff_id: 직원 ID (선택)
            schedule_date: 방문 날짜 (선택)
            start_time: 시작 시간 (선택)
            end_time: 종료 시간 (선택)
            service_type: 서비스 유형 (선택)
            notes: 일정 메모 (선택)
            is_completed: 완료 여부 (선택)

        Returns:
            Schedule: 수정된 일정 엔티티

        Raises:
            ValueError: 일정을 찾을 수 없거나 충돌이 발생하는 경우
        """
        with self.session_scope() as session:
            schedule_repo = ScheduleRepository(session)
            patient_repo = PatientRepository(session)
            staff_repo = StaffRepository(session)

            schedule = schedule_repo.get_by_id(schedule_id)
            if not schedule:
                raise ValueError(f"일정을 찾을 수 없습니다: ID {schedule_id}")

            # 수정할 값 결정 (기존 값 유지)
            new_patient_id = patient_id if patient_id is not None else schedule.patient_id
            new_staff_id = staff_id if staff_id is not None else schedule.staff_id
            new_schedule_date = schedule_date if schedule_date is not None else schedule.schedule_date
            new_start_time = start_time if start_time is not None else schedule.start_time
            new_end_time = end_time if end_time is not None else schedule.end_time

            # 고객/직원 변경 시 존재 여부 확인
            if patient_id is not None and patient_id != schedule.patient_id:
                patient = patient_repo.get_by_id(patient_id)
                if not patient or not patient.is_active:
                    raise ValueError(f"유효하지 않은 고객입니다: ID {patient_id}")

            if staff_id is not None and staff_id != schedule.staff_id:
                staff = staff_repo.get_by_id(staff_id)
                if not staff or not staff.is_active:
                    raise ValueError(f"유효하지 않은 직원입니다: ID {staff_id}")

            # 시간 유효성 검증
            if new_start_time >= new_end_time:
                raise ValueError(f"시작 시간이 종료 시간보다 늦거나 같습니다: {new_start_time} >= {new_end_time}")

            # 직원 일정 충돌 검사 (자기 자신 제외)
            if schedule_repo.check_staff_time_conflict(
                staff_id=new_staff_id,
                schedule_date=new_schedule_date,
                start_time=new_start_time,
                end_time=new_end_time,
                exclude_schedule_id=schedule_id
            ):
                raise ValueError(
                    f"직원의 일정이 충돌합니다: ID {new_staff_id} - "
                    f"{new_schedule_date} {new_start_time}~{new_end_time}"
                )

            # 고객 일정 충돌 검사 (자기 자신 제외)
            if schedule_repo.check_patient_time_conflict(
                patient_id=new_patient_id,
                schedule_date=new_schedule_date,
                start_time=new_start_time,
                end_time=new_end_time,
                exclude_schedule_id=schedule_id
            ):
                raise ValueError(
                    f"고객의 일정이 충돌합니다: ID {new_patient_id} - "
                    f"{new_schedule_date} {new_start_time}~{new_end_time}"
                )

            # 필드 업데이트
            if patient_id is not None:
                schedule.patient_id = patient_id
            if staff_id is not None:
                schedule.staff_id = staff_id
            if schedule_date is not None:
                schedule.schedule_date = schedule_date
            if start_time is not None:
                schedule.start_time = start_time
            if end_time is not None:
                schedule.end_time = end_time
            if service_type is not None:
                schedule.service_type = service_type
            if notes is not None:
                schedule.notes = notes
            if is_completed is not None:
                schedule.is_completed = is_completed

            updated_schedule = schedule_repo.update(schedule)
            self.logger.info(f"일정 수정 완료: ID {schedule_id}")
            return updated_schedule

    def delete_schedule(self, schedule_id: int) -> bool:
        """
        일정 삭제

        Args:
            schedule_id: 삭제할 일정 ID

        Returns:
            bool: 성공 여부
        """
        with self.session_scope() as session:
            repo = ScheduleRepository(session)
            result = repo.delete(schedule_id)
            if result:
                self.logger.info(f"일정 삭제 완료: ID {schedule_id}")
            return result

    def complete_schedule(self, schedule_id: int) -> Schedule:
        """
        일정 완료 처리

        Args:
            schedule_id: 완료 처리할 일정 ID

        Returns:
            Schedule: 완료 처리된 일정

        Raises:
            ValueError: 일정을 찾을 수 없는 경우
        """
        return self.update_schedule(schedule_id, is_completed=True)

    def get_schedules_by_patient(self, patient_id: int) -> List[Schedule]:
        """
        특정 고객의 모든 일정 조회

        Args:
            patient_id: 고객 ID

        Returns:
            List[Schedule]: 일정 리스트
        """
        with self.session_scope() as session:
            repo = ScheduleRepository(session)
            return repo.find_by_patient_id(patient_id)

    def get_schedules_by_staff(self, staff_id: int) -> List[Schedule]:
        """
        특정 직원의 모든 일정 조회

        Args:
            staff_id: 직원 ID

        Returns:
            List[Schedule]: 일정 리스트
        """
        with self.session_scope() as session:
            repo = ScheduleRepository(session)
            return repo.find_by_staff_id(staff_id)

    def get_schedules_by_date(self, target_date: date) -> List[Schedule]:
        """
        특정 날짜의 모든 일정 조회

        Args:
            target_date: 조회할 날짜

        Returns:
            List[Schedule]: 일정 리스트
        """
        with self.session_scope() as session:
            repo = ScheduleRepository(session)
            return repo.find_by_date(target_date)

    def get_schedules_by_date_range(self, start_date: date, end_date: date) -> List[Schedule]:
        """
        날짜 범위로 일정 조회

        Args:
            start_date: 시작 날짜
            end_date: 종료 날짜

        Returns:
            List[Schedule]: 일정 리스트
        """
        with self.session_scope() as session:
            repo = ScheduleRepository(session)
            return repo.find_by_date_range(start_date, end_date)

    def get_staff_schedule_by_date(self, staff_id: int, target_date: date) -> List[Schedule]:
        """
        특정 직원의 특정 날짜 일정 조회

        Args:
            staff_id: 직원 ID
            target_date: 조회할 날짜

        Returns:
            List[Schedule]: 일정 리스트
        """
        with self.session_scope() as session:
            repo = ScheduleRepository(session)
            return repo.find_by_staff_and_date(staff_id, target_date)

    def get_patient_schedule_by_date(self, patient_id: int, target_date: date) -> List[Schedule]:
        """
        특정 고객의 특정 날짜 일정 조회

        Args:
            patient_id: 고객 ID
            target_date: 조회할 날짜

        Returns:
            List[Schedule]: 일정 리스트
        """
        with self.session_scope() as session:
            repo = ScheduleRepository(session)
            return repo.find_by_patient_and_date(patient_id, target_date)

    def get_incomplete_schedules(self) -> List[Schedule]:
        """
        미완료 일정 조회

        Returns:
            List[Schedule]: 미완료 일정 리스트
        """
        with self.session_scope() as session:
            repo = ScheduleRepository(session)
            return repo.find_incomplete_schedules()

    def get_completed_schedules(self) -> List[Schedule]:
        """
        완료된 일정 조회

        Returns:
            List[Schedule]: 완료된 일정 리스트
        """
        with self.session_scope() as session:
            repo = ScheduleRepository(session)
            return repo.find_completed_schedules()

    def get_schedules_by_service_type(self, service_type: ServiceType) -> List[Schedule]:
        """
        서비스 유형별 일정 조회

        Args:
            service_type: 서비스 유형

        Returns:
            List[Schedule]: 일정 리스트
        """
        with self.session_scope() as session:
            repo = ScheduleRepository(session)
            return repo.find_by_service_type(service_type)
