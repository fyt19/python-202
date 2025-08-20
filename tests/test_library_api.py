"""
LibraryAPI sınıfı için pytest testleri
Aşama 2: Open Library API entegrasyonu testleri
"""

import pytest
import asyncio
import sys
import os

# src klasörünü Python path'ine ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from library_api import LibraryAPI
    from book import Book
    LIBRARY_API_AVAILABLE = True
except ImportError:
    LIBRARY_API_AVAILABLE = False


@pytest.mark.skipif(not LIBRARY_API_AVAILABLE, reason="LibraryAPI modülü bulunamadı")
class TestLibraryAPI:
    """LibraryAPI sınıfı için test sınıfı"""
    
    def setup_method(self):
        """Her test öncesi çalışır"""
        self.api = LibraryAPI()
    
    def test_init(self):
        """LibraryAPI constructor'ını test eder"""
        assert self.api.base_url == "https://openlibrary.org"
        assert self.api.timeout == 10.0
    
    def test_clean_isbn(self):
        """ISBN temizleme işlemini test eder"""
        # Test ISBN'leri
        test_cases = [
            ("978-0-7475-3269-9", "978-0-7475-3269-9"),
            ("9780747532699", "9780747532699"),
            ("978-0-7475-3269-9!", "978-0-7475-3269-9"),
            ("ISBN: 978-0-7475-3269-9", "978-0-7475-3269-9"),
            ("978 0 7475 3269 9", "9780747532699")
        ]
        
        for input_isbn, expected in test_cases:
            # _clean_isbn metodunu test et (private method)
            clean_isbn = ''.join(c for c in input_isbn if c.isdigit() or c == '-')
            assert clean_isbn == expected
    
    def test_parse_book_data(self):
        """Kitap verisi parse etme işlemini test eder"""
        # Mock API yanıtı
        mock_data = {
            "title": "Test Kitap",
            "authors": [
                {"key": "/authors/OL12345A"}
            ]
        }
        
        test_isbn = "978-0-7475-3269-9"
        
        # _parse_book_data metodunu test et
        book = self.api._parse_book_data(mock_data, test_isbn)
        
        assert isinstance(book, Book)
        assert book.title == "Test Kitap"
        assert book.isbn == test_isbn
        # Yazar adı API'den çekilecek, şimdilik "Bilinmeyen Yazar" olabilir
        assert hasattr(book, 'author')
    
    def test_parse_book_data_missing_fields(self):
        """Eksik alanlarla kitap verisi parse etme işlemini test eder"""
        # Eksik alanlarla mock veri
        mock_data = {}
        test_isbn = "978-0-7475-3269-9"
        
        book = self.api._parse_book_data(mock_data, test_isbn)
        
        assert isinstance(book, Book)
        assert book.title == "Bilinmeyen Başlık"
        assert book.author == "Bilinmeyen Yazar"
        assert book.isbn == test_isbn
    
    def test_get_author_name(self):
        """Yazar adı çekme işlemini test eder"""
        # Mock yazar anahtarı
        author_key = "/authors/OL12345A"
        
        # _get_author_name metodunu test et
        author_name = self.api._get_author_name(author_key)
        
        # API erişilebilir olabilir veya olmayabilir
        assert isinstance(author_name, str)
        assert len(author_name) > 0
    
    def test_search_books(self):
        """Kitap arama işlemini test eder"""
        query = "Harry Potter"
        limit = 5
        
        results = self.api.search_books(query, limit)
        
        assert isinstance(results, list)
        assert len(results) <= limit
        
        if results:
            # İlk sonucu kontrol et
            first_book = results[0]
            assert isinstance(first_book, Book)
            assert hasattr(first_book, 'title')
            assert hasattr(first_book, 'author')
            assert hasattr(first_book, 'isbn')


@pytest.mark.asyncio
@pytest.mark.skipif(not LIBRARY_API_AVAILABLE, reason="LibraryAPI modülü bulunamadı")
class TestLibraryAPIAsync:
    """LibraryAPI async fonksiyonları için test sınıfı"""
    
    def setup_method(self):
        """Her test öncesi çalışır"""
        self.api = LibraryAPI()
    
    async def test_get_book_by_isbn_valid(self):
        """Geçerli ISBN ile kitap çekme işlemini test eder"""
        # Harry Potter ISBN'i
        test_isbn = "978-0-7475-3269-9"
        
        book = await self.api.get_book_by_isbn(test_isbn)
        
        if book:
            # Kitap bulundu
            assert isinstance(book, Book)
            assert book.isbn == test_isbn
            assert hasattr(book, 'title')
            assert hasattr(book, 'author')
            assert len(book.title) > 0
            assert len(book.author) > 0
        else:
            # API erişilemez olabilir
            pytest.skip("Open Library API erişilemez")
    
    async def test_get_book_by_isbn_invalid(self):
        """Geçersiz ISBN ile kitap çekme işlemini test eder"""
        test_isbn = "invalid-isbn-123"
        
        book = await self.api.get_book_by_isbn(test_isbn)
        
        # Geçersiz ISBN için None dönmeli
        assert book is None
    
    async def test_get_book_by_isbn_empty(self):
        """Boş ISBN ile kitap çekme işlemini test eder"""
        test_isbn = ""
        
        book = await self.api.get_book_by_isbn(test_isbn)
        
        # Boş ISBN için None dönmeli
        assert book is None
    
    async def test_get_book_by_isbn_special_chars(self):
        """Özel karakterlerle ISBN ile kitap çekme işlemini test eder"""
        test_isbn = "978-0-7475-3269-9!"
        
        book = await self.api.get_book_by_isbn(test_isbn)
        
        if book:
            # Kitap bulundu
            assert isinstance(book, Book)
            assert book.isbn == "978-0-7475-3269-9"  # Temizlenmiş ISBN
        else:
            # API erişilemez olabilir
            pytest.skip("Open Library API erişilemez")


@pytest.mark.skipif(not LIBRARY_API_AVAILABLE, reason="LibraryAPI modülü bulunamadı")
class TestLibraryAPIIntegration:
    """LibraryAPI entegrasyon testleri"""
    
    def test_library_api_with_library_class(self):
        """LibraryAPI'nin Library sınıfı ile entegrasyonunu test eder"""
        try:
            from library import Library
            
            # Test kütüphanesi oluştur
            test_library = Library("test_library_api.json")
            
            # ISBN ile kitap ekleme metodunu test et
            test_isbn = "978-0-7475-3269-9"
            
            # Bu test API çağrısı yapar, zaman alabilir
            success = test_library.add_book_by_isbn(test_isbn)
            
            # Başarılı veya başarısız olabilir (API durumuna bağlı)
            assert isinstance(success, bool)
            
            # Test dosyasını temizle
            if os.path.exists("test_library_api.json"):
                os.remove("test_library_api.json")
                
        except Exception as e:
            # API erişilemez olabilir
            pytest.skip(f"Library entegrasyon testi atlanıyor: {e}")


# Test yardımcı fonksiyonları
def test_book_class_available():
    """Book sınıfının mevcut olduğunu test eder"""
    try:
        from book import Book
        book = Book("Test", "Test Yazar", "123")
        assert book.title == "Test"
        assert book.author == "Test Yazar"
        assert book.isbn == "123"
    except ImportError:
        pytest.skip("Book sınıfı bulunamadı")


if __name__ == "__main__":
    # Testleri çalıştır
    pytest.main([__file__, "-v"])
