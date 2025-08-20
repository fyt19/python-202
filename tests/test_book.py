"""
Book sınıfı için test dosyası
"""

import pytest
import sys
import os

# src klasörünü Python path'ine ekle
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from book import Book

class TestBook:
    """Book sınıfı test sınıfı"""
    
    def test_book_creation(self):
        """Book nesnesi oluşturma testi"""
        book = Book("Test Book", "Test Author", "123-456-789")
        
        assert book.title == "Test Book"
        assert book.author == "Test Author"
        assert book.isbn == "123-456-789"
    
    def test_book_str_method(self):
        """__str__ metodu testi"""
        book = Book("Ulysses", "James Joyce", "978-0199535675")
        expected = "Ulysses by James Joyce (ISBN: 978-0199535675)"
        
        assert str(book) == expected
    
    def test_book_repr_method(self):
        """__repr__ metodu testi"""
        book = Book("Test Book", "Test Author", "123-456-789")
        expected = "Book(title='Test Book', author='Test Author', isbn='123-456-789')"
        
        assert repr(book) == expected
    
    def test_book_to_dict(self):
        """to_dict metodu testi"""
        book = Book("Test Book", "Test Author", "123-456-789")
        book_dict = book.to_dict()
        
        assert book_dict['title'] == "Test Book"
        assert book_dict['author'] == "Test Author"
        assert book_dict['isbn'] == "123-456-789"
        assert isinstance(book_dict, dict)
    
    def test_book_from_dict(self):
        """from_dict class method testi"""
        book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '123-456-789'
        }
        
        book = Book.from_dict(book_data)
        
        assert book.title == "Test Book"
        assert book.author == "Test Author"
        assert book.isbn == "123-456-789"
        assert isinstance(book, Book)
    
    def test_empty_strings(self):
        """Boş string'ler ile Book oluşturma testi"""
        book = Book("", "", "")
        
        assert book.title == ""
        assert book.author == ""
        assert book.isbn == ""

if __name__ == "__main__":
    pytest.main([__file__])
