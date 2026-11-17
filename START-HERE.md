# 여기부터 읽기 (컴퓨터로 이사 온 자료)

이 폴더는 클라우드에서 만든 클로드 스킬 모음입니다.
`바탕화면\클로드 작성 자료` 같은 곳에 풀어 두고 아래 순서대로 하세요.

## 1. 코워크 (Claude 앱) — 프로그램 설치 없음

1. Claude 앱 → Customize → Skills 에서 예전에 하나씩 올린 스킬을 지웁니다 (회사가 넣어 준 ecorbit-… 은 그대로).
2. `cowork-bundles` 폴더의 `○○-kit.zip` 을 **풀지 말고** 하나씩 올립니다.
   먼저: `daily-kit.zip`, `infographic-kit.zip` → 다음: `design-kit.zip`, `egm-kit.zip` → 필요할 때: `dev-kit.zip`, `idea-kit.zip`

## 2. 클로드 코드 (내 컴퓨터) — 설치 스크립트 한 번

- **Windows:** 이 폴더에서 주소창에 `powershell` 입력 → 엔터 → 아래 한 줄
  ```
  powershell -ExecutionPolicy Bypass -File tools\install-windows.ps1
  ```
- **Mac:** 이 폴더에서 터미널을 열고 `bash tools/install-mac.sh`

끝나면 Claude Code를 껐다 켜고 `/` 를 쳐서 `handoff`, `crash-out`, `infographic-kit` 이 보이는지 확인합니다.
회사 PC에 스크립트 실행이 허용되는지 IT 담당자에게 먼저 확인하세요.

## 3. 이어서 작업하기

이 폴더에서 Claude Code를 열고 이렇게 말하세요.

> HANDOFF.md 읽고 이어서 해줘

## 폴더 안내

| 파일·폴더 | 내용 |
|---|---|
| `HANDOFF.md` | 지금까지 한 일, 결정 이유, 다음 할 일 |
| `SKILLS-GUIDE.md` | 상황별 스킬 사용법 |
| `INSTALL-ON-MY-PC.md` | 설치 방법 자세히 (플러그인, 외부 프로그램 포함) |
| `CLAUDE.md` | Claude가 자동으로 읽는 규칙 (압축 지침, 스킬 자동 선택 표) |
| `.claude/` | 스킬 27개, 명령어 4개, 에이전트 3개 (숨김 폴더일 수 있음) |
| `cowork-bundles/` | 코워크용 묶음 ZIP 6개 |
| `tools/` | 설치 스크립트, 코워크 묶음 생성기 |

`.claude` 폴더가 안 보이면: Windows 탐색기 → 보기 → 숨긴 항목 체크 / Mac Finder → ⌘ + Shift + .
