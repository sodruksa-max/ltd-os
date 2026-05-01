# Valorant Windows 11 Latency Optimizer

ลด client-side processing delay สำหรับ Valorant บน Windows 11  
**เป้าหมาย**: ลด ~3-8ms จาก current 68ms ping ไป SG server

---

## วิธีรัน

เปิด **PowerShell as Administrator** แล้วรัน:

```powershell
# 1. ดู preview ก่อน (ไม่แก้อะไร — dry-run)
.\valorant-tweak.ps1

# 2. แก้จริง พร้อมถามยืนยันแต่ละ tweak
.\valorant-tweak.ps1 -Apply

# 3. แก้ทุกอย่างโดยไม่ถาม
.\valorant-tweak.ps1 -Apply -Force
```

**Restore** (ถ้าอยากเลิกทุกอย่าง):
```powershell
.\valorant-tweak-restore.ps1
```

---

## สิ่งที่ script ทำ

### [1] Nagle's Algorithm
**Registry**: `HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\{adapter-GUID}`

| Key | Value | ความหมาย |
|-----|-------|----------|
| TcpAckFrequency | 1 | ส่ง ACK ทันทีทุก packet |
| TCPNoDelay | 1 | ปิดการรวม packets เล็กๆ ก่อนส่ง |

Nagle's algorithm ออกแบบมาเพื่อ throughput — รวม packets ไว้จนกว่าจะใหญ่พอ ดีสำหรับ file transfer แต่เพิ่ม latency 10-40ms ในเกม FPS ที่ส่ง packets เล็กๆ ต่อเนื่อง

**Expected: 5-20ms** (ขึ้นกับ ISP และ current state)

---

### [2] NetworkThrottlingIndex
**Registry**: `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile`  
**Value**: `NetworkThrottlingIndex = 0xFFFFFFFF`

Windows จำกัด CPU interrupt สำหรับ network โดย default เพื่อประหยัดพลังงาน ค่า `0xFFFFFFFF` = ปิด throttling ทั้งหมดสำหรับ multimedia apps (Valorant จัดเป็น multimedia app)

**Expected: 1-3ms**

---

### [3] SystemResponsiveness
**Registry**: `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile`  
**Value**: `SystemResponsiveness = 0`

กำหนด % CPU ที่ reserved ให้ background processes  
- Default = 20 (20% ของ CPU time ให้ background)
- Value 0 = เกม (foreground) ได้ CPU สูงสุด

**Expected: 1-2ms**

---

### [4] TCP Autotuning
**Command**: `netsh int tcp set global autotuninglevel=normal`

| Level | ผล |
|-------|-----|
| disabled | แย่ — ปิด dynamic window sizing |
| normal | ✅ ดีที่สุดสำหรับ gaming |
| experimental | อาจดีกว่าแต่ไม่เสถียร |

script ตั้งเป็น `normal` เท่านั้น — ไม่ปิด (disabled ทำให้แย่ลง)

**Expected: 0-2ms**

---

### [5] Hardware-Accelerated GPU Scheduling (HAGS)
**Registry**: `HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers`  
**Value**: `HwSchMode = 2`

ให้ GPU จัดการ VRAM scheduling ตัวเอง แทนที่ CPU ต้องทำ ลด CPU-GPU handoff overhead และ frame pacing variance

> **ต้อง restart** ถึงจะมีผล  
> ต้องการ GPU driver ที่รองรับ (NVIDIA 451.48+ / AMD 20.5.1+)

**Expected: 1-3ms frame latency + ลด stutters**

---

### [6] Ultimate Performance Power Plan
**Command**: `powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61`

ลบ CPU power states ทั้งหมด — CPU พร้อมทำงาน 100% ตลอด ไม่มี ramp-up delay

พร้อมกัน script ปิด:

| Setting | ผล |
|---------|-----|
| USB Selective Suspend | ป้องกัน USB devices (mouse/headset) หลุด power state |
| PCIe Link State Power Management | ป้องกัน GPU/NIC ลด PCIe speed ชั่วคราว |

**Expected: 1-2ms + ลด micro-stutter**

---

### [7] Game DVR / Xbox Game Bar
**Registry**:
- `HKCU\System\GameConfigStore` → `GameDVR_Enabled = 0`, `GameDVR_FSEBehaviorMode = 2`
- `HKLM\SOFTWARE\Policies\Microsoft\Windows\GameDVR` → `AllowGameDVR = 0`

Xbox Game DVR record gameplay ใน background ใช้ GPU encoder, RAM, และ CPU ที่แย่งกับเกม ปิดแล้วลด background load

**Expected: 0-2ms + ลด CPU spikes**

---

### [8] Valorant Compatibility Flags
**Registry**: `HKCU\Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers`  
**Value**: `~ DISABLEDXMAXIMIZEDWINDOWEDMODE HIGHDPIAWARE`

| Flag | ความหมาย |
|------|----------|
| DISABLEDXMAXIMIZEDWINDOWEDMODE | ปิด fullscreen optimizations — Windows จะไม่ intercept render pipeline |
| HIGHDPIAWARE | Valorant จัดการ DPI เอง ไม่ให้ Windows scale |

**Expected: 1-3ms input lag + ลด Valorant fullscreen stutters**

---

## สรุปผลที่คาดหวัง

| Tweak | คาดว่าลดได้ |
|-------|------------|
| Nagle's Algorithm | 5-20ms |
| Multimedia Profile | 1-3ms |
| TCP Autotuning | 0-2ms |
| HAGS | 1-3ms frame |
| Power Plan | 1-2ms |
| Game DVR | 0-2ms |
| Compat Flags | 1-3ms |
| **รวม realistic** | **~3-8ms** |

ตัวเลขไม่บวกกันตรงๆ เพราะ: tweaks บางตัวแก้ปัญหาเดียวกัน, Windows อาจทำไว้แล้ว, ผลขึ้นกับ hardware + driver + ISP

---

## Physical RTT limit — ทำไมถึงลดได้จำกัด

```
Bangkok → Singapore ≈ 1,400 km
Speed of light in fiber ≈ 200,000 km/s
One-way delay ≈ 7ms
Round-trip ≈ 14ms (minimum theoretical)
Routing overhead + processing ≈ +40-50ms
Total ≈ 54-68ms (จริง)
```

**Windows tweaks ลด client-side processing delay ไม่ใช่ physical RTT**

ถ้าต้องการลด physical latency เพิ่มเติม:
- ใช้ ISP ที่มี direct peering กับ Riot (หา ISP ที่ให้ ping SG ต่ำที่สุด)
- ทดลอง gaming VPN (Exitlag / Mudfish / NoPing) — route อาจดีกว่า ISP default route แต่ผลแตกต่างกันมากตามผู้ใช้

---

## สิ่งที่ script ไม่ทำ (intentional)

- Windows Update service — ไม่ปิด (security risk)
- DNS settings — user จัดการเอง
- TCP extreme tweaks (TcpMaxDataRetransmissions, custom MTU) — risk > reward
- 3rd party gaming boosters — ไม่ติดตั้ง

---

## Files

| File | หน้าที่ |
|------|---------|
| `valorant-tweak.ps1` | Main script (dry-run default, `-Apply` to commit) |
| `valorant-tweak-restore.ps1` | Restore จาก backup บน Desktop |
| `tweak-log.txt` | Log ทุก action (สร้างเมื่อรัน) |
| `%USERPROFILE%\Desktop\valorant-tweak-backup-<timestamp>.reg` | Registry backup (สร้างเมื่อ `-Apply`) |
