# 내 컴퓨터에 스킬 설치하기

이 저장소에 모아 둔 스킬 18개와 명령어 4개를 회사 컴퓨터의 Claude Code와 코워크에 설치하는 방법이다.
위에서부터 순서대로 하면 된다. 각 단계는 5분 안팎.

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

이 대화에서 받은 ZIP 묶음 5개를 쓴다.

| 묶음 파일 | 들어 있는 스킬 |
|---|---|
| `cowork-skills.zip` | handoff, crash-out, frontend-design, aura-farming, 67, larp, china-maxing, task-observer, ecc-plan, ecc-code-review, ecc-build-fix, ecc-test-coverage |
| `cowork-skills-2.zip` | i-have-adhd, humanizer, caveman, karpathy-guidelines |
| `limit-skills.zip` | limit-saver (caveman, handoff는 위와 중복) |
| `design-skills.zip` | awesome-design, taste(가벼운 버전), image-to-code, web-design-guidelines, agent-browser |

1. 묶음 파일을 **한 번만** 압축 해제한다. 안에서 나온 `스킬이름.zip`은 풀지 않는다.
2. Claude 앱 → **Customize → Skills → "+" → Upload a skill**
3. `스킬이름.zip`을 하나씩 올린다. 올리면 자동으로 켜진다.
4. 이미 올린 스킬은 건너뛴다 (목록에 `crash-out` 같은 이름이 보이면 이미 있는 것).

**우선 올릴 것 (이것만 해도 충분):** handoff, limit-saver, crash-out, i-have-adhd, humanizer, aura-farming, awesome-design

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
