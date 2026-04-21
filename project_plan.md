# 효심케어 개발 로드맵 (Project Plan)

## Phase 1: 기반 구조 설정 (Infrastructure) ✅ 완료
- [x] 가상환경 구성 및 의존성 라이브러리 설정 (PyQt6, SQLAlchemy, SQLCipher, PyInstaller)
- [x] `settings.py` 내 로컬 경로 및 로깅(logging) 시스템 구축
- [x] SQLite 암호화 연결 및 Scoped Session 베이스 코드 작성
- [x] 프로젝트 디렉토리 구조 생성 (클린 아키텍처)
- [x] .gitignore 및 환경 변수 예제 파일 작성
- [x] main.py 메인 진입점 작성

## Phase 2: 도메인 및 데이터 레이어 (Core & Data) ✅ 완료
- [x] 핵심 엔티티 설계: `Patient`, `Staff`, `VisitLog`, `Schedule`
- [x] 데이케어 확장을 고려한 `ServiceType` 구분 로직 설계
- [x] Repository 인터페이스 및 SQLAlchemy 기반 구현체 작성
  - [x] BaseRepository (제네릭 인터페이스)
  - [x] PatientRepository (고객 CRUD 및 검색)
  - [x] StaffRepository (직원 CRUD 및 역할별 조회)
  - [x] ScheduleRepository (일정 CRUD 및 시간 충돌 검증)
  - [x] VisitLogRepository (방문 일지 CRUD 및 통계)
- [x] Git Flow 브랜치 초기화 및 GitHub Repository 설정
  - [x] main 브랜치 (최종 배포용)
  - [x] dev 브랜치 (개발용)
  - [x] GitHub 원격 저장소 연동 완료
- [ ] GitHub Actions CI 워크플로우 구축 (Phase 5에서 진행 예정)

## Phase 3: 비즈니스 로직 구현 (Service Layer) 🚧 다음 단계
- [ ] PatientService: 고객 관리 비즈니스 로직
- [ ] StaffService: 직원 관리 비즈니스 로직
- [ ] ScheduleService: 일정 관리 및 **중복 방지 검증 알고리즘** 구현
- [ ] VisitLogService: 방문 일지 작성 및 통계 로직
- [ ] MatchingService: 방문요양/사회복지사 매칭 로직 (향후)
- [ ] 급여 및 서비스 비용 계산 모듈 (향후 확장 대비)

## Phase 4: UI 개발 (Presentation)
- [ ] 관리자용 메인 대시보드 (PyQt6)
- [ ] 고객/직원 등록 및 관리 화면
- [ ] 캘린더 형태의 일정 관리 뷰

## Phase 5: 보안 및 배포 최적화 (Security & Deployment)
- [ ] 데이터 백업/복구 유틸리티 개발
- [ ] PyInstaller를 이용한 단일 실행 파일(.exe) 빌드 테스트
- [ ] 사용자 매뉴얼 및 배포 패키징 확인

---
## 📅 현재 진행 상황 및 히스토리
- **2026-04-21 오전**: 프로젝트 초기 아키텍처 설계 완료 및 `Claude.md`, `project_plan.md` 작성
- **2026-04-21 오후 (1차)**: Phase 1 기반 구조 설정 완료
  - 프로젝트 디렉토리 구조 생성 (클린 아키텍처)
  - requirements.txt 작성 (PyQt6, SQLAlchemy, pysqlcipher3 등)
  - settings.py 작성 (로깅 시스템 포함)
  - database.py 작성 (SQLCipher 암호화 연결, Scoped Session 관리)
  - 도메인 모델 작성 (Patient, Staff, Schedule, VisitLog)
  - main.py 메인 진입점 작성
  - .gitignore, .env.example 작성
  - README.md 업데이트
- **2026-04-21 오후 (2차)**: Phase 2 완료 - Repository 레이어 구현
  - BaseRepository 인터페이스 작성 (제네릭 타입, ABC 패턴)
  - PatientRepository 구현 (CRUD + 이름/전화번호/서비스타입별 검색)
  - StaffRepository 구현 (CRUD + 역할별/자격증별 검색)
  - ScheduleRepository 구현 (CRUD + **시간 충돌 검증 로직** 포함)
  - VisitLogRepository 구현 (CRUD + 통계 쿼리)
  - Repository 모듈 패키지 정리 (__init__.py)
- **2026-04-21 오후 (3차)**: Git Flow 브랜치 전략 적용
  - Phase 2 작업 main 브랜치에 커밋
  - dev 브랜치 생성 및 GitHub 원격 저장소에 push
  - 향후 기능 개발은 dev 브랜치에서 진행 예정
- **Next Step**: Phase 3 - Service 레이어 구현 (비즈니스 로직 및 유스케이스)
- **현재 브랜치**: `dev` (개발용)

## 🚩 미해결 이슈 및 메모
- [ ] SQLite 암호화 라이브러리(`pysqlcipher3`)가 Windows 환경에서 컴파일 에러가 발생하는지 확인 필요
  - 개발 중에는 일반 SQLite 사용 가능, 배포 시 암호화 버전 필수
- [ ] 데이케어 확장을 위해 `Patient` 테이블에 '입소 유형' 컬럼 미리 설계하기 (완료됨 - service_type 필드)
- [ ] 가상환경 생성 후 의존성 설치 테스트 필요