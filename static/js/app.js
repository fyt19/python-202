// Library Management System - Frontend JavaScript

// Global variables
let socket;
let currentBooks = [];
let isSearchMode = false;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeSocket();
    initializeEventListeners();
    loadBooks();
    loadStats();
    updateCurrentTime();
    setInterval(updateCurrentTime, 1000);
});

// Socket.IO initialization (disabled for simple version)
function initializeSocket() {
    console.log('Socket.IO disabled - using simple HTTP requests');
    // Socket.IO özellikleri devre dışı
}

// Initialize event listeners
function initializeEventListeners() {
    // Add book form
    const addBookForm = document.getElementById('addBookForm');
    addBookForm.addEventListener('submit', handleAddBook);
    
    // Search form
    const searchForm = document.getElementById('searchForm');
    searchForm.addEventListener('input', handleSearchInput);
    searchForm.addEventListener('submit', handleSearch);
    
    // Delete confirmation
    const confirmDeleteBtn = document.getElementById('confirmDelete');
    confirmDeleteBtn.addEventListener('click', handleConfirmDelete);
    
    // Form validation
    const inputs = document.querySelectorAll('input[required]');
    inputs.forEach(input => {
        input.addEventListener('blur', validateField);
        input.addEventListener('input', clearFieldError);
    });
}

// Load all books
async function loadBooks() {
    try {
        showLoading(true);
        
        const response = await fetch('/api/books');
        const data = await response.json();
        
        if (data.success) {
            currentBooks = data.books;
            displayBooks(data.books);
            updateBookCount(data.total);
        } else {
            showToast('Kitaplar yüklenirken hata oluştu', 'error');
        }
    } catch (error) {
        console.error('Error loading books:', error);
        showToast('Bağlantı hatası', 'error');
    } finally {
        showLoading(false);
    }
}

// Display books in the UI
function displayBooks(books) {
    const booksList = document.getElementById('booksList');
    const emptyState = document.getElementById('emptyState');
    const booksContainer = document.getElementById('booksContainer');
    
    if (books.length === 0) {
        booksContainer.classList.add('d-none');
        emptyState.classList.remove('d-none');
        return;
    }
    
    booksContainer.classList.remove('d-none');
    emptyState.classList.add('d-none');
    
    booksList.innerHTML = '';
    
    books.forEach((book, index) => {
        const bookCard = createBookCard(book, index);
        booksList.appendChild(bookCard);
    });
}

// Create a book card element
function createBookCard(book, index) {
    const col = document.createElement('div');
    col.className = 'col-lg-6 col-xl-4 mb-4';
    
    col.innerHTML = `
        <div class="book-card fade-in" data-isbn="${book.isbn}">
            <div class="d-flex align-items-start justify-content-between">
                <div class="flex-grow-1">
                    <h5 class="book-title">${escapeHtml(book.title)}</h5>
                    <p class="book-author">
                        <i class="fas fa-user me-2"></i>
                        ${escapeHtml(book.author)}
                    </p>
                    <div class="book-isbn">
                        <i class="fas fa-barcode me-2"></i>
                        ${escapeHtml(book.isbn)}
                    </div>
                </div>
                <div class="book-icon">
                    <i class="fas fa-book"></i>
                </div>
            </div>
            <div class="book-actions">
                <button class="btn btn-sm btn-outline-primary" onclick="editBook('${book.isbn}')" title="Düzenle">
                    <i class="fas fa-edit"></i>
                    Düzenle
                </button>
                <button class="btn btn-sm btn-outline-danger" onclick="deleteBook('${book.isbn}', '${escapeHtml(book.title)}', '${escapeHtml(book.author)}')" title="Sil">
                    <i class="fas fa-trash"></i>
                    Sil
                </button>
            </div>
        </div>
    `;
    
    return col;
}

// Handle add book form submission
async function handleAddBook(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    
    const bookData = {
        title: document.getElementById('bookTitle').value.trim(),
        author: document.getElementById('bookAuthor').value.trim(),
        isbn: document.getElementById('bookIsbn').value.trim()
    };
    
    // Validation
    if (!validateBookData(bookData)) {
        return;
    }
    
    try {
        const submitBtn = form.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Ekleniyor...';
        
        const response = await fetch('/api/books', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(bookData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast(data.message, 'success');
            form.reset();
            clearFormErrors();
        } else {
            showToast(data.message, 'error');
        }
    } catch (error) {
        console.error('Error adding book:', error);
        showToast('Kitap eklenirken hata oluştu', 'error');
    } finally {
        const submitBtn = form.querySelector('button[type="submit"]');
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-save me-2"></i>Kitap Ekle';
    }
}

// Handle search
async function handleSearch(event) {
    event.preventDefault();
    
    const keyword = document.getElementById('searchKeyword').value.trim();
    
    if (!keyword) {
        showToast('Arama terimi gerekli', 'warning');
        return;
    }
    
    try {
        showLoading(true);
        
        const response = await fetch(`/api/books/search?q=${encodeURIComponent(keyword)}`);
        const data = await response.json();
        
        if (data.success) {
            isSearchMode = true;
            displayBooks(data.books);
            showSearchResults(data.total, keyword);
        } else {
            showToast(data.message, 'error');
        }
    } catch (error) {
        console.error('Error searching books:', error);
        showToast('Arama sırasında hata oluştu', 'error');
    } finally {
        showLoading(false);
    }
}

// Handle search input (real-time search)
let searchTimeout;
function handleSearchInput(event) {
    const keyword = event.target.value.trim();
    
    clearTimeout(searchTimeout);
    
    if (keyword.length >= 2) {
        searchTimeout = setTimeout(() => {
            performSearch(keyword);
        }, 500);
    } else if (keyword.length === 0 && isSearchMode) {
        clearSearch();
    }
}

// Perform search
async function performSearch(keyword) {
    try {
        const response = await fetch(`/api/books/search?q=${encodeURIComponent(keyword)}`);
        const data = await response.json();
        
        if (data.success) {
            isSearchMode = true;
            displayBooks(data.books);
            showSearchResults(data.total, keyword);
        }
    } catch (error) {
        console.error('Error performing search:', error);
    }
}

// Show search results
function showSearchResults(count, keyword) {
    const searchResults = document.getElementById('searchResults');
    const searchCount = document.getElementById('searchCount');
    
    searchCount.textContent = count;
    searchResults.classList.remove('d-none');
}

// Clear search
function clearSearch() {
    isSearchMode = false;
    document.getElementById('searchKeyword').value = '';
    document.getElementById('searchResults').classList.add('d-none');
    loadBooks();
}

// Delete book
function deleteBook(isbn, title, author) {
    document.getElementById('deleteBookTitle').textContent = title;
    document.getElementById('deleteBookAuthor').textContent = author;
    document.getElementById('deleteBookIsbn').textContent = isbn;
    
    const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
    deleteModal.show();
    
    // Store the ISBN for confirmation
    document.getElementById('confirmDelete').dataset.isbn = isbn;
}

// Handle delete confirmation
async function handleConfirmDelete() {
    const isbn = this.dataset.isbn;
    
    try {
        this.disabled = true;
        this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Siliniyor...';
        
        const response = await fetch(`/api/books/${isbn}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast(data.message, 'success');
            bootstrap.Modal.getInstance(document.getElementById('deleteModal')).hide();
        } else {
            showToast(data.message, 'error');
        }
    } catch (error) {
        console.error('Error deleting book:', error);
        showToast('Kitap silinirken hata oluştu', 'error');
    } finally {
        this.disabled = false;
        this.innerHTML = '<i class="fas fa-trash me-2"></i>Sil';
    }
}

// Load statistics
async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        if (data.success) {
            const stats = data.stats;
            document.getElementById('totalBooks').textContent = stats.total_books;
            document.getElementById('fileStatus').textContent = stats.file_exists ? '✓' : '✗';
            document.getElementById('fileStatus').className = stats.file_exists ? 'status-online' : 'status-offline';
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Show/hide loading spinner
function showLoading(show) {
    const spinner = document.getElementById('loadingSpinner');
    const container = document.getElementById('booksContainer');
    
    if (show) {
        spinner.classList.remove('d-none');
        container.classList.add('d-none');
    } else {
        spinner.classList.add('d-none');
        container.classList.remove('d-none');
    }
}

// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    const toastTitle = document.getElementById('toastTitle');
    const toastMessage = document.getElementById('toastMessage');
    
    // Set icon and title based on type
    let icon, title;
    switch (type) {
        case 'success':
            icon = 'fas fa-check-circle';
            title = 'Başarılı';
            toast.classList.add('bg-success', 'text-white');
            break;
        case 'error':
            icon = 'fas fa-exclamation-circle';
            title = 'Hata';
            toast.classList.add('bg-danger', 'text-white');
            break;
        case 'warning':
            icon = 'fas fa-exclamation-triangle';
            title = 'Uyarı';
            toast.classList.add('bg-warning', 'text-dark');
            break;
        default:
            icon = 'fas fa-info-circle';
            title = 'Bilgi';
            toast.classList.add('bg-info', 'text-white');
    }
    
    toastTitle.innerHTML = `<i class="${icon} me-2"></i>${title}`;
    toastMessage.textContent = message;
    
    // Remove previous type classes
    toast.classList.remove('bg-success', 'bg-danger', 'bg-warning', 'bg-info', 'text-white', 'text-dark');
    
    // Add new type classes
    switch (type) {
        case 'success':
            toast.classList.add('bg-success', 'text-white');
            break;
        case 'error':
            toast.classList.add('bg-danger', 'text-white');
            break;
        case 'warning':
            toast.classList.add('bg-warning', 'text-dark');
            break;
        default:
            toast.classList.add('bg-info', 'text-white');
    }
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
}

// Update current time
function updateCurrentTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('tr-TR');
    document.getElementById('current-time').textContent = timeString;
}

// Update book count
function updateBookCount(count) {
    document.getElementById('totalBooks').textContent = count;
}

// Validation functions
function validateBookData(data) {
    if (!data.title || data.title.length < 2) {
        showFieldError('bookTitle', 'Kitap başlığı en az 2 karakter olmalıdır');
        return false;
    }
    
    if (!data.author || data.author.length < 2) {
        showFieldError('bookAuthor', 'Yazar adı en az 2 karakter olmalıdır');
        return false;
    }
    
    if (!data.isbn || data.isbn.length < 5) {
        showFieldError('bookIsbn', 'ISBN en az 5 karakter olmalıdır');
        return false;
    }
    
    return true;
}

function validateField(event) {
    const field = event.target;
    const value = field.value.trim();
    
    if (field.hasAttribute('required') && !value) {
        showFieldError(field.id, 'Bu alan zorunludur');
        return false;
    }
    
    return true;
}

function showFieldError(fieldId, message) {
    const field = document.getElementById(fieldId);
    field.classList.add('error-border');
    
    // Remove existing error message
    const existingError = field.parentNode.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    // Add error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message text-danger mt-1';
    errorDiv.style.fontSize = '0.875rem';
    errorDiv.textContent = message;
    field.parentNode.appendChild(errorDiv);
}

function clearFieldError(event) {
    const field = event.target;
    field.classList.remove('error-border');
    
    const errorMessage = field.parentNode.querySelector('.error-message');
    if (errorMessage) {
        errorMessage.remove();
    }
}

function clearFormErrors() {
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.classList.remove('error-border');
    });
    
    const errorMessages = document.querySelectorAll('.error-message');
    errorMessages.forEach(error => error.remove());
}

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Edit book function (placeholder for future implementation)
function editBook(isbn) {
    showToast('Düzenleme özelliği yakında eklenecek!', 'info');
}

// Export functions for global access
window.loadBooks = loadBooks;
window.clearSearch = clearSearch;
window.deleteBook = deleteBook;
window.editBook = editBook;

