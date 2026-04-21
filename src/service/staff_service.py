"""
StaffService - 직원 관리 비즈니스 로직

직원 등록, 수정, 검색 등의 유스케이스 구현
"""
from typing import List, Optional
from datetime import date

from src.service.base_service import BaseService
from src.domain.models import Staff, StaffRole
from src.repository import StaffRepository
from src.config.database import DatabaseManager


class StaffService(BaseService[Staff]):
    """
    직원 관리 서비스

    직원 등록, 수정, 삭제, 검색 등의 비즈니스 로직 제공
    """

    def __init__(self, db_manager: DatabaseManager):
        super().__init__(db_manager)

    def create_staff(
        self,
        name: str,
        role: StaffRole,
        phone: str,
        hire_date: date,
        email: Optional[str] = None,
        license_number: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Staff:
        """
        새로운 직원 등록

        Args:
            name: 직원명
            role: 직원 역할 (요양보호사/사회복지사/간호사/관리자)
            phone: 연락처
            hire_date: 입사일
            email: 이메일
            license_number: 자격증 번호
            notes: 메모

        Returns:
            Staff: 생성된 직원 엔티티

        Raises:
            ValueError: 중복된 전화번호 또는 자격증 번호가 존재하는 경우
        """
        with self.session_scope() as session:
            repo = StaffRepository(session)

            # 비즈니스 규칙: 전화번호 중복 확인
            existing_staff = repo.find_by_phone(phone)
            if existing_staff:
                self.logger.warning(f"전화번호 중복: {phone} (기존 직원 ID: {existing_staff.id})")
                raise ValueError(f"이미 등록된 전화번호입니다: {phone} (직원명: {existing_staff.name})")

            # 비즈니스 규칙: 자격증 번호 중복 확인 (있는 경우)
            if license_number:
                existing_license = repo.find_by_license_number(license_number)
                if existing_license:
                    self.logger.warning(
                        f"자격증 번호 중복: {license_number} (기존 직원 ID: {existing_license.id})"
                    )
                    raise ValueError(
                        f"이미 등록된 자격증 번호입니다: {license_number} (직원명: {existing_license.name})"
                    )

            # 직원 엔티티 생성
            staff = Staff(
                name=name,
                role=role,
                phone=phone,
                email=email,
                license_number=license_number,
                hire_date=hire_date,
                notes=notes,
                is_active=True
            )

            created_staff = repo.create(staff)
            self.logger.info(
                f"직원 등록 완료: {created_staff.name} (ID: {created_staff.id}, 역할: {role.value})"
            )
            return created_staff

    def get_staff_by_id(self, staff_id: int) -> Optional[Staff]:
        """
        ID로 직원 조회

        Args:
            staff_id: 직원 ID

        Returns:
            Optional[Staff]: 직원 엔티티 또는 None
        """
        with self.session_scope() as session:
            repo = StaffRepository(session)
            return repo.get_by_id(staff_id)

    def get_all_staff(self, skip: int = 0, limit: int = 100) -> List[Staff]:
        """
        모든 재직 중인 직원 조회

        Args:
            skip: 건너뛸 개수
            limit: 조회할 최대 개수

        Returns:
            List[Staff]: 직원 리스트
        """
        with self.session_scope() as session:
            repo = StaffRepository(session)
            return repo.get_all(skip=skip, limit=limit)

    def update_staff(
        self,
        staff_id: int,
        name: Optional[str] = None,
        role: Optional[StaffRole] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        license_number: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Staff:
        """
        직원 정보 수정

        Args:
            staff_id: 수정할 직원 ID
            name: 직원명 (선택)
            role: 직원 역할 (선택)
            phone: 연락처 (선택)
            email: 이메일 (선택)
            license_number: 자격증 번호 (선택)
            notes: 메모 (선택)

        Returns:
            Staff: 수정된 직원 엔티티

        Raises:
            ValueError: 직원을 찾을 수 없거나 중복된 정보가 있는 경우
        """
        with self.session_scope() as session:
            repo = StaffRepository(session)

            staff = repo.get_by_id(staff_id)
            if not staff:
                raise ValueError(f"직원을 찾을 수 없습니다: ID {staff_id}")

            # 전화번호 변경 시 중복 확인
            if phone and phone != staff.phone:
                existing = repo.find_by_phone(phone)
                if existing:
                    raise ValueError(f"이미 등록된 전화번호입니다: {phone}")

            # 자격증 번호 변경 시 중복 확인
            if license_number and license_number != staff.license_number:
                existing = repo.find_by_license_number(license_number)
                if existing:
                    raise ValueError(f"이미 등록된 자격증 번호입니다: {license_number}")

            # 필드 업데이트 (None이 아닌 값만)
            if name is not None:
                staff.name = name
            if role is not None:
                staff.role = role
            if phone is not None:
                staff.phone = phone
            if email is not None:
                staff.email = email
            if license_number is not None:
                staff.license_number = license_number
            if notes is not None:
                staff.notes = notes

            updated_staff = repo.update(staff)
            self.logger.info(f"직원 정보 수정 완료: {updated_staff.name} (ID: {staff_id})")
            return updated_staff

    def deactivate_staff(self, staff_id: int) -> bool:
        """
        직원 퇴사 처리 (Soft Delete)

        Args:
            staff_id: 퇴사 처리할 직원 ID

        Returns:
            bool: 성공 여부
        """
        with self.session_scope() as session:
            repo = StaffRepository(session)
            result = repo.delete(staff_id)
            if result:
                self.logger.info(f"직원 퇴사 처리 완료: ID {staff_id}")
            return result

    def search_staff_by_name(self, name: str) -> List[Staff]:
        """
        이름으로 직원 검색

        Args:
            name: 검색할 이름 (부분 일치)

        Returns:
            List[Staff]: 검색 결과
        """
        with self.session_scope() as session:
            repo = StaffRepository(session)
            return repo.find_by_name(name)

    def get_staff_by_phone(self, phone: str) -> Optional[Staff]:
        """
        전화번호로 직원 조회

        Args:
            phone: 전화번호

        Returns:
            Optional[Staff]: 직원 엔티티 또는 None
        """
        with self.session_scope() as session:
            repo = StaffRepository(session)
            return repo.find_by_phone(phone)

    def get_staff_by_role(self, role: StaffRole) -> List[Staff]:
        """
        역할별 직원 조회

        Args:
            role: 직원 역할

        Returns:
            List[Staff]: 직원 리스트
        """
        with self.session_scope() as session:
            repo = StaffRepository(session)
            return repo.find_by_role(role)

    def get_care_workers(self) -> List[Staff]:
        """
        요양보호사 목록 조회

        Returns:
            List[Staff]: 요양보호사 리스트
        """
        with self.session_scope() as session:
            repo = StaffRepository(session)
            return repo.find_care_workers()

    def get_social_workers(self) -> List[Staff]:
        """
        사회복지사 목록 조회

        Returns:
            List[Staff]: 사회복지사 리스트
        """
        with self.session_scope() as session:
            repo = StaffRepository(session)
            return repo.find_social_workers()

    def get_staff_by_email(self, email: str) -> Optional[Staff]:
        """
        이메일로 직원 조회

        Args:
            email: 이메일

        Returns:
            Optional[Staff]: 직원 엔티티 또는 None
        """
        with self.session_scope() as session:
            repo = StaffRepository(session)
            return repo.find_by_email(email)

    def get_staff_by_license_number(self, license_number: str) -> Optional[Staff]:
        """
        자격증 번호로 직원 조회

        Args:
            license_number: 자격증 번호

        Returns:
            Optional[Staff]: 직원 엔티티 또는 None
        """
        with self.session_scope() as session:
            repo = StaffRepository(session)
            return repo.find_by_license_number(license_number)

    def get_staff_count(self) -> int:
        """
        재직 중인 직원 수 조회

        Returns:
            int: 재직 직원 수
        """
        with self.session_scope() as session:
            repo = StaffRepository(session)
            return repo.count()
