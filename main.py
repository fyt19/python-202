#!/usr/bin/env python3
"""
Kütüphane Yönetim Sistemi - Aşama 1
OOP prensipleri kullanılarak geliştirilmiş terminal uygulaması
"""

import sys
import os

# src klasörünü Python path'ine ekle
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from library import Library
from book import Book

def clear_screen():
    """Ekranı temizler"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Uygulama başlığını yazdırır"""
    print("=" * 60)
    print("📚 KÜTÜPHANE YÖNETİM SİSTEMİ 📚")
    print("=" * 60)

def print_menu():
    """Ana menüyü yazdırır"""
    print("\n🔍 MENÜ:")
    print("1. 📖 Kitap Ekle")
    print("2. 🗑️  Kitap Sil")
    print("3. 📋 Kitapları Listele")
    print("4. 🔍 Kitap Ara (ISBN)")
    print("5. 🔎 Kitap Ara (Anahtar Kelime)")
    print("6. 📊 Kütüphane İstatistikleri")
    print("7. 🚪 Çıkış")
    print("-" * 40)

def add_book_manually(library: Library):
    """Manuel olarak kitap ekler"""
    print("\n📖 YENİ KİTAP EKLEME")
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

def remove_book_by_isbn(library: Library):
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

def search_book_by_isbn(library: Library):
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

def search_books_by_keyword(library: Library):
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

def show_library_stats(library: Library):
    """Kütüphane istatistiklerini gösterir"""
    print("\n📊 KÜTÜPHANE İSTATİSTİKLERİ")
    print("-" * 30)
    
    stats = library.get_stats()
    print(f"📚 Toplam kitap sayısı: {stats['total_books']}")
    print(f"📁 Veri dosyası: {stats['filename']}")
    print(f"💾 Dosya mevcut: {'✅ Evet' if stats['file_exists'] else '❌ Hayır'}")

def main():
    """Ana uygulama fonksiyonu"""
    clear_screen()
    print_header()
    
    # Kütüphane nesnesini oluştur
    library = Library()
    
    print(f"✅ Kütüphane başlatıldı. Veri dosyası: {library.filename}")
    
    while True:
        try:
            print_menu()
            choice = input("Seçiminizi yapın (1-7): ").strip()
            
            if choice == '1':
                add_book_manually(library)
            elif choice == '2':
                remove_book_by_isbn(library)
            elif choice == '3':
                library.list_books()
            elif choice == '4':
                search_book_by_isbn(library)
            elif choice == '5':
                search_books_by_keyword(library)
            elif choice == '6':
                show_library_stats(library)
            elif choice == '7':
                print("\n👋 Kütüphane yönetim sisteminden çıkılıyor...")
                print("💾 Veriler kaydedildi.")
                break
            else:
                print("❌ Geçersiz seçim! Lütfen 1-7 arasında bir sayı girin.")
            
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
