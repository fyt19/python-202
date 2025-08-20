#!/usr/bin/env python3
"""
Kütüphane Yönetim Sistemi - Basit Web Arayüzü
Socket.IO olmadan, sadece Flask ile çalışan versiyon
"""

import sys
import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
from datetime import datetime

# src klasörünü Python path'ine ekle
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from library import Library
from book import Book

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kutuphane_yonetim_sistemi_2024'

# Global kütüphane nesnesi
library = Library()

@app.route('/')
def index():
    """Ana sayfa - Login kontrolü"""
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard sayfası"""
    return render_template('index.html')

@app.route('/api/books', methods=['GET'])
def get_books():
    """Tüm kitapları JSON formatında döndürür"""
    books_data = [book.to_dict() for book in library.books]
    return jsonify({
        'success': True,
        'books': books_data,
        'total': len(books_data)
    })

@app.route('/api/books', methods=['POST'])
def add_book():
    """Yeni kitap ekler"""
    try:
        data = request.get_json()
        title = data.get('title', '').strip()
        author = data.get('author', '').strip()
        isbn = data.get('isbn', '').strip()
        
        if not title or not author or not isbn:
            return jsonify({
                'success': False,
                'message': 'Tüm alanlar zorunludur!'
            }), 400
        
        # Kitap nesnesi oluştur
        new_book = Book(title, author, isbn)
        
        # Kütüphaneye ekle
        if library.add_book(new_book):
            return jsonify({
                'success': True,
                'message': 'Kitap başarıyla eklendi!',
                'book': new_book.to_dict()
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Bu ISBN zaten kütüphanede mevcut!'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Hata oluştu: {str(e)}'
        }), 500

@app.route('/api/books/isbn', methods=['POST'])
def add_book_by_isbn():
    """ISBN ile Open Library API'den kitap bilgilerini çeker ve ekler"""
    try:
        data = request.get_json()
        isbn = data.get('isbn', '').strip()
        
        if not isbn:
            return jsonify({
                'success': False,
                'message': 'ISBN alanı zorunludur!'
            }), 400
        
        # ISBN ile kitap ekle
        if library.add_book_by_isbn(isbn):
            return jsonify({
                'success': True,
                'message': 'Kitap başarıyla eklendi!'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Kitap eklenemedi!'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Hata oluştu: {str(e)}'
        }), 500

@app.route('/api/books/<isbn>', methods=['PUT'])
def update_book(isbn):
    """ISBN ile kitap günceller"""
    try:
        data = request.get_json()
        title = data.get('title', '').strip()
        author = data.get('author', '').strip()
        
        if not title or not author:
            return jsonify({
                'success': False,
                'message': 'Başlık ve yazar alanları zorunludur!'
            }), 400
        
        # Kitabı bul ve güncelle
        book = library.find_book(isbn)
        if not book:
            return jsonify({
                'success': False,
                'message': 'Kitap bulunamadı!'
            }), 404
        
        # Kitabı güncelle
        book.title = title
        book.author = author
        
        # Kütüphaneyi kaydet
        library.save_books()
        
        return jsonify({
            'success': True,
            'message': 'Kitap başarıyla güncellendi!',
            'book': book.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Hata oluştu: {str(e)}'
        }), 500

@app.route('/api/books/<isbn>', methods=['DELETE'])
def delete_book(isbn):
    """ISBN ile kitap siler"""
    try:
        if library.remove_book(isbn):
            return jsonify({
                'success': True,
                'message': 'Kitap başarıyla silindi!'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Kitap bulunamadı!'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Hata oluştu: {str(e)}'
        }), 500

@app.route('/api/books/search', methods=['GET'])
def search_books():
    """Kitap arama"""
    keyword = request.args.get('q', '').strip()
    if not keyword:
        return jsonify({
            'success': False,
            'message': 'Arama terimi gerekli!'
        }), 400
    
    found_books = library.search_books(keyword)
    books_data = [book.to_dict() for book in found_books]
    
    return jsonify({
        'success': True,
        'books': books_data,
        'total': len(books_data),
        'keyword': keyword
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Kütüphane istatistiklerini döndürür"""
    stats = library.get_stats()
    return jsonify({
        'success': True,
        'stats': stats
    })

if __name__ == '__main__':
    print("🌐 Web arayüzü başlatılıyor...")
    print("📱 Tarayıcınızda http://127.0.0.1:5000 adresini açın")
    print("⏹️  Durdurmak için Ctrl+C tuşlayın")
    print("-" * 50)
    
    app.run(debug=True, host='127.0.0.1', port=5001)
