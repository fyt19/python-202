#!/usr/bin/env python3
"""
Kütüphane Yönetim Sistemi - Web Arayüzü Başlatıcı
Bu script web arayüzünü başlatır ve gerekli kontrolleri yapar.
"""

import sys
import os
import subprocess
import webbrowser
import time

def check_dependencies():
    """Gerekli paketlerin yüklü olup olmadığını kontrol eder"""
    required_packages = ['flask', 'flask_socketio']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Eksik paketler tespit edildi:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Paketleri yüklemek için şu komutu çalıştırın:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def check_files():
    """Gerekli dosyaların var olup olmadığını kontrol eder"""
    required_files = [
        'web_interface.py',
        'templates/index.html',
        'static/css/style.css',
        'static/js/app.js',
        'src/book.py',
        'src/library.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Eksik dosyalar tespit edildi:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    return True

def main():
    """Ana fonksiyon"""
    print("🌐 Kütüphane Yönetim Sistemi - Web Arayüzü")
    print("=" * 50)
    
    # Bağımlılık kontrolü
    print("🔍 Bağımlılıklar kontrol ediliyor...")
    if not check_dependencies():
        return
    
    # Dosya kontrolü
    print("📁 Dosyalar kontrol ediliyor...")
    if not check_files():
        return
    
    print("✅ Tüm kontroller başarılı!")
    print("\n🚀 Web arayüzü başlatılıyor...")
    print("📱 Tarayıcınızda http://localhost:5000 adresini açın")
    print("⏹️  Durdurmak için Ctrl+C tuşlayın")
    print("-" * 50)
    
    # 3 saniye bekle ve tarayıcıyı aç
    time.sleep(3)
    try:
        webbrowser.open('http://localhost:5000')
    except:
        print("⚠️  Tarayıcı otomatik açılamadı. Manuel olarak http://localhost:5000 adresini açın.")
    
    # Web arayüzünü başlat
    try:
        subprocess.run([sys.executable, 'web_interface.py'])
    except KeyboardInterrupt:
        print("\n\n👋 Web arayüzü kapatıldı.")
    except Exception as e:
        print(f"\n❌ Hata oluştu: {e}")

if __name__ == '__main__':
    main()

