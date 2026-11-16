#!/usr/bin/env python3
"""코워크 업로드용 "묶음 스킬" ZIP을 만든다.

코워크는 올릴 수 있는 스킬 개수가 제한되어 있어, 비슷한 스킬을 묶음 하나로 합친다.
묶음 스킬의 SKILL.md는 상황을 보고 modes/<원래이름>/MODE.md를 읽어 따르게 하는 안내판이다.

실행: python3 tools/build_cowork_bundles.py   (저장소 맨 위 폴더에서)
결과: cowork-bundles/<묶음>.zip, cowork-bundles/all-bundles.zip
"""
import os
import re
import shutil
import tempfile
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, ".claude", "skills")
COMMANDS = os.path.join(ROOT, ".claude", "commands")
OUT = os.path.join(ROOT, "cowork-bundles")

# (모드 이름, 언제 쓰는지 - 한국어 한 줄)
BUNDLES = {
    "daily-kit": {
        "desc": (
            "매일 쓰는 업무 보조 묶음. 대화 정리·인수인계(handoff), 사용량 한도 절약(limit-saver), "
            "숫자·법규·사실 검증(crash-out), AI티 나는 글 다듬기(humanizer), 답을 첫 줄에 쓰는 간결 모드(i-have-adhd), "
            "초간결 답변(caveman). \"정리해서 넘겨줘\", \"인수인계\", \"한도\", \"토큰 아껴\", \"맞는지 확인\", \"검증해줘\", "
            "\"사실 확인\", \"요율\", \"법 조항\", \"공지문 다듬어\", \"메일 자연스럽게\", \"AI티 없애\", \"짧게 답해\", "
            "\"/handoff\", \"/crash-out\", \"/humanizer\", \"/limit-saver\", \"/i-have-adhd\", \"/caveman\" 요청에 사용."
        ),
        "modes": [
            ("handoff", "대화가 길어졌거나 \"정리해서 넘겨줘\", \"인수인계\"라고 할 때"),
            ("limit-saver", "\"한도\", \"토큰 아껴\", \"사용량 아껴\"라고 할 때 (켜면 대화 끝까지 유지)"),
            ("crash-out", "숫자·금액·요율·법 조항·사실을 확인할 때, \"맞는지 확인\", \"검증\"이라고 할 때"),
            ("humanizer", "공지문·메일·보고서 문장을 자연스럽게 다듬을 때, \"AI티 없애\"라고 할 때"),
            ("i-have-adhd", "\"/i-have-adhd\" 또는 \"답부터 짧게\"라고 할 때 (켜면 \"stop adhd mode\"까지 유지)"),
            ("caveman", "\"/caveman\", \"초간결\", \"아주 짧게\"라고 할 때. limit-saver·i-have-adhd와 동시에 켜지 않는다"),
        ],
    },
    "design-kit": {
        "desc": (
            "보여줄 결과물 디자인 묶음. 해외 서비스 84곳의 디자인 시스템 적용(awesome-design), AI티 금지 목록과 자가 검사"
            "(aura-farming), 개성 있는 웹 디자인(frontend-design), 회사 웹사이트 제작(taste), 이미지·스크린샷을 웹페이지로"
            "(image-to-code), 웹 접근성·UI 점검(web-design-guidelines). \"슬라이드\", \"PPT\", \"발표자료\", \"포스터\", "
            "\"OO 스타일로\", \"OO 느낌으로\", \"디자인 시스템\", \"웹페이지\", \"랜딩\", \"사이트\", \"이 이미지처럼\", "
            "\"스크린샷을 코드로\", \"UI 검토\", \"접근성 점검\", \"AI티 안 나게\" 요청에 사용."
        ),
        "modes": [
            ("awesome-design", "\"OO 스타일로\", \"디자인 시스템 골라줘\", PPT·보고서·웹의 색과 서체를 정할 때"),
            ("aura-farming", "슬라이드·포스터·광고·웹 같은 보여줄 결과물을 만들 때, 내보내기 전 AI티 검사"),
            ("frontend-design", "웹페이지·화면을 새로 만들거나 고칠 때 (taste와 둘 중 하나만)"),
            ("taste", "회사·제품·가게 웹사이트를 본격적으로 만들 때 (frontend-design과 둘 중 하나만)"),
            ("image-to-code", "스크린샷·시안 이미지를 웹페이지 코드로 만들 때"),
            ("web-design-guidelines", "만든 웹페이지를 접근성·폼·애니메이션 규칙으로 점검할 때"),
        ],
        "order": "PPT·보고서: awesome-design → 제작 → aura-farming. 웹: awesome-design → frontend-design 또는 taste → web-design-guidelines.",
    },
    "egm-kit": {
        "desc": (
            "구글 코끼리·금붕어 모델(EGM). 맥락을 아는 AI가 기획서·설계 문서를 쓰고, 이전 대화를 모르는 새 AI 리뷰어들이 "
            "백지 상태에서 허점을 찾는다. 사용자가 \"egm 써줘\", \"egm으로\", \"egm 검토\", \"코끼리 금붕어\", \"금붕어 검토\", "
            "\"egm 초안\", \"egm 지적 반영\"이라고 할 때 사용. \"egm\"이라는 말 없이 기획서·제안서 검토만 부탁하면 바로 실행하지 "
            "말고 \"EGM으로 검토할까요? 한도를 많이 씁니다\"라고 먼저 묻는다."
        ),
        "modes": [
            ("egm-brainstorm", "아이디어만 있을 때 \"egm 써줘\" — 질문으로 요구사항 정리"),
            ("egm-draft", "\"egm으로 기획서 써줘\", \"egm 초안\" — 설계 문서를 섹션별로 작성"),
            ("egm-review", "문서가 있을 때 \"egm 써줘\", \"egm 검토\" — 금붕어 리뷰어 5단계 검토"),
            ("egm-resolve", "\"egm 지적 반영해줘\" — 리뷰 지적 사항 반영"),
            ("egm-review-loop", "\"지적 없을 때까지 egm\" — 검토·수정 반복"),
            ("egm-bootstrap", "\"egm으로 코드 문서화\" — 기존 코드에서 README·설계 문서 만들기"),
            ("egm-drift-report", "\"egm으로 설계와 코드 비교\" — 코드가 설계에서 벗어났는지 점검"),
        ],
        "order": "문서가 있는지 애매하면 한 줄로 묻는다. 순서: brainstorm → draft → review → resolve.",
    },
    "dev-kit": {
        "desc": (
            "프로그램·코드 작업 묶음. 구현 계획(ecc-plan), 코드 리뷰(ecc-code-review), 빌드 에러 수정(ecc-build-fix), "
            "테스트 보강(ecc-test-coverage), 과한 코드 막는 원칙(karpathy-guidelines), 메타 Astryx 디자인 시스템으로 React "
            "웹앱 만들기(astryx), 브라우저 자동화(agent-browser). \"계획 세워줘\", \"코드 리뷰\", \"빌드 에러\", \"테스트 추가\", "
            "\"커버리지\", \"스크립트 짜줘\", \"매크로\", \"사내 웹앱\", \"관리자 대시보드\", \"Astryx\", \"브라우저로 확인\" 요청에 사용."
        ),
        "modes": [
            ("karpathy-guidelines", "코드·스크립트·매크로를 쓰거나 고칠 때 항상 (가정 먼저 밝히기, 최소 코드)"),
            ("ecc-plan", "기능을 새로 만들기 전 \"계획 세워줘\" — 확인받기 전에는 코드를 쓰지 않는다"),
            ("ecc-code-review", "\"코드 리뷰\", \"검토해줘\" — 보안·품질 점검 (GitHub 게시는 요청할 때만)"),
            ("ecc-build-fix", "\"빌드 에러\", \"빌드가 안 돼\" — 에러를 하나씩 최소 수정"),
            ("ecc-test-coverage", "\"테스트 추가\", \"커버리지\" — 80% 미만 파일에 테스트 보강"),
            ("astryx", "\"Astryx\"라고 하거나 React로 사내 웹앱·대시보드를 만들 때 (astryx 프로그램 설치 필요)"),
            ("agent-browser", "\"agent-browser\"라고 하거나 그 프로그램이 설치된 컴퓨터에서 브라우저 확인이 필요할 때"),
        ],
    },
    "idea-kit": {
        "desc": (
            "아이디어·중요 결과물 묶음. 창업·서비스 아이디어를 혹독하게 검증(larp), 같은 과제를 6가지 전략으로 동시에 풀고 "
            "심판이 좋은 부분만 합치기(67, 한도를 많이 씀). \"사업 아이디어 어때\", \"이 서비스 될까\", \"아이디어 검증\", "
            "\"/larp\", \"/67\", \"여러 버전으로 만들어서 제일 좋은 걸로\" 요청에 사용."
        ),
        "modes": [
            ("larp", "사업·앱·서비스 아이디어를 평가할 때"),
            ("67", "사용자가 \"/67\" 또는 \"여러 버전 비교\"를 명시할 때만. 한도를 7배 쓰므로 먼저 확인한다"),
        ],
    },
}

STANDALONE = ["infographic-kit"]  # 그대로 올리는 스킬
SKIP_DIRS = {"assets"}  # taste의 38MB 이미지 자산은 코워크용에서 뺀다


def copy_mode(name, dest):
    src = os.path.join(SKILLS, name)
    if os.path.isdir(src):
        ignore = shutil.ignore_patterns(*SKIP_DIRS) if name == "taste" else None
        shutil.copytree(src, dest, ignore=ignore)
        os.rename(os.path.join(dest, "SKILL.md"), os.path.join(dest, "MODE.md"))
        return
    cmd = os.path.join(COMMANDS, name + ".md")  # ecc-* 명령어를 스킬 형식으로 바꾼다
    text = open(cmd, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    desc = re.search(r"^description:\s*(.*)$", m.group(1), re.M).group(1)
    os.makedirs(dest)
    with open(os.path.join(dest, "MODE.md"), "w", encoding="utf-8") as f:
        f.write(f"---\nname: {name}\ndescription: {desc}\n---\n{m.group(2)}")


def router(name, spec):
    assert len(spec["desc"]) <= 1024, f"{name} 설명이 1024자를 넘음: {len(spec['desc'])}"
    rows = "\n".join(f"| `{m}` | {w} | `modes/{m}/MODE.md` |" for m, w in spec["modes"])
    order = f"\n**순서:** {spec['order']}\n" if spec.get("order") else ""
    return f"""---
name: {name}
description: {spec['desc']}
---

# {name}

여러 스킬을 하나로 묶은 안내판이다. 요청에 맞는 모드를 고르고, 그 모드의 `MODE.md`를 **끝까지 읽은 뒤 그대로 따른다.** (`MODE.md`는 원래 스킬의 SKILL.md를 이름만 바꾼 것이다.)

| 모드 | 언제 | 읽을 파일 |
|---|---|---|
{rows}
{order}
## 규칙

- 모드의 `MODE.md`가 가리키는 파일 경로(`references/`, `agents/`, `resources/`, `scripts/` 등)는 그 모드 폴더(`modes/<모드>/`) 기준이다.
- 맞는 모드가 둘 이상이면 표의 위쪽부터 쓴다. 맞는 모드가 없으면 이 묶음을 쓰지 않는다.
- 모드 이름으로 부르면(예: "/crash-out", "crash-out 써줘") 그 모드를 바로 쓴다.
- 어떤 모드를 쓰는지 첫 줄에 한 번만 짧게 알린다. 예: "crash-out 모드로 확인합니다."
"""


def zipdir(folder, zpath):
    base = os.path.dirname(folder)
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for d, _, files in os.walk(folder):
            for f in sorted(files):
                p = os.path.join(d, f)
                z.write(p, os.path.relpath(p, base))


def main():
    if os.path.isdir(OUT):
        for f in os.listdir(OUT):
            if f.endswith(".zip"):
                os.remove(os.path.join(OUT, f))
    os.makedirs(OUT, exist_ok=True)
    made = []
    with tempfile.TemporaryDirectory() as tmp:
        for name, spec in BUNDLES.items():
            b = os.path.join(tmp, name)
            os.makedirs(os.path.join(b, "modes"))
            for mode, _ in spec["modes"]:
                copy_mode(mode, os.path.join(b, "modes", mode))
            open(os.path.join(b, "SKILL.md"), "w", encoding="utf-8").write(router(name, spec))
            zipdir(b, os.path.join(OUT, name + ".zip"))
            made.append(name)
        for name in STANDALONE:
            zipdir(os.path.join(SKILLS, name), os.path.join(OUT, name + ".zip"))
            made.append(name)
    with zipfile.ZipFile(os.path.join(OUT, "all-bundles.zip"), "w") as z:
        for name in made:
            z.write(os.path.join(OUT, name + ".zip"), name + ".zip")
    for name in made:
        kb = os.path.getsize(os.path.join(OUT, name + ".zip")) // 1024
        print(f"{name}.zip\t{kb} KB")


if __name__ == "__main__":
    main()
