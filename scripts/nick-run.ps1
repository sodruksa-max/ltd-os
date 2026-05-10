# nick-run.ps1 — run Nick exit check daily (9:30 AM ET = 8:30 PM Thailand)
# Setup Task Scheduler: schtasks /create /tn "Nick Exit Check" /tr "powershell -File C:\Users\sodru\ltd-os\scripts\nick-run.ps1" /sc daily /st 20:30

$repoRoot = "C:\Users\sodru\ltd-os"
$venvPython = "$repoRoot\code\python\screener-venv\Scripts\python.exe"
$script = "$repoRoot\code\python\nick_trader\exit_check.py"
$envFile = "$repoRoot\.secrets\.env"

# Load .env
Get-Content $envFile | Where-Object { $_ -notmatch "^#" -and $_ -match "=" } | ForEach-Object {
    $parts = $_ -split "=", 2
    [System.Environment]::SetEnvironmentVariable($parts[0].Trim(), $parts[1].Trim(), "Process")
}

Set-Location $repoRoot
& $venvPython $script
