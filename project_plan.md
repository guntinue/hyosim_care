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

## Phase 3: 비즈니스 로직 구현 (Service Layer) ✅ 완료
- [x] BaseService: Service 레이어 기본 클래스 작성
- [x] PatientService: 고객 관리 비즈니스 로직
  - 고객 등록/수정/삭제 (전화번호 중복 검증)
  - 이름/전화번호/서비스타입/등급별 검색
- [x] StaffService: 직원 관리 비즈니스 로직
  - 직원 등록/수정/퇴사 처리 (전화번호/자격증 중복 검증)
  - 역할별/자격증별 조회
- [x] ScheduleService: 일정 관리 및 **중복 방지 검증 알고리즘** 구현 ⭐
  - 일정 생성 시 직원/고객 시간 충돌 검증
  - 일정 수정/삭제/완료 처리
  - 날짜별/직원별/고객별 일정 조회
- [x] VisitLogService: 방문 일지 작성 및 통계 로직
  - 방문 일지 생성/수정/삭제
  - 출퇴근 체크인/체크아웃
  - 고객별/직원별 방문 횟수 통계
- [ ] MatchingService: 방문요양/사회복지사 매칭 로직 (Phase 4 이후)
- [ ] 급여 및 서비스 비용 계산 모듈 (향후 확장 대비)

## Phase 4: UI 개발 (Presentation) 🚧 진행 중
- [x] 관리자용 메인 대시보드 (PyQt6)
  - [x] MainWindow 클래스 구현
  - [x] DashboardCard 위젯 (통계 카드)
  - [x] 헤더 영역 (타이틀, 버전 정보)
  - [x] 빠른 작업 버튼 영역 (고객/직원 등록, 일정 관리, 방문 일지)
  - [x] 최근 활동 영역 (플레이스홀더)
  - [ ] 실시간 통계 데이터 연동 (Service 레이어)
- [x] 고객 등록 및 관리 화면
  - [x] PatientForm 다이얼로그 구현
  - [x] 기본 정보 입력 (이름, 생년월일, 연락처, 주소)
  - [x] 서비스 정보 입력 (서비스 유형, 등급)
  - [x] 보호자 정보 입력 (이름, 연락처, 관계)
  - [x] 추가 정보 입력 (의료 정보, 메모)
  - [x] 유효성 검증 (필수 필드 체크)
  - [x] PatientService 연동 (등록/수정)
  - [x] MainWindow 연동 (고객 등록 버튼)
  - [ ] 고객 목록 조회 화면
  - [ ] 고객 검색 기능
- [ ] 직원 등록 및 관리 화면
- [ ] 캘린더 형태의 일정 관리 뷰
- [ ] 방문 일지 작성 화면
- [ ] 통계 및 리포트 화면

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
- **2026-04-21 오후 (4차)**: Phase 3 완료 - Service 레이어 구현
  - BaseService 작성 (DatabaseManager 통합)
  - PatientService 구현 (전화번호 중복 검증 포함)
  - StaffService 구현 (전화번호/자격증 중복 검증 포함)
  - ScheduleService 구현 (**시간 충돌 검증 알고리즘** 포함) ⭐
  - VisitLogService 구현 (출퇴근 체크인/통계 기능)
  - Service 모듈 패키지 정리 (__init__.py)
- **2026-04-22 오후 (1차)**: Phase 4 시작 - 메인 대시보드 UI 구현
  - feature/ui-main-dashboard 브랜치 생성
  - MainWindow 클래스 구현 (헤더, 통계 카드, 빠른 작업 버튼)
  - DashboardCard 위젯 구현
  - main.py 수정 (UI 통합, 인코딩 문제 해결)
  - 애플리케이션 실행 테스트 성공
  - dev 브랜치로 머지 및 푸시 완료
- **2026-04-23 오전**: 고객 등록 화면 구현
  - feature/ui-patient-form 브랜치 생성
  - PatientForm 다이얼로그 구현
    - 기본 정보, 서비스 정보, 보호자 정보, 추가 정보 입력 폼
    - 유효성 검증 로직 (필수 필드 체크)
    - PatientService 연동 (등록/수정 기능)
    - 스타일시트 적용 (모던한 UI 디자인)
  - MainWindow에 PatientService 연동
  - 고객 등록 버튼 이벤트 핸들러 구현
  - 애플리케이션 실행 테스트 성공
- **Next Step**:
  - 직원 등록 화면 구현 (feature/ui-staff-form)
  - 고객 목록 조회 화면 구현 (feature/ui-patient-list)
  - 메인 대시보드에 실시간 통계 연동
- **현재 브랜치**: `feature/ui-patient-form`

## 🚩 미해결 이슈 및 메모
- [ ] SQLite 암호화 라이브러리(`pysqlcipher3`)가 Windows 환경에서 컴파일 에러가 발생하는지 확인 필요
  - 개발 중에는 일반 SQLite 사용 가능, 배포 시 암호화 버전 필수
- [ ] 데이케어 확장을 위해 `Patient` 테이블에 '입소 유형' 컬럼 미리 설계하기 (완료됨 - service_type 필드)
- [ ] 가상환경 생성 후 의존성 설치 테스트 필요