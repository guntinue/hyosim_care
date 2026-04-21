#!/usr/bin/env python3
"""
코드 검증 스크립트

Git 커밋 전에 실행하여 기본적인 오류를 확인합니다.
- import 오류 확인
- 구문 오류 확인
- 데이터베이스 초기화 테스트
"""
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)


def test_imports():
    """모든 모듈 import 테스트"""
    print("=" * 60)
    print("1. Import 테스트 시작...")
    print("=" * 60)

    try:
        print("\n[Config] settings.py import...")
        from src.config import settings
        print("✅ settings.py import 성공")

        print("\n[Config] database.py import...")
        from src.config.database import DatabaseManager, Base
        print("✅ database.py import 성공")

        print("\n[Domain] models.py import...")
        from src.domain.models import Patient, Staff, Schedule, VisitLog, ServiceType, StaffRole
        print("✅ models.py import 성공")

        print("\n[Repository] import...")
        from src.repository import (
            BaseRepository,
            PatientRepository,
            StaffRepository,
            ScheduleRepository,
            VisitLogRepository
        )
        print("✅ Repository 레이어 import 성공")

        print("\n[Service] import...")
        from src.service import (
            BaseService,
            PatientService,
            StaffService,
            ScheduleService,
            VisitLogService
        )
        print("✅ Service 레이어 import 성공")

        print("\n" + "=" * 60)
        print("✅ 모든 모듈 import 성공!")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n❌ Import 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_database_init():
    """데이터베이스 초기화 테스트"""
    print("\n" + "=" * 60)
    print("2. 데이터베이스 초기화 테스트 시작...")
    print("=" * 60)

    try:
        # 임시 데이터베이스 사용
        import tempfile
        from src.config.database import DatabaseManager, Base

        # 임시 DB 파일 생성
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_db_path = temp_db.name
        temp_db.close()

        print(f"\n임시 데이터베이스 생성: {temp_db_path}")

        # DB 초기화는 실제 암호화 없이 테스트
        print("\n주의: 실제 SQLCipher 암호화는 배포 시 테스트 필요")
        print("개발 환경에서는 일반 SQLite로 구조 검증만 수행")

        # 데이터베이스 URL 생성 (일반 SQLite)
        db_url = f"sqlite:///{temp_db_path}"

        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        engine = create_engine(db_url)
        Base.metadata.create_all(engine)

        print("\n✅ 데이터베이스 테이블 생성 성공")

        # 테이블 목록 확인
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        print(f"\n생성된 테이블 목록:")
        for table in tables:
            print(f"  - {table}")

        expected_tables = ['patients', 'staffs', 'schedules', 'visit_logs']
        missing_tables = [t for t in expected_tables if t not in tables]

        if missing_tables:
            print(f"\n❌ 누락된 테이블: {missing_tables}")
            return False

        print("\n✅ 모든 필수 테이블 존재 확인")

        # 임시 파일 삭제
        os.unlink(temp_db_path)
        print(f"\n임시 데이터베이스 삭제: {temp_db_path}")

        print("\n" + "=" * 60)
        print("✅ 데이터베이스 초기화 테스트 성공!")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n❌ 데이터베이스 초기화 오류: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_basic_crud():
    """기본 CRUD 작동 테스트"""
    print("\n" + "=" * 60)
    print("3. 기본 CRUD 테스트 시작...")
    print("=" * 60)

    try:
        import tempfile
        from datetime import date, time
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from src.config.database import Base
        from src.domain.models import Patient, Staff, ServiceType, StaffRole
        from src.repository import PatientRepository, StaffRepository

        # 임시 DB
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_db_path = temp_db.name
        temp_db.close()

        # 엔진 및 세션 생성
        engine = create_engine(f"sqlite:///{temp_db_path}")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        print("\n[테스트] Patient CRUD...")
        patient_repo = PatientRepository(session)

        # Create
        patient = Patient(
            name="테스트고객",
            birth_date=date(1950, 1, 1),
            phone="010-1234-5678",
            address="서울시 강남구",
            service_type=ServiceType.HOME_CARE,
            care_grade="1등급"
        )
        created_patient = patient_repo.create(patient)
        session.commit()
        print(f"✅ Patient 생성: ID {created_patient.id}")

        # Read
        found_patient = patient_repo.get_by_id(created_patient.id)
        assert found_patient is not None
        assert found_patient.name == "테스트고객"
        print(f"✅ Patient 조회: {found_patient.name}")

        # Update
        found_patient.care_grade = "2등급"
        updated_patient = patient_repo.update(found_patient)
        session.commit()
        assert updated_patient.care_grade == "2등급"
        print(f"✅ Patient 수정: 등급 {updated_patient.care_grade}")

        # Delete (Soft)
        patient_repo.delete(created_patient.id)
        session.commit()
        deleted_patient = patient_repo.get_by_id(created_patient.id)
        assert deleted_patient.is_active == False
        print(f"✅ Patient 비활성화 완료")

        print("\n[테스트] Staff CRUD...")
        staff_repo = StaffRepository(session)

        # Create
        staff = Staff(
            name="테스트직원",
            role=StaffRole.CARE_WORKER,
            phone="010-9876-5432",
            hire_date=date(2024, 1, 1),
            license_number="12345"
        )
        created_staff = staff_repo.create(staff)
        session.commit()
        print(f"✅ Staff 생성: ID {created_staff.id}")

        # Read
        found_staff = staff_repo.get_by_id(created_staff.id)
        assert found_staff is not None
        assert found_staff.name == "테스트직원"
        print(f"✅ Staff 조회: {found_staff.name}")

        session.close()
        os.unlink(temp_db_path)

        print("\n" + "=" * 60)
        print("✅ 기본 CRUD 테스트 성공!")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n❌ CRUD 테스트 오류: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """메인 검증 함수"""
    print("\n")
    print("🔍 효심케어 코드 검증 시작")
    print("=" * 60)

    results = []

    # 1. Import 테스트
    results.append(("Import 테스트", test_imports()))

    # 2. 데이터베이스 초기화 테스트
    results.append(("데이터베이스 초기화", test_database_init()))

    # 3. 기본 CRUD 테스트
    results.append(("기본 CRUD 테스트", test_basic_crud()))

    # 결과 요약
    print("\n" + "=" * 60)
    print("📊 검증 결과 요약")
    print("=" * 60)

    all_passed = True
    for test_name, result in results:
        status = "✅ 성공" if result else "❌ 실패"
        print(f"{status} - {test_name}")
        if not result:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("\n✅ 모든 검증 통과! 커밋 가능합니다.")
        return 0
    else:
        print("\n❌ 검증 실패! 오류를 수정한 후 다시 시도하세요.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
