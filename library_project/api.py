#!/usr/bin/env python3
"""
Kütüphane Yönetim Sistemi - Aşama 3
FastAPI ile web servisi
"""

import sys
import os
from typing import List, Optional, Dict, Any

# src klasörünü Python path'ine ekle
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import httpx
from library_api import LibraryAPI
from book import Book

# FastAPI uygulaması oluştur
app = FastAPI(
    title="📚 Kütüphane Yönetim Sistemi API",
    description="Python 202 Bootcamp projesi - FastAPI ile geliştirilmiş kütüphane yönetim sistemi",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Pydantic modelleri
class BookResponse(BaseModel):
    """Kitap yanıt modeli"""
    title: str = Field(..., description="Kitap başlığı")
    author: str = Field(..., description="Yazar adı")
    isbn: str = Field(..., description="ISBN numarası")
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Python Crash Course",
                "author": "Eric Matthes",
                "isbn": "978-1593276034"
            }
        }

class BookCreate(BaseModel):
    """Kitap oluşturma modeli"""
    isbn: str = Field(..., description="Kitap ISBN numarası", min_length=1)
    
    class Config:
        schema_extra = {
            "example": {
                "isbn": "978-1593276034"
            }
        }

class BookList(BaseModel):
    """Kitap listesi modeli"""
    books: List[BookResponse] = Field(..., description="Kitap listesi")
    total: int = Field(..., description="Toplam kitap sayısı")

class MessageResponse(BaseModel):
    """Mesaj yanıt modeli"""
    message: str = Field(..., description="Yanıt mesajı")
    success: bool = Field(..., description="İşlem başarılı mı?")

class StatsResponse(BaseModel):
    """İstatistik yanıt modeli"""
    total_books: int = Field(..., description="Toplam kitap sayısı")
    filename: str = Field(..., description="Veri dosyası adı")
    file_exists: bool = Field(..., description="Dosya mevcut mu?")
    api_base_url: str = Field(..., description="API temel URL'i")

# Global kütüphane nesnesi
library = LibraryAPI()

@app.get("/", response_model=MessageResponse)
async def root():
    """Ana sayfa"""
    return MessageResponse(
        message="📚 Kütüphane Yönetim Sistemi API'ye Hoş Geldiniz!",
        success=True
    )

@app.get("/books", response_model=BookList)
async def get_books():
    """Kütüphanedeki tüm kitapları listeler"""
    books = library.books
    book_responses = [
        BookResponse(
            title=book.title,
            author=book.author,
            isbn=book.isbn
        ) for book in books
    ]
    
    return BookList(
        books=book_responses,
        total=len(books)
    )

@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book_data: BookCreate):
    """ISBN ile yeni kitap ekler (Open Library API'den)"""
    try:
        # ISBN kontrolü
        if library.find_book(book_data.isbn):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Bu ISBN ({book_data.isbn}) zaten kütüphanede mevcut!"
            )
        
        # API'den kitap ekle
        success = library.add_book_by_isbn(book_data.isbn)
        
        if success:
            # Eklenen kitabı bul
            added_book = library.find_book(book_data.isbn)
            if added_book:
                return BookResponse(
                    title=added_book.title,
                    author=added_book.author,
                    isbn=added_book.isbn
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Kitap eklendi ancak bulunamadı"
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ISBN {book_data.isbn} ile kitap bulunamadı"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Kitap eklenirken hata oluştu: {str(e)}"
        )

@app.delete("/books/{isbn}", response_model=MessageResponse)
async def delete_book(isbn: str):
    """ISBN ile kitap siler"""
    try:
        success = library.remove_book(isbn)
        
        if success:
            return MessageResponse(
                message=f"ISBN {isbn} ile kitap başarıyla silindi",
                success=True
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ISBN {isbn} ile kitap bulunamadı"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Kitap silinirken hata oluştu: {str(e)}"
        )

@app.get("/books/{isbn}", response_model=BookResponse)
async def get_book(isbn: str):
    """ISBN ile belirli bir kitabı getirir"""
    book = library.find_book(isbn)
    
    if book:
        return BookResponse(
            title=book.title,
            author=book.author,
            isbn=book.isbn
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ISBN {isbn} ile kitap bulunamadı"
        )

@app.get("/books/search/{keyword}", response_model=BookList)
async def search_books(keyword: str):
    """Anahtar kelime ile kitap arar"""
    found_books = library.search_books(keyword)
    
    book_responses = [
        BookResponse(
            title=book.title,
            author=book.author,
            isbn=book.isbn
        ) for book in found_books
    ]
    
    return BookList(
        books=book_responses,
        total=len(found_books)
    )

@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Kütüphane istatistiklerini döndürür"""
    stats = library.get_stats()
    
    return StatsResponse(
        total_books=stats['total_books'],
        filename=stats['filename'],
        file_exists=stats['file_exists'],
        api_base_url=stats['api_base_url']
    )

@app.get("/health", response_model=MessageResponse)
async def health_check():
    """API sağlık kontrolü"""
    try:
        # Basit sağlık kontrolü
        stats = library.get_stats()
        
        return MessageResponse(
            message="API çalışıyor ve sağlıklı",
            success=True
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"API sağlık kontrolü başarısız: {str(e)}"
        )

@app.get("/api-test", response_model=MessageResponse)
async def test_api_connection():
    """Open Library API bağlantısını test eder"""
    try:
        if library.test_api_connection():
            return MessageResponse(
                message="Open Library API'ye bağlantı başarılı",
                success=True
            )
        else:
            return MessageResponse(
                message="Open Library API'ye bağlantı başarısız",
                success=False
            )
    except Exception as e:
        return MessageResponse(
            message=f"API test hatası: {str(e)}",
            success=False
        )

# Hata yakalayıcılar
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP hata yakalayıcı"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail,
            "success": False,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Genel hata yakalayıcı"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": f"Beklenmeyen hata: {str(exc)}",
            "success": False,
            "status_code": 500
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
