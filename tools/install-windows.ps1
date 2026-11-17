# 클로드 스킬 설치 (Windows)
# 사용: 이 폴더에서 PowerShell을 열고  powershell -ExecutionPolicy Bypass -File tools\install-windows.ps1
$ErrorActionPreference = "Stop"
$src = Split-Path -Parent $PSScriptRoot
$dst = Join-Path $env:USERPROFILE ".claude"
foreach ($d in "skills","commands","agents") {
  New-Item -ItemType Directory -Force (Join-Path $dst $d) | Out-Null
  Copy-Item -Recurse -Force (Join-Path $src ".claude\$d\*") (Join-Path $dst "$d\")
}
$md = Join-Path $dst "CLAUDE.md"
if (Test-Path $md) {
  Write-Host "기존 $md 가 있어 덮어쓰지 않았습니다. 이 폴더의 CLAUDE.md 내용을 직접 붙여 넣으세요."
} else {
  Copy-Item (Join-Path $src "CLAUDE.md") $md
}
$n = (Get-ChildItem (Join-Path $dst "skills") -Directory).Count
Write-Host "완료: 스킬 $n 개가 $dst\skills 에 있습니다. Claude Code를 껐다 켜세요."
