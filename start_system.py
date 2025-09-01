#!/usr/bin/env python3
"""
HealTrack Sistem Başlatıcısı
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def check_python_version():
    """Python versiyonu kontrolü"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 veya üzeri gerekli")
        return False
    print(f"✅ Python {sys.version}")
    return True

def install_requirements():
    """Gereksinimleri yükle"""
    print("📦 Gerekli paketler yükleniyor...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Paketler başarıyla yüklendi")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Paket yükleme hatası: {e}")
        return False

def test_model():
    """Model testı"""
    print("🧠 AI model test ediliyor...")
    try:
        from wound_analysis_model import WoundAnalysisModel
        model = WoundAnalysisModel()
        print("✅ AI model başarıyla yüklendi")
        return True
    except Exception as e:
        print(f"❌ Model yükleme hatası: {e}")
        return False

def start_api_server():
    """API sunucusunu başlat"""
    print("🚀 API sunucusu başlatılıyor...")
    print("📋 Swagger UI: http://localhost:8000/docs")
    print("🌐 Frontend: x.html dosyasını tarayıcıda açın")
    print("⏹️  Durdurmak için Ctrl+C")
    
    try:
        subprocess.run([
            sys.executable, "api_server.py"
        ])
    except KeyboardInterrupt:
        print("\n👋 Sunucu durduruldu")

def main():
    print("🏥 HealTrack - Ameliyat Sonrası İyileşme Takibi")
    print("=" * 50)
    
    # Klasör kontrolü
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt bulunamadı")
        return
    
    if not Path("wound_analysis_model.py").exists():
        print("❌ wound_analysis_model.py bulunamadı")
        return
    
    if not Path("api_server.py").exists():
        print("❌ api_server.py bulunamadı")
        return
    
    # Sistem kontrolü
    if not check_python_version():
        return
    
    # Paket yükleme
    if not install_requirements():
        print("💡 Manuel yükleme: pip install -r requirements.txt")
        return
    
    # Model testi
    if not test_model():
        print("💡 Model dosyalarını kontrol edin")
        return
    
    print("🎉 Sistem hazır!")
    time.sleep(1)
    
    # Sunucu başlat
    start_api_server()

if __name__ == "__main__":
    main()
