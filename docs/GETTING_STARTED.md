# Getting Started — LTD-OS

คู่มือ setup ครั้งแรก สำหรับคนที่เขียนโค้ดไม่เป็น

---

## Step 1: ติดตั้ง WSL2 + Ubuntu (Windows)

เปิด **PowerShell as Administrator** แล้วรัน:

```powershell
wsl --install -d Ubuntu
```

รอ download เสร็จ → restart Windows → Ubuntu จะเปิดมาขอตั้ง username/password

> **คำเตือน**: password ที่ตั้งใน Ubuntu คนละตัวกับ Windows password จำให้แม่น

หลังเข้า Ubuntu สำเร็จ ให้รัน:
```bash
sudo apt update && sudo apt upgrade -y
```

---

## Step 2: ย้ายโฟลเดอร์ ltd-os เข้า WSL2

ใน Ubuntu terminal:

```bash
mkdir -p ~/projects
cd ~/projects
# วางโฟลเดอร์ ltd-os ที่นี่ (จะเอามาจากไหนก็ได้ — copy จาก Windows ผ่าน /mnt/c/ ก็ได้)
```

ถ้าโฟลเดอร์อยู่บน Windows ที่ `C:\Users\<you>\Downloads\ltd-os`:
```bash
cp -r /mnt/c/Users/$(whoami)/Downloads/ltd-os ~/projects/
cd ~/projects/ltd-os
```

---

## Step 3: รัน bootstrap

```bash
cd ~/projects/ltd-os
bash scripts/bootstrap.sh
```

สคริปต์จะ:
- ติดตั้ง git, python, node, ripgrep, direnv
- ติดตั้ง Claude Code
- ตั้งค่า git (จะถามชื่อ + email)
- init git repo + commit แรก
- ตั้ง direnv hook

ใช้เวลา 5-10 นาที

---

## Step 4: เปิด terminal ใหม่ + allow direnv

```bash
exec bash   # หรือปิด/เปิด terminal ใหม่
cd ~/projects/ltd-os
direnv allow
```

---

## Step 5: Login Claude Code

```bash
claude
```

จะมี link ขึ้นมา — copy ไปเปิดใน browser → login ด้วย Anthropic account → กลับมา terminal

---

## Step 6: ใส่ secrets

```bash
cp .secrets/.env.example .secrets/.env
nano .secrets/.env   # หรือใช้ editor อื่น
```

ใส่ API keys ที่ใช้ (ANTHROPIC_API_KEY etc.) แล้วบันทึก

ตรวจว่าโหลด:
```bash
direnv reload
echo $ANTHROPIC_API_KEY   # ควรเห็นค่า (อย่า copy ไปแชร์ที่ไหน)
```

---

## Step 7: เปิด Obsidian (Windows side)

1. Download Obsidian จาก obsidian.md
2. เปิด → "Open folder as vault"
3. ใน address bar พิมพ์: `\\wsl$\Ubuntu\home\<your-ubuntu-username>\projects\ltd-os\vault`
4. กด Enter → Open

แนะนำติดตั้ง plugins: **Dataview**, **Templater**, **Git**

---

## Step 8: ลองใช้ครั้งแรก

ใน Ubuntu terminal:

```bash
cd ~/projects/ltd-os
claude
```

**สิ่งแรกที่ควรทำ — /onboard:**

```
/onboard
```

Claude จะสัมภาษณ์คุณ 5 กลุ่ม (~15-30 นาที) เพื่อเติม `vault/_memory/PREFERENCES.md`:
1. Background + communication style
2. Depth + tone signals
3. Voice (ถ้าจะทำ content)
4. Investment style (ถ้าลงทุน)
5. Conventions + hard no's

**ทำครั้งเดียวตอนเริ่มใช้** — หลังจากนี้ Claude จะอ่าน PREFERENCES ทุก session

---

ถ้าอยากข้าม `/onboard` ก่อน ลองอย่างอื่น:

```
ใช้ planner agent วางแผนการทำสรุปบทความ "Attention is All You Need"
```

Claude จะ:
1. invoke `planner` → ถามคำถาม + เขียน plan.md
2. invoke `executor` → ทำตาม plan
3. invoke `reviewer` → ตรวจก่อน commit
4. ถ้าผ่าน → บอกให้รัน `bash scripts/safe-commit.sh "feat: add attention paper summary"`

---

## Step 9: สร้างโปรเจกต์ใหม่

Python:
```bash
bash scripts/new-project.sh python my-first-bot
```

Web:
```bash
bash scripts/new-project.sh web my-landing-page
```

---

## Weekly routine

ทุกวันอาทิตย์:
```bash
bash scripts/weekly-review.sh
```

จะสร้าง log + แสดงสถานะ inbox / activity / commits

---

## Troubleshooting

**`direnv: error .envrc is blocked`** → รัน `direnv allow`

**`claude: command not found`** → `source ~/.bashrc` หรือเปิด terminal ใหม่

**Obsidian หา vault ไม่เจอ** → ใน Windows Explorer พิมพ์ `\\wsl$` ก่อนเพื่อเปิด WSL filesystem

**Git ขอ password ทุกครั้ง** → setup SSH key หรือใช้ GitHub CLI: `gh auth login`

---

## เมื่อพร้อม "อัพเกรด" ระบบ

อย่ารีบเพิ่ม agent ใหม่ — รอจนเจอ pain จริงๆ:

| Pain ที่เจอ | เพิ่มอะไร |
|---|---|
| Token bill สูง ไม่รู้ใช้กับอะไร | analyst agent + cost log |
| หาไฟล์ไม่เจอบ่อย | librarian agent + tagging script |
| Vault ใหญ่ขึ้นจน context ไม่พอ | memory condensation script |
| อยากให้คนอื่นใช้ด้วย | sync ผ่าน private git remote |
| งาน research ใช้ source สำคัญซ้ำๆ | embeddings + semantic search |

อย่าแก้ปัญหาที่ยังไม่มี
