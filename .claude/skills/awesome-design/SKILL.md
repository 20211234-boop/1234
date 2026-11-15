---
name: awesome-design
description: 해외 서비스 84곳(Claude, Linear, Vercel, Stripe, Notion, Apple 등)의 디자인 시스템(색·서체·간격·버튼 규칙)을 골라 웹페이지, 슬라이드(PPT), 보고서, 포스터에 적용한다. "OO 스타일로", "Linear 느낌으로", "디자인 시스템 골라줘", "/awesome-design" 같은 요청에 사용.
---

# Awesome Design — 디자인 시스템 고르고 적용하기

`systems/` 폴더에 실제 서비스의 디자인을 분석한 DESIGN.md 파일 84개가 있다.
각 파일 머리말(frontmatter)에 색(colors), 서체(typography), 모서리·간격 규칙이 토큰으로 정리되어 있다.

## 절차

1. **고르기.** 사용자가 브랜드를 지정하면 그 파일을 쓴다. 지정하지 않으면 결과물의 대상·분위기를 묻거나
   추정해서 2~3개 후보를 한 줄씩 비교해 제안하고, 하나를 고르게 한다. 파일 전체를 다 읽지 말고
   후보 파일의 앞부분(description, colors, typography)만 읽어 비교한다.
2. **읽기.** 고른 파일을 읽고 색 토큰, 서체 역할, 크기 단계, 모서리 반경, 간격 단위, 버튼·카드 규칙을 뽑는다.
3. **적용.** 결과물 형식에 맞게 옮긴다.
   - 웹: CSS 변수(`:root`)로 토큰을 정의하고 컴포넌트에 쓴다.
   - 슬라이드(PPT)·보고서: 배경/본문/강조색 3~4개, 제목·본문 서체, 글자 크기 단계만 가져온다.
     한글 본문은 원래 서체 대신 비슷한 성격의 한글 서체(예: Pretendard, Noto Sans KR, 나눔명조)로 바꾼다.
   - 포스터·SNS 이미지: 대표색 1개 + 보조색 1개 + 서체 1~2개로 단순화한다.
4. **보고.** 적용한 시스템 이름과 쓴 토큰(색 hex, 서체)을 3줄 이내로 알린다.

## 지켜야 할 것

- **분위기와 규칙만 빌린다.** 그 회사의 로고, 상표, 이름, 문구, 사진을 넣거나 그 회사 사이트처럼 보이게 만들지 않는다.
- 이 파일들은 공식 문서가 아니라 제3자가 분석한 것이다. 사용자 회사의 브랜드 가이드가 있으면 그것이 우선이다.
- 사용자가 직접 정한 색·서체가 있으면 그것을 따른다.

## 들어 있는 시스템

1win airbnb airtable aljazeera apple binance bmw-m bmw bugatti cal claude clay clickhouse cohere coinbase composio cursor dell-1996 dji elevenlabs expo ferrari figma framer hashicorp hp ibm intercom jobright kraken lamborghini linear.app lovable mastercard mercury meta minimax mintlify miro mistral.ai mongodb mydealz nerdwallet nike nintendo-2001 notion nvidia ollama opencode.ai oracle oura pinterest playstation posthog raycast renault replicate resend revolut runwayml sanity sap sentry shopify slack spacex spotify starbucks stripe supabase superhuman tesla theverge together.ai uber vercel vodafone voltagent warp webflow wired wise x.ai zapier 
