"""
VisitLogService - 방문 일지 관리 비즈니스 로직

방문 일지 작성, 수정, 통계 조회 등의 유스케이스 구현
"""
from typing import List, Optional
from datetime import date, datetime

from src.service.base_service import BaseService
from src.domain.models import VisitLog
from src.repository import VisitLogRepository, ScheduleRepository, PatientRepository, StaffRepository
from src.config.database import DatabaseManager


class VisitLogService(BaseService[VisitLog]):
    """
    방문 일지 관리 서비스

    방문 일지 작성, 수정, 삭제 및 통계 조회 등의 비즈니스 로직 제공
    """

    def __init__(self, db_manager: DatabaseManager):
        super().__init__(db_manager)

    def create_visit_log(
        self,
        schedule_id: int,
        patient_id: int,
        staff_id: int,
        visit_date: date,
        check_in_time: Optional[datetime] = None,
        check_out_time: Optional[datetime] = None,
        service_content: Optional[str] = None,
        patient_condition: Optional[str] = None,
        special_notes: Optional[str] = None
    ) -> VisitLog:
        """
        새로운 방문 일지 생성

        Args:
            schedule_id: 일정 ID
            patient_id: 고객 ID
            staff_id: 직원 ID
            visit_date: 방문 날짜
            check_in_time: 출근 시간
            check_out_time: 퇴근 시간
            service_content: 서비스 내용
            patient_condition: 고객 상태
            special_notes: 특이사항

        Returns:
            VisitLog: 생성된 방문 일지 엔티티

        Raises:
            ValueError: 일정/고객/직원이 존재하지 않거나 중복된 일지가 있는 경우
        """
        with self.session_scope() as session:
            visit_log_repo = VisitLogRepository(session)
            schedule_repo = ScheduleRepository(session)
            patient_repo = PatientRepository(session)
            staff_repo = StaffRepository(session)

            # 비즈니스 규칙 1: 일정 존재 여부 확인
            schedule = schedule_repo.get_by_id(schedule_id)
            if not schedule:
                raise ValueError(f"존재하지 않는 일정입니다: ID {schedule_id}")

            # 비즈니스 규칙 2: 일정에 대한 방문 일지 중복 확인 (1:1 관계)
            existing_log = visit_log_repo.find_by_schedule_id(schedule_id)
            if existing_log:
                raise ValueError(
                    f"해당 일정에 대한 방문 일지가 이미 존재합니다: "
                    f"일정 ID {schedule_id}, 일지 ID {existing_log.id}"
                )

            # 비즈니스 규칙 3: 고객 존재 여부 확인
            patient = patient_repo.get_by_id(patient_id)
            if not patient:
                raise ValueError(f"존재하지 않는 고객입니다: ID {patient_id}")

            # 비즈니스 규칙 4: 직원 존재 여부 확인
            staff = staff_repo.get_by_id(staff_id)
            if not staff:
                raise ValueError(f"존재하지 않는 직원입니다: ID {staff_id}")

            # 비즈니스 규칙 5: 출퇴근 시간 유효성 검증
            if check_in_time and check_out_time:
                if check_in_time >= check_out_time:
                    raise ValueError(
                        f"출근 시간이 퇴근 시간보다 늦거나 같습니다: "
                        f"{check_in_time} >= {check_out_time}"
                    )

            # 방문 일지 엔티티 생성
            visit_log = VisitLog(
                schedule_id=schedule_id,
                patient_id=patient_id,
                staff_id=staff_id,
                visit_date=visit_date,
                check_in_time=check_in_time,
                check_out_time=check_out_time,
                service_content=service_content,
                patient_condition=patient_condition,
                special_notes=special_notes
            )

            created_log = visit_log_repo.create(visit_log)
            self.logger.info(
                f"방문 일지 생성 완료: ID {created_log.id}, "
                f"일정 ID {schedule_id}, 고객 {patient.name}, 직원 {staff.name}"
            )
            return created_log

    def get_visit_log_by_id(self, visit_log_id: int) -> Optional[VisitLog]:
        """
        ID로 방문 일지 조회

        Args:
            visit_log_id: 방문 일지 ID

        Returns:
            Optional[VisitLog]: 방문 일지 엔티티 또는 None
        """
        with self.session_scope() as session:
            repo = VisitLogRepository(session)
            return repo.get_by_id(visit_log_id)

    def get_visit_log_by_schedule(self, schedule_id: int) -> Optional[VisitLog]:
        """
        일정 ID로 방문 일지 조회

        Args:
            schedule_id: 일정 ID

        Returns:
            Optional[VisitLog]: 방문 일지 엔티티 또는 None
        """
        with self.session_scope() as session:
            repo = VisitLogRepository(session)
            return repo.find_by_schedule_id(schedule_id)

    def get_all_visit_logs(self, skip: int = 0, limit: int = 100) -> List[VisitLog]:
        """
        모든 방문 일지 조회

        Args:
            skip: 건너뛸 개수
            limit: 조회할 최대 개수

        Returns:
            List[VisitLog]: 방문 일지 리스트
        """
        with self.session_scope() as session:
            repo = VisitLogRepository(session)
            return repo.get_all(skip=skip, limit=limit)

    def update_visit_log(
        self,
        visit_log_id: int,
        check_in_time: Optional[datetime] = None,
        check_out_time: Optional[datetime] = None,
        service_content: Optional[str] = None,
        patient_condition: Optional[str] = None,
        special_notes: Optional[str] = None
    ) -> VisitLog:
        """
        방문 일지 수정

        Args:
            visit_log_id: 수정할 방문 일지 ID
            check_in_time: 출근 시간 (선택)
            check_out_time: 퇴근 시간 (선택)
            service_content: 서비스 내용 (선택)
            patient_condition: 고객 상태 (선택)
            special_notes: 특이사항 (선택)

        Returns:
            VisitLog: 수정된 방문 일지 엔티티

        Raises:
            ValueError: 일지를 찾을 수 없거나 유효하지 않은 시간인 경우
        """
        with self.session_scope() as session:
            repo = VisitLogRepository(session)

            visit_log = repo.get_by_id(visit_log_id)
            if not visit_log:
                raise ValueError(f"방문 일지를 찾을 수 없습니다: ID {visit_log_id}")

            # 수정할 값 결정
            new_check_in = check_in_time if check_in_time is not None else visit_log.check_in_time
            new_check_out = check_out_time if check_out_time is not None else visit_log.check_out_time

            # 출퇴근 시간 유효성 검증
            if new_check_in and new_check_out:
                if new_check_in >= new_check_out:
                    raise ValueError(
                        f"출근 시간이 퇴근 시간보다 늦거나 같습니다: "
                        f"{new_check_in} >= {new_check_out}"
                    )

            # 필드 업데이트
            if check_in_time is not None:
                visit_log.check_in_time = check_in_time
            if check_out_time is not None:
                visit_log.check_out_time = check_out_time
            if service_content is not None:
                visit_log.service_content = service_content
            if patient_condition is not None:
                visit_log.patient_condition = patient_condition
            if special_notes is not None:
                visit_log.special_notes = special_notes

            updated_log = repo.update(visit_log)
            self.logger.info(f"방문 일지 수정 완료: ID {visit_log_id}")
            return updated_log

    def delete_visit_log(self, visit_log_id: int) -> bool:
        """
        방문 일지 삭제

        Args:
            visit_log_id: 삭제할 방문 일지 ID

        Returns:
            bool: 성공 여부
        """
        with self.session_scope() as session:
            repo = VisitLogRepository(session)
            result = repo.delete(visit_log_id)
            if result:
                self.logger.info(f"방문 일지 삭제 완료: ID {visit_log_id}")
            return result

    def get_visit_logs_by_patient(self, patient_id: int) -> List[VisitLog]:
        """
        특정 고객의 모든 방문 일지 조회

        Args:
            patient_id: 고객 ID

        Returns:
            List[VisitLog]: 방문 일지 리스트
        """
        with self.session_scope() as session:
            repo = VisitLogRepository(session)
            return repo.find_by_patient_id(patient_id)

    def get_visit_logs_by_staff(self, staff_id: int) -> List[VisitLog]:
        """
        특정 직원의 모든 방문 일지 조회

        Args:
            staff_id: 직원 ID

        Returns:
            List[VisitLog]: 방문 일지 리스트
        """
        with self.session_scope() as session:
            repo = VisitLogRepository(session)
            return repo.find_by_staff_id(staff_id)

    def get_visit_logs_by_date(self, target_date: date) -> List[VisitLog]:
        """
        특정 날짜의 모든 방문 일지 조회

        Args:
            target_date: 조회할 날짜

        Returns:
            List[VisitLog]: 방문 일지 리스트
        """
        with self.session_scope() as session:
            repo = VisitLogRepository(session)
            return repo.find_by_date(target_date)

    def get_visit_logs_by_date_range(self, start_date: date, end_date: date) -> List[VisitLog]:
        """
        날짜 범위로 방문 일지 조회

        Args:
            start_date: 시작 날짜
            end_date: 종료 날짜

        Returns:
            List[VisitLog]: 방문 일지 리스트
        """
        with self.session_scope() as session:
            repo = VisitLogRepository(session)
            return repo.find_by_date_range(start_date, end_date)

    def get_visit_logs_by_patient_and_date_range(
        self,
        patient_id: int,
        start_date: date,
        end_date: date
    ) -> List[VisitLog]:
        """
        특정 고객의 특정 기간 방문 일지 조회

        Args:
            patient_id: 고객 ID
            start_date: 시작 날짜
            end_date: 종료 날짜

        Returns:
            List[VisitLog]: 방문 일지 리스트
        """
        with self.session_scope() as session:
            repo = VisitLogRepository(session)
            return repo.find_by_patient_and_date_range(patient_id, start_date, end_date)

    def get_visit_logs_by_staff_and_date_range(
        self,
        staff_id: int,
        start_date: date,
        end_date: date
    ) -> List[VisitLog]:
        """
        특정 직원의 특정 기간 방문 일지 조회

        Args:
            staff_id: 직원 ID
            start_date: 시작 날짜
            end_date: 종료 날짜

        Returns:
            List[VisitLog]: 방문 일지 리스트
        """
        with self.session_scope() as session:
            repo = VisitLogRepository(session)
            return repo.find_by_staff_and_date_range(staff_id, start_date, end_date)

    def get_incomplete_logs(self) -> List[VisitLog]:
        """
        미작성 방문 일지 조회

        출퇴근 시간이나 서비스 내용이 작성되지 않은 일지

        Returns:
            List[VisitLog]: 미작성 방문 일지 리스트
        """
        with self.session_scope() as session:
            repo = VisitLogRepository(session)
            return repo.find_incomplete_logs()

    def get_patient_visit_count(self, patient_id: int) -> int:
        """
        특정 고객의 총 방문 횟수

        Args:
            patient_id: 고객 ID

        Returns:
            int: 방문 횟수
        """
        with self.session_scope() as session:
            repo = VisitLogRepository(session)
            return repo.count_by_patient(patient_id)

    def get_staff_visit_count(self, staff_id: int) -> int:
        """
        특정 직원의 총 방문 횟수

        Args:
            staff_id: 직원 ID

        Returns:
            int: 방문 횟수
        """
        with self.session_scope() as session:
            repo = VisitLogRepository(session)
            return repo.count_by_staff(staff_id)

    def check_in(self, visit_log_id: int, check_in_time: datetime) -> VisitLog:
        """
        출근 체크인

        Args:
            visit_log_id: 방문 일지 ID
            check_in_time: 출근 시간

        Returns:
            VisitLog: 업데이트된 방문 일지
        """
        return self.update_visit_log(visit_log_id, check_in_time=check_in_time)

    def check_out(self, visit_log_id: int, check_out_time: datetime) -> VisitLog:
        """
        퇴근 체크아웃

        Args:
            visit_log_id: 방문 일지 ID
            check_out_time: 퇴근 시간

        Returns:
            VisitLog: 업데이트된 방문 일지
        """
        return self.update_visit_log(visit_log_id, check_out_time=check_out_time)
