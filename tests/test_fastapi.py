"""
FastAPI endpoint'leri için pytest testleri
Aşama 3: FastAPI testleri
"""

import pytest
import httpx
import asyncio
from fastapi.testclient import TestClient
import sys
import os

# src klasörünü Python path'ine ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from api import app

# Test client oluştur
client = TestClient(app)


class TestFastAPI:
    """FastAPI endpoint'leri için test sınıfı"""
    
    def test_root_endpoint(self):
        """Ana sayfa endpoint'ini test eder"""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
    
    def test_get_books_endpoint(self):
        """GET /books endpoint'ini test eder"""
        response = client.get("/books")
        assert response.status_code == 200
        assert "books" in response.json()
        assert isinstance(response.json()["books"], list)
    
    def test_post_books_endpoint_valid_isbn(self):
        """POST /books endpoint'ini geçerli ISBN ile test eder"""
        # Test ISBN'i (Harry Potter)
        test_data = {"isbn": "978-0-7475-3269-9"}
        
        response = client.post("/books", json=test_data)
        
        # API çağrısı başarılı olmalı
        assert response.status_code in [200, 201]
        response_data = response.json()
        
        # Başarılı ise kitap bilgileri dönmeli
        if response_data.get("success"):
            assert "book" in response_data
            assert response_data["book"]["isbn"] == test_data["isbn"]
        else:
            # Başarısız ise hata mesajı olmalı
            assert "message" in response_data
    
    def test_post_books_endpoint_invalid_isbn(self):
        """POST /books endpoint'ini geçersiz ISBN ile test eder"""
        test_data = {"isbn": "invalid-isbn-123"}
        
        response = client.post("/books", json=test_data)
        
        # Geçersiz ISBN için hata dönmeli
        assert response.status_code in [400, 404, 422]
        response_data = response.json()
        assert "message" in response_data
    
    def test_post_books_endpoint_missing_isbn(self):
        """POST /books endpoint'ini eksik ISBN ile test eder"""
        test_data = {}  # ISBN yok
        
        response = client.post("/books", json=test_data)
        
        # Eksik veri için hata dönmeli
        assert response.status_code == 422  # Validation error
        response_data = response.json()
        assert "detail" in response_data
    
    def test_delete_books_endpoint(self):
        """DELETE /books/{isbn} endpoint'ini test eder"""
        # Önce bir kitap ekle
        test_isbn = "test-delete-123"
        test_book = {
            "title": "Test Kitap",
            "author": "Test Yazar",
            "isbn": test_isbn
        }
        
        # Kitabı ekle
        add_response = client.post("/books", json=test_book)
        if add_response.status_code == 200:
            # Şimdi sil
            delete_response = client.delete(f"/books/{test_isbn}")
            assert delete_response.status_code in [200, 204]
        else:
            # Kitap eklenemezse test atla
            pytest.skip("Kitap eklenemedi, silme testi atlanıyor")
    
    def test_docs_endpoint(self):
        """/docs endpoint'ini test eder"""
        response = client.get("/docs")
        assert response.status_code == 200
        # HTML içeriği olmalı
        assert "text/html" in response.headers.get("content-type", "")
    
    def test_openapi_endpoint(self):
        """/openapi.json endpoint'ini test eder"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        assert "openapi" in response.json()
        assert "paths" in response.json()


class TestFastAPIIntegration:
    """FastAPI ile Library sınıfı entegrasyon testleri"""
    
    def test_library_class_integration(self):
        """Library sınıfının FastAPI ile entegrasyonunu test eder"""
        from library import Library
        
        # Test kütüphanesi oluştur
        test_library = Library("test_library.json")
        
        # Kitap ekle
        from book import Book
        test_book = Book("Test Kitap", "Test Yazar", "test-123")
        success = test_library.add_book(test_book)
        
        assert success == True
        assert len(test_library.books) == 1
        
        # Test dosyasını temizle
        if os.path.exists("test_library.json"):
            os.remove("test_library.json")


# Async test fonksiyonları
@pytest.mark.asyncio
async def test_async_library_api():
    """LibraryAPI sınıfının async fonksiyonlarını test eder"""
    try:
        from library_api import LibraryAPI
        
        api = LibraryAPI()
        
        # Test ISBN ile kitap çekme
        book = await api.get_book_by_isbn("978-0-7475-3269-9")
        
        # Kitap bulunabilir veya bulunamayabilir (API durumuna bağlı)
        if book:
            assert hasattr(book, 'title')
            assert hasattr(book, 'author')
            assert hasattr(book, 'isbn')
        else:
            # API erişilemez olabilir
            pytest.skip("Open Library API erişilemez")
            
    except ImportError:
        pytest.skip("LibraryAPI modülü bulunamadı")


if __name__ == "__main__":
    # Testleri çalıştır
    pytest.main([__file__, "-v"])
