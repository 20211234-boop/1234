#!/bin/bash
# 클로드 스킬 설치 (Mac/Linux)
# 사용: 이 폴더에서 터미널을 열고  bash tools/install-mac.sh
set -e
SRC="$(cd "$(dirname "$0")/.." && pwd)"
DST="$HOME/.claude"
for d in skills commands agents; do
  mkdir -p "$DST/$d"
  cp -R "$SRC/.claude/$d/." "$DST/$d/"
done
if [ -f "$DST/CLAUDE.md" ]; then
  echo "기존 $DST/CLAUDE.md 가 있어 덮어쓰지 않았습니다. 이 폴더의 CLAUDE.md 내용을 직접 붙여 넣으세요."
else
  cp "$SRC/CLAUDE.md" "$DST/CLAUDE.md"
fi
echo "완료: 스킬 $(ls -d "$DST/skills"/*/ | wc -l | tr -d ' ')개가 $DST/skills 에 있습니다. Claude Code를 껐다 켜세요."
