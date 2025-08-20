"""
Library sınıfı için test dosyası
"""

import pytest
import sys
import os
import tempfile
import json

# src klasörünü Python path'ine ekle
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from library import Library
from book import Book

class TestLibrary:
    """Library sınıfı test sınıfı"""
    
    def setup_method(self):
        """Her test öncesi çalışır"""
        # Geçici dosya oluştur
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_filename = self.temp_file.name
        self.temp_file.close()
        
        # Test kütüphanesi oluştur
        self.library = Library(self.temp_filename)
    
    def teardown_method(self):
        """Her test sonrası çalışır"""
        # Geçici dosyayı sil
        if os.path.exists(self.temp_filename):
            os.unlink(self.temp_filename)
    
    def test_library_initialization(self):
        """Library başlatma testi"""
        assert self.library.books == []
        assert self.library.filename == self.temp_filename
    
    def test_add_book(self):
        """Kitap ekleme testi"""
        book = Book("Test Book", "Test Author", "123-456-789")
        
        result = self.library.add_book(book)
        
        assert result == True
        assert len(self.library.books) == 1
        assert self.library.books[0] == book
    
    def test_add_duplicate_book(self):
        """Aynı ISBN ile kitap ekleme testi"""
        book1 = Book("Test Book 1", "Test Author 1", "123-456-789")
        book2 = Book("Test Book 2", "Test Author 2", "123-456-789")
        
        # İlk kitabı ekle
        self.library.add_book(book1)
        assert len(self.library.books) == 1
        
        # Aynı ISBN ile ikinci kitabı eklemeye çalış
        result = self.library.add_book(book2)
        
        assert result == False
        assert len(self.library.books) == 1  # Hala 1 kitap olmalı
    
    def test_remove_book(self):
        """Kitap silme testi"""
        book = Book("Test Book", "Test Author", "123-456-789")
        self.library.add_book(book)
        
        result = self.library.remove_book("123-456-789")
        
        assert result == True
        assert len(self.library.books) == 0
    
    def test_remove_nonexistent_book(self):
        """Var olmayan kitap silme testi"""
        result = self.library.remove_book("999-999-999")
        
        assert result == False
        assert len(self.library.books) == 0
    
    def test_find_book(self):
        """Kitap bulma testi"""
        book = Book("Test Book", "Test Author", "123-456-789")
        self.library.add_book(book)
        
        found_book = self.library.find_book("123-456-789")
        
        assert found_book == book
    
    def test_find_nonexistent_book(self):
        """Var olmayan kitap bulma testi"""
        found_book = self.library.find_book("999-999-999")
        
        assert found_book is None
    
    def test_search_books_by_keyword(self):
        """Anahtar kelime ile kitap arama testi"""
        book1 = Book("Python Programming", "John Doe", "123-456-789")
        book2 = Book("Java Basics", "Jane Smith", "987-654-321")
        book3 = Book("Python Advanced", "Bob Johnson", "555-555-555")
        
        self.library.add_book(book1)
        self.library.add_book(book2)
        self.library.add_book(book3)
        
        # "Python" kelimesi ile ara
        found_books = self.library.search_books("Python")
        
        assert len(found_books) == 2
        assert book1 in found_books
        assert book3 in found_books
    
    def test_save_and_load_books(self):
        """Kitapları kaydetme ve yükleme testi"""
        book1 = Book("Test Book 1", "Test Author 1", "123-456-789")
        book2 = Book("Test Book 2", "Test Author 2", "987-654-321")
        
        self.library.add_book(book1)
        self.library.add_book(book2)
        
        # Yeni kütüphane oluştur (aynı dosyayı kullanacak)
        new_library = Library(self.temp_filename)
        
        assert len(new_library.books) == 2
        assert new_library.find_book("123-456-789") is not None
        assert new_library.find_book("987-654-321") is not None
    
    def test_library_stats(self):
        """Kütüphane istatistikleri testi"""
        stats = self.library.get_stats()
        
        assert stats['total_books'] == 0
        assert stats['filename'] == self.temp_filename
        assert stats['file_exists'] == True
    
    def test_empty_library_list(self):
        """Boş kütüphane listeleme testi"""
        # Bu test sadece çalışıp çalışmadığını kontrol eder
        # Çıktıyı yakalamak için capture kullanılabilir
        self.library.list_books()
        assert True  # Eğer buraya kadar geldiyse hata yok demektir

if __name__ == "__main__":
    pytest.main([__file__])
