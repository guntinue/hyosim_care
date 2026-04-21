# 프로젝트명: 효심케어 (Hyosim care) 관리 시스템

## 1. 프로젝트 비전
본 프로젝트는 방문요양 서비스를 시작으로, 추후 데이케어(주간보호센터) 서비스까지 확장 가능한 유연하고 안전한 관리 시스템을 지향한다. 'Local-First' 원칙을 준수하여 민감한 고객 데이터를 로컬 환경에 격리 저장함으로써 보안성을 극대화한다.

## 2. 페르소나 및 요구사항
### 관리자 (대표 - Desktop/Local)
- **데이터 주권**: 모든 데이터는 클라우드 없이 로컬 DB(SQLite)에만 저장.
- **관리 기능**: 고객/직원(요양사, 사회복지사) 관리, 매칭 정보 확인.
- **서비스 설정**: 방문요양/데이케어 등 서비스 타입 선택 및 메모 관리.

### 직원/고객 (App - 향후 확장 고려)
- **주요 기능**: 출퇴근 기록, 일지 작성, 일정 관리, 담당자 정보 확인.
- *참고: 로컬 저장 원칙과 앱 통신 간의 기술적 접점은 추후 API Server 레이어 추가로 대응한다.*

## 3. 기술 스택 및 아키텍처
- **언어 및 프레임워크**: Python 3.10+, PyQt6
- **데이터베이스**: SQLite + SQLCipher (AES-256 암호화)
- **ORM**: SQLAlchemy (Scoped Session 관리)
- **배포**: PyInstaller (Single Executable, --onefile)
- **아키텍처**: 클린 아키텍처 (Clean Architecture)
  - `domain`: 엔티티 및 비즈니스 규칙 (의존성 없음)
  - `service`: 유스케이스 로직 (방문 시간 중복 검증 등)
  - `repository`: 데이터 액세스 인터페이스 및 구현
  - `ui`: PyQt6 기반의 프레젠테이션 레이어

## 4. 브랜치 전략 (Git Flow)

main: 최종 배포용 브랜치 (PyInstaller로 빌드된 .exe의 소스 코드)

dev: 다음 버전을 위한 개발 브랜치 (기능 통합)

feat/: 각 기능 개발 (예: feature/db-encryption, feature/schedule-algorithm)

refactor/: 코드 리팩토링

release/: 배포 전 QA 및 최종 버그 수정

hotfix/: 배포 후 발생한 긴급 버그 수정

## 5. 개발 원칙 (Critical)
1. **Security First**: 민감 정보는 반드시 DB 암호화 및 서비스 레이어 내 암호화 로직을 거친다.
2. **Business Logic Isolation**: 모든 검증(일정 중복 등)은 UI가 아닌 Service 레이어에서 수행한다.
3. **Robustness**: `logging`을 통한 로컬 로그 기록 및 SQLite `Database is locked` 방지를 위한 세션 관리 철저.
4. **Git Strategy**: Git Flow를 준수한다. 모든 작업은 `feature/` 브랜치에서 시작하며 `dev`로 머지한다.
5. **Async Architecture**: 시스템 확장성을 위해 RabbitMQ 기반의 메시징 구조를 염두에 둔다. (CI 환경에서는 GitHub Actions Service 활용)

## 6. 작업 프로세스 및 문서화 규칙 (Workflow)
1. **Self-Updating Roadmap**: 모든 기능 구현이나 주요 설계 변경이 완료된 후에는 반드시 `project_plan.md` 파일을 업데이트한다.
   - 완료된 태스크는 `[ ]`에서 `[x]`로 변경한다.
   - 작업 중 발견된 새로운 이슈나 하위 태스크는 즉시 `project_plan.md`에 추가한다.
   - '현재 진행 상황' 섹션에 마지막 작업 일자와 작업 내용을 간략히 기록한다.
2. **Context Persistence**: 다음 대화 세션에서도 작업 흐름이 이어질 수 있도록, 현재 어디까지 진행되었고 다음 단계에서 무엇을 해야 하는지 `project_plan.md`의 하단에 명확히 명시한다.

## 예시
## 📅 현재 진행 상황 및 히스토리
- **2026-04-21**: 프로젝트 초기 아키텍처 설계 완료 및 `Claude.md`, `project_plan.md` 작성.
- **Next Step**: `src/config/settings.py` 작성 및 로깅 시스템(logger) 설정.

## 🚩 미해결 이슈 및 메모
- [ ] SQLite 암호화 라이브러리(`pysqlcipher3`)가 Windows 환경에서 컴파일 에러가 발생하는지 확인 필요.
- [ ] 데이케어 확장을 위해 `Patient` 테이블에 '입소 유형' 컬럼 미리 설계하기.