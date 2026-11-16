---
name: astryx
description: "Meta의 오픈소스 디자인 시스템 Astryx(React 컴포넌트 150개+, 테마, 다크모드, 템플릿)로 웹앱·대시보드 화면을 만든다. 사용자가 Astryx를 이름으로 부르거나, 프로젝트에 @astryxdesign 패키지가 있거나, React로 사내 웹앱·관리자 대시보드를 새로 만들 때 사용. astryx 명령이 없으면 설치 명령을 안내한다."
---

<!-- ASTRYX:START -->
<!-- astryx-managed sha256:40630d74e252372984af6d16edfbb1e2ab5d54143e05bc4af7f0f54d74852499 -->
Astryx, a design system and UI library, is available on this computer.
Use it when you build or change UI, pick components, or style or theme an app.
Its docs, components, templates, and themes are all reachable through `astryx`. To make a page, run `astryx build "<what the page is for>"` first, as the WORKFLOW below says. Start with `astryx search '<what you need>'` for anything else.
Then read `astryx component <Name>` or `astryx docs <topic>`, not the package's files.
In a project, the project's version of Astryx answers automatically.
To build UI, work in a project folder (create one if there is none). Add `@astryxdesign/core` and `@astryxdesign/cli` to a new project or one without `@astryxdesign/core`; to a project that already has `@astryxdesign/core`, add `@astryxdesign/cli` at the same version. Run `astryx init` there and follow the agent docs it writes.
WORKFLOW — start every page from a template, never from scratch:
1. `astryx build "<idea>"` — names the template to scaffold from and the parts it lacks.
2. `astryx template <name> <path>` — scaffold it; keep its frame, gap and padding; replace the content.
3. `astryx template <Block>` for parts it lacks; `astryx component <Name>` to read props before using one.
Before you deliver, re-read each file; replace any raw <div>/<span>, imported .css/@apply, or hardcoded #hex/px with the component or a token. Then build the project and deliver that build, not a description of it.
If `astryx` is not found, run `npm i -g @astryxdesign/cli` first.
<!-- ASTRYX:END -->
