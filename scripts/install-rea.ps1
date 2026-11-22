# REA 일괄 설치 (Windows): Node.js LTS -> REA 설정
$ErrorActionPreference = "Stop"

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "[1/3] Node.js LTS 설치"
    winget install OpenJS.NodeJS.LTS --accept-source-agreements --accept-package-agreements
    $env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" +
                [Environment]::GetEnvironmentVariable("Path", "User")
} else {
    Write-Host "[1/3] Node.js 이미 설치됨"
}

Write-Host "[2/3] 버전 확인"
node -v
npm -v

Write-Host "[3/3] REA 설정 (Claude Code 선택 -> 승인)"
$dir = Join-Path $env:USERPROFILE "rea-setup"
New-Item -ItemType Directory -Force -Path $dir | Out-Null
Set-Location $dir
npx rea-agents setup

Write-Host "완료. Claude Code를 완전히 종료한 뒤 다시 실행하세요."
