import json
import os
from typing import List, Optional
from book import Book

class Library:
    """Kütüphane sınıfı - tüm kütüphane operasyonlarını yönetir"""
    
    def __init__(self, filename: str = "library.json"):
        """
        Library sınıfının constructor'ı
        
        Args:
            filename (str): Kitapların saklanacağı JSON dosya adı
        """
        self.filename = filename
        self.books: List[Book] = []
        self.load_books()
    
    def add_book(self, book: Book) -> bool:
        """
        Yeni bir kitabı kütüphaneye ekler
        
        Args:
            book (Book): Eklenecek kitap nesnesi
            
        Returns:
            bool: İşlem başarılı mı?
        """
        # ISBN kontrolü - aynı ISBN varsa ekleme
        if self.find_book(book.isbn):
            print(f"Bu ISBN ({book.isbn}) zaten kütüphanede mevcut!")
            return False
        
        self.books.append(book)
        self.save_books()
        print(f"Kitap başarıyla eklendi: {book}")
        return True
    
    def remove_book(self, isbn: str) -> bool:
        """
        ISBN numarasına göre kitabı kütüphaneden siler
        
        Args:
            isbn (str): Silinecek kitabın ISBN'i
            
        Returns:
            bool: İşlem başarılı mı?
        """
        book = self.find_book(isbn)
        if book:
            self.books.remove(book)
            self.save_books()
            print(f"Kitap başarıyla silindi: {book}")
            return True
        else:
            print(f"ISBN {isbn} ile kitap bulunamadı.")
            return False
    
    def list_books(self) -> None:
        """Kütüphanedeki tüm kitapları listeler"""
        if not self.books:
            print("Kütüphanede hiç kitap bulunmuyor.")
            return
        
        print(f"\n📚 Kütüphanede {len(self.books)} kitap bulunuyor:")
        print("-" * 60)
        for i, book in enumerate(self.books, 1):
            print(f"{i}. {book}")
        print("-" * 60)
    
    def find_book(self, isbn: str) -> Optional[Book]:
        """
        ISBN ile belirli bir kitabı bulur
        
        Args:
            isbn (str): Aranacak kitabın ISBN'i
            
        Returns:
            Optional[Book]: Bulunan kitap veya None
        """
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None
    
    def search_books(self, keyword: str) -> List[Book]:
        """
        Başlık veya yazar adında anahtar kelime arar
        
        Args:
            keyword (str): Aranacak anahtar kelime
            
        Returns:
            List[Book]: Bulunan kitaplar listesi
        """
        keyword = keyword.lower()
        found_books = []
        
        for book in self.books:
            if (keyword in book.title.lower() or 
                keyword in book.author.lower() or
                keyword in book.isbn):
                found_books.append(book)
        
        return found_books
    
    def load_books(self) -> None:
        """JSON dosyasından kitapları yükler"""
        if not os.path.exists(self.filename):
            print(f"'{self.filename}' dosyası bulunamadı. Yeni kütüphane oluşturuluyor.")
            return
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.books = [Book.from_dict(book_data) for book_data in data]
                print(f"'{self.filename}' dosyasından {len(self.books)} kitap yüklendi.")
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Dosya okuma hatası: {e}")
            self.books = []
    
    def save_books(self) -> None:
        """Kitap listesini JSON dosyasına kaydeder"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump([book.to_dict() for book in self.books], 
                         file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Dosya kaydetme hatası: {e}")
    
    def get_stats(self) -> dict:
        """Kütüphane istatistiklerini döndürür"""
        return {
            'total_books': len(self.books),
            'filename': self.filename,
            'file_exists': os.path.exists(self.filename)
        }
