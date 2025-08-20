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
    const bookItem = document.createElement('div');
    bookItem.className = 'book-item';
    bookItem.setAttribute('data-isbn', book.isbn);
    
    bookItem.innerHTML = `
        <div class="book-header">
            <div class="book-info">
                <h3 class="book-title">${escapeHtml(book.title)}</h3>
                <p class="book-author">
                    <i class="fas fa-user"></i>
                    ${escapeHtml(book.author)}
                </p>
                <div class="book-isbn">
                    <i class="fas fa-barcode"></i>
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
    `;
    
    return bookItem;
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
    
    // Show modal
    document.getElementById('deleteModal').classList.remove('d-none');
    
    // Store the ISBN for confirmation
    document.getElementById('confirmDelete').dataset.isbn = isbn;
}

// Close delete modal
function closeDeleteModal() {
    document.getElementById('deleteModal').classList.add('d-none');
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
            closeDeleteModal();
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
    const toastMessage = document.getElementById('toastMessage');
    
    // Set message
    toastMessage.textContent = message;
    
    // Remove previous type classes
    toast.classList.remove('success', 'error', 'warning', 'info');
    
    // Add new type class
    toast.classList.add(type);
    
    // Show toast
    toast.style.display = 'block';
    
    // Auto hide after 3 seconds
    setTimeout(() => {
        toast.style.display = 'none';
    }, 3000);
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

// Edit book function
function editBook(isbn) {
    // Find the book
    const book = currentBooks.find(b => b.isbn === isbn);
    if (!book) {
        showToast('Kitap bulunamadı!', 'error');
        return;
    }
    
    // Show edit modal
    showEditModal(book);
}

// Show edit modal
function showEditModal(book) {
    // Create modal HTML
    const modalHTML = `
        <div id="editModal" class="modal">
            <div class="modal-overlay"></div>
            <div class="modal-content">
                <div class="modal-header">
                    <h3 class="modal-title">
                        <i class="fas fa-edit"></i>
                        Kitap Düzenle
                    </h3>
                </div>
                <div class="modal-body">
                    <form id="editBookForm">
                        <div class="form-group">
                            <label for="editBookTitle" class="form-label">Kitap Başlığı</label>
                            <input type="text" class="form-input" id="editBookTitle" value="${escapeHtml(book.title)}" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="editBookAuthor" class="form-label">Yazar</label>
                            <input type="text" class="form-input" id="editBookAuthor" value="${escapeHtml(book.author)}" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="editBookIsbn" class="form-label">ISBN</label>
                            <input type="text" class="form-input" id="editBookIsbn" value="${escapeHtml(book.isbn)}" readonly>
                            <small class="form-text">ISBN değiştirilemez</small>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" onclick="closeEditModal()">
                        <i class="fas fa-times"></i>
                        İptal
                    </button>
                    <button type="button" class="btn btn-primary" onclick="saveBookEdit()">
                        <i class="fas fa-save"></i>
                        Kaydet
                    </button>
                </div>
            </div>
        </div>
    `;
    
    // Add modal to page
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Show modal
    document.getElementById('editModal').classList.remove('d-none');
}

// Close edit modal
function closeEditModal() {
    const modal = document.getElementById('editModal');
    if (modal) {
        modal.remove();
    }
}

// Save book edit
async function saveBookEdit() {
    const title = document.getElementById('editBookTitle').value.trim();
    const author = document.getElementById('editBookAuthor').value.trim();
    const isbn = document.getElementById('editBookIsbn').value.trim();
    
    if (!title || !author) {
        showToast('Lütfen tüm alanları doldurun!', 'error');
        return;
    }
    
    try {
        const response = await fetch(`/api/books/${isbn}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title, author })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('Kitap başarıyla güncellendi!', 'success');
            closeEditModal();
            loadBooks(); // Refresh the list
        } else {
            showToast(data.message || 'Güncelleme başarısız!', 'error');
        }
    } catch (error) {
        console.error('Error updating book:', error);
        showToast('Güncelleme sırasında hata oluştu!', 'error');
    }
}

// Logout function
function logout() {
    // Clear all storage
    localStorage.clear();
    sessionStorage.clear();
    
    // Redirect to login
    window.location.href = '/';
}

// Export functions for global access
window.loadBooks = loadBooks;
window.clearSearch = clearSearch;
window.deleteBook = deleteBook;
window.editBook = editBook;
window.closeDeleteModal = closeDeleteModal;
window.closeEditModal = closeEditModal;
window.saveBookEdit = saveBookEdit;
window.logout = logout;

