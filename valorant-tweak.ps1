#Requires -RunAsAdministrator
<#
.SYNOPSIS  Valorant Windows 11 latency optimizer
.PARAMETER Apply   Apply changes (default: dry-run preview)
.PARAMETER Force   Skip per-tweak confirmation (requires -Apply)
.EXAMPLE
    .\valorant-tweak.ps1                # preview
    .\valorant-tweak.ps1 -Apply         # interactive apply
    .\valorant-tweak.ps1 -Apply -Force  # apply all without prompts
#>
param([switch]$Apply, [switch]$Force)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Continue'

$DryRun    = -not $Apply
$LogFile   = Join-Path $PSScriptRoot "tweak-log.txt"
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$BackupReg = "$env:USERPROFILE\Desktop\valorant-tweak-backup-$Timestamp.reg"

$script:nOK       = 0
$script:nSkip     = 0
$script:nErr      = 0
$script:needsBoot = $false
$script:results   = [System.Collections.Generic.List[string]]::new()

# ---- helpers ----------------------------------------------------------------

function wLog([string]$msg, [string]$lvl = "INFO") {
    $line = "[$(Get-Date -Format 'HH:mm:ss')][$lvl] $msg"
    Add-Content $LogFile $line -Encoding UTF8
    $col = switch ($lvl) { "WARN"{"Yellow"} "ERROR"{"Red"} "OK"{"Green"} "DRY"{"Cyan"} default{"Gray"} }
    Write-Host $line -ForegroundColor $col
}

function hdr([string]$t) {
    Write-Host ""
    Write-Host ("=" * 64) -ForegroundColor DarkCyan
    Write-Host "  $t" -ForegroundColor Cyan
    Write-Host ("=" * 64) -ForegroundColor DarkCyan
    wLog "=== $t ==="
}

function getReg([string]$p, [string]$n) {
    try { return (Get-ItemProperty $p -Name $n -EA Stop).$n } catch { return $null }
}

function to32u($v) {
    # Reinterpret any int32/uint32 value as its unsigned 32-bit equivalent via byte reinterpretation
    try {
        $as32 = [System.Convert]::ToInt32($v)
        return [System.BitConverter]::ToUInt32([System.BitConverter]::GetBytes($as32), 0)
    } catch {
        return [System.Convert]::ToUInt32($v)
    }
}

function valEq($a, $b, [string]$type) {
    if ($null -eq $a) { return $false }
    if ($type -eq "String") { return "$a" -eq "$b" }
    try { return (to32u $a) -eq (to32u $b) } catch { return $false }
}

function fmtVal($v, [string]$type) {
    if ($null -eq $v) { return "(not set)" }
    if ($type -eq "String") { return "$v" }
    try { return ("0x{0:X8}" -f (to32u $v)) } catch { return "$v" }
}

function tweak([string]$label, [string]$path, [string]$name, $val, [string]$type = "DWord") {
    $cur = getReg $path $name
    Write-Host ""
    Write-Host "  [$label]" -ForegroundColor White
    Write-Host "    Path   : $path"
    Write-Host "    Key    : $name"
    Write-Host "    Before : $(fmtVal $cur $type)"
    Write-Host "    After  : $(fmtVal $val $type)"

    if (valEq $cur $val $type) {
        Write-Host "    Status : already correct" -ForegroundColor Green
        wLog "SKIP  $label"
        $script:nSkip++; $script:results.Add("SKIP   $label"); return
    }
    if ($DryRun) {
        Write-Host "    Status : [DRY-RUN] would change $(fmtVal $cur $type) -> $(fmtVal $val $type)" -ForegroundColor Cyan
        wLog "DRY   $label" "DRY"
        $script:nSkip++; $script:results.Add("DRY    $label"); return
    }
    $go = $Force -or ((Read-Host "    Apply? (y/n)") -eq 'y')
    if (-not $go) {
        Write-Host "    Status : skipped" -ForegroundColor Yellow
        wLog "SKIP  $label (user)" "WARN"
        $script:nSkip++; $script:results.Add("SKIP   $label"); return
    }
    try {
        if (-not (Test-Path $path)) { New-Item $path -Force | Out-Null }
        Set-ItemProperty $path $name $val -Type $type
        Write-Host "    Status : applied" -ForegroundColor Green
        wLog "OK    $label" "OK"
        $script:nOK++; $script:results.Add("OK     $label")
    } catch {
        Write-Host "    Status : ERROR -- $_" -ForegroundColor Red
        wLog "ERROR $label : $_" "ERROR"
        $script:nErr++; $script:results.Add("ERROR  $label")
    }
}

function pingStats([string]$h = "1.1.1.1", [int]$n = 10) {
    $out = ping.exe -n $n $h 2>&1
    $ln  = $out | Where-Object { $_ -match "Minimum" } | Select-Object -First 1
    if ($ln -match "Minimum = (\d+)ms.*Maximum = (\d+)ms.*Average = (\d+)ms") {
        return [pscustomobject]@{ Min=[int]$Matches[1]; Max=[int]$Matches[2]; Avg=[int]$Matches[3] }
    }
    return $null
}

function getAdapterGuid {
    $r = Get-NetRoute -DestinationPrefix "0.0.0.0/0" -EA SilentlyContinue |
         Sort-Object RouteMetric | Select-Object -First 1
    if (-not $r) { return $null }
    $a = Get-NetAdapter -InterfaceIndex $r.InterfaceIndex -EA SilentlyContinue
    if (-not $a) { return $null }
    Write-Host "  Adapter : $($a.Name) [$($a.InterfaceDescription)]" -ForegroundColor Gray
    Write-Host "  GUID    : $($a.InterfaceGuid)" -ForegroundColor Gray
    wLog "Adapter: $($a.Name) GUID=$($a.InterfaceGuid)"
    return $a.InterfaceGuid
}

function getValorantExe {
    $paths = @(
        "C:\Riot Games\VALORANT\live\ShooterGame\Binaries\Win64\VALORANT-Win64-Shipping.exe"
        "D:\Riot Games\VALORANT\live\ShooterGame\Binaries\Win64\VALORANT-Win64-Shipping.exe"
        "E:\Riot Games\VALORANT\live\ShooterGame\Binaries\Win64\VALORANT-Win64-Shipping.exe"
    )
    foreach ($p in $paths) { if (Test-Path $p) { return $p } }
    return $null
}

function backupKeys([string[]]$keys) {
    $header = "Windows Registry Editor Version 5.00`r`n`r`n"
    $body   = ""
    foreach ($k in $keys) {
        $tmp = [IO.Path]::Combine([IO.Path]::GetTempPath(), [IO.Path]::GetRandomFileName() + ".reg")
        & reg.exe export $k $tmp /y 2>$null | Out-Null
        if (Test-Path $tmp) {
            $raw  = [IO.File]::ReadAllText($tmp, [Text.Encoding]::Unicode)
            $raw  = [regex]::Replace($raw, "^Windows Registry Editor Version 5\.00\r?\n(\r?\n)?", "")
            $body += $raw + "`r`n"
            Remove-Item $tmp -Force
        }
    }
    [IO.File]::WriteAllText($BackupReg, $header + $body, [Text.Encoding]::Unicode)
    Write-Host "  Backup  : $BackupReg" -ForegroundColor Green
    wLog "Backup saved: $BackupReg" "OK"
}

# ---- banner -----------------------------------------------------------------

Write-Host ""
Write-Host "+----------------------------------------------------------+" -ForegroundColor Cyan
Write-Host "|  Valorant Windows 11 Latency Optimizer                  |" -ForegroundColor Cyan
$modeStr = if ($DryRun) { "DRY-RUN  (preview -- no changes made)   " } else { "APPLY    (writing registry + settings)  " }
Write-Host "|  Mode : $modeStr|" -ForegroundColor Cyan
Write-Host "+----------------------------------------------------------+" -ForegroundColor Cyan
if ($DryRun) { Write-Host "  Re-run with -Apply to commit. Add -Force to skip prompts." -ForegroundColor Yellow }
wLog "=== Session start | DryRun=$DryRun Force=$Force ==="

# ---- ping BEFORE ------------------------------------------------------------

hdr "Baseline Ping -- 1.1.1.1 (10 packets)"
Write-Host "  Running..." -ForegroundColor Gray
$pb = pingStats
if ($pb) {
    Write-Host "  Before  : min=$($pb.Min)ms  avg=$($pb.Avg)ms  max=$($pb.Max)ms" -ForegroundColor White
    wLog "Ping BEFORE: min=$($pb.Min) avg=$($pb.Avg) max=$($pb.Max)"
}

# ---- detect adapter ---------------------------------------------------------

hdr "Detect Active Network Adapter"
$guid = getAdapterGuid
if (-not $guid) { Write-Host "  WARN: No active adapter detected -- Nagle tweaks skipped" -ForegroundColor Yellow }

# ---- backup -----------------------------------------------------------------

hdr "Registry Backup"

$keysToBackup = @(
    "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile"
    "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\GraphicsDrivers"
    "HKEY_CURRENT_USER\System\GameConfigStore"
    "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\GameDVR"
    "HKEY_CURRENT_USER\Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers"
)
if ($guid) { $keysToBackup += "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\$guid" }

if ($DryRun) {
    Write-Host "  [DRY-RUN] Would backup to : $BackupReg" -ForegroundColor Cyan
    wLog "DRY -- would backup to $BackupReg" "DRY"
} else {
    backupKeys $keysToBackup
}

# ============================================================================
#  [1] NAGLE'S ALGORITHM
# ============================================================================

hdr "[1] Network -- Nagle's Algorithm (per-adapter)"

if ($guid) {
    $tcpIf = "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\$guid"
    tweak "TcpAckFrequency=1 (send ACK immediately)" $tcpIf "TcpAckFrequency" 1
    tweak "TCPNoDelay=1 (disable Nagle batching)"    $tcpIf "TCPNoDelay"      1
} else {
    Write-Host "  Skipped -- adapter GUID not found" -ForegroundColor Yellow
    $script:nSkip += 2
    $script:results.Add("SKIP   TcpAckFrequency (no adapter)")
    $script:results.Add("SKIP   TCPNoDelay (no adapter)")
}

# ============================================================================
#  [2] MULTIMEDIA PROFILE
# ============================================================================

hdr "[2] Network -- Multimedia System Profile"

$mm = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile"
tweak "NetworkThrottlingIndex=0xFFFFFFFF (disable throttle)" $mm "NetworkThrottlingIndex" ([int32]-1)
tweak "SystemResponsiveness=0 (max foreground CPU)"          $mm "SystemResponsiveness"   0

# ============================================================================
#  [3] TCP AUTOTUNING
# ============================================================================

hdr "[3] Network -- TCP Autotuning"

$netshOut  = (& netsh int tcp show global 2>&1) -join "`n"
$curTuning = if ($netshOut -match "Receive Window Auto-Tuning Level\s*:\s*(\S+)") { $Matches[1] } else { "unknown" }
Write-Host ""
Write-Host "  [TCP Autotune]" -ForegroundColor White
Write-Host "    Before : $curTuning"
Write-Host "    Target : normal"

if ($curTuning -eq "normal") {
    Write-Host "    Status : already normal" -ForegroundColor Green
    wLog "SKIP  TCP autotuning (already normal)"
    $script:nSkip++; $script:results.Add("SKIP   TCP autotuning (already normal)")
} elseif ($DryRun) {
    Write-Host "    Status : [DRY-RUN] would set autotuninglevel=normal" -ForegroundColor Cyan
    wLog "DRY   TCP autotuning : $curTuning -> normal" "DRY"
    $script:nSkip++; $script:results.Add("DRY    TCP autotuning")
} else {
    $go = $Force -or ((Read-Host "    Apply? (y/n)") -eq 'y')
    if ($go) {
        & netsh int tcp set global autotuninglevel=normal 2>&1 | Out-Null
        Write-Host "    Status : applied -> normal" -ForegroundColor Green
        wLog "OK    TCP autotuning: $curTuning -> normal" "OK"
        $script:nOK++; $script:results.Add("OK     TCP autotuning -> normal")
    } else {
        Write-Host "    Status : skipped" -ForegroundColor Yellow
        wLog "SKIP  TCP autotuning (user)" "WARN"
        $script:nSkip++; $script:results.Add("SKIP   TCP autotuning")
    }
}

# ============================================================================
#  [4] GPU SCHEDULING (HAGS)
# ============================================================================

hdr "[4] GPU -- Hardware-Accelerated GPU Scheduling"
tweak "HwSchMode=2 (enable HAGS)" "HKLM:\SYSTEM\CurrentControlSet\Control\GraphicsDrivers" "HwSchMode" 2
$script:needsBoot = $true

# ============================================================================
#  [5] POWER PLAN
# ============================================================================

hdr "[5] Power Plan -- Ultimate Performance + USB/PCIe"

$activeOut  = (& powercfg -getactivescheme 2>&1) -join ""
$activeGuid = [regex]::Match($activeOut, '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}').Value
Write-Host "  Current active : $activeOut" -ForegroundColor Gray

if ($DryRun) {
    Write-Host "  [DRY-RUN] Would create/activate Ultimate Performance + disable USB suspend + PCIe LSPM" -ForegroundColor Cyan
    wLog "DRY -- power plan changes" "DRY"
    $script:nSkip += 3
    $script:results.Add("DRY    Ultimate Performance power plan")
    $script:results.Add("DRY    USB selective suspend -> disabled")
    $script:results.Add("DRY    PCIe LSPM -> off")
} else {
    $ultLine = (& powercfg -list 2>&1) | Where-Object { $_ -match "Ultimate Performance" } | Select-Object -First 1
    if ($ultLine) {
        $ultGuid = [regex]::Match("$ultLine", '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}').Value
        Write-Host "  Found existing : $ultGuid" -ForegroundColor Gray
    } else {
        Write-Host "  Creating Ultimate Performance scheme..." -ForegroundColor Gray
        $createOut = (& powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61 2>&1) -join ""
        $ultGuid   = [regex]::Match($createOut, '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}').Value
        if ($ultGuid) {
            & powercfg -changename $ultGuid "Ultimate Performance" 2>&1 | Out-Null
            Write-Host "  Created : $ultGuid" -ForegroundColor Green
            wLog "Created Ultimate Performance $ultGuid" "OK"
        }
    }

    if ($ultGuid) {
        $go = $Force -or ((Read-Host "  Activate + disable USB suspend + PCIe LSPM? (y/n)") -eq 'y')
        if ($go) {
            & powercfg -setactive $ultGuid 2>&1 | Out-Null
            & powercfg -setacvalueindex $ultGuid 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0 2>&1 | Out-Null
            & powercfg -setdcvalueindex $ultGuid 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0 2>&1 | Out-Null
            & powercfg -setacvalueindex $ultGuid 501a4d13-42af-4429-9fd1-a8218c268e20 ee12f906-d277-404b-b6da-e5fa1a576df5 0 2>&1 | Out-Null
            & powercfg -setdcvalueindex $ultGuid 501a4d13-42af-4429-9fd1-a8218c268e20 ee12f906-d277-404b-b6da-e5fa1a576df5 0 2>&1 | Out-Null
            & powercfg -setactive $ultGuid 2>&1 | Out-Null
            Write-Host "  Status  : activated + USB suspend off + PCIe LSPM off" -ForegroundColor Green
            wLog "OK    Power: Ultimate Performance + USB off + PCIe off" "OK"
            $script:nOK += 3
            $script:results.Add("OK     Ultimate Performance power plan")
            $script:results.Add("OK     USB selective suspend -> disabled")
            $script:results.Add("OK     PCIe LSPM -> off")
        } else {
            $script:nSkip += 3
            $script:results.Add("SKIP   Power plan (user)")
            $script:results.Add("SKIP   USB selective suspend")
            $script:results.Add("SKIP   PCIe LSPM")
        }
    } else {
        Write-Host "  ERROR : Could not find/create Ultimate Performance scheme" -ForegroundColor Red
        wLog "ERROR Could not create Ultimate Performance scheme" "ERROR"
        $script:nErr++; $script:results.Add("ERROR  Ultimate Performance scheme")
    }
}

# ============================================================================
#  [6] GAME DVR
# ============================================================================

hdr "[6] Game DVR / Game Bar"
tweak "GameDVR_Enabled=0"         "HKCU:\System\GameConfigStore"                      "GameDVR_Enabled"         0
tweak "GameDVR_FSEBehaviorMode=2" "HKCU:\System\GameConfigStore"                      "GameDVR_FSEBehaviorMode"  2
tweak "AllowGameDVR=0 (policy)"   "HKLM:\SOFTWARE\Policies\Microsoft\Windows\GameDVR" "AllowGameDVR"            0

# ============================================================================
#  [7] VALORANT COMPAT FLAGS
# ============================================================================

hdr "[7] Valorant EXE Compatibility Flags"
$vExe = getValorantExe
if ($vExe) {
    Write-Host "  Found   : $vExe" -ForegroundColor Gray
    tweak "Disable fullscreen opt + DPI aware" `
          "HKCU:\Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers" `
          $vExe `
          "~ DISABLEDXMAXIMIZEDWINDOWEDMODE HIGHDPIAWARE" `
          "String"
} else {
    Write-Host "  WARN: VALORANT-Win64-Shipping.exe not found -- skipping compat flags" -ForegroundColor Yellow
    wLog "WARN Valorant exe not found" "WARN"
    $script:nSkip++; $script:results.Add("SKIP   Valorant compat flags (exe not found)")
}

# ---- ping AFTER -------------------------------------------------------------

if (-not $DryRun -and $script:nOK -gt 0) {
    hdr "Post-Tweak Ping -- 1.1.1.1 (10 packets)"
    Start-Sleep -Seconds 2
    $pa = pingStats
    if ($pa -and $pb) {
        Write-Host "  Before  : min=$($pb.Min)ms  avg=$($pb.Avg)ms  max=$($pb.Max)ms"
        Write-Host "  After   : min=$($pa.Min)ms  avg=$($pa.Avg)ms  max=$($pa.Max)ms"
        $d    = [int]$pb.Avg - [int]$pa.Avg
        $note = if ($d -gt 0) { "-$d ms improvement" } elseif ($d -lt 0) { "+$([math]::Abs($d)) ms regression" } else { "no change" }
        $col  = if ($d -ge 0) { "Green" } else { "Yellow" }
        Write-Host "  Delta   : $note" -ForegroundColor $col
        wLog "Ping AFTER: min=$($pa.Min) avg=$($pa.Avg) max=$($pa.Max) | delta=$note"
    }
}

# ---- summary ----------------------------------------------------------------

hdr "Summary"
Write-Host ""
foreach ($ln in $script:results) {
    $col = if ($ln -match "^OK") {"Green"} elseif ($ln -match "^ERROR") {"Red"} elseif ($ln -match "^DRY") {"Cyan"} else {"Gray"}
    Write-Host "  $ln" -ForegroundColor $col
}
Write-Host ""
Write-Host ("  Applied  : {0,2}" -f $script:nOK)   -ForegroundColor Green
Write-Host ("  Skipped  : {0,2}" -f $script:nSkip)
if ($script:nErr -gt 0) { Write-Host ("  Errors   : {0,2}" -f $script:nErr) -ForegroundColor Red }

if ($DryRun) {
    Write-Host ""
    Write-Host "  MODE: DRY-RUN -- nothing was changed." -ForegroundColor Cyan
    Write-Host "  Run with -Apply to commit. Add -Force to skip per-tweak prompts." -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "  Backup  : $BackupReg" -ForegroundColor Gray
    Write-Host "  Log     : $LogFile"   -ForegroundColor Gray
    if ($script:needsBoot) {
        Write-Host ""
        Write-Host "  !! RESTART REQUIRED -- HAGS (GPU Scheduling) needs a reboot !!" -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "  REMINDER: Tweaks reduce client processing delay ~3-8ms total." -ForegroundColor DarkGray
    Write-Host "            Physical RTT to SG (~68ms) is distance-bound, not reducible by Windows tweaks." -ForegroundColor DarkGray
}

wLog "=== Session end | OK=$($script:nOK) Skip=$($script:nSkip) Err=$($script:nErr) ==="
