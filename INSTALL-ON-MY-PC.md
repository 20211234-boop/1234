# 내 컴퓨터에 스킬 설치하기

이 저장소에 모아 둔 스킬 28개와 명령어 4개를 회사 컴퓨터의 Claude Code와 코워크에 설치하는 방법이다.
위에서부터 순서대로 하면 된다. 각 단계는 5분 안팎.

## 어디서 무엇이 되나

| 기능 | 코워크 | Claude Code (내 컴퓨터) | 클라우드 세션 (웹) |
|---|---|---|---|
| 스킬 28개 | ✅ ZIP 업로드 | ✅ 폴더 복사 | ✅ 이 저장소에 이미 있음 |
| ecc 명령어 4개 | ✅ 스킬로 바꾼 ZIP | ✅ `~/.claude/commands` | ✅ |
| 에이전트 3개 (planner 등) | ❌ | ✅ `~/.claude/agents` | ✅ |
| "스킬 자동 선택" 표 (CLAUDE.md) | ❌ (대신 각 스킬 설명으로 자동 선택) | ✅ | ✅ |
| `/compact`, `/context` | ❌ (`/handoff` 후 새 대화로 대신) | ✅ | ✅ |
| 플러그인 (`/plugin`) | 코워크 Plugins 메뉴 | ✅ | ❌ 막혀 있음 |
| taste 이미지 자산 | ❌ (가벼운 버전) | ✅ | ✅ |
| agent-browser, astryx, Headroom 프로그램 | ❌ | ✅ 설치 필요 | ❌ |

> **먼저 확인:** 회사 컴퓨터에 프로그램(Git, Node.js)을 설치하거나 외부 GitHub 파일을 받는 것이
> 사내 보안 규정상 허용되는지 IT 담당자에게 확인한다. 1단계(코워크 업로드)는 프로그램 설치가 필요 없다.

---

## 0. 무엇을 어디에 설치하나

| 쓰는 곳 | 설치 방법 | 필요한 것 |
|---|---|---|
| 코워크 (Claude 앱) | ZIP 파일을 메뉴에서 업로드 | 없음 |
| Claude Code (터미널) | 스킬 폴더를 `~/.claude/skills/`에 복사 | Claude Code |
| 외부 프로그램 (Headroom, agent-browser) | 명령어로 설치 | Python 또는 Node.js |

둘 다 쓴다면 1단계와 2단계를 모두 한다.

---

## 1단계. 코워크에 올리기 (프로그램 설치 없음)

**`all-skills-cowork.zip` 하나만 쓴다.** 이전에 받은 묶음(cowork-skills, design-skills 등)은 옛 버전이니 버린다.
안에 31개(스킬 27 + ecc 명령어 4)가 최신판으로 들어 있다.

1. `all-skills-cowork.zip`을 **한 번만** 압축 해제한다. 안에서 나온 `스킬이름.zip`은 풀지 않는다.
2. Claude 앱 → **Customize → Skills → "+" → Upload a skill**
3. `스킬이름.zip`을 하나씩 올린다. 올리면 자동으로 켜진다.
4. **이미 올린 스킬 중 아래 두 가지는 지우고 다시 올린다** (설명이 바뀌어 자동 실행 조건이 달라졌다).
   - `infographic-kit` — "픽토그램 넣어줘"로 자동 실행
   - `egm-*` 7개 — "egm 써줘"로 실행
   나머지는 이미 있으면 건너뛴다.

**우선순위별로 올리기 (다 올릴 필요 없다)**

| 순서 | 스킬 | 이유 |
|---|---|---|
| 1 (필수) | handoff, limit-saver, crash-out, infographic-kit | 매일 쓰는 것 |
| 2 (문서) | humanizer, i-have-adhd, awesome-design, aura-farming, egm-review, egm-brainstorm, egm-draft, egm-resolve | 보고서·기획서·공지 |
| 3 (웹·코드) | frontend-design, taste, image-to-code, web-design-guidelines, karpathy-guidelines, ecc-plan, ecc-code-review | 프로그램 만들 때 |
| 4 (가끔) | caveman, 67, larp, egm-review-loop, egm-bootstrap, egm-drift-report, ecc-build-fix, ecc-test-coverage | 필요할 때만 |
| 5 (보류) | task-observer, china-maxing, agent-browser, astryx | 무겁거나 프로그램 설치 필요 |

많이 올릴수록 Claude가 어떤 스킬을 고를지 헷갈릴 수 있다. 1·2번부터 올리고 필요할 때 추가한다.

업로드 메뉴가 안 보이면 회사 관리자가 스킬 기능을 꺼 둔 것이다. 관리자에게 요청한다.

---

## 2단계. Claude Code에 설치하기

### 2-1. 저장소 받기

**방법 A — Git이 있을 때 (권장)**

```bash
git clone -b ccr-ff767a2c-ui8si4 https://github.com/20211234-boop/1234.git claude-skills
```

**방법 B — Git이 없을 때**

1. 브라우저로 `https://github.com/20211234-boop/1234` 접속 (회사 GitHub 계정으로 로그인)
2. 왼쪽 위 브랜치 선택에서 `ccr-ff767a2c-ui8si4` 선택
3. 초록색 **Code** 버튼 → **Download ZIP** → 압축 해제 → 폴더 이름을 `claude-skills`로 바꾼다

### 2-2. 스킬 복사하기

모든 프로젝트에서 쓰려면 사용자 폴더의 `.claude`에 복사한다.

**Windows (PowerShell)**

```powershell
cd claude-skills
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills","$env:USERPROFILE\.claude\commands","$env:USERPROFILE\.claude\agents" | Out-Null
Copy-Item -Recurse -Force .claude\skills\*   "$env:USERPROFILE\.claude\skills\"
Copy-Item -Recurse -Force .claude\commands\* "$env:USERPROFILE\.claude\commands\"
Copy-Item -Recurse -Force .claude\agents\*   "$env:USERPROFILE\.claude\agents\"
```

**Mac / Linux (터미널)**

```bash
cd claude-skills
mkdir -p ~/.claude/skills ~/.claude/commands ~/.claude/agents
cp -R .claude/skills/*   ~/.claude/skills/
cp -R .claude/commands/* ~/.claude/commands/
cp -R .claude/agents/*   ~/.claude/agents/
```

> 이미 같은 이름의 스킬이 있으면 덮어쓴다. 직접 고친 스킬이 있다면 먼저 백업한다.

### 2-3. 압축 지침(CLAUDE.md) 넣기 — 선택

`/compact` 할 때 결정 사항과 수정한 파일만 남기게 하는 지침이다.
`~/.claude/CLAUDE.md` 파일이 **없으면** 저장소의 `CLAUDE.md`를 그대로 복사한다.
**있으면** 덮어쓰지 말고 저장소 `CLAUDE.md`의 내용을 기존 파일 맨 아래에 붙여 넣는다.

### 2-4. 확인

1. Claude Code를 완전히 껐다 다시 켠다.
2. 입력창에 `/`를 치고 `handoff`, `crash-out`, `limit-saver`가 목록에 보이는지 본다.
3. `/crash-out 1+1은 3이야?` 같은 질문으로 동작을 확인한다.

---

## 3단계. 선택 — 플러그인 설치 (Claude Code 터미널)

웹·클라우드 환경에서는 막혀 있지만 내 컴퓨터의 Claude Code에서는 된다.
**필요한 것만** 설치한다. 많이 설치할수록 컨텍스트를 많이 쓴다.

| 플러그인 | 설치 명령 | 언제 |
|---|---|---|
| Everything Claude Code (전체) | `/plugin marketplace add affaan-m/everything-claude-code` 후 `/plugin install everything-claude-code@everything-claude-code` | 개발 작업이 많을 때. 핵심 4개는 이미 2단계로 설치됨 |
| Claude-Mem (세션 간 기억) | `/plugin marketplace add thedotmack/claude-mem` 후 `/plugin install claude-mem` | 지난 대화를 자동으로 기억시키고 싶을 때. Node.js 18 이상 필요 |

npm에 있는 `everything-claude-code` 패키지는 보안 경고가 있으니 쓰지 않는다. 위 GitHub 경로만 쓴다.

---

## 4단계. 선택 — 외부 프로그램

### agent-browser (스킬 `/agent-browser`가 쓰는 브라우저 도구)

Node.js가 있어야 한다 (nodejs.org에서 LTS 설치).

```bash
npm i -g agent-browser
agent-browser install
agent-browser --version   # 버전이 나오면 성공
```

### REA (스킬 `/reverse-engineer-anything`가 쓰는 분석 도구)

Node.js가 있어야 한다. 믿을 수 있는 폴더에서 실행한다.

```bash
npx rea-agents setup   # 쓰는 에이전트(Claude Code 등) 선택 → 설정 계획 확인 후 승인
```

끝나면 Claude Code를 다시 시작한다. 프로그램(.exe 등)을 깊게 분석하려면 Ghidra(무료) 같은 분석 엔진을 따로 설치한다. 웹·자바스크립트 앱 분석은 엔진 없이 된다. 회사 PC라면 IT 담당자 확인 후 설치한다.

### Headroom (토큰 압축 프록시)

Python이 있어야 한다.

```bash
pip install "headroom-ai[code]"   # [code]를 빼면 Claude Code에서 효과가 거의 없음
headroom wrap claude              # Headroom을 거쳐 Claude Code 실행
```

회사 데이터가 오가는 경로에 끼는 프로그램이므로 IT 담당자 확인 후 설치한다.

### 설치하지 말 것

- **OmniRoute** 같은 "다른 AI로 돌려주는 무료 게이트웨이": 한도가 차면 대화 내용(개인정보 포함)이 다른 회사로 넘어갈 수 있다. 업무용 금지.

---

## 5단계. 다음부터 Claude가 직접 설치하게 하려면 — 선택

내 컴퓨터를 Claude 클라우드 세션에 연결해 두면, 다음에 "설치해줘"라고 했을 때 Claude가 직접 복사할 수 있다.

1. 회사 컴퓨터에 Claude 데스크톱 앱 설치
2. **Settings → Claude Code → Remote Control**에서 작업 폴더(예: `Documents\claude-skills`) 추가
3. 앱을 켜 둔 상태로 클라우드 세션에서 요청

사내 보안 규정상 원격 연결이 허용되는지 먼저 확인한다. 이 기능은 아직 모든 계정에 열려 있지 않을 수 있다.

---

## 문제 해결

| 증상 | 해결 |
|---|---|
| `/`에 스킬이 안 보임 | Claude Code 재시작. 폴더 구조가 `~/.claude/skills/스킬이름/SKILL.md`인지 확인 (한 단계 더 들어가 있으면 안 됨) |
| 코워크 업로드 실패 | ZIP 안 맨 위에 `스킬이름/SKILL.md`가 있어야 함. 묶음 파일을 통째로 올리지 말 것 |
| "이 환경에서는 플러그인을 사용할 수 없습니다" | 웹·클라우드 환경이라서. 내 컴퓨터 Claude Code 터미널에서 실행 |
| 스킬이 너무 많아 느림 | 안 쓰는 스킬 폴더를 지우거나, 코워크에서 스위치를 끈다 (특히 task-observer, taste, 67) |

사용법은 `SKILLS-GUIDE.md` 참고.

---

## 부록. 설치 후 첫 테스트 (5분)

| 테스트 | 입력 | 정상이면 |
|---|---|---|
| 도식 자동 실행 | "연차 신청 승인 흐름에 픽토그램 넣어서 그려줘" | 아이콘이 겹치지 않는 흐름도가 나온다 |
| EGM 실행 | "egm 써줘 — 신입 온보딩을 2주에서 1주로 줄이고 싶어" | 질문으로 아이디어를 정리하기 시작한다 |
| 사실 검증 | "/crash-out 올해 최저임금 시급 맞는지 확인해줘" | 검증됨/불확실/틀림으로 나눠 답한다 |
| 한도 절약 | "토큰 아껴줘" | "한도 절약 모드 켰습니다" 한 줄 |
| 인수인계 | "/handoff" | HANDOFF.md(코워크는 정리 문서)가 만들어진다 |

하나라도 안 되면 그 스킬이 목록에 켜져 있는지 먼저 확인한다.
