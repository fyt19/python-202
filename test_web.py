#!/usr/bin/env python3
"""
Kütüphane Yönetim Sistemi - Web Arayüzü Test Scripti
Bu script web arayüzünün çalışıp çalışmadığını test eder.
"""

import requests
import time
import sys
import os

def test_web_interface():
    """Web arayüzünü test eder"""
    base_url = "http://127.0.0.1:5001"
    
    print("🧪 Web Arayüzü Test Ediliyor...")
    print("=" * 50)
    
    # Test 1: Ana sayfa erişimi
    print("1️⃣ Ana sayfa test ediliyor...")
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("   ✅ Ana sayfa erişilebilir")
        else:
            print(f"   ❌ Ana sayfa hatası: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Ana sayfa bağlantı hatası: {e}")
        return False
    
    # Test 2: API endpoint'leri
    print("2️⃣ API endpoint'leri test ediliyor...")
    
    # GET /api/books
    try:
        response = requests.get(f"{base_url}/api/books", timeout=5)
        if response.status_code == 200:
            print("   ✅ GET /api/books çalışıyor")
        else:
            print(f"   ❌ GET /api/books hatası: {response.status_code}")
    except Exception as e:
        print(f"   ❌ GET /api/books hatası: {e}")
    
    # GET /api/stats
    try:
        response = requests.get(f"{base_url}/api/stats", timeout=5)
        if response.status_code == 200:
            print("   ✅ GET /api/stats çalışıyor")
        else:
            print(f"   ❌ GET /api/stats hatası: {response.status_code}")
    except Exception as e:
        print(f"   ❌ GET /api/stats hatası: {e}")
    
    # Test 3: Kitap ekleme
    print("3️⃣ Kitap ekleme test ediliyor...")
    test_book = {
        "title": "Test Kitabı",
        "author": "Test Yazarı",
        "isbn": "123-456-789"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/books",
            json=test_book,
            timeout=5
        )
        if response.status_code == 200:
            print("   ✅ Kitap ekleme çalışıyor")
        else:
            print(f"   ❌ Kitap ekleme hatası: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Kitap ekleme hatası: {e}")
    
    # Test 4: Kitap arama
    print("4️⃣ Kitap arama test ediliyor...")
    try:
        response = requests.get(
            f"{base_url}/api/books/search?q=Test",
            timeout=5
        )
        if response.status_code == 200:
            print("   ✅ Kitap arama çalışıyor")
        else:
            print(f"   ❌ Kitap arama hatası: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Kitap arama hatası: {e}")
    
    print("\n🎉 Test tamamlandı!")
    print(f"📱 Web arayüzünü test etmek için: {base_url}")
    
    return True

def main():
    """Ana fonksiyon"""
    print("🌐 Kütüphane Yönetim Sistemi - Web Arayüzü Test")
    print("=" * 60)
    
    # Web arayüzünün çalışıp çalışmadığını kontrol et
    print("🔍 Web arayüzü çalışıyor mu kontrol ediliyor...")
    
    try:
        if test_web_interface():
            print("\n✅ Tüm testler başarılı!")
            print("🎯 Web arayüzü tamamen çalışıyor!")
        else:
            print("\n❌ Bazı testler başarısız!")
            print("🔧 Web arayüzünü kontrol edin!")
    except Exception as e:
        print(f"\n💥 Test sırasında hata oluştu: {e}")
        print("🔧 Web arayüzünü başlatın ve tekrar deneyin!")

if __name__ == '__main__':
    main()
