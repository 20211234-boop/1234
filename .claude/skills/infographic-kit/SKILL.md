---
name: infographic-kit
description: 보고서·슬라이드·웹페이지·대시보드에 픽토그램(아이콘)과 도식(레인, 점선 화살표, 그룹 상자, 단계 번호, 마름모 판정, 원통 DB, A vs B 비교, 통계 카드, 도넛)을 넣는다. 아이콘 2,089개(Lucide)에서 개념마다 다른 아이콘을 골라 같은 그림이 반복되지 않게 한다. 사용자가 "픽토그램 넣어줘", "픽토그래픽", "아이콘 넣어줘", "그림 넣어줘", "시각화해줘", "도식", "도식화", "인포그래픽", "구조도", "흐름도", "프로세스 그림", "다이어그램", "대시보드 카드", "보기 좋게 정리해줘"라고 하거나, 보고서·PPT·웹페이지에 아이콘이나 도형이 들어갈 때 항상 먼저 이 스킬을 쓴다. 이모지를 아이콘 대신 쓰려 할 때도 이 스킬을 쓴다.
---

# Infographic Kit — 픽토그램과 도형 도식

같은 아이콘과 같은 상자가 계속 반복되는 문제를 막는 도구 모음이다.

| 파일 | 내용 |
|---|---|
| `assets/icons.json` | Lucide 아이콘 2,089개 (이름, 태그, 범주, SVG 경로) |
| `assets/ko-keywords.json` | 인사·업무 한국어 단어 → 아이콘 이름 (급여, 근태, 채용, 평가 등 90여 개) |
| `scripts/icons.py` | 아이콘 검색·중복 없는 선택·SVG 출력 (파이썬 표준 라이브러리만 사용) |
| `templates/diagram-kit.html` | 도형 부품 10종과 예시 3개 (레인 흐름, A vs B 비교, 대시보드 카드) |
| `references/patterns.md` | 언제 어떤 도식을 쓰는지, 반복을 피하는 규칙 |

## 절차

1. **내용부터 정리한다.** 도식에 넣을 개념(명사)과 흐름(누가 → 무엇을 → 결과)을 목록으로 뽑는다.
2. **도식 형태를 고른다.** `references/patterns.md`의 "어떤 도식을 쓸까" 표에서 내용에 맞는 형태를 하나 고른다.
   한 문서에서 같은 형태를 연달아 쓰지 않는다.
3. **아이콘을 고른다.** 개념 목록을 한 번에 넣어 중복 없이 고른다.
   ```bash
   python scripts/icons.py pick 급여 근태 채용 평가 교육
   python scripts/icons.py search approval      # 후보가 마음에 안 들면 영어로 다시 검색
   ```
   스크립트를 실행할 수 없으면 `assets/ko-keywords.json`과 `assets/icons.json`의 이름·태그를 직접 찾아본다.
4. **도형 부품을 가져온다.** `templates/diagram-kit.html`의 CSS(토큰 + 부품)를 복사하고 필요한 부품만 쓴다.
   아이콘은 `python scripts/icons.py symbol 이름1 이름2 ...`로 만든 `<symbol>` 묶음을 본문 맨 위에 한 번 넣고
   `<svg class="ico"><use href="#i-이름"/></svg>`로 쓴다.
5. **결과물 형식에 맞게 내보낸다.** 아래 "형식별 적용"을 따른다.
6. **반복 검사를 한다.** 내보내기 전에 `references/patterns.md`의 "반복 검사" 6개 항목을 확인하고 걸리는 것을 고친다.

## 형식별 적용

| 결과물 | 방법 |
|---|---|
| 웹페이지·대시보드 (React, HTML) | CSS 토큰과 부품을 그대로 쓴다. React는 `lucide-react` 패키지가 있으면 그것을 쓰고, 없으면 `icons.py svg`로 인라인 SVG를 넣는다 |
| 슬라이드 (pptx 스킬과 함께) | 도식을 HTML로 만든 뒤 브라우저로 PNG 캡처(2배 해상도)해서 넣는다. 아이콘만 필요하면 `icons.py svg 이름 --size 96 --color "#hex"`로 SVG를 만들어 넣는다 |
| 보고서 (docx 스킬과 함께) | 슬라이드와 같다. 본문 폭에 맞게 1600px 안팎으로 캡처한다 |
| 아티팩트·HTML 보고서 | `templates/diagram-kit.html`을 그대로 바탕으로 쓴다 |

캡처 예시 (Playwright가 있을 때):
```js
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1100,height:800},deviceScaleFactor:2});
await p.goto('file:///절대경로/diagram.html');await p.locator('.sheet').screenshot({path:'diagram.png'});await b.close()})()
```
브라우저가 없으면 캡처하지 못했다고 알리고, HTML 파일을 열어 직접 캡처하도록 안내한다.

## 색

- 색은 `:root` 토큰만 바꾼다. 레인 색(`--c1`~`--c4`)은 서로 다른 계열 4개, 채도는 비슷하게 둔다.
- `/awesome-design`으로 고른 디자인 시스템이 있으면 그 색으로 `--c1`~`--c4`, `--ink`, `--canvas`를 바꾼다.
- 회사 브랜드 색이 있으면 그것이 우선이다.

## 지켜야 할 것

- 아이콘은 Lucide만 쓴다(ISC 라이선스, 상업적 사용 가능). 이모지를 아이콘 대신 쓰지 않는다.
- 다른 회사의 로고·상표 아이콘을 도식에 넣지 않는다. Lucide에도 브랜드 아이콘은 없다.
- 장식용 아이콘에는 `aria-hidden="true"`를 붙인다. 아이콘만 있는 버튼에는 `aria-label`을 붙인다.
- 숫자·금액 같은 실제 데이터는 사용자가 준 값만 쓴다. 예시 템플릿의 숫자를 그대로 남기지 않는다.
