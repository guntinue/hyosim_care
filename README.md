# 효심케어 (Hyosim Care) 관리 시스템

방문요양 및 데이케어 서비스를 위한 로컬 우선(Local-First) 관리 시스템

## 📋 프로젝트 개요

효심케어는 방문요양 서비스를 시작으로, 데이케어(주간보호센터)까지 확장 가능한 관리 시스템입니다.
민감한 고객 데이터를 로컬 환경에 안전하게 저장하여 보안성을 극대화합니다.

## 🛠 기술 스택

- **언어**: Python 3.10+
- **GUI 프레임워크**: PyQt6
- **데이터베이스**: SQLite + SQLCipher (AES-256 암호화)
- **ORM**: SQLAlchemy 2.0+
- **배포**: PyInstaller (단일 실행 파일)

## 🏗 아키텍처

클린 아키텍처(Clean Architecture) 기반 설계:

```
hyosim_care/
├── src/
│   ├── domain/          # 핵심 비즈니스 엔티티
│   ├── service/         # 비즈니스 로직 (유스케이스)
│   ├── repository/      # 데이터 액세스 레이어
│   ├── ui/              # PyQt6 기반 프레젠테이션
│   ├── config/          # 설정 및 데이터베이스 연결
│   └── utils/           # 공통 유틸리티
├── data/                # 로컬 데이터베이스 저장
├── logs/                # 애플리케이션 로그
├── tests/               # 테스트 코드
└── main.py              # 메인 진입점
```

## 🚀 설치 및 실행

### 1. 가상환경 생성 및 활성화

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정

```bash
cp .env.example .env
# .env 파일을 열어서 DB_ENCRYPTION_KEY를 안전한 값으로 변경하세요
```

### 4. 실행

```bash
python main.py
```

## 📊 핵심 기능

- ✅ 고객(환자) 관리
- ✅ 직원(요양보호사, 사회복지사) 관리
- ✅ 방문 일정 관리 및 중복 검증
- ✅ 방문 일지 작성 및 관리
- ✅ 데이터 암호화 및 로컬 저장

## 🔒 보안

- SQLCipher를 통한 데이터베이스 AES-256 암호화
- 모든 민감 정보 로컬 저장 (클라우드 미사용)
- 환경 변수를 통한 암호화 키 관리

## 📝 개발 상태

현재 **Phase 1: 기반 구조 설정** 완료

- [x] 프로젝트 구조 설계
- [x] 데이터베이스 암호화 연결
- [x] 도메인 모델 정의
- [x] 로깅 시스템 구축
- [ ] Repository 레이어 구현 (다음 단계)
- [ ] Service 레이어 구현
- [ ] UI 개발

자세한 로드맵은 [project_plan.md](./project_plan.md) 참조

## 📖 문서

- [프로젝트 비전 및 요구사항](./Claude.md)
- [개발 로드맵](./project_plan.md)

## 📄 라이선스

Private - 내부 사용 목적
