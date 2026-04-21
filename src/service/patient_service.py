"""
PatientService - 고객 관리 비즈니스 로직

고객 등록, 수정, 검색 등의 유스케이스 구현
"""
from typing import List, Optional
from datetime import date

from src.service.base_service import BaseService
from src.domain.models import Patient, ServiceType
from src.repository import PatientRepository
from src.config.database import DatabaseManager


class PatientService(BaseService[Patient]):
    """
    고객(환자) 관리 서비스

    고객 등록, 수정, 삭제, 검색 등의 비즈니스 로직 제공
    """

    def __init__(self, db_manager: DatabaseManager):
        super().__init__(db_manager)

    def create_patient(
        self,
        name: str,
        birth_date: date,
        phone: str,
        address: str,
        service_type: ServiceType = ServiceType.HOME_CARE,
        care_grade: Optional[str] = None,
        guardian_name: Optional[str] = None,
        guardian_phone: Optional[str] = None,
        guardian_relation: Optional[str] = None,
        medical_info: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Patient:
        """
        새로운 고객 등록

        Args:
            name: 고객명
            birth_date: 생년월일
            phone: 연락처
            address: 주소
            service_type: 서비스 유형 (방문요양/데이케어)
            care_grade: 등급 (1~5등급, 인지지원등급 등)
            guardian_name: 보호자명
            guardian_phone: 보호자 연락처
            guardian_relation: 보호자 관계
            medical_info: 의료 정보 및 특이사항
            notes: 메모

        Returns:
            Patient: 생성된 고객 엔티티

        Raises:
            ValueError: 중복된 전화번호가 이미 존재하는 경우
        """
        with self.session_scope() as session:
            repo = PatientRepository(session)

            # 비즈니스 규칙: 전화번호 중복 확인
            existing_patient = repo.find_by_phone(phone)
            if existing_patient:
                self.logger.warning(f"전화번호 중복: {phone} (기존 고객 ID: {existing_patient.id})")
                raise ValueError(f"이미 등록된 전화번호입니다: {phone} (고객명: {existing_patient.name})")

            # 고객 엔티티 생성
            patient = Patient(
                name=name,
                birth_date=birth_date,
                phone=phone,
                address=address,
                service_type=service_type,
                care_grade=care_grade,
                guardian_name=guardian_name,
                guardian_phone=guardian_phone,
                guardian_relation=guardian_relation,
                medical_info=medical_info,
                notes=notes,
                is_active=True
            )

            created_patient = repo.create(patient)
            self.logger.info(f"고객 등록 완료: {created_patient.name} (ID: {created_patient.id})")
            return created_patient

    def get_patient_by_id(self, patient_id: int) -> Optional[Patient]:
        """
        ID로 고객 조회

        Args:
            patient_id: 고객 ID

        Returns:
            Optional[Patient]: 고객 엔티티 또는 None
        """
        with self.session_scope() as session:
            repo = PatientRepository(session)
            return repo.get_by_id(patient_id)

    def get_all_patients(self, skip: int = 0, limit: int = 100) -> List[Patient]:
        """
        모든 활성 고객 조회

        Args:
            skip: 건너뛸 개수
            limit: 조회할 최대 개수

        Returns:
            List[Patient]: 고객 리스트
        """
        with self.session_scope() as session:
            repo = PatientRepository(session)
            return repo.get_all(skip=skip, limit=limit)

    def update_patient(
        self,
        patient_id: int,
        name: Optional[str] = None,
        birth_date: Optional[date] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        service_type: Optional[ServiceType] = None,
        care_grade: Optional[str] = None,
        guardian_name: Optional[str] = None,
        guardian_phone: Optional[str] = None,
        guardian_relation: Optional[str] = None,
        medical_info: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Patient:
        """
        고객 정보 수정

        Args:
            patient_id: 수정할 고객 ID
            name: 고객명 (선택)
            birth_date: 생년월일 (선택)
            phone: 연락처 (선택)
            address: 주소 (선택)
            service_type: 서비스 유형 (선택)
            care_grade: 등급 (선택)
            guardian_name: 보호자명 (선택)
            guardian_phone: 보호자 연락처 (선택)
            guardian_relation: 보호자 관계 (선택)
            medical_info: 의료 정보 (선택)
            notes: 메모 (선택)

        Returns:
            Patient: 수정된 고객 엔티티

        Raises:
            ValueError: 고객을 찾을 수 없거나 전화번호가 중복되는 경우
        """
        with self.session_scope() as session:
            repo = PatientRepository(session)

            patient = repo.get_by_id(patient_id)
            if not patient:
                raise ValueError(f"고객을 찾을 수 없습니다: ID {patient_id}")

            # 전화번호 변경 시 중복 확인
            if phone and phone != patient.phone:
                existing = repo.find_by_phone(phone)
                if existing:
                    raise ValueError(f"이미 등록된 전화번호입니다: {phone}")

            # 필드 업데이트 (None이 아닌 값만)
            if name is not None:
                patient.name = name
            if birth_date is not None:
                patient.birth_date = birth_date
            if phone is not None:
                patient.phone = phone
            if address is not None:
                patient.address = address
            if service_type is not None:
                patient.service_type = service_type
            if care_grade is not None:
                patient.care_grade = care_grade
            if guardian_name is not None:
                patient.guardian_name = guardian_name
            if guardian_phone is not None:
                patient.guardian_phone = guardian_phone
            if guardian_relation is not None:
                patient.guardian_relation = guardian_relation
            if medical_info is not None:
                patient.medical_info = medical_info
            if notes is not None:
                patient.notes = notes

            updated_patient = repo.update(patient)
            self.logger.info(f"고객 정보 수정 완료: {updated_patient.name} (ID: {patient_id})")
            return updated_patient

    def deactivate_patient(self, patient_id: int) -> bool:
        """
        고객 비활성화 (Soft Delete)

        Args:
            patient_id: 비활성화할 고객 ID

        Returns:
            bool: 성공 여부
        """
        with self.session_scope() as session:
            repo = PatientRepository(session)
            result = repo.delete(patient_id)
            if result:
                self.logger.info(f"고객 비활성화 완료: ID {patient_id}")
            return result

    def search_patients_by_name(self, name: str) -> List[Patient]:
        """
        이름으로 고객 검색

        Args:
            name: 검색할 이름 (부분 일치)

        Returns:
            List[Patient]: 검색 결과
        """
        with self.session_scope() as session:
            repo = PatientRepository(session)
            return repo.find_by_name(name)

    def get_patient_by_phone(self, phone: str) -> Optional[Patient]:
        """
        전화번호로 고객 조회

        Args:
            phone: 전화번호

        Returns:
            Optional[Patient]: 고객 엔티티 또는 None
        """
        with self.session_scope() as session:
            repo = PatientRepository(session)
            return repo.find_by_phone(phone)

    def get_patients_by_service_type(self, service_type: ServiceType) -> List[Patient]:
        """
        서비스 유형별 고객 조회

        Args:
            service_type: 서비스 유형 (방문요양/데이케어)

        Returns:
            List[Patient]: 고객 리스트
        """
        with self.session_scope() as session:
            repo = PatientRepository(session)
            return repo.find_by_service_type(service_type)

    def get_patients_by_care_grade(self, care_grade: str) -> List[Patient]:
        """
        등급별 고객 조회

        Args:
            care_grade: 등급 (예: "1등급", "2등급" 등)

        Returns:
            List[Patient]: 고객 리스트
        """
        with self.session_scope() as session:
            repo = PatientRepository(session)
            return repo.find_by_care_grade(care_grade)

    def get_patient_count(self) -> int:
        """
        활성 고객 수 조회

        Returns:
            int: 활성 고객 수
        """
        with self.session_scope() as session:
            repo = PatientRepository(session)
            return repo.count()

    def get_home_care_patients(self) -> List[Patient]:
        """
        방문요양 고객 조회 (자주 사용되는 쿼리)

        Returns:
            List[Patient]: 방문요양 고객 리스트
        """
        return self.get_patients_by_service_type(ServiceType.HOME_CARE)

    def get_day_care_patients(self) -> List[Patient]:
        """
        데이케어 고객 조회

        Returns:
            List[Patient]: 데이케어 고객 리스트
        """
        return self.get_patients_by_service_type(ServiceType.DAY_CARE)
