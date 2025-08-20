"""
Open Library API entegrasyonu için LibraryAPI sınıfı
Aşama 2: Harici API entegrasyonu
"""

import httpx
import json
from typing import Optional, Dict, Any
from book import Book


class LibraryAPI:
    """Open Library Books API ile entegrasyon"""
    
    def __init__(self):
        self.base_url = "https://openlibrary.org"
        self.timeout = 10.0  # 10 saniye timeout
    
    async def get_book_by_isbn(self, isbn: str) -> Optional[Book]:
        """
        ISBN ile Open Library API'den kitap bilgilerini çeker
        
        Args:
            isbn (str): Kitap ISBN numarası
            
        Returns:
            Optional[Book]: Kitap nesnesi veya None
        """
        try:
            # ISBN formatını temizle (sadece rakam ve tire)
            clean_isbn = ''.join(c for c in isbn if c.isdigit() or c == '-')
            
            # API endpoint
            url = f"{self.base_url}/isbn/{clean_isbn}.json"
            
            # HTTP isteği gönder
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
                
                if response.status_code == 200:
                    # JSON yanıtını parse et
                    book_data = response.json()
                    return self._parse_book_data(book_data, clean_isbn)
                elif response.status_code == 404:
                    print(f"❌ ISBN {isbn} ile kitap bulunamadı!")
                    return None
                else:
                    print(f"❌ API hatası: {response.status_code}")
                    return None
                    
        except httpx.TimeoutException:
            print("❌ API isteği zaman aşımına uğradı!")
            return None
        except httpx.RequestError as e:
            print(f"❌ Ağ hatası: {e}")
            return None
        except Exception as e:
            print(f"❌ Beklenmeyen hata: {e}")
            return None
    
    def _parse_book_data(self, data: Dict[str, Any], isbn: str) -> Book:
        """
        API yanıtından Book nesnesi oluşturur
        
        Args:
            data (Dict): API yanıt verisi
            isbn (str): Kitap ISBN'i
            
        Returns:
            Book: Oluşturulan kitap nesnesi
        """
        # Kitap başlığı
        title = data.get('title', 'Bilinmeyen Başlık')
        
        # Yazar bilgisi
        authors = data.get('authors', [])
        if authors and len(authors) > 0:
            # İlk yazarın adını al
            author_key = authors[0].get('key', '')
            if author_key:
                # Yazar detaylarını çek
                author_name = self._get_author_name(author_key)
            else:
                author_name = 'Bilinmeyen Yazar'
        else:
            author_name = 'Bilinmeyen Yazar'
        
        # Yeni Book nesnesi oluştur
        book = Book(title=title, author=author_name, isbn=isbn)
        
        print(f"✅ Kitap bulundu: {title} by {author_name}")
        return book
    
    def _get_author_name(self, author_key: str) -> str:
        """
        Yazar anahtarından yazar adını çeker
        
        Args:
            author_key (str): Yazar anahtarı
            
        Returns:
            str: Yazar adı
        """
        try:
            # Senkron HTTP isteği (basitlik için)
            url = f"{self.base_url}{author_key}.json"
            
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(url)
                if response.status_code == 200:
                    author_data = response.json()
                    return author_data.get('name', 'Bilinmeyen Yazar')
                else:
                    return 'Bilinmeyen Yazar'
                    
        except Exception:
            return 'Bilinmeyen Yazar'
    
    def search_books(self, query: str, limit: int = 10) -> list:
        """
        Kitap arama (basit implementasyon)
        
        Args:
            query (str): Arama terimi
            limit (int): Maksimum sonuç sayısı
            
        Returns:
            list: Kitap listesi
        """
        try:
            url = f"{self.base_url}/search.json"
            params = {
                'q': query,
                'limit': limit
            }
            
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(url, params=params)
                
                if response.status_code == 200:
                    search_data = response.json()
                    books = []
                    
                    for doc in search_data.get('docs', [])[:limit]:
                        title = doc.get('title', 'Bilinmeyen Başlık')
                        author = doc.get('author_name', ['Bilinmeyen Yazar'])[0] if doc.get('author_name') else 'Bilinmeyen Yazar'
                        isbn = doc.get('isbn', [''])[0] if doc.get('isbn') else f"search-{len(books)}"
                        
                        book = Book(title=title, author=author, isbn=isbn)
                        books.append(book)
                    
                    return books
                else:
                    return []
                    
        except Exception as e:
            print(f"❌ Arama hatası: {e}")
            return []


# Test fonksiyonu
def test_library_api():
    """LibraryAPI sınıfını test eder"""
    import asyncio
    
    async def test():
        api = LibraryAPI()
        
        # Test ISBN'ler
        test_isbns = [
            "978-0-7475-3269-9",  # Harry Potter
            "978-0-14-143951-8",  # Pride and Prejudice
            "invalid-isbn"        # Geçersiz ISBN
        ]
        
        for isbn in test_isbns:
            print(f"\n🔍 ISBN {isbn} test ediliyor...")
            book = await api.get_book_by_isbn(isbn)
            if book:
                print(f"✅ Bulunan kitap: {book}")
            else:
                print(f"❌ Kitap bulunamadı")
    
    # Async test çalıştır
    asyncio.run(test())


if __name__ == "__main__":
    test_library_api()
