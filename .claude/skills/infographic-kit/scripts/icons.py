#!/usr/bin/env python3
"""Lucide 아이콘 검색·출력 도구 (표준 라이브러리만 사용).

사용법
  python icons.py search 급여 연봉            # 키워드(한/영)로 후보 찾기
  python icons.py svg wallet --size 32 --color "#1d4ed8"
  python icons.py pick 급여 근태 채용 평가      # 개념마다 서로 다른 아이콘 1개씩 (중복 없음)
  python icons.py symbol wallet clock target   # HTML에 한 번 넣는 <symbol> 묶음 + <use> 예시
  python icons.py categories                   # 범주 목록
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ICONS = json.load(open(os.path.join(HERE, "..", "assets", "icons.json"), encoding="utf-8"))
KO = json.load(open(os.path.join(HERE, "..", "assets", "ko-keywords.json"), encoding="utf-8"))


def search(word, limit=12):
    w = word.lower()
    hits = [n for n in KO.get(word, []) if n in ICONS]
    for k, names in KO.items():
        if w in k.lower() and k != word:
            hits += [n for n in names if n in ICONS]
    scored = []
    for name, d in ICONS.items():
        s = 0
        if w == name:
            s = 100
        elif w in name.split("-"):
            s = 60
        elif w in name:
            s = 40
        if w in [t.lower() for t in d["t"]]:
            s = max(s, 50)
        elif any(w in t.lower() for t in d["t"]):
            s = max(s, 20)
        if w in d["c"]:
            s = max(s, 10)
        if s:
            scored.append((-s, name))
    hits += [n for _, n in sorted(scored)]
    seen, out = set(), []
    for n in hits:
        if n not in seen:
            seen.add(n)
            out.append(n)
    return out[:limit]


def svg(name, size=24, color="currentColor", stroke=2, extra=""):
    if name not in ICONS:
        sys.exit(f"없는 아이콘: {name}  (search로 찾기)")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" '
            f'fill="none" stroke="{color}" stroke-width="{stroke}" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true"{extra}>{ICONS[name]["b"]}</svg>')


def pick(words):
    used, rows = set(), []
    for w in words:
        choice = next((n for n in search(w, 30) if n not in used), None)
        if choice:
            used.add(choice)
        rows.append((w, choice or "(후보 없음: 영어 키워드로 다시 검색)"))
    return rows


def main(a):
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        return
    cmd, rest = a[0], a[1:]
    if cmd == "search":
        for w in rest:
            print(f"{w}: " + ", ".join(search(w)))
    elif cmd == "svg":
        name = rest[0]
        opts = dict(zip(rest[1::2], rest[2::2]))
        print(svg(name, opts.get("--size", 24), opts.get("--color", "currentColor"), opts.get("--stroke", 2)))
    elif cmd == "pick":
        for w, n in pick(rest):
            print(f"{w}\t{n}")
    elif cmd == "symbol":
        print('<svg style="display:none" xmlns="http://www.w3.org/2000/svg">')
        for n in rest:
            if n not in ICONS:
                sys.exit(f"없는 아이콘: {n}")
            print(f'  <symbol id="i-{n}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                  f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[n]["b"]}</symbol>')
        print("</svg>")
        print(f'<!-- 사용: <svg class="ico"><use href="#i-{rest[0]}"/></svg> -->')
    elif cmd == "categories":
        cats = {}
        for d in ICONS.values():
            for c in d["c"]:
                cats[c] = cats.get(c, 0) + 1
        for c, k in sorted(cats.items(), key=lambda x: -x[1]):
            print(f"{c}\t{k}")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
