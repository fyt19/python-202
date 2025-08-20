// Login Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    
    // Check if user is already logged in
    if (localStorage.getItem('isLoggedIn') === 'true') {
        window.location.href = '/dashboard';
        return;
    }
    
    loginForm.addEventListener('submit', handleLogin);
});

async function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();
    const rememberMe = document.getElementById('rememberMe').checked;
    
    // Simple validation
    if (!username || !password) {
        showError('Lütfen tüm alanları doldurun.');
        return;
    }
    
    // Demo credentials
    if (username === 'admin' && password === '1234') {
        // Success
        if (rememberMe) {
            localStorage.setItem('isLoggedIn', 'true');
            localStorage.setItem('username', username);
        } else {
            sessionStorage.setItem('isLoggedIn', 'true');
            sessionStorage.setItem('username', username);
        }
        
        showSuccess('Giriş başarılı! Yönlendiriliyorsunuz...');
        
        // Redirect after 1 second
        setTimeout(() => {
            window.location.href = '/dashboard';
        }, 1000);
        
    } else {
        showError('Kullanıcı adı veya şifre hatalı!');
        document.getElementById('password').value = '';
        document.getElementById('password').focus();
    }
}

function showSuccess(message) {
    showToast(message, 'success');
}

function showError(message) {
    showToast(message, 'error');
}

function showToast(message, type = 'info') {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.style.position = 'fixed';
    toast.style.top = '2rem';
    toast.style.right = '2rem';
    toast.style.zIndex = '1000';
    toast.style.padding = '1rem 1.5rem';
    toast.style.borderRadius = '10px';
    toast.style.color = 'white';
    toast.style.fontWeight = '500';
    toast.style.minWidth = '300px';
    toast.style.transform = 'translateX(100%)';
    toast.style.animation = 'slideIn 0.3s ease forwards';
    
    // Set background color based on type
    switch (type) {
        case 'success':
            toast.style.background = 'linear-gradient(135deg, #27ae60 0%, #2ecc71 100%)';
            break;
        case 'error':
            toast.style.background = 'linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)';
            break;
        default:
            toast.style.background = 'linear-gradient(135deg, #3498db 0%, #2980b9 100%)';
    }
    
    toast.textContent = message;
    
    // Add to page
    document.body.appendChild(toast);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        to { transform: translateX(0); }
    }
    
    @keyframes slideOut {
        to { transform: translateX(100%); }
    }
`;
document.head.appendChild(style);
