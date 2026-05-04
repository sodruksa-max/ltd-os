@echo off
cd /d C:\Users\sodru\ltd-os

echo [%date% %time%] Running monthly S^&P 500 universe update...

code\python\.venv\Scripts\python scripts\update-universe.py
if errorlevel 1 (
    echo [ERROR] update-universe.py failed
    exit /b 1
)

code\python\.venv\Scripts\python scripts\update-sectors.py
if errorlevel 1 (
    echo [ERROR] update-sectors.py failed
    exit /b 1
)

git add config\universe-sp500.txt config\sector-map.json
git diff --cached --quiet || git commit -m "chore: monthly S&P 500 universe + sector map update"

echo [%date% %time%] Done.
