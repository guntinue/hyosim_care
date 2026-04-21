"""
효심케어 도메인 모델
클린 아키텍처의 Domain Layer - 핵심 비즈니스 엔티티 정의
"""
from datetime import datetime, date, time
from typing import Optional
from sqlalchemy import String, Integer, DateTime, Date, Time, Text, Enum, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from src.config.database import Base


class ServiceType(str, enum.Enum):
    """서비스 유형"""
    HOME_CARE = "home_care"  # 방문요양
    DAY_CARE = "day_care"    # 데이케어 (주간보호센터)


class StaffRole(str, enum.Enum):
    """직원 역할"""
    CARE_WORKER = "care_worker"        # 요양보호사
    SOCIAL_WORKER = "social_worker"    # 사회복지사
    NURSE = "nurse"                     # 간호사
    ADMIN = "admin"                     # 관리자


class Patient(Base):
    """고객(환자) 엔티티"""
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="고객명")
    birth_date: Mapped[date] = mapped_column(Date, nullable=False, comment="생년월일")
    phone: Mapped[str] = mapped_column(String(20), nullable=False, comment="연락처")
    address: Mapped[str] = mapped_column(String(255), nullable=False, comment="주소")

    # 서비스 정보
    service_type: Mapped[ServiceType] = mapped_column(
        Enum(ServiceType),
        nullable=False,
        default=ServiceType.HOME_CARE,
        comment="서비스 유형"
    )
    care_grade: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        comment="등급 (1~5등급, 인지지원등급 등)"
    )

    # 보호자 정보
    guardian_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="보호자명")
    guardian_phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment="보호자 연락처")
    guardian_relation: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="보호자 관계")

    # 의료 정보
    medical_info: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="의료 정보 및 특이사항")

    # 메타 정보
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="메모")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="활성 상태")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="등록일시")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="수정일시"
    )

    # 관계
    schedules: Mapped[list["Schedule"]] = relationship("Schedule", back_populates="patient")
    visit_logs: Mapped[list["VisitLog"]] = relationship("VisitLog", back_populates="patient")

    def __repr__(self):
        return f"<Patient(id={self.id}, name='{self.name}', service_type='{self.service_type.value}')>"


class Staff(Base):
    """직원 엔티티"""
    __tablename__ = "staffs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="직원명")
    role: Mapped[StaffRole] = mapped_column(
        Enum(StaffRole),
        nullable=False,
        comment="직원 역할"
    )
    phone: Mapped[str] = mapped_column(String(20), nullable=False, comment="연락처")
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="이메일")

    # 자격 정보
    license_number: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="자격증 번호"
    )
    hire_date: Mapped[date] = mapped_column(Date, nullable=False, comment="입사일")

    # 메타 정보
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="메모")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="재직 상태")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="등록일시")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="수정일시"
    )

    # 관계
    schedules: Mapped[list["Schedule"]] = relationship("Schedule", back_populates="staff")
    visit_logs: Mapped[list["VisitLog"]] = relationship("VisitLog", back_populates="staff")

    def __repr__(self):
        return f"<Staff(id={self.id}, name='{self.name}', role='{self.role.value}')>"


class Schedule(Base):
    """일정 엔티티"""
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # 외래 키
    patient_id: Mapped[int] = mapped_column(Integer, ForeignKey("patients.id"), nullable=False)
    staff_id: Mapped[int] = mapped_column(Integer, ForeignKey("staffs.id"), nullable=False)

    # 일정 정보
    schedule_date: Mapped[date] = mapped_column(Date, nullable=False, comment="방문 날짜")
    start_time: Mapped[time] = mapped_column(Time, nullable=False, comment="시작 시간")
    end_time: Mapped[time] = mapped_column(Time, nullable=False, comment="종료 시간")

    # 서비스 정보
    service_type: Mapped[ServiceType] = mapped_column(
        Enum(ServiceType),
        nullable=False,
        comment="서비스 유형"
    )

    # 메타 정보
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="일정 메모")
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, comment="완료 여부")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="등록일시")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="수정일시"
    )

    # 관계
    patient: Mapped["Patient"] = relationship("Patient", back_populates="schedules")
    staff: Mapped["Staff"] = relationship("Staff", back_populates="schedules")
    visit_log: Mapped[Optional["VisitLog"]] = relationship(
        "VisitLog",
        back_populates="schedule",
        uselist=False
    )

    def __repr__(self):
        return (f"<Schedule(id={self.id}, patient_id={self.patient_id}, "
                f"staff_id={self.staff_id}, date={self.schedule_date})>")


class VisitLog(Base):
    """방문 일지 엔티티"""
    __tablename__ = "visit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # 외래 키
    schedule_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("schedules.id"),
        nullable=False,
        unique=True
    )
    patient_id: Mapped[int] = mapped_column(Integer, ForeignKey("patients.id"), nullable=False)
    staff_id: Mapped[int] = mapped_column(Integer, ForeignKey("staffs.id"), nullable=False)

    # 방문 정보
    visit_date: Mapped[date] = mapped_column(Date, nullable=False, comment="방문 날짜")
    check_in_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="출근 시간"
    )
    check_out_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="퇴근 시간"
    )

    # 서비스 내용
    service_content: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="서비스 내용"
    )
    patient_condition: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="고객 상태"
    )
    special_notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="특이사항"
    )

    # 메타 정보
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="작성일시")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="수정일시"
    )

    # 관계
    schedule: Mapped["Schedule"] = relationship("Schedule", back_populates="visit_log")
    patient: Mapped["Patient"] = relationship("Patient", back_populates="visit_logs")
    staff: Mapped["Staff"] = relationship("Staff", back_populates="visit_logs")

    def __repr__(self):
        return (f"<VisitLog(id={self.id}, schedule_id={self.schedule_id}, "
                f"visit_date={self.visit_date})>")
