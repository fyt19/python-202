#!/usr/bin/env python3
"""
Kütüphane Yönetim Sistemi - Aşama 2
API entegrasyonu ile geliştirilmiş terminal uygulaması
"""

import sys
import os

# src klasörünü Python path'ine ekle
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from library_api import LibraryAPI
from book import Book

def clear_screen():
    """Ekranı temizler"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Uygulama başlığını yazdırır"""
    print("=" * 70)
    print("📚 KÜTÜPHANE YÖNETİM SİSTEMİ - API ENTEGRASYONU 📚")
    print("=" * 70)

def print_menu():
    """Ana menüyü yazdırır"""
    print("\n🔍 MENÜ:")
    print("1. 📖 Kitap Ekle (ISBN ile API'den)")
    print("2. 📝 Kitap Ekle (Manuel)")
    print("3. 🗑️  Kitap Sil")
    print("4. 📋 Kitapları Listele")
    print("5. 🔍 Kitap Ara (ISBN)")
    print("6. 🔎 Kitap Ara (Anahtar Kelime)")
    print("7. 📊 Kütüphane İstatistikleri")
    print("8. 🌐 API Bağlantı Testi")
    print("9. 🚪 Çıkış")
    print("-" * 50)

def add_book_by_isbn(library: LibraryAPI):
    """ISBN ile API'den kitap ekler"""
    print("\n📖 ISBN İLE KİTAP EKLEME (API)")
    print("-" * 40)
    
    try:
        isbn = input("Kitap ISBN numarası: ").strip()
        if not isbn:
            print("❌ ISBN numarası boş olamaz!")
            return
        
        print(f"🔍 ISBN {isbn} için kitap aranıyor...")
        print("⏳ Open Library API'den bilgiler çekiliyor...")
        
        # API'den kitap ekle
        success = library.add_book_by_isbn(isbn)
        
        if success:
            print("✅ Kitap başarıyla API'den çekildi ve eklendi!")
        else:
            print("❌ Kitap eklenemedi. Lütfen ISBN'i kontrol edin.")
        
    except KeyboardInterrupt:
        print("\n\n❌ İşlem iptal edildi.")
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")

def add_book_manually(library: LibraryAPI):
    """Manuel olarak kitap ekler"""
    print("\n📝 MANUEL KİTAP EKLEME")
    print("-" * 30)
    
    try:
        title = input("Kitap başlığı: ").strip()
        if not title:
            print("❌ Kitap başlığı boş olamaz!")
            return
        
        author = input("Yazar adı: ").strip()
        if not author:
            print("❌ Yazar adı boş olamaz!")
            return
        
        isbn = input("ISBN numarası: ").strip()
        if not isbn:
            print("❌ ISBN numarası boş olamaz!")
            return
        
        # Kitap nesnesi oluştur
        new_book = Book(title, author, isbn)
        
        # Kütüphaneye ekle
        library.add_book(new_book)
        
    except KeyboardInterrupt:
        print("\n\n❌ İşlem iptal edildi.")
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")

def remove_book_by_isbn(library: LibraryAPI):
    """ISBN ile kitap siler"""
    print("\n🗑️  KİTAP SİLME")
    print("-" * 20)
    
    try:
        isbn = input("Silinecek kitabın ISBN'i: ").strip()
        if not isbn:
            print("❌ ISBN numarası boş olamaz!")
            return
        
        library.remove_book(isbn)
        
    except KeyboardInterrupt:
        print("\n\n❌ İşlem iptal edildi.")
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")

def search_book_by_isbn(library: LibraryAPI):
    """ISBN ile kitap arar"""
    print("\n🔍 ISBN İLE KİTAP ARAMA")
    print("-" * 30)
    
    try:
        isbn = input("Aranacak kitabın ISBN'i: ").strip()
        if not isbn:
            print("❌ ISBN numarası boş olamaz!")
            return
        
        book = library.find_book(isbn)
        if book:
            print(f"\n✅ Kitap bulundu:")
            print(f"   📖 {book}")
        else:
            print(f"\n❌ ISBN {isbn} ile kitap bulunamadı.")
        
    except KeyboardInterrupt:
        print("\n\n❌ İşlem iptal edildi.")
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")

def search_books_by_keyword(library: LibraryAPI):
    """Anahtar kelime ile kitap arar"""
    print("\n🔎 ANAHTAR KELİME İLE KİTAP ARAMA")
    print("-" * 40)
    
    try:
        keyword = input("Aranacak anahtar kelime: ").strip()
        if not keyword:
            print("❌ Anahtar kelime boş olamaz!")
            return
        
        found_books = library.search_books(keyword)
        
        if found_books:
            print(f"\n✅ '{keyword}' ile {len(found_books)} kitap bulundu:")
            print("-" * 50)
            for i, book in enumerate(found_books, 1):
                print(f"{i}. {book}")
            print("-" * 50)
        else:
            print(f"\n❌ '{keyword}' ile kitap bulunamadı.")
        
    except KeyboardInterrupt:
        print("\n\n❌ İşlem iptal edildi.")
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")

def show_library_stats(library: LibraryAPI):
    """Kütüphane istatistiklerini gösterir"""
    print("\n📊 KÜTÜPHANE İSTATİSTİKLERİ")
    print("-" * 30)
    
    stats = library.get_stats()
    print(f"📚 Toplam kitap sayısı: {stats['total_books']}")
    print(f"📁 Veri dosyası: {stats['filename']}")
    print(f"💾 Dosya mevcut: {'✅ Evet' if stats['file_exists'] else '❌ Hayır'}")
    print(f"🌐 API URL: {stats['api_base_url']}")

def test_api_connection(library: LibraryAPI):
    """API bağlantısını test eder"""
    print("\n🌐 API BAĞLANTI TESTİ")
    print("-" * 25)
    
    print("🔍 Open Library API'ye bağlantı test ediliyor...")
    
    if library.test_api_connection():
        print("✅ API bağlantısı başarılı!")
        print("🌐 Open Library API'ye erişim mevcut.")
    else:
        print("❌ API bağlantısı başarısız!")
        print("🌐 Open Library API'ye erişim yok.")
        print("💡 İnternet bağlantınızı kontrol edin.")

def main():
    """Ana uygulama fonksiyonu"""
    clear_screen()
    print_header()
    
    # Kütüphane nesnesini oluştur
    library = LibraryAPI()
    
    print(f"✅ Kütüphane başlatıldı. Veri dosyası: {library.filename}")
    print(f"🌐 API entegrasyonu aktif: {library.api_base_url}")
    
    while True:
        try:
            print_menu()
            choice = input("Seçiminizi yapın (1-9): ").strip()
            
            if choice == '1':
                add_book_by_isbn(library)
            elif choice == '2':
                add_book_manually(library)
            elif choice == '3':
                remove_book_by_isbn(library)
            elif choice == '4':
                library.list_books()
            elif choice == '5':
                search_book_by_isbn(library)
            elif choice == '6':
                search_books_by_keyword(library)
            elif choice == '7':
                show_library_stats(library)
            elif choice == '8':
                test_api_connection(library)
            elif choice == '9':
                print("\n👋 Kütüphane yönetim sisteminden çıkılıyor...")
                print("💾 Veriler kaydedildi.")
                break
            else:
                print("❌ Geçersiz seçim! Lütfen 1-9 arasında bir sayı girin.")
            
            input("\n⏎ Devam etmek için Enter'a basın...")
            clear_screen()
            print_header()
            
        except KeyboardInterrupt:
            print("\n\n👋 Program sonlandırılıyor...")
            break
        except Exception as e:
            print(f"\n❌ Beklenmeyen hata: {e}")
            input("Devam etmek için Enter'a basın...")

if __name__ == "__main__":
    main()
