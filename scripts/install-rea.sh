#!/usr/bin/env bash
# REA 일괄 설치 (Mac/Linux): Node.js LTS -> REA 설정
set -euo pipefail

if ! command -v node >/dev/null 2>&1; then
  echo "[1/3] Node.js 설치"
  if command -v brew >/dev/null 2>&1; then
    brew install node
  else
    echo "Homebrew가 없습니다. https://nodejs.org 에서 LTS를 설치한 뒤 다시 실행하세요."
    exit 1
  fi
else
  echo "[1/3] Node.js 이미 설치됨"
fi

echo "[2/3] 버전 확인"
node -v
npm -v

echo "[3/3] REA 설정 (Claude Code 선택 -> 승인)"
mkdir -p "$HOME/rea-setup"
cd "$HOME/rea-setup"
npx rea-agents setup

echo "완료. Claude Code를 완전히 종료한 뒤 다시 실행하세요."
