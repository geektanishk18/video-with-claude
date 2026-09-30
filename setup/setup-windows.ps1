# FiguredOutAI reel workflow: one-time setup for Windows.
# Run from the repo root in PowerShell:   powershell -ExecutionPolicy Bypass -File setup\setup-windows.ps1
$ErrorActionPreference = 'Stop'
$Repo = Split-Path -Parent $PSScriptRoot

function Have($cmd) { [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }
function Refresh-Path {
  $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [Environment]::GetEnvironmentVariable('Path', 'User')
}

Write-Host "`n1/5  System tools (winget)" -ForegroundColor Cyan
$tools = @(
  @{cmd = 'python'; id = 'Python.Python.3.12'},
  @{cmd = 'node';   id = 'OpenJS.NodeJS.LTS'},
  @{cmd = 'ffmpeg'; id = 'Gyan.FFmpeg'},
  @{cmd = 'git';    id = 'Git.Git'}
)
foreach ($t in $tools) {
  if (Have $t.cmd) { Write-Host "  $($t.cmd) already installed" }
  else { Write-Host "  installing $($t.id)..."; winget install --id $t.id -e --accept-source-agreements --accept-package-agreements | Out-Null }
}
Refresh-Path

Write-Host "`n2/5  Python packages" -ForegroundColor Cyan
python -m pip install --upgrade pip | Out-Null
python -m pip install -r "$Repo\setup\requirements.txt"

Write-Host "`n3/5  Brand fonts (Poppins, Inter) for this user" -ForegroundColor Cyan
$fontDir = "$env:LOCALAPPDATA\Microsoft\Windows\Fonts"
New-Item -ItemType Directory -Force -Path $fontDir | Out-Null
$regKey = 'HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Fonts'
Get-ChildItem "$Repo\skills\figuredout-reel\assets\fonts\*.ttf" | ForEach-Object {
  $dest = Join-Path $fontDir $_.Name
  Copy-Item $_.FullName $dest -Force
  New-ItemProperty -Path $regKey -Name ($_.BaseName + ' (TrueType)') -Value $dest -PropertyType String -Force | Out-Null
  Write-Host "  $($_.Name)"
}

Write-Host "`n4/5  Claude Code skills -> $HOME\.claude\skills" -ForegroundColor Cyan
$skillDir = "$HOME\.claude\skills"
New-Item -ItemType Directory -Force -Path $skillDir | Out-Null
foreach ($s in 'figuredout-reel', 'figuredout-reel-rick-morty') {
  if (Test-Path "$skillDir\$s") { Remove-Item -Recurse -Force "$skillDir\$s" }
  Copy-Item -Recurse "$Repo\skills\$s" "$skillDir\$s"
  Write-Host "  $s"
}

Write-Host "`n5/5  Remotion for the example reel (npm install)" -ForegroundColor Cyan
Push-Location "$Repo\reels\unified-ai-inbox\video"
npm install
Pop-Location

Write-Host "`nChecking everything..." -ForegroundColor Cyan
python "$Repo\setup\check.py"
Write-Host "Restart Claude Code so it picks up the skills. The first Remotion render downloads its own browser (~100 MB); the first voiceover alignment downloads the Whisper model (~480 MB)."
