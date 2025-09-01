@echo off
echo 🏥 HealTrack - Sistem Başlatılıyor...
echo.

REM Python kontrolü
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python bulunamadı! Python 3.8+ yükleyin.
    pause
    exit /b 1
)

REM Sanal ortam oluştur (opsiyonel)
if not exist "venv" (
    echo 📦 Sanal ortam oluşturuluyor...
    python -m venv venv
)

REM Sanal ortamı aktifleştir
if exist "venv\Scripts\activate.bat" (
    echo 🔧 Sanal ortam aktifleştiriliyor...
    call venv\Scripts\activate.bat
)

REM Sistem başlat
echo 🚀 HealTrack başlatılıyor...
python start_system.py

echo.
echo 👋 Sistem durduruldu.
pause
