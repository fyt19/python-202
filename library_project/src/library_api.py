import json
import os
import httpx
from typing import List, Optional, Dict, Any
from book import Book

class LibraryAPI:
    """API entegrasyonlu kütüphane sınıfı - Open Library API kullanır"""
    
    def __init__(self, filename: str = "library.json"):
        """
        LibraryAPI sınıfının constructor'ı
        
        Args:
            filename (str): Kitapların saklanacağı JSON dosya adı
        """
        self.filename = filename
        self.books: List[Book] = []
        self.api_base_url = "https://openlibrary.org"
        self.load_books()
    
    def add_book_by_isbn(self, isbn: str) -> bool:
        """
        ISBN numarası ile Open Library API'den kitap bilgilerini çeker ve ekler
        
        Args:
            isbn (str): Kitabın ISBN numarası
            
        Returns:
            bool: İşlem başarılı mı?
        """
        # ISBN kontrolü - aynı ISBN varsa ekleme
        if self.find_book(isbn):
            print(f"Bu ISBN ({isbn}) zaten kütüphanede mevcut!")
            return False
        
        try:
            # Open Library API'den kitap bilgilerini çek
            book_data = self._fetch_book_from_api(isbn)
            
            if book_data:
                # Book nesnesi oluştur
                new_book = Book(
                    title=book_data['title'],
                    author=book_data['author'],
                    isbn=isbn
                )
                
                # Kütüphaneye ekle
                self.books.append(new_book)
                self.save_books()
                print(f"✅ Kitap başarıyla eklendi: {new_book}")
                return True
            else:
                print(f"❌ ISBN {isbn} ile kitap bulunamadı.")
                return False
                
        except Exception as e:
            print(f"❌ Kitap eklenirken hata oluştu: {e}")
            return False
    
    def _fetch_book_from_api(self, isbn: str) -> Optional[Dict[str, Any]]:
        """
        Open Library API'den kitap bilgilerini çeker
        
        Args:
            isbn (str): Kitabın ISBN numarası
            
        Returns:
            Optional[Dict[str, Any]]: Kitap bilgileri veya None
        """
        try:
            # API endpoint'i
            url = f"{self.api_base_url}/isbn/{isbn}.json"
            
            # HTTP isteği gönder
            with httpx.Client(timeout=10.0) as client:
                response = client.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Kitap bilgilerini çıkar
                    title = data.get('title', 'Bilinmeyen Başlık')
                    
                    # Yazar bilgisini çıkar
                    authors = data.get('authors', [])
                    if authors:
                        # İlk yazarın adını al
                        author_key = authors[0].get('key')
                        if author_key:
                            author_name = self._fetch_author_name(author_key)
                        else:
                            author_name = 'Bilinmeyen Yazar'
                    else:
                        author_name = 'Bilinmeyen Yazar'
                    
                    return {
                        'title': title,
                        'author': author_name
                    }
                else:
                    print(f"❌ API hatası: {response.status_code}")
                    return None
                    
        except httpx.TimeoutException:
            print("❌ API isteği zaman aşımına uğradı.")
            return None
        except httpx.RequestError as e:
            print(f"❌ API isteği hatası: {e}")
            return None
        except Exception as e:
            print(f"❌ Beklenmeyen hata: {e}")
            return None
    
    def _fetch_author_name(self, author_key: str) -> str:
        """
        Yazar anahtarı ile yazar adını çeker
        
        Args:
            author_key (str): Yazar anahtarı
            
        Returns:
            str: Yazar adı
        """
        try:
            url = f"{self.api_base_url}{author_key}.json"
            
            with httpx.Client(timeout=5.0) as client:
                response = client.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get('name', 'Bilinmeyen Yazar')
                else:
                    return 'Bilinmeyen Yazar'
                    
        except Exception:
            return 'Bilinmeyen Yazar'
    
    def add_book(self, book: Book) -> bool:
        """
        Yeni bir kitabı kütüphaneye ekler (manuel ekleme için)
        
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
        print(f"✅ Kitap başarıyla eklendi: {book}")
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
            print(f"✅ Kitap başarıyla silindi: {book}")
            return True
        else:
            print(f"❌ ISBN {isbn} ile kitap bulunamadı.")
            return False
    
    def list_books(self) -> None:
        """Kütüphanedeki tüm kitapları listeler"""
        if not self.books:
            print("📚 Kütüphanede hiç kitap bulunmuyor.")
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
            print(f"📁 '{self.filename}' dosyası bulunamadı. Yeni kütüphane oluşturuluyor.")
            return
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.books = [Book.from_dict(book_data) for book_data in data]
                print(f"📚 '{self.filename}' dosyasından {len(self.books)} kitap yüklendi.")
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"❌ Dosya okuma hatası: {e}")
            self.books = []
    
    def save_books(self) -> None:
        """Kitap listesini JSON dosyasına kaydeder"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump([book.to_dict() for book in self.books], 
                         file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ Dosya kaydetme hatası: {e}")
    
    def get_stats(self) -> dict:
        """Kütüphane istatistiklerini döndürür"""
        return {
            'total_books': len(self.books),
            'filename': self.filename,
            'file_exists': os.path.exists(self.filename),
            'api_base_url': self.api_base_url
        }
    
    def test_api_connection(self) -> bool:
        """API bağlantısını test eder"""
        try:
            test_isbn = "978-0134685991"  # Python Crash Course ISBN
            url = f"{self.api_base_url}/isbn/{test_isbn}.json"
            
            with httpx.Client(timeout=5.0) as client:
                response = client.get(url)
                return response.status_code == 200
                
        except Exception:
            return False
