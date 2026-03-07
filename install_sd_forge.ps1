# SD Forge (Stable Diffusion) 설치 스크립트
# 이 스크립트는 1-Click Standalone 버전을 다운로드하고 압축을 해제합니다.

$ErrorActionPreference = "Stop"

$InstallDir = "C:\sd-webui-forge"
$DownloadUrl = "https://github.com/lllyasviel/stable-diffusion-webui-forge/releases/download/latest/webui_forge_cu121_torch21.7z"
$ZipFile = "$InstallDir\webui_forge.7z"

Write-Host "========================================"
Write-Host "Stable Diffusion WebUI Forge 설치 준비"
Write-Host "========================================"

# 설치 폴더 생성
if (-not (Test-Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
    Write-Host "[$InstallDir] 폴더를 생성했습니다."
}

Write-Host "1. Forge 1-Click 패키지를 다운로드합니다. (약 1.8GB, 시간이 오래 걸릴 수 있습니다)"
Invoke-WebRequest -Uri $DownloadUrl -OutFile $ZipFile -UseBasicParsing

Write-Host "2. 다운로드 완료! 압축을 해제하려면 7-Zip이 필요합니다."
Write-Host "만약 7-Zip이 없다면, winget으로 설치를 시도합니다."
if (-not (Get-Command "7z" -ErrorAction SilentlyContinue)) {
    Write-Host "7-Zip이 설치되어 있지 않아 설치를 진행합니다..."
    winget install -e --id 7zip.7zip --accept-source-agreements --accept-package-agreements
}

Write-Host "3. 압축을 해제합니다..."
# 7z.exe 경로 찾기 (환경 변수에 없을 경우 대비)
$7zPath = "C:\Program Files\7-Zip\7z.exe"
if (Test-Path $7zPath) {
    & $7zPath x $ZipFile -o"$InstallDir" -y
}
else {
    7z x $ZipFile -o"$InstallDir" -y
}

Write-Host "4. 압축 해제 완료! 다운로드한 7z 파일은 삭제합니다."
Remove-Item $ZipFile -Force

Write-Host "========================================"
Write-Host "설치가 완료되었습니다!"
Write-Host "다음 파일을 실행하여 SD Forge를 시작하세요:"
Write-Host "1. C:\sd-webui-forge\webui_forge_cu121_torch21\update.bat (최초 1회 실행하여 최신 버전 업데이트)"
Write-Host "2. C:\sd-webui-forge\webui_forge_cu121_torch21\run.bat (이후 실행 시 사용)"
Write-Host "========================================"
Write-Host "주의: run.bat을 처음 실행하면 필수 모델(약 4~5GB)을 추가 다운로드하므로 시간이 다소 소요됩니다."
