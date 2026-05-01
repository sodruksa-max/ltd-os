#Requires -RunAsAdministrator
<#
.SYNOPSIS  Restore registry from valorant-tweak backup
.PARAMETER BackupFile  Path to .reg file. Omit to auto-find latest on Desktop.
#>
param([string]$BackupFile = "")

if (-not $BackupFile) {
    $found = Get-ChildItem "$env:USERPROFILE\Desktop\valorant-tweak-backup-*.reg" -EA SilentlyContinue |
             Sort-Object Name -Descending | Select-Object -First 1
    if ($found) {
        $BackupFile = $found.FullName
        Write-Host "Auto-selected backup: $BackupFile" -ForegroundColor Cyan
    } else {
        Write-Error "No backup found on Desktop matching 'valorant-tweak-backup-*.reg'. Run valorant-tweak.ps1 -Apply first."
        exit 1
    }
}

if (-not (Test-Path $BackupFile)) {
    Write-Error "File not found: $BackupFile"
    exit 1
}

Write-Host ""
Write-Host "Restoring registry from:" -ForegroundColor Cyan
Write-Host "  $BackupFile" -ForegroundColor White
Write-Host ""

$result = & reg.exe import $BackupFile 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "Registry restored successfully." -ForegroundColor Green
    Write-Host ""
    Write-Host "Notes:" -ForegroundColor Yellow
    Write-Host "  - Some settings (e.g. HAGS) require a restart to take full effect."
    Write-Host "  - Power plan is NOT restored by this script."
    Write-Host "    To restore: powercfg -setactive <original-guid>"
    Write-Host "    To list schemes: powercfg -list"
    Write-Host "  - TCP autotuning is NOT restored by this script."
    Write-Host "    To restore: netsh int tcp set global autotuninglevel=normal (or disabled/experimental)"
} else {
    Write-Host "Restore failed:" -ForegroundColor Red
    Write-Host $result
    exit 1
}
