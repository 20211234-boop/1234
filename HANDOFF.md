# Handoff — 2026-11-17

## 목표
인사 업무(회사 HR 담당자)에 쓸 Claude 스킬을 모아 이 저장소에 저장하고, 클로드 코드와 코워크 둘 다에서 쓰게 한다.
다음 목표: 이 스킬로 실제 업무용 프로그램·보고서 만들기 (무엇을 만들지는 아직 미정).

## 결정 사항
- 외부 스킬은 내용을 다 읽고 외부 통신·삭제 코드 없는 것만 설치 — 회사 업무용이라 안전 우선
- 과하게 끼어드는 스킬(agent-browser, astryx, code-reviewer)은 실행 조건을 좁힘 — 엉뚱한 작업 가로채기 방지
- EGM은 "egm 써줘"로 실행되게 바꿈(원본은 이름 입력 필수). "egm" 없이 검토만 부탁하면 먼저 물음 — 한도를 많이 씀
- 코워크는 스킬 개수 제한(20개 안팎) 때문에 묶음 6개(kit)로 합침. 묶음 안 원본은 `MODE.md`로 이름 변경 — 별도 스킬로 잘못 인식 방지
- 클로드 코드는 27개 그대로 유지 (개수 제한 없음)
- OmniRoute(다른 AI로 우회)는 설치 안 함 — 개인정보 유출 위험
- task-observer, china-maxing은 코워크 묶음에서 제외 — 무겁거나 효과 미검증

## 수정한 파일
- `.claude/skills/` — 스킬 27개 (기본·디자인·EGM 7개·infographic-kit 등)
- `.claude/commands/ecc-*.md`, `.claude/agents/` — ECC 명령어 4개, 에이전트 3개
- `CLAUDE.md` — 압축 지침 + "스킬 자동 선택" 표 (요청 문구 → 스킬)
- `SKILLS-GUIDE.md` — 상황별 사용법, 출처·라이선스 표
- `INSTALL-ON-MY-PC.md` — 코워크 업로드(묶음 6개), 회사 PC 설치, 첫 테스트
- `tools/build_cowork_bundles.py` — 코워크 묶음 ZIP 생성기
- `cowork-bundles/*.zip` — 묶음 결과물 (daily, design, egm, dev, idea, infographic + all-bundles)

## 현재 상태
- 완료: PR #1 `main`에 머지됨 (스킬 27개·안내서). 이후 커밋 1개(코워크 묶음)는 브랜치 `ccr-ff767a2c-ui8si4`에만 있음
- 테스트: infographic-kit 템플릿만 브라우저 캡처로 확인. 나머지 스킬과 코워크 묶음 업로드는 실제 실행 미확인
- 코워크 계정에는 예전에 하나씩 올린 스킬이 이미 많음(anthropic-skills:egm-*, infographic-kit 등) → 개수 제한에 걸린 원인

## 다음 할 일
1. 사용자: 코워크에서 하나씩 올린 옛 스킬 삭제 → `all-bundles.zip` 풀어서 kit 6개 업로드 (daily, infographic 먼저)
2. 원하면 코워크 묶음 커밋을 PR로 `main`에 머지
3. 사용자: 저장소 비공개 전환 (Settings → General → Danger Zone → Private)
4. 사용자: 회사 PC에 `INSTALL-ON-MY-PC.md` 2단계대로 설치 (IT 승인 먼저)
5. 만들 프로그램 정하기 (후보: 연말정산·원천세 검토, 퇴직금 계산, 인사 보고서 자동화, 사내 대시보드) → `/ecc-plan` 또는 "egm 써줘"로 시작

## 주의할 점
- 저장소가 **공개(public)** 상태. 회사 코드·인사 데이터 올리기 전에 반드시 비공개로
- 회사 PC는 이 세션에 연결 안 됨(Remote Control 폴더 0개) — 직접 설치 불가, 안내서로만 진행
- 스킬 수정 후에는 `python3 tools/build_cowork_bundles.py`로 코워크 묶음 다시 생성
- `/plugin` 명령은 웹·클라우드 환경에서 막혀 있음 (회사 PC 터미널에서만 됨)
