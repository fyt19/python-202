#!/usr/bin/env python3
"""
Kütüphane Yönetim Sistemi - Web Arayüzü
Modern ve kullanıcı dostu web arayüzü
"""

import sys
import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_socketio import SocketIO
import json
from datetime import datetime

# src klasörünü Python path'ine ekle
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from library import Library
from book import Book

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kutuphane_yonetim_sistemi_2024'
socketio = SocketIO(app, async_mode='threading')

# Global kütüphane nesnesi
library = Library()

@app.route('/')
def index():
    """Ana sayfa"""
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
            socketio.emit('book_added', new_book.to_dict())
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

@app.route('/api/books/<isbn>', methods=['DELETE'])
def delete_book(isbn):
    """ISBN ile kitap siler"""
    try:
        if library.remove_book(isbn):
            socketio.emit('book_deleted', {'isbn': isbn})
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
    print("📱 Tarayıcınızda http://localhost:5000 adresini açın")
    socketio.run(app, debug=True, host='127.0.0.1', port=5000)

