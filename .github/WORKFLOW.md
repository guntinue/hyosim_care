# Git 워크플로우 가이드

## 기본 원칙
- ❌ **dev 브랜치에 직접 커밋/푸시 금지**
- ✅ **모든 작업은 기능 브랜치(feature/)에서 진행**
- ✅ **dev 브랜치로의 머지는 GitHub PR을 통해서만**

## 작업 흐름

### 1. 새 기능 개발 시작
```bash
# dev 브랜치 최신 상태로 업데이트
git checkout dev
git pull origin dev

# 새 기능 브랜치 생성
git checkout -b feature/[기능명]
```

### 2. 개발 및 커밋
```bash
# 작업 진행...
git add [변경된 파일들]
git commit -m "feat: [기능 설명]"
```

### 3. 기능 브랜치에 푸시
```bash
# ✅ 기능 브랜치에만 푸시
git push origin feature/[기능명]

# ❌ dev 브랜치로 절대 푸시하지 않음
# git push origin dev  <- 이거 안 함!
```

### 4. GitHub에서 PR 생성
1. GitHub 저장소로 이동
2. "Pull requests" 탭 클릭
3. "New pull request" 클릭
4. base: `dev` ← compare: `feature/[기능명]`
5. PR 생성 및 검토
6. **GitHub에서 Merge** (로컬에서 머지하지 않음)

### 5. PR 머지 후 정리
```bash
# dev 브랜치로 이동 및 최신 상태로 업데이트
git checkout dev
git pull origin dev

# (선택) 머지된 기능 브랜치 삭제
git branch -d feature/[기능명]
```

## 예시: 고객 등록 화면 개발

```bash
# 1. 기능 브랜치 생성
git checkout dev
git pull origin dev
git checkout -b feature/ui-patient-form

# 2. 개발 및 커밋
# ... 코드 작성 ...
git add src/ui/patient_form.py
git commit -m "feat: 고객 등록 화면 구현"

# 3. 기능 브랜치에 푸시 (dev에 푸시 ❌)
git push origin feature/ui-patient-form

# 4. GitHub에서 PR 생성 및 머지
# (웹 브라우저에서 작업)

# 5. PR 머지 후
git checkout dev
git pull origin dev
git branch -d feature/ui-patient-form
```

## 주의사항

### ❌ 절대 하지 말 것
```bash
# dev 브랜치에서 직접 작업
git checkout dev
# ... 작업 ...
git commit -m "..."
git push origin dev  # ← 이렇게 하지 말 것!

# 로컬에서 dev로 머지
git checkout dev
git merge feature/xxx  # ← GitHub PR로 대신할 것!
git push origin dev
```

### ✅ 올바른 방법
```bash
# 항상 기능 브랜치에서 작업
git checkout -b feature/new-feature
# ... 작업 ...
git commit -m "..."
git push origin feature/new-feature  # ← 기능 브랜치만 푸시!

# GitHub에서 PR 생성 및 머지
```

## 브랜치 명명 규칙

- `feature/ui-[화면명]` - UI 개발
- `feature/service-[기능명]` - 서비스 로직
- `feature/[기능명]` - 일반 기능
- `fix/[버그명]` - 버그 수정
- `refactor/[대상]` - 리팩토링
- `docs/[문서명]` - 문서 작업

## 요약

**핵심**:
1. 모든 작업은 `feature/` 브랜치에서
2. `feature/` 브랜치만 푸시
3. `dev` 브랜치로의 머지는 GitHub PR로만
4. 로컬에서 `dev`로 머지 금지
